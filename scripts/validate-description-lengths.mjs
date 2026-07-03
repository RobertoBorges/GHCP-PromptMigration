/**
 * Validate YAML frontmatter description fields on all skill/chatmode/prompt
 * markdown files don't exceed the 1024-character limit enforced by
 * GitHub Copilot when loading them.
 *
 * A real bug in v0.1.0-insider.0: migration-strategy-report/SKILL.md had a
 * 1273-char description and crashed the Copilot extension loader. This check fails the
 * build before publish so it never ships again.
 */

import { promises as fs, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');

const MAX_DESCRIPTION_LENGTH = 1024;

const SCAN_DIRS = [
  '.github/skills',
  '.github/chatmodes',
  '.github/prompts',
];

/** Extract YAML frontmatter description field from markdown content. */
function extractDescription(content) {
  const fmMatch = content.match(/^---\s*\r?\n([\s\S]*?)\r?\n---/);
  if (!fmMatch) return null;
  const fm = fmMatch[1];

  // YAML literal block: description: |  (then 2-space-indented lines)
  let m = fm.match(/^description:\s*\|\s*\r?\n((?:  .+\r?\n?)+)/m);
  if (m) {
    // strip the 2-space indent from each line for accurate length
    return m[1].replace(/^  /gm, '');
  }

  // YAML folded block: description: >
  m = fm.match(/^description:\s*>\s*\r?\n((?:  .+\r?\n?)+)/m);
  if (m) return m[1].replace(/^  /gm, '');

  // Quoted string
  m = fm.match(/^description:\s*"((?:[^"\\]|\\.)*)"/m);
  if (m) return m[1];
  m = fm.match(/^description:\s*'((?:[^'\\]|\\.)*)'/m);
  if (m) return m[1];

  // Plain scalar
  m = fm.match(/^description:\s*(.+)$/m);
  if (m) return m[1];

  return null;
}

async function* walk(dir) {
  let entries;
  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of entries) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      yield* walk(p);
    } else if (e.name.endsWith('.md')) {
      yield p;
    }
  }
}

let problems = 0;
const overLimit = [];

for (const dir of SCAN_DIRS) {
  const absDir = path.join(repoRoot, dir);
  for await (const file of walk(absDir)) {
    const content = readFileSync(file, 'utf-8');
    const desc = extractDescription(content);
    if (desc && desc.length > MAX_DESCRIPTION_LENGTH) {
      overLimit.push({
        file: path.relative(repoRoot, file),
        length: desc.length,
        over: desc.length - MAX_DESCRIPTION_LENGTH,
      });
      problems++;
    }
  }
}

if (problems > 0) {
  console.error('✗ Description-length check FAILED. The following files exceed the 1024-char limit:');
  console.error('');
  for (const { file, length, over } of overLimit) {
    console.error(`  • ${file}`);
    console.error(`    description: ${length} chars (${over} over limit)`);
  }
  console.error('');
  console.error('Fix: shorten each "description:" YAML frontmatter field to ≤1024 chars.');
  console.error('GitHub Copilot refuses to load skills with longer descriptions.');
  process.exit(1);
}

console.log('✓ All description fields are within the 1024-character limit.');
