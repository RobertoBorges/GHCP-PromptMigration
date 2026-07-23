#!/usr/bin/env node
/**
 * Local counterpart to release-please for the VS Code extension.
 *
 * What it does:
 *   1. Parses conventional commits since the last vscode-v* tag
 *   2. Determines semver bump (auto, or forced via --patch / --minor / --major)
 *   3. Previews the change (version bump + CHANGELOG addition)
 *   4. Asks confirmation (unless --yes)
 *   5. Updates package.json + CHANGELOG.md locally
 *   6. Runs `npm run build && npm run package` to produce the versioned .vsix
 *
 * What it does NOT do:
 *   - Commit
 *   - Create a git tag
 *   - Push
 *   - Publish to the marketplace
 *
 * Deliberate — this is a preview / emergency-hotfix tool. The normal path
 * is: push conventional-commit PRs to main, and release-please handles it.
 *
 * Usage:
 *   node scripts/local-release.mjs [flags]
 *
 * Flags:
 *   --patch                Force patch bump (default when no commits found)
 *   --minor                Force minor bump
 *   --major                Force major bump
 *   --dry-run              Print the plan, make no changes
 *   --yes                  Skip the confirmation prompt
 *   --no-build             Skip the build + package step
 *   --tag-prefix=<prefix>  Override tag prefix (default: vscode-v)
 *   -h, --help             Show this help
 */

import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import readline from 'node:readline/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgRoot = path.resolve(__dirname, '..');
const monorepoRoot = path.resolve(pkgRoot, '..', '..');
const pkgJsonPath = path.join(pkgRoot, 'package.json');
const changelogPath = path.join(pkgRoot, 'CHANGELOG.md');

// ANSI helpers (no chalk dependency)
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const BLUE = '\x1b[34m';
const RESET = '\x1b[0m';

function parseArgs() {
  const args = process.argv.slice(2);
  const flags = {
    bump: null,
    dryRun: false,
    yes: false,
    build: true,
    tagPrefix: 'vscode-v',
    help: false,
  };
  for (const arg of args) {
    if (arg === '--patch') flags.bump = 'patch';
    else if (arg === '--minor') flags.bump = 'minor';
    else if (arg === '--major') flags.bump = 'major';
    else if (arg === '--dry-run') flags.dryRun = true;
    else if (arg === '--yes' || arg === '-y') flags.yes = true;
    else if (arg === '--no-build') flags.build = false;
    else if (arg.startsWith('--tag-prefix=')) flags.tagPrefix = arg.slice('--tag-prefix='.length);
    else if (arg === '-h' || arg === '--help') flags.help = true;
  }
  return flags;
}

function printHelp() {
  console.log(`
${BOLD}local-release${RESET} — preview the next VS Code extension release locally

Usage: node scripts/local-release.mjs [flags]

Flags:
  ${GREEN}--patch${RESET}                Force patch bump
  ${GREEN}--minor${RESET}                Force minor bump
  ${GREEN}--major${RESET}                Force major bump
  ${GREEN}--dry-run${RESET}              Print the plan, make no changes
  ${GREEN}--yes${RESET}, ${GREEN}-y${RESET}             Skip the confirmation prompt
  ${GREEN}--no-build${RESET}             Skip the build + package step
  ${GREEN}--tag-prefix=<prefix>${RESET}  Override tag prefix (default: vscode-v)
  ${GREEN}-h${RESET}, ${GREEN}--help${RESET}            Show this help

Without --patch/--minor/--major, the bump is auto-detected from conventional
commits since the last ${DIM}vscode-v*${RESET} tag:
  ${DIM}feat!:${RESET} or ${DIM}BREAKING CHANGE:${RESET}  → major
  ${DIM}feat:${RESET}                        → minor
  ${DIM}fix:${RESET} / ${DIM}perf:${RESET} / ${DIM}revert:${RESET}    → patch
  Only ${DIM}chore/docs/refactor/test/build/ci${RESET} → no bump (script exits with a note)

This script ${BOLD}does not${RESET} commit, tag, or push. It updates package.json,
CHANGELOG.md, and produces a versioned .vsix. Inspect and commit yourself.

For the normal release flow (release-please on main), see
${BLUE}docs/publishing-vscode-extension.md${RESET}.
`);
}

