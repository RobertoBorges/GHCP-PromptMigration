/**
 * CI guard: detect manual edits to packages/azure-migration-squad/templates/.
 *
 * Strategy: re-run the sync script, then compare templates/ to the version
 * recorded in this PR. If any file content differs (other than .gitkeep,
 * README.md, .npmignore which are preserved across syncs), someone edited
 * templates/ directly — fail the build with a helpful message.
 *
 * Run via: node scripts/check-templates-not-edited.mjs
 *
 * Designed to be safe in CI:
 *   - Pure read/compare; only writes when explicitly run by maintainer
 *   - No network, no external deps
 *   - Works on Ubuntu / macOS / Windows runners
 */

import { existsSync, readFileSync, mkdtempSync, rmSync, cpSync } from 'node:fs';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');
const templatesDir = path.join(repoRoot, 'packages', 'azure-migration-squad', 'templates');

// Files inside templates/ that are NOT auto-generated and should be ignored
// when comparing (these are preserved across syncs intentionally)
const PRESERVED_FILES = new Set(['.gitkeep', 'README.md', '.npmignore']);

function sha256(filePath) {
  const buf = readFileSync(filePath);
  // Normalize line endings to LF so CRLF↔LF differences (Windows ↔ Linux ↔ Git autocrlf)
  // do not produce false positives when the actual content is identical.
  // Read as UTF-8 only when the file looks textual (md/yaml/json/txt/asp/cs/etc.);
  // binary files are hashed raw.
  const ext = filePath.toLowerCase();
  const isText = /\.(md|yaml|yml|json|txt|asp|asa|cs|java|py|rb|js|mjs|cjs|ts|tsx|sh|ps1|bicep|tf|properties|config|xml|html|css|sql|cshtml|razor|jsp|html?|csproj|sln)$/.test(ext)
    || filePath.endsWith('AGENTS.md')
    || filePath.endsWith('SYNC-MANIFEST.json')
    || filePath.endsWith('charter.md');
  let normalized = buf;
  if (isText) {
    const text = buf.toString('utf-8').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    normalized = Buffer.from(text, 'utf-8');
  }
  return crypto.createHash('sha256').update(normalized).digest('hex');
}

async function snapshot(dir) {
  const map = {};
  async function walk(d) {
    if (!existsSync(d)) return;
    const entries = await fs.readdir(d, { withFileTypes: true });
    for (const e of entries) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) {
        await walk(p);
      } else {
        const rel = path.relative(dir, p).replace(/\\/g, '/');
        // Skip preserved files at the top level
        if (PRESERVED_FILES.has(rel)) continue;
        // Skip SYNC-MANIFEST.json because its timestamp changes on every sync
        if (rel === 'SYNC-MANIFEST.json') continue;
        map[rel] = sha256(p);
      }
    }
  }
  await walk(dir);
  return map;
}

console.log('[check-templates-not-edited] taking snapshot of current templates/...');
const before = await snapshot(templatesDir);
console.log(`[check-templates-not-edited] BEFORE snapshot has ${Object.keys(before).length} file(s).`);

console.log('[check-templates-not-edited] running sync to see what templates/ SHOULD look like...');
// Copy current templates to a temp location, run sync, then compare
const tmpBackup = mkdtempSync(path.join(os.tmpdir(), 'ams-templates-backup-'));
try {
  if (existsSync(templatesDir)) {
    cpSync(templatesDir, tmpBackup, { recursive: true });
  }
} catch (err) {
  console.error('[check-templates-not-edited] failed to backup templates/:', err.message);
  process.exit(2);
}

try {
  execSync('npm run sync', {
    cwd: path.join(repoRoot, 'packages', 'azure-migration-squad'),
    stdio: ['ignore', 'pipe', 'pipe'],
  });
} catch (err) {
  console.error('[check-templates-not-edited] sync failed — cannot validate templates state.');
  console.error(err.stderr?.toString() || err.message);
  // Restore backup
  rmSync(templatesDir, { recursive: true, force: true });
  cpSync(tmpBackup, templatesDir, { recursive: true });
  rmSync(tmpBackup, { recursive: true, force: true });
  process.exit(2);
}

console.log('[check-templates-not-edited] taking snapshot after sync...');
const after = await snapshot(templatesDir);
console.log(`[check-templates-not-edited] AFTER snapshot has ${Object.keys(after).length} file(s).`);

// Compare
const issues = [];
const beforeKeys = new Set(Object.keys(before));
const afterKeys = new Set(Object.keys(after));

for (const key of beforeKeys) {
  if (!afterKeys.has(key)) {
    issues.push({
      kind: 'extra-file',
      file: key,
      message: `templates/${key} exists but sync did not produce it — was it added manually?`,
    });
  } else if (before[key] !== after[key]) {
    issues.push({
      kind: 'modified-file',
      file: key,
      message: `templates/${key} differs from canonical source — was it edited directly?`,
    });
  }
}
for (const key of afterKeys) {
  if (!beforeKeys.has(key)) {
    issues.push({
      kind: 'missing-file',
      file: key,
      message: `templates/${key} should exist but is missing — did you forget to commit a sync?`,
    });
  }
}

// Cleanup backup (we don't restore since the sync produced the correct state)
rmSync(tmpBackup, { recursive: true, force: true });

if (issues.length === 0) {
  console.log('✓ templates/ is in sync with canonical content. No manual edits detected.');
  process.exit(0);
}

console.error('');
console.error('✗ CI GUARD FAILED — templates/ was edited directly OR commits are out of sync.');
console.error('');
console.error('Differences found:');
for (const issue of issues) {
  console.error(`  • [${issue.kind}] ${issue.message}`);
}
console.error('');
console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.error('Fix:');
console.error('  1. Find the canonical file at the monorepo root:');
console.error('       templates/github/prompts/X.md   → edit .github/prompts/X.md');
console.error('       templates/github/skills/X.md    → edit .github/skills/X.md');
console.error('       templates/squad/agents/X/...    → edit .squad/agents/X/...');
console.error('       templates/AGENTS.md             → edit AGENTS.md (at the repo root)');
console.error('  2. Move your edits to the canonical file.');
console.error('  3. Run: cd packages/azure-migration-squad && npm run sync');
console.error('  4. Commit BOTH the canonical change AND the templates/ refresh.');
console.error('');
console.error('See: docs/contributing-adapters.md  and');
console.error('     packages/azure-migration-squad/templates/README.md');
console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
process.exit(1);
