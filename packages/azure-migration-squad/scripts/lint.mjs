/**
 * Lightweight lint — checks no PII fields slip into telemetry calls and no obvious bugs.
 */

import { promises as fs, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgRoot = path.resolve(__dirname, '..');

let problems = 0;

async function* walk(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (['node_modules', 'templates', '.git'].includes(e.name)) continue;
      yield* walk(p);
    } else {
      yield p;
    }
  }
}

const FORBIDDEN_IN_TELEMETRY = [
  /track\([^)]*['"]\s*path\s*['"]/i,
  /track\([^)]*['"]\s*file_path\s*['"]/i,
  /track\([^)]*['"]\s*email\s*['"]/i,
  /track\([^)]*['"]\s*git_remote\s*['"]/i,
  /track\([^)]*['"]\s*cwd\s*['"]/i,
];

for await (const file of walk(pkgRoot)) {
  if (!file.endsWith('.js') && !file.endsWith('.mjs')) continue;
  const content = readFileSync(file, 'utf-8');
  for (const re of FORBIDDEN_IN_TELEMETRY) {
    if (re.test(content)) {
      console.error(`✗ Potential PII in telemetry: ${path.relative(pkgRoot, file)} matches ${re}`);
      problems++;
    }
  }
}

if (problems > 0) {
  console.error(`\n[lint] FAILED — ${problems} potential PII leak(s) in telemetry code.`);
  process.exit(1);
}
console.log('[lint] no PII leaks detected in telemetry calls.');
