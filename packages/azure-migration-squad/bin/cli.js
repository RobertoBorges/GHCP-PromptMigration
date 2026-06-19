#!/usr/bin/env node
/**
 * @robertoborges/azure-migration-squad — CLI entry point
 *
 * Usage:
 *   azure-migration-squad <command> [options]
 *   ams <command> [options]                  # short alias
 *
 * Commands:
 *   init                     Scaffold migration squad into the current repo (Squad-first)
 *   upgrade                  Refresh squad content without touching user customizations
 *   doctor                   Validate installed squad integrity
 *   list                     List installed adapters (sources / stacks / workloads)
 *   telemetry <on|off|status> Manage anonymous usage telemetry
 *   help [command]           Show help
 *   version                  Print version
 *
 * Design notes:
 *   - Zero runtime dependencies (Node built-ins only) for fast install / minimal supply chain
 *   - All commands are idempotent — safe to re-run
 *   - Refuses to scaffold without a Squad runtime present (.squad/ directory)
 *   - Telemetry is opt-out (see lib/telemetry.js)
 */

import { promises as fs, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import os from 'node:os';
import readline from 'node:readline/promises';

import {
  resolveTelemetryEnabled,
  setTelemetryEnabled,
  getTelemetryStatus,
  hasSeenFirstRunNotice,
  markFirstRunNoticeShown,
  getUserConfigPath,
} from '../lib/telemetry-consent.js';

import {
  trackInstall,
  trackUpgrade,
  trackCommand,
  trackError,
  trackTelemetryDisabled,
} from '../lib/telemetry.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgRoot = path.resolve(__dirname, '..');
const templatesDir = path.join(pkgRoot, 'templates');

const PKG = JSON.parse(readFileSync(path.join(pkgRoot, 'package.json'), 'utf-8'));
const VERSION = PKG.version;

// ──────────────────────────────────────────────────────────────────────────
// ANSI helpers (no chalk dep)
// ──────────────────────────────────────────────────────────────────────────

const useColor = process.stdout.isTTY && !process.env['NO_COLOR'];
const RESET = useColor ? '\x1b[0m' : '';
const BOLD = useColor ? '\x1b[1m' : '';
const DIM = useColor ? '\x1b[2m' : '';
const GREEN = useColor ? '\x1b[32m' : '';
const YELLOW = useColor ? '\x1b[33m' : '';
const RED = useColor ? '\x1b[31m' : '';
const CYAN = useColor ? '\x1b[36m' : '';

const log = (msg) => process.stdout.write(msg + '\n');
const info = (msg) => log(`${CYAN}ℹ${RESET}  ${msg}`);
const success = (msg) => log(`${GREEN}✓${RESET}  ${msg}`);
const warn = (msg) => log(`${YELLOW}⚠${RESET}  ${msg}`);
const error = (msg) => log(`${RED}✗${RESET}  ${msg}`);
const heading = (msg) => log(`\n${BOLD}${msg}${RESET}`);

// ──────────────────────────────────────────────────────────────────────────
// Argument parsing (minimal — no commander dep)
// ──────────────────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = argv.slice(2);
  const flags = {};
  const positional = [];
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--no-')) {
      // --no-X → store as both 'no-X':true and 'X':false for consumer convenience
      const key = arg.slice(5);
      flags[`no-${key}`] = true;
      flags[key] = false;
    } else if (arg.startsWith('--')) {
      const eq = arg.indexOf('=');
      if (eq > -1) {
        flags[arg.slice(2, eq)] = arg.slice(eq + 1);
      } else {
        const next = args[i + 1];
        if (next && !next.startsWith('-')) {
          flags[arg.slice(2)] = next;
          i++;
        } else {
          flags[arg.slice(2)] = true;
        }
      }
    } else if (arg.startsWith('-') && arg.length === 2) {
      flags[arg.slice(1)] = true;
    } else {
      positional.push(arg);
    }
  }
  return { positional, flags };
}

// ──────────────────────────────────────────────────────────────────────────
// Squad detection
// ──────────────────────────────────────────────────────────────────────────

function detectSquad(cwd = process.cwd()) {
  const squadDir = path.join(cwd, '.squad');
  return {
    present: existsSync(squadDir),
    path: squadDir,
    hasTeamMd: existsSync(path.join(squadDir, 'team.md')),
    hasAgents: existsSync(path.join(squadDir, 'agents')),
  };
}

