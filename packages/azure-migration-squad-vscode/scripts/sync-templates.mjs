/**
 * Sync canonical `.github/*` + MIGRATION-START-HERE.md from the monorepo root
 * into the extension's `templates/` folder. This folder is bundled into the
 * .vsix so the extension can copy it into a user's workspace on Initialize.
 *
 * Run automatically via `prepackage` (which runs before `vsce package`) and
 * `pretest` (before headless tests).
 */

import { promises as fs } from 'node:fs';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgRoot = path.resolve(__dirname, '..');
const monorepoRoot = path.resolve(pkgRoot, '..', '..');
const templatesDir = path.join(pkgRoot, 'templates');

const COPY_MAP = [
  { src: '.github/agents', dest: 'github/agents' },
  { src: '.github/prompts', dest: 'github/prompts' },
  { src: '.github/skills', dest: 'github/skills' },
  { src: '.github/chatmodes', dest: 'github/chatmodes' },
  { src: '.github/hooks', dest: 'github/hooks' },
  { src: '.github/copilot-instructions.md', dest: 'github/copilot-instructions.md' },
  { src: 'MIGRATION-START-HERE.md', dest: 'MIGRATION-START-HERE.md' },
];

const EXCLUDE_PATTERNS = [/[\\/]legacy[\\/]/i, /node_modules/];

function shouldExclude(p) {
  return EXCLUDE_PATTERNS.some((re) => re.test(p));
}

async function copyRecursive(src, dest) {
  const stat = await fs.stat(src);
  if (stat.isDirectory()) {
    await fs.mkdir(dest, { recursive: true });
    const entries = await fs.readdir(src);
    for (const entry of entries) {
      const srcChild = path.join(src, entry);
      const destChild = path.join(dest, entry);
      if (shouldExclude(srcChild)) continue;
      await copyRecursive(srcChild, destChild);
    }
  } else {
    await fs.mkdir(path.dirname(dest), { recursive: true });
    await fs.copyFile(src, dest);
  }
}

async function countFiles(dir) {
  if (!existsSync(dir)) return 0;
  const stat = await fs.stat(dir);
  if (stat.isFile()) return 1;
  let count = 0;
  const entries = await fs.readdir(dir);
  for (const entry of entries) {
    count += await countFiles(path.join(dir, entry));
  }
  return count;
}

async function cleanTemplates() {
  if (!existsSync(templatesDir)) {
    await fs.mkdir(templatesDir, { recursive: true });
    return;
  }
  const entries = await fs.readdir(templatesDir);
  for (const entry of entries) {
    if (entry === '.gitkeep' || entry === 'README.md') continue;
    await fs.rm(path.join(templatesDir, entry), {
      recursive: true,
      force: true,
      maxRetries: 3,
      retryDelay: 200,
    });
  }
}

async function main() {
  console.log(`[sync-templates] monorepo root: ${monorepoRoot}`);
  console.log(`[sync-templates] target:        ${templatesDir}`);

  await cleanTemplates();
  await fs.mkdir(templatesDir, { recursive: true });

  let total = 0;
  for (const { src, dest } of COPY_MAP) {
    const srcPath = path.join(monorepoRoot, src);
    const destPath = path.join(templatesDir, dest);
    if (!existsSync(srcPath)) {
      console.warn(`[sync-templates] ⚠  Source missing, skipping: ${src}`);
      continue;
    }
    await copyRecursive(srcPath, destPath);
    const fileCount = await countFiles(destPath);
    total += fileCount;
    console.log(
      `[sync-templates]  ✓ ${src.padEnd(40)} → templates/${dest} (${fileCount} file${
        fileCount !== 1 ? 's' : ''
      })`
    );
  }

  await fs.writeFile(
    path.join(templatesDir, 'SYNC-MANIFEST.json'),
    JSON.stringify(
      {
        syncedAt: new Date().toISOString(),
        totalFiles: total,
        sources: COPY_MAP.map((c) => c.src),
      },
      null,
      2
    ) + '\n'
  );

  console.log(`[sync-templates] done. ${total} file(s) synced.`);
}

main().catch((err) => {
  console.error('[sync-templates] FAILED:', err);
  process.exit(1);
});