function run(cmd, opts = {}) {
  const result = execSync(cmd, { encoding: 'utf-8', cwd: monorepoRoot, ...opts });
  // When stdio is 'inherit', execSync returns null (output goes straight to
  // the terminal, nothing is captured). Only .trim() the string case.
  return typeof result === 'string' ? result.trim() : '';
}

function safeRun(cmd) {
  try {
    return run(cmd);
  } catch {
    return null;
  }
}

function findLastTag(prefix) {
  // Look for the most recent tag matching `<prefix>*` (e.g., vscode-v*).
  // Portable: no shell pipes so this works on Windows PowerShell too.
  const raw = safeRun(`git tag --list "${prefix}*" --sort=-v:refname`);
  if (!raw) return null;
  const firstLine = raw.split(/\r?\n/).find((line) => line.trim().length > 0);
  return firstLine ? firstLine.trim() : null;
}

function getCommitsSince(ref) {
  // If no reference tag exists yet, look at the last 50 commits (bootstrap).
  const range = ref ? `${ref}..HEAD` : '-n 50';
  const raw = safeRun(`git log ${range} --pretty=format:"%H%x1f%s%x1f%b%x1e"`);
  if (!raw) return [];
  return raw
    .split('\x1e')
    .map((entry) => entry.trim())
    .filter(Boolean)
    .map((entry) => {
      const [sha, subject, body] = entry.split('\x1f');
      return { sha, subject: subject ?? '', body: body ?? '' };
    });
}

function classifyCommit(commit) {
  const s = commit.subject;
  // BREAKING CHANGE marker in the subject or body → major
  if (/^[a-z]+(\(.+\))?!:/i.test(s) || /BREAKING CHANGE:/.test(commit.body)) {
    return { kind: 'major', type: 'breaking' };
  }
  const m = s.match(/^(feat|fix|perf|revert|refactor|docs|chore|test|build|ci)(\(.+\))?:/i);
  if (!m) return { kind: 'none', type: 'unknown' };
  const type = m[1].toLowerCase();
  if (type === 'feat') return { kind: 'minor', type };
  if (type === 'fix' || type === 'perf' || type === 'revert') return { kind: 'patch', type };
  return { kind: 'none', type };
}

function decideBumpFromCommits(commits) {
  let highest = 'none';
  const relevant = [];
  for (const c of commits) {
    const { kind, type } = classifyCommit(c);
    if (kind === 'none') continue;
    relevant.push({ ...c, kind, type });
    if (kind === 'major') highest = 'major';
    else if (kind === 'minor' && highest !== 'major') highest = 'minor';
    else if (kind === 'patch' && highest === 'none') highest = 'patch';
  }
  return { bump: highest, relevant };
}

function bumpVersion(current, kind) {
  const parts = current.split('.').map(Number);
  if (parts.length !== 3 || parts.some((n) => Number.isNaN(n))) {
    throw new Error(`Cannot parse version "${current}" as semver X.Y.Z`);
  }
  const [major, minor, patch] = parts;
  if (kind === 'major') return `${major + 1}.0.0`;
  if (kind === 'minor') return `${major}.${minor + 1}.0`;
  if (kind === 'patch') return `${major}.${minor}.${patch + 1}`;
  throw new Error(`Unknown bump kind: ${kind}`);
}

function readPkgVersion() {
  const pkg = JSON.parse(readFileSync(pkgJsonPath, 'utf-8'));
  return pkg.version;
}

function writePkgVersion(newVersion) {
  const raw = readFileSync(pkgJsonPath, 'utf-8');
  // Preserve JSON formatting by regexing on the version line only.
  const updated = raw.replace(
    /("version"\s*:\s*")([^"]+)(")/,
    `$1${newVersion}$3`
  );
  if (updated === raw) {
    throw new Error('Could not find "version" field to update in package.json');
  }
  writeFileSync(pkgJsonPath, updated);
}