// ──────────────────────────────────────────────────────────────────────────
// Capability Matrix validation (lightweight — no schema lib dependency)
// ──────────────────────────────────────────────────────────────────────────

/**
 * Minimal YAML scalar/array reader. We only need to read top-level keys and
 * a small set of nested fields — full schema validation lives in CI.
 */
function tinyYamlParse(text) {
  // Strip comments
  const cleaned = text.split('\n').map((l) => l.replace(/\s+#.*$/, '')).join('\n');
  const obj = {};
  let current = obj;
  const stack = [{ obj, indent: -1 }];
  for (const raw of cleaned.split('\n')) {
    if (!raw.trim()) continue;
    const indent = raw.length - raw.trimStart().length;
    const line = raw.trim();
    // Pop stack until we find parent
    while (stack.length > 1 && stack[stack.length - 1].indent >= indent) stack.pop();
    current = stack[stack.length - 1].obj;
    const m = line.match(/^([a-zA-Z_][\w-]*):\s*(.*)$/);
    if (m) {
      const [, key, val] = m;
      if (val === '' || val === '|' || val === '>') {
        current[key] = {};
        stack.push({ obj: current[key], indent });
      } else {
        // Strip quotes
        let v = val.trim();
        if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
          v = v.slice(1, -1);
        }
        current[key] = v;
      }
    }
  }
  return obj;
}

async function validateCapabilityMatrix(matrixPath) {
  const errors = [];
  try {
    const content = await fs.readFile(matrixPath, 'utf-8');
    const matrix = tinyYamlParse(content);

    // Spot-check required top-level keys
    for (const k of ['schema_version', 'application', 'source', 'stack', 'workload', 'data', 'migration_strategy']) {
      if (!(k in matrix)) errors.push(`missing required key: ${k}`);
    }

    // Spot-check confidence labels on each axis
    for (const axis of ['source', 'stack', 'workload', 'data']) {
      if (matrix[axis] && matrix[axis].evidence_confidence) {
        const conf = matrix[axis].evidence_confidence;
        if (!['high', 'medium', 'low'].includes(conf)) {
          errors.push(`${axis}.evidence_confidence "${conf}" not in [high, medium, low]`);
        }
      } else if (matrix[axis]) {
        errors.push(`${axis}.evidence_confidence missing`);
      }
    }

    // Spot-check 6Rs
    const validStrategies = ['rehost', 'replatform', 'refactor', 'rearchitect', 'rebuild', 'retire', 'retain'];
    const strat = matrix.migration_strategy?.recommendation;
    if (strat && !validStrategies.includes(strat)) {
      errors.push(`migration_strategy.recommendation "${strat}" not in [${validStrategies.join(', ')}]`);
    }

    return { ok: errors.length === 0, errors, strategy: strat || 'unknown' };
  } catch (err) {
    return { ok: false, errors: [`failed to parse matrix: ${err.message}`], strategy: null };
  }
}

// ──────────────────────────────────────────────────────────────────────────
// File operations
// ──────────────────────────────────────────────────────────────────────────

async function ensureDir(p) {
  await fs.mkdir(p, { recursive: true });
}

async function copyRecursive(src, dest, { overwrite = false, onSkip = null, onCopy = null } = {}) {
  const stat = await fs.stat(src);
  if (stat.isDirectory()) {
    await ensureDir(dest);
    const entries = await fs.readdir(src);
    for (const entry of entries) {
      await copyRecursive(path.join(src, entry), path.join(dest, entry), { overwrite, onSkip, onCopy });
    }
  } else {
    if (existsSync(dest) && !overwrite) {
      onSkip?.(dest);
      return;
    }
    await ensureDir(path.dirname(dest));
    await fs.copyFile(src, dest);
    onCopy?.(dest);
  }
}

// ──────────────────────────────────────────────────────────────────────────
// Commands
// ──────────────────────────────────────────────────────────────────────────

async function cmdInit(flags) {
  const cwd = process.cwd();
  await showFirstRunNoticeIfNeeded(flags);

  heading('🛬 azure-migration-squad init');
  info(`Target: ${cwd}`);
  info(`Version: ${VERSION}`);

  // Detect Squad
  const squad = detectSquad(cwd);
  if (!squad.present && !flags.force) {
    error('Squad runtime not detected in this directory.');
    log('');
    log(`  azure-migration-squad is designed to extend an existing Squad-managed repo.`);
    log(`  Please initialize Squad first:`);
    log('');
    log(`    ${BOLD}npm install -g @bradygaster/squad-cli${RESET}`);
    log(`    ${BOLD}squad init${RESET}`);
    log('');
    log(`  Then re-run:  ${BOLD}npx @robertoborges/azure-migration-squad init${RESET}`);
    log('');
    log(`  ${DIM}(To skip this check for testing, use --force — content will be installed anyway.)${RESET}`);
    await trackInstall({ result: 'no-squad', forced: false }, { flagDisabled: flags['no-telemetry'] });
    process.exit(1);
  }

  if (!existsSync(templatesDir) || (await fs.readdir(templatesDir)).filter((f) => f !== '.gitkeep').length === 0) {
    error('templates/ directory is empty.');
    log('  This usually means the package was published without the prebuild sync step.');
    log('  If you are developing locally, run: npm run sync');
    process.exit(1);
  }

  // Plan: install templates/github/* → .github/* and templates/squad/* → .squad/*
  const copied = [];
  const skipped = [];

  const installMap = [
    { from: path.join(templatesDir, 'github'), to: path.join(cwd, '.github') },
    { from: path.join(templatesDir, 'squad'), to: path.join(cwd, '.squad') },
    { from: path.join(templatesDir, 'AGENTS.md'), to: path.join(cwd, 'AGENTS.md') },
  ];

  const overwrite = !!flags.overwrite;

  for (const { from, to } of installMap) {
    if (!existsSync(from)) continue;
    await copyRecursive(from, to, {
      overwrite,
      onSkip: (p) => skipped.push(path.relative(cwd, p)),
      onCopy: (p) => copied.push(path.relative(cwd, p)),
    });
  }

  // Welcome doc — install once, never overwrite (user may annotate it / delete it).
  // Lives at the repo root so VS Code Explorer surfaces it next to README.md.
  const welcomeSrc = path.join(templatesDir, 'MIGRATION-START-HERE.md');
  const welcomeDest = path.join(cwd, 'MIGRATION-START-HERE.md');
  let welcomeJustWritten = false;
  if (existsSync(welcomeSrc)) {
    if (existsSync(welcomeDest)) {
      skipped.push('MIGRATION-START-HERE.md');
    } else {
      await ensureDir(path.dirname(welcomeDest));
      await fs.copyFile(welcomeSrc, welcomeDest);
      copied.push('MIGRATION-START-HERE.md');
      welcomeJustWritten = true;
    }
  }

  // Manifest
  const manifestPath = path.join(cwd, '.azure-migration-squad', 'manifest.json');
  await ensureDir(path.dirname(manifestPath));
  await fs.writeFile(
    manifestPath,
    JSON.stringify(
      {
        package: PKG.name,
        version: VERSION,
        installedAt: new Date().toISOString(),
        filesCopied: copied.length,
        filesSkipped: skipped.length,
        squadDetected: squad.present,
      },
      null,
      2
    ) + '\n'
  );

  log('');
  success(`Installed ${copied.length} file(s); skipped ${skipped.length} existing file(s).`);
  if (skipped.length > 0 && !overwrite) {
    log(`  ${DIM}(Use --overwrite to replace existing files.)${RESET}`);
  }
  success(`Manifest written to .azure-migration-squad/manifest.json`);
  if (welcomeJustWritten) {
    success(`Welcome guide written to MIGRATION-START-HERE.md — open it for your 60-second quickstart.`);
  }
  log('');
  heading('Next steps');
  if (welcomeJustWritten) {
    log(`  1. Open ${BOLD}MIGRATION-START-HERE.md${RESET} for the 60-second quickstart.`);
    log(`  2. Open GitHub Copilot Chat (${BOLD}Ctrl+Alt+I${RESET} in VS Code).`);
    log(`  3. Run:  ${BOLD}/assess-any-application${RESET}`);
    log(`  4. The Discovery Engineer (Saul Bloom Jr.) will walk you through intake.`);
  } else {
    log(`  1. Open GitHub Copilot Chat (${BOLD}Ctrl+Alt+I${RESET} in VS Code).`);
    log(`  2. Run:  ${BOLD}/assess-any-application${RESET}`);
    log(`  3. The Discovery Engineer (Saul Bloom Jr.) will walk you through intake.`);
  }
  log('');

  await trackInstall(
    {
      result: 'ok',
      forced: !squad.present,
      squad_detected: squad.present,
      files_copied: copied.length,
      files_skipped: skipped.length,
    },
    { flagDisabled: flags['no-telemetry'] }
  );
}

async function cmdUpgrade(flags) {
  const cwd = process.cwd();
  heading('⬆️  azure-migration-squad upgrade');

  const manifestPath = path.join(cwd, '.azure-migration-squad', 'manifest.json');
  if (!existsSync(manifestPath)) {
    error('No installation manifest found at .azure-migration-squad/manifest.json');
    log(`  Run ${BOLD}azure-migration-squad init${RESET} first.`);
    process.exit(1);
  }

  const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf-8'));
  info(`Current installed version: ${manifest.version}`);
  info(`Package version available: ${VERSION}`);

  // Upgrade IS init with overwrite=true. User customizations should live OUTSIDE
  // the squad-managed files (e.g., reports/ folder is never touched).
  const copied = [];
  const installMap = [
    { from: path.join(templatesDir, 'github'), to: path.join(cwd, '.github') },
    { from: path.join(templatesDir, 'squad'), to: path.join(cwd, '.squad') },
    { from: path.join(templatesDir, 'AGENTS.md'), to: path.join(cwd, 'AGENTS.md') },
  ];

  for (const { from, to } of installMap) {
    if (!existsSync(from)) continue;
    await copyRecursive(from, to, {
      overwrite: true,
      onCopy: (p) => copied.push(path.relative(cwd, p)),
    });
  }

  // Update manifest
  manifest.version = VERSION;
  manifest.upgradedAt = new Date().toISOString();
  manifest.filesCopied = copied.length;
  await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2) + '\n');

  success(`Upgraded to ${VERSION}. ${copied.length} file(s) refreshed.`);
  warn(`Your reports/ folder, .squad/decisions.md, and .squad/history are NOT touched by upgrade.`);

  await trackUpgrade(
    {
      from_version: manifest.version,
      to_version: VERSION,
      files_copied: copied.length,
    },
    { flagDisabled: flags['no-telemetry'] }
  );
}

