/**
 * Build-time validation — runs after `npm run sync`, before `npm pack`.
 *
 * Validates:
 *   - templates/ exists and is non-empty
 *   - Expected key files were synced (Capability Matrix skill, Discovery dossier, etc.)
 *   - JSON Schemas parse as valid JSON
 *   - package.json `files` list covers what's actually shipped
 *   - ALL skill / chatmode / prompt frontmatter descriptions are ≤1024 chars
 *     (GitHub Copilot/Squad refuses to load longer descriptions — real bug in v0.1.0-insider.0)
 *
 * Exits non-zero on any failure.
 */

import { promises as fs, existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgRoot = path.resolve(__dirname, '..');
const templatesDir = path.join(pkgRoot, 'templates');

let problems = 0;
const fail = (msg) => {
  console.error(`  ✗ ${msg}`);
  problems++;
};
const ok = (msg) => console.log(`  ✓ ${msg}`);

console.log('[validate-build] checking package integrity...\n');

// 1. templates/ exists
if (!existsSync(templatesDir)) {
  fail('templates/ directory missing — did you forget `npm run sync`?');
} else {
  ok('templates/ exists');
}

// 2. Key files synced
const REQUIRED_TEMPLATE_FILES = [
  'templates/github/skills/capability-matrix.md',
  'templates/github/skills/migration-strategy-decision-tree.md',
  'templates/github/skills/discovery-dossier-template.md',
  'templates/github/skills/stack-detection.md',
  'templates/github/prompts/Assess-Any-Application.prompt.md',
  'templates/github/prompts/Build-Migration-Plan.prompt.md',
  'templates/github/chatmodes/Discovery-Intake.chatmode.md',
  'templates/github/chatmodes/Migration-Orchestrator.chatmode.md',
  'templates/squad/agents/discovery-engineer/charter.md',
];
for (const f of REQUIRED_TEMPLATE_FILES) {
  const fp = path.join(pkgRoot, f);
  existsSync(fp) ? ok(`required file synced: ${f}`) : fail(`MISSING required file: ${f}`);
}

// 3. JSON Schemas parse
const SCHEMAS = ['schemas/capability-matrix.schema.json', 'schemas/discovery-dossier.schema.json'];
for (const s of SCHEMAS) {
  const fp = path.join(pkgRoot, s);
  try {
    const content = readFileSync(fp, 'utf-8');
    const parsed = JSON.parse(content);
    if (!parsed.$schema || !parsed.title) {
      fail(`schema ${s} missing $schema or title`);
    } else {
      ok(`schema valid JSON: ${s}`);
    }
  } catch (err) {
    fail(`schema ${s} failed to parse: ${err.message}`);
  }
}

// 4. package.json `files` allow-list sanity
const pkg = JSON.parse(readFileSync(path.join(pkgRoot, 'package.json'), 'utf-8'));
const REQUIRED_IN_FILES = ['bin', 'lib', 'schemas', 'templates'];
for (const r of REQUIRED_IN_FILES) {
  pkg.files?.includes(r)
    ? ok(`package.json "files" includes: ${r}`)
    : fail(`package.json "files" MISSING: ${r}`);
}

// 5. bin/cli.js executable
const cliPath = path.join(pkgRoot, 'bin', 'cli.js');
if (existsSync(cliPath)) {
  const content = readFileSync(cliPath, 'utf-8');
  content.startsWith('#!/usr/bin/env node')
    ? ok('bin/cli.js has shebang')
    : fail('bin/cli.js missing #!/usr/bin/env node shebang');
}

// 6. Frontmatter description lengths in templates/ (≤1024 chars).
// GitHub Copilot/Squad refuses to load skills/chatmodes/prompts with longer
// descriptions. Real bug caught only in v0.1.0-insider.0 when users hit it.
const MAX_DESC = 1024;

function extractDescription(content) {
  const fmMatch = content.match(/^---\s*\r?\n([\s\S]*?)\r?\n---/);
  if (!fmMatch) return null;
  const fm = fmMatch[1];
  let m = fm.match(/^description:\s*\|\s*\r?\n((?:  .+\r?\n?)+)/m);
  if (m) return m[1].replace(/^  /gm, '');
  m = fm.match(/^description:\s*>\s*\r?\n((?:  .+\r?\n?)+)/m);
  if (m) return m[1].replace(/^  /gm, '');
  m = fm.match(/^description:\s*"((?:[^"\\]|\\.)*)"/m);
  if (m) return m[1];
  m = fm.match(/^description:\s*'((?:[^'\\]|\\.)*)'/m);
  if (m) return m[1];
  m = fm.match(/^description:\s*(.+)$/m);
  if (m) return m[1];
  return null;
}

async function walkMd(dir) {
  const out = [];
  if (!existsSync(dir)) return out;
  const stack = [dir];
  while (stack.length) {
    const cur = stack.pop();
    const entries = await fs.readdir(cur, { withFileTypes: true });
    for (const e of entries) {
      const p = path.join(cur, e.name);
      if (e.isDirectory()) stack.push(p);
      else if (e.name.endsWith('.md')) out.push(p);
    }
  }
  return out;
}

const TEMPLATE_SCAN = [
  path.join(templatesDir, 'github', 'skills'),
  path.join(templatesDir, 'github', 'chatmodes'),
  path.join(templatesDir, 'github', 'prompts'),
];

let descOver = 0;
for (const dir of TEMPLATE_SCAN) {
  const files = await walkMd(dir);
  for (const f of files) {
    const desc = extractDescription(readFileSync(f, 'utf-8'));
    if (desc && desc.length > MAX_DESC) {
      fail(`description >1024 chars (${desc.length}): templates/${path.relative(templatesDir, f).replace(/\\/g, '/')}`);
      descOver++;
    }
  }
}
if (descOver === 0) ok('All template description fields ≤1024 chars');

console.log('');
if (problems > 0) {
  console.error(`[validate-build] FAILED — ${problems} problem(s).`);
  process.exit(1);
} else {
  console.log('[validate-build] all checks passed.');
}
