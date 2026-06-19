/**
 * Remove everything in templates/ except the directory itself and .gitkeep,
 * so the next sync starts from a clean slate.
 */

import { promises as fs } from 'node:fs';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const templatesDir = path.resolve(__dirname, '..', 'templates');

async function main() {
  if (!existsSync(templatesDir)) {
    await fs.mkdir(templatesDir, { recursive: true });
    return;
  }

  const entries = await fs.readdir(templatesDir);
  for (const entry of entries) {
    if (entry === '.gitkeep') continue;
    await fs.rm(path.join(templatesDir, entry), { recursive: true, force: true });
  }

  console.log(`[clean-templates] cleaned ${templatesDir}`);
}

main().catch((err) => {
  console.error('[clean-templates] FAILED:', err);
  process.exit(1);
});
