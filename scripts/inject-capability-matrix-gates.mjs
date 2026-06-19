/**
 * Insert/refresh the Capability Matrix hard-gate preamble in all Phase + Database
 * Migration + Security Hardening + Cost Optimization prompts.
 *
 * Run via: node scripts/inject-capability-matrix-gates.mjs
 *
 * Idempotent: re-running produces the same output. Recognizes the existing gate
 * block by its sentinel markers and replaces in place.
 */

import { promises as fs, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const promptsDir = path.resolve(__dirname, '..', '.github', 'prompts');

// Each prompt: (file, niceName) — phase number for messaging
const PROMPTS = [
  { file: 'Phase1-PlanAndAssess.prompt.md',       phase: 'Phase 1 — Plan & Assess' },
  { file: 'Phase2-MigrateCode.prompt.md',         phase: 'Phase 2 — Migrate Code' },
  { file: 'Phase3-GenerateInfra.prompt.md',       phase: 'Phase 3 — Generate Infra' },
  { file: 'Phase4-DeployToAzure.prompt.md',       phase: 'Phase 4 — Deploy to Azure' },
  { file: 'Phase5-SetupCICD.prompt.md',           phase: 'Phase 5 — Setup CI/CD' },
  { file: 'Phase6-PostMigrationOps.prompt.md',    phase: 'Phase 6 — Post-Migration Ops' },
  { file: 'DatabaseMigration.prompt.md',          phase: 'Database Migration' },
  { file: 'SecurityHardening.prompt.md',          phase: 'Security Hardening' },
  { file: 'CostOptimization.prompt.md',           phase: 'Cost Optimization' },
];

const SENTINEL_START = '<!-- BEGIN: capability-matrix-gate (auto-managed by inject-capability-matrix-gates.mjs) -->';
const SENTINEL_END = '<!-- END: capability-matrix-gate -->';

function buildGate(phase) {
  return [
    SENTINEL_START,
    '',
    `## 🚦 MANDATORY OPENING CHECK — Capability Matrix Required`,
    '',
    `**Before doing ANY work for ${phase}, verify the Discovery contract:**`,
    '',
    '| Required artifact | Location | If missing |',
    '|-------------------|----------|------------|',
    '| Discovery Dossier | `reports/Discovery-Dossier.md` | **STOP** — route to Discovery Engineer |',
    '| Capability Matrix | `reports/Capability-Matrix.yaml` | **STOP** — route to Discovery Engineer |',
    '| Approved Migration Plan | `reports/Migration-Plan.md` | **STOP** — route to Architect (run `/build-migration-plan`) |',
    '',
    '### If ANY of those three artifacts is missing',
    '',
    'Reply with exactly:',
    '',
    '```',
    `🚨 ${phase} cannot proceed without the Discovery contract.`,
    '',
    'Missing artifacts:',
    '  - reports/Discovery-Dossier.md          [missing/present]',
    '  - reports/Capability-Matrix.yaml         [missing/present]',
    '  - reports/Migration-Plan.md              [missing/present]',
    '',
    'Required steps before re-running this phase:',
    '  1. Open Copilot Chat → /assess-any-application  (or in CLI: "assess this application")',
    '  2. Then: /build-migration-plan                  (or in CLI: "build the migration plan")',
    '  3. Then: /' + phase.split(' ')[0].toLowerCase() + '...',
    '',
    'To override (skip Discovery and accept risk), log a waiver in .squad/decisions.md',
    'with `Waiver-<app>: skip-discovery=<reason>` and re-invoke this prompt with the',
    '`--accept-risk` natural-language flag in your request.',
    '```',
    '',
    '**Do NOT proceed past this gate unless:**',
    '- All three artifacts exist, OR',
    '- A waiver entry exists in `.squad/decisions.md` AND the user explicitly said "skip discovery" or similar',
    '',
    '### When the gate passes',
    '',
    '1. Read `reports/Capability-Matrix.yaml` and extract these fields you must honor:',
    '   - `source.primary_adapter` → load the matching `source-*` skill',
    '   - `stack.primary_stack` + `stack.secondary_stacks` → load matching `stack-*` skills',
    '   - `workload.primary_pattern` → load matching `workload-*` skill',
    '   - `migration_strategy.recommendation` → adjust phase emphasis per the strategy table in `.squad/routing.md`',
    '   - `risk_flags` → auto-dispatch the specialists listed in `.squad/routing.md`',
    '   - `required_specialists` → ensure all are in the room',
    '   - `unresolved_questions` → if any remain unanswered, surface them BEFORE starting work',
    '2. Read `reports/Migration-Plan.md` for the Architect\'s approved sequencing and any app-specific extra gates.',
    '3. Confirm Phase prerequisites are met (see standard gates in `.squad/routing.md`).',
    '',
    SENTINEL_END,
    '',
  ].join('\n');
}

const GATE_RE = new RegExp(
  `${SENTINEL_START.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\$&')}[\\s\\S]*?${SENTINEL_END.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\$&')}\\s*`,
  'g'
);

/**
 * Inject the gate AFTER the YAML frontmatter (which ends with `---`) but BEFORE
 * any other markdown body.
 */
function injectGate(content, gateBlock) {
  // Remove any existing gate
  const stripped = content.replace(GATE_RE, '');

  // Split off frontmatter
  const fmMatch = stripped.match(/^(---\s*\r?\n[\s\S]*?\r?\n---\s*\r?\n)/);
  if (fmMatch) {
    const fm = fmMatch[1];
    const rest = stripped.slice(fm.length);
    return fm + '\n' + gateBlock + rest;
  }
  // No frontmatter — just prepend
  return gateBlock + stripped;
}

let problems = 0;
let updated = 0;

for (const { file, phase } of PROMPTS) {
  const fp = path.join(promptsDir, file);
  if (!existsSync(fp)) {
    console.error(`✗ ${file} — missing`);
    problems++;
    continue;
  }
  const content = readFileSync(fp, 'utf-8');
  const gate = buildGate(phase);
  const next = injectGate(content, gate);
  if (next !== content) {
    await fs.writeFile(fp, next);
    console.log(`✓ ${file} — gate injected/refreshed`);
    updated++;
  } else {
    console.log(`= ${file} — already up to date`);
  }
}

console.log(`\n[inject-capability-matrix-gates] ${updated} file(s) updated; ${problems} problem(s).`);
if (problems > 0) process.exit(1);