function buildChangelogEntry(version, commits, bumpKind) {
  const today = new Date().toISOString().slice(0, 10);
  const sections = { feat: [], fix: [], perf: [], revert: [], breaking: [] };
  for (const c of commits) {
    if (c.kind === 'major') sections.breaking.push(c);
    else if (c.type === 'feat') sections.feat.push(c);
    else if (c.type === 'fix') sections.fix.push(c);
    else if (c.type === 'perf') sections.perf.push(c);
    else if (c.type === 'revert') sections.revert.push(c);
  }
  const lines = [`## [${version}] — ${today}`, ''];
  if (sections.breaking.length) {
    lines.push('### ⚠ BREAKING CHANGES');
    for (const c of sections.breaking) lines.push(`- ${c.subject} (${c.sha.slice(0, 7)})`);
    lines.push('');
  }
  if (sections.feat.length) {
    lines.push('### Features');
    for (const c of sections.feat) lines.push(`- ${c.subject} (${c.sha.slice(0, 7)})`);
    lines.push('');
  }
  if (sections.fix.length) {
    lines.push('### Bug Fixes');
    for (const c of sections.fix) lines.push(`- ${c.subject} (${c.sha.slice(0, 7)})`);
    lines.push('');
  }
  if (sections.perf.length) {
    lines.push('### Performance');
    for (const c of sections.perf) lines.push(`- ${c.subject} (${c.sha.slice(0, 7)})`);
    lines.push('');
  }
  if (sections.revert.length) {
    lines.push('### Reverts');
    for (const c of sections.revert) lines.push(`- ${c.subject} (${c.sha.slice(0, 7)})`);
    lines.push('');
  }
  if (!sections.feat.length && !sections.fix.length && !sections.perf.length && !sections.revert.length && !sections.breaking.length) {
    // Forced-bump path — no conventional commits detected.
    lines.push(`### ${bumpKind[0].toUpperCase()}${bumpKind.slice(1)} release (forced)`);
    lines.push(`- No conventional-commit-tagged changes detected; version bumped manually.`);
    lines.push('');
  }
  return lines.join('\n');
}

