/**
 * Sync canonical content from the monorepo root into the package's templates/ folder.
 *
 * Source of truth lives at the root (.github/* and .squad/agents/) — they're actively
 * dogfooded as the user runs Copilot/Squad against this very repo. The templates/ folder
 * in this package is a build artifact, produced by this script.
 *
 * Run automatically via `npm run prebuild` (which runs before `npm pack` / `npm publish`).
 * Manual: `npm run sync` from inside packages/azure-migration-squad/.
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
  { src: '.github/chatmodes', dest: 'github/chatmodes' },
  { src: '.github/prompts', dest: 'github/prompts' },
  { src: '.github/skills', dest: 'github/skills' },
  { src: '.github/hooks', dest: 'github/hooks' },
  { src: '.github/copilot-instructions.md', dest: 'github/copilot-instructions.md' },
  { src: '.squad/agents', dest: 'squad/agents' },
  { src: '.squad/team.md', dest: 'squad/team.md' },
  { src: '.squad/routing.md', dest: 'squad/routing.md' },
  { src: 'AGENTS.md', dest: 'AGENTS.md' },
  { src: 'MIGRATION-START-HERE.md', dest: 'MIGRATION-START-HERE.md' },
];

const EXCLUDE_PATTERNS = [
  /[\\/]legacy[\\/]/i,
  /\.azure-pipelines/i,
  /node_modules/,
];

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
  let count = 0;
  const stat = await fs.stat(dir);
  if (stat.isFile()) return 1;
  const entries = await fs.readdir(dir);
  for (const entry of entries) {
    count += await countFiles(path.join(dir, entry));
  }
  return count;
}

async function main() {
  console.log(`[sync-from-root] monorepo root: ${monorepoRoot}`);
  console.log(`[sync-from-root] target:        ${templatesDir}`);

  await fs.mkdir(templatesDir, { recursive: true });

  let total = 0;
  for (const { src, dest } of COPY_MAP) {
    const srcPath = path.join(monorepoRoot, src);
    const destPath = path.join(templatesDir, dest);

    if (!existsSync(srcPath)) {
      console.warn(`[sync-from-root] ⚠  Source missing, skipping: ${src}`);
      continue;
    }

    await copyRecursive(srcPath, destPath);
    const fileCount = await countFiles(destPath);
    total += fileCount;
    console.log(`[sync-from-root]  ✓ ${src.padEnd(40)} → templates/${dest} (${fileCount} file${fileCount !== 1 ? 's' : ''})`);
  }

  console.log(`[sync-from-root] done. ${total} file(s) synced.`);

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
    )
  );
}

main().catch((err) => {
  console.error('[sync-from-root] FAILED:', err);
  process.exit(1);
});