async function cmdDoctor(flags) {
  const cwd = process.cwd();
  heading('🩺 azure-migration-squad doctor');

  let problems = 0;
  const ok = (msg) => success(msg);
  const fail = (msg) => {
    error(msg);
    problems++;
  };

  // 1. Squad detected?
  const squad = detectSquad(cwd);
  squad.present ? ok('Squad runtime detected (.squad/ exists)') : fail('Squad runtime missing');

  // 2. Manifest present?
  const manifestPath = path.join(cwd, '.azure-migration-squad', 'manifest.json');
  if (existsSync(manifestPath)) {
    const m = JSON.parse(await fs.readFile(manifestPath, 'utf-8'));
    ok(`Installation manifest present (version ${m.version})`);
    if (m.version !== VERSION) {
      warn(`Installed version (${m.version}) differs from package version (${VERSION}) — consider 'upgrade'`);
    }
  } else {
    fail('No installation manifest found — run `azure-migration-squad init`');
  }

  // 3. Key squad agents installed?
  const requiredAgents = ['discovery-engineer', 'architect', 'coder', 'azure-specialist'];
  for (const agent of requiredAgents) {
    const charterPath = path.join(cwd, '.squad', 'agents', agent, 'charter.md');
    existsSync(charterPath)
      ? ok(`Agent installed: ${agent}`)
      : fail(`Agent missing: .squad/agents/${agent}/charter.md`);
  }

  // 4. Key skills installed?
  const requiredSkills = [
    '.github/skills/capability-matrix.md',
    '.github/skills/migration-strategy-decision-tree.md',
    '.github/skills/discovery-dossier-template.md',
    '.github/skills/stack-detection.md',
  ];
  for (const skill of requiredSkills) {
    existsSync(path.join(cwd, skill))
      ? ok(`Skill installed: ${skill.split('/').pop()}`)
      : fail(`Skill missing: ${skill}`);
  }

  // 5. Key prompts installed?
  const requiredPrompts = [
    '.github/prompts/Assess-Any-Application.prompt.md',
    '.github/prompts/Build-Migration-Plan.prompt.md',
  ];
  for (const prompt of requiredPrompts) {
    existsSync(path.join(cwd, prompt))
      ? ok(`Prompt installed: ${prompt.split('/').pop()}`)
      : fail(`Prompt missing: ${prompt}`);
  }

  // 6. Capability Matrix schema validation (if matrix exists)
  const matrixPath = path.join(cwd, 'reports', 'Capability-Matrix.yaml');
  if (existsSync(matrixPath)) {
    const matrixCheck = await validateCapabilityMatrix(matrixPath);
    if (matrixCheck.ok) {
      ok(`Capability Matrix passes schema validation (strategy: ${matrixCheck.strategy})`);
    } else {
      for (const err of matrixCheck.errors) {
        fail(`Capability Matrix: ${err}`);
      }
    }
  } else {
    info('reports/Capability-Matrix.yaml not present (run /assess-any-application to generate)');
  }

  // 7. Telemetry status
  const tStatus = getTelemetryStatus();
  info(`Telemetry: ${tStatus.enabled ? 'enabled' : 'disabled'} (${tStatus.source})`);

  log('');
  if (problems === 0) {
    success(`All checks passed.`);
  } else {
    error(`${problems} problem(s) found.`);
    process.exit(1);
  }

  await trackCommand('doctor', { problems_found: problems }, { flagDisabled: flags['no-telemetry'] });
}