function prependToChangelog(entry) {
  if (!existsSync(changelogPath)) {
    writeFileSync(changelogPath, `# Changelog\n\n${entry}\n`);
    return;
  }
  const existing = readFileSync(changelogPath, 'utf-8');
  // Insert new entry after the first "# Changelog" heading and any intro text.
  // Heuristic: after the first `## ` heading OR at end of intro. Simplest: after the
  // "# Changelog" line + one blank line, or at position 0 if none.
  const headingMatch = existing.match(/^# Changelog[\s\S]*?\n(?=(?:##[^#])|(?:# ))/);
  if (headingMatch) {
    const preserved = existing.slice(0, headingMatch[0].length);
    const rest = existing.slice(headingMatch[0].length);
    writeFileSync(changelogPath, preserved + entry + '\n' + rest);
  } else {
    // No standard header — just prepend after the first line.
    const firstNewline = existing.indexOf('\n');
    if (firstNewline < 0) {
      writeFileSync(changelogPath, existing + '\n\n' + entry + '\n');
    } else {
      writeFileSync(
        changelogPath,
        existing.slice(0, firstNewline + 1) + '\n' + entry + '\n' + existing.slice(firstNewline + 1)
      );
    }
  }
}

async function confirm(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  try {
    const answer = await rl.question(`${question} [y/N] `);
    return /^y(es)?$/i.test(answer.trim());
  } finally {
    rl.close();
  }
}

async function main() {
  const flags = parseArgs();
  if (flags.help) {
    printHelp();
    process.exit(0);
  }

  console.log(`${BOLD}${BLUE}local-release${RESET} — preview the next VS Code extension release`);
  console.log(`  package: ${pkgRoot}`);

  const currentVersion = readPkgVersion();
  const lastTag = findLastTag(flags.tagPrefix);
  console.log(`  current version:      ${BOLD}${currentVersion}${RESET}`);
  console.log(`  last release tag:     ${lastTag ?? '(none — first release)'}`);

  const commits = getCommitsSince(lastTag);
  const { bump: detectedBump, relevant } = decideBumpFromCommits(commits);

  const bumpKind = flags.bump ?? detectedBump;
  console.log(`  commits since tag:    ${commits.length}`);
  console.log(`  relevant commits:     ${relevant.length}`);
  console.log(`  detected bump:        ${detectedBump}${flags.bump ? ` (overridden with --${flags.bump})` : ''}`);
  console.log();

  if (bumpKind === 'none') {
    console.log(`${YELLOW}⚠ No version bump needed.${RESET}`);
    console.log(`  ${DIM}Only chore/docs/refactor/test/build/ci commits since ${lastTag ?? 'bootstrap'}.${RESET}`);
    console.log(`  ${DIM}To force a bump anyway, re-run with --patch / --minor / --major.${RESET}`);
    process.exit(0);
  }

  const newVersion = bumpVersion(currentVersion, bumpKind);
  console.log(`${BOLD}Planned change:${RESET}`);
  console.log(`  ${currentVersion}  →  ${GREEN}${newVersion}${RESET}  (${bumpKind})`);
  console.log();

  if (relevant.length > 0) {
    console.log(`${BOLD}Commits that will be listed in CHANGELOG:${RESET}`);
    for (const c of relevant) {
      const tag = c.type === 'breaking' ? `${RED}BREAKING${RESET}` : `${BLUE}${c.type}${RESET}`;
      console.log(`  ${DIM}${c.sha.slice(0, 7)}${RESET}  [${tag}] ${c.subject}`);
    }
    console.log();
  }

  const changelogEntry = buildChangelogEntry(newVersion, relevant, bumpKind);
  console.log(`${BOLD}CHANGELOG entry (preview):${RESET}`);
  console.log(DIM);
  console.log(
    changelogEntry
      .split('\n')
      .map((l) => `  ${l}`)
      .join('\n')
  );
  console.log(RESET);

  if (flags.dryRun) {
    console.log(`${YELLOW}--dry-run: no files modified.${RESET}`);
    process.exit(0);
  }

  if (!flags.yes) {
    const ok = await confirm(`Apply this bump + CHANGELOG entry?`);
    if (!ok) {
      console.log(`${DIM}Aborted.${RESET}`);
      process.exit(0);
    }
  }

  writePkgVersion(newVersion);
  console.log(`${GREEN}✓${RESET} Wrote version ${newVersion} to packages/azure-migration-squad-vscode/package.json`);

  prependToChangelog(changelogEntry);
  console.log(`${GREEN}✓${RESET} Updated CHANGELOG.md`);

  if (flags.build) {
    console.log();
    console.log(`${BOLD}Building + packaging the .vsix...${RESET}`);
    run('npm run build', { cwd: pkgRoot, stdio: 'inherit' });
    run('npm run package', { cwd: pkgRoot, stdio: 'inherit' });
  }

  console.log();
  console.log(`${GREEN}✓ Done.${RESET}`);
  console.log();
  console.log(`${BOLD}Next steps (NOT automated — inspect first):${RESET}`);
  console.log(`  ${DIM}# Review the changes${RESET}`);
  console.log(`  git diff packages/azure-migration-squad-vscode/package.json packages/azure-migration-squad-vscode/CHANGELOG.md`);
  console.log(`  ${DIM}# If it looks right:${RESET}`);
  console.log(`  git add packages/azure-migration-squad-vscode/{package.json,CHANGELOG.md}`);
  console.log(`  git commit -m "chore: release ${flags.tagPrefix}${newVersion}"`);
  console.log(`  git tag ${flags.tagPrefix}${newVersion}`);
  console.log(`  git push origin HEAD ${flags.tagPrefix}${newVersion}`);
  console.log();
  console.log(`${DIM}For the automated flow, see docs/publishing-vscode-extension.md${RESET}`);
}

main().catch((err) => {
  console.error(`${RED}✗ local-release failed:${RESET} ${err.message}`);
  process.exit(1);
});
