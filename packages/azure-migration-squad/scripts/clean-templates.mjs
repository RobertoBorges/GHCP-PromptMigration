/**
 * Remove everything in templates/ except the directory itself, .gitkeep, and README.md
 * so the next sync starts from a clean slate.
 *
 * README.md in templates/ is a "DO NOT EDIT" sign for anyone opening the folder —
 * it's intentionally preserved across syncs.
 */

import { promises as fs } from 'node:fs';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const templatesDir = path.resolve(__dirname, '..', 'templates');

const PRESERVE = new Set(['.gitkeep', 'README.md']);

async function main() {
  if (!existsSync(templatesDir)) {
    await fs.mkdir(templatesDir, { recursive: true });
    return;
  }

  const entries = await fs.readdir(templatesDir);
  for (const entry of entries) {
    if (PRESERVE.has(entry)) continue;
    await fs.rm(path.join(templatesDir, entry), { recursive: true, force: true });
  }

  console.log(`[clean-templates] cleaned ${templatesDir} (preserved: ${[...PRESERVE].join(', ')})`);
}

main().catch((err) => {
  console.error('[clean-templates] FAILED:', err);
  process.exit(1);
});