async function cmdList(flags) {
  const cwd = process.cwd();
  heading('📋 Installed adapters');

  const skillsDir = path.join(cwd, '.github', 'skills');
  if (!existsSync(skillsDir)) {
    warn('No .github/skills/ directory — squad not installed here.');
    return;
  }

  const categories = {
    'Source adapters': /^source-/,
    'Stack adapters': /^stack-/,
    'Workload patterns': /^workload-/,
    'Universal skills': /^(stack-detection|migration-strategy-decision-tree|capability-matrix|discovery-dossier-template|migration-plan-template)$/,
  };

  const entries = await fs.readdir(skillsDir);
  for (const [category, pattern] of Object.entries(categories)) {
    const matches = entries
      .filter((e) => e.endsWith('.md'))
      .map((e) => e.replace('.md', ''))
      .filter((e) => pattern.test(e))
      .sort();
    log(`\n${BOLD}${category}${RESET} (${matches.length})`);
    matches.forEach((m) => log(`  • ${m}`));
  }
  log('');
  await trackCommand('list', {}, { flagDisabled: flags['no-telemetry'] });
}

async function cmdTelemetry(args, flags) {
  const sub = args[0];
  if (sub === 'on') {
    setTelemetryEnabled(true);
    success('Telemetry enabled.');
    info(`Settings persisted to: ${getUserConfigPath()}`);
  } else if (sub === 'off') {
    setTelemetryEnabled(false);
    success('Telemetry disabled.');
    info(`Settings persisted to: ${getUserConfigPath()}`);
    await trackTelemetryDisabled('user-command', { flagDisabled: true });
  } else if (sub === 'status' || !sub) {
    const status = getTelemetryStatus();
    heading('📊 Telemetry status');
    log(`  Enabled:           ${status.enabled ? GREEN + 'yes' + RESET : YELLOW + 'no' + RESET}`);
    log(`  Source:            ${status.source}`);
    log(`  Install ID:        ${status.installId || '(none — disabled)'}`);
    log(`  User config:       ${status.userConfigPath}`);
    log(`  Project config:    ${status.projectConfigPath || '(none)'}`);
    log('');
    log(`  ${DIM}Backend: PostHog Cloud (US region)${RESET}`);
    log(`  ${DIM}Public dashboard: (TBD — link will be published with v0.1.0 stable)${RESET}`);
    log('');
    log(`  To opt out:  ${BOLD}azure-migration-squad telemetry off${RESET}`);
    log(`  Env opt-out: ${BOLD}AZURE_MIGRATION_SQUAD_TELEMETRY=0${RESET}  or  ${BOLD}DO_NOT_TRACK=1${RESET}`);
  } else {
    error(`Unknown telemetry subcommand: ${sub}`);
    log('  Usage: azure-migration-squad telemetry <on|off|status>');
    process.exit(1);
  }
}

async function cmdHelp() {
  log(`${BOLD}azure-migration-squad${RESET} ${DIM}v${VERSION}${RESET}`);
  log(`Azure migration agents for GitHub Copilot + Squad.`);
  log('');
  log(`${BOLD}USAGE${RESET}`);
  log(`  ams <command> [options]                       ${DIM}(short alias — recommended)${RESET}`);
  log(`  azure-migration-squad <command> [options]     ${DIM}(full name, same binary)${RESET}`);
  log('');
  log(`${BOLD}COMMANDS${RESET}`);
  log(`  init                  Scaffold migration squad into the current repo`);
  log(`  upgrade               Refresh squad content to the latest version`);
  log(`  doctor                Validate squad integrity (incl. Capability Matrix schema)`);
  log(`  list                  List installed adapters`);
  log(`  telemetry <sub>       Manage telemetry — sub: on|off|status`);
  log(`  help                  Show this help`);
  log(`  version               Print version`);
  log('');
  log(`${BOLD}EXAMPLES${RESET}`);
  log(`  ams init                          ${DIM}# install squad into current dir${RESET}`);
  log(`  ams init --overwrite              ${DIM}# refresh installed files${RESET}`);
  log(`  ams doctor                        ${DIM}# verify everything is wired correctly${RESET}`);
  log(`  ams list                          ${DIM}# show all installed adapters${RESET}`);
  log(`  ams telemetry off                 ${DIM}# disable telemetry permanently${RESET}`);
  log('');
  log(`${BOLD}FLAGS${RESET}`);
  log(`  --force               (init) Bypass Squad-detection check`);
  log(`  --overwrite           (init) Replace existing files instead of skipping`);
  log(`  --no-telemetry        Skip telemetry for this invocation`);
  log('');
  log(`${BOLD}LINKS${RESET}`);
  log(`  Docs:        https://github.com/RobertoBorges/GHCP-PromptMigration`);
  log(`  Telemetry:   https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/telemetry.md`);
  log(`  Issues:      https://github.com/RobertoBorges/GHCP-PromptMigration/issues`);
  log('');
}

// ──────────────────────────────────────────────────────────────────────────
// First-run notice (one-time consent)
// ──────────────────────────────────────────────────────────────────────────

async function showFirstRunNoticeIfNeeded(flags) {
  if (hasSeenFirstRunNotice()) return;
  if (flags['no-telemetry']) {
    markFirstRunNoticeShown();
    return;
  }

  // CI auto-accepts silently
  if (process.env['CI'] === 'true') {
    markFirstRunNoticeShown();
    return;
  }

  heading('🔍 First-run notice — anonymous telemetry');
  log('');
  log(`This tool collects anonymous usage data to help us improve it:`);
  log(`  • Install ID (random UUID)        • Command name`);
  log(`  • Package version                 • OS family and Node major`);
  log(`  • Squad-detected (yes/no)         • Error class names (no stack traces)`);
  log('');
  log(`${BOLD}We NEVER collect:${RESET}`);
  log(`  • File paths, project content, source code, or prompts`);
  log(`  • Customer data, emails, IPs, or git remote URLs`);
  log('');
  log(`Backend: PostHog Cloud (US region). Opt out at any time:`);
  log(`  ${BOLD}azure-migration-squad telemetry off${RESET}`);
  log('');
  log(`Full policy: https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/telemetry.md`);
  log('');

  if (process.stdin.isTTY) {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    try {
      const ans = (await rl.question(`Continue with anonymous telemetry enabled? [Y/n] `)).trim().toLowerCase();
      if (ans === 'n' || ans === 'no') {
        setTelemetryEnabled(false);
        warn('Telemetry disabled. Continuing...');
      } else {
        success('Telemetry enabled (you can change this at any time).');
      }
    } finally {
      rl.close();
    }
  }
  markFirstRunNoticeShown();
  log('');
}

// ──────────────────────────────────────────────────────────────────────────
// Main dispatcher
// ──────────────────────────────────────────────────────────────────────────

async function main() {
  const { positional, flags } = parseArgs(process.argv);

  // Handle -v / --version / -h / --help as flags BEFORE positional dispatch
  if (flags.v || flags.version) {
    log(VERSION);
    return;
  }
  if (flags.h || flags.help) {
    await cmdHelp();
    return;
  }

  const cmd = positional[0] || 'help';
  const rest = positional.slice(1);

  try {
    switch (cmd) {
      case 'init':       await cmdInit(flags); break;
      case 'upgrade':    await cmdUpgrade(flags); break;
      case 'doctor':     await cmdDoctor(flags); break;
      case 'list':       await cmdList(flags); break;
      case 'telemetry':  await cmdTelemetry(rest, flags); break;
      case 'version':    log(VERSION); break;
      case 'help':       await cmdHelp(); break;
      default:
        error(`Unknown command: ${cmd}`);
        await cmdHelp();
        process.exit(1);
    }
  } catch (err) {
    error(`Command failed: ${err.message}`);
    if (process.env['DEBUG']) console.error(err.stack);
    await trackError(err.constructor?.name || 'Error', { command: cmd }, { flagDisabled: flags['no-telemetry'] });
    process.exit(1);
  }
}

main();
