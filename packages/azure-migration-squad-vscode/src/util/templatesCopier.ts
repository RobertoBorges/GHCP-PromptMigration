/**
 * Copy bundled templates from the extension into the user's workspace.
 *
 * The extension ships a `templates/` directory at its installation root
 * (populated from .github/* at build time by scripts/sync-templates.mjs).
 * This module finds that directory and copies its contents into the user's
 * workspace under `.github/` (or relevant paths).
 *
 * Replaces the old npx-based init flow — no Node.js shell-out required.
 */

import * as path from 'path';
import * as fs from 'fs';
import * as vscode from 'vscode';

export interface CopyResult {
  copied: number;
  skipped: number;
  copiedFiles: string[];
  skippedFiles: string[];
}

/**
 * Map of `templates/<source>` → `<workspace>/<target>`.
 * Order matters only for messaging; copies are independent.
 */
const COPY_MAP: Array<{ src: string; dest: string }> = [
  { src: 'github/agents', dest: '.github/agents' },
  { src: 'github/prompts', dest: '.github/prompts' },
  { src: 'github/skills', dest: '.github/skills' },
  { src: 'github/chatmodes', dest: '.github/chatmodes' },
  { src: 'github/hooks', dest: '.github/hooks' },
  { src: 'github/copilot-instructions.md', dest: '.github/copilot-instructions.md' },
  { src: 'MIGRATION-START-HERE.md', dest: 'MIGRATION-START-HERE.md' },
];

/** Returns the templates root inside the installed extension. */
export function getTemplatesRoot(extensionUri: vscode.Uri): string {
  return path.join(extensionUri.fsPath, 'templates');
}

/**
 * Copy templates into the workspace.
 *
 * Behavior:
 *   - For directories: recursive copy. Existing files at the destination are
 *     overwritten if `overwrite=true`, otherwise skipped.
 *   - For single files (e.g., copilot-instructions.md, MIGRATION-START-HERE.md):
 *     same overwrite-vs-skip rule.
 *   - Always creates parent directories.
 *
 * Throws if `templates/` doesn't exist (means the extension was packaged
 * incorrectly).
 */
export async function copyTemplatesToWorkspace(
  extensionUri: vscode.Uri,
  workspaceRoot: string,
  options: { overwrite?: boolean } = {}
): Promise<CopyResult> {
  const overwrite = options.overwrite ?? false;
  const templatesRoot = getTemplatesRoot(extensionUri);
  if (!fs.existsSync(templatesRoot)) {
    throw new Error(
      `Templates not found at ${templatesRoot}. The extension may have been packaged incorrectly.`
    );
  }

  const result: CopyResult = { copied: 0, skipped: 0, copiedFiles: [], skippedFiles: [] };

  for (const { src, dest } of COPY_MAP) {
    const srcPath = path.join(templatesRoot, src);
    const destPath = path.join(workspaceRoot, dest);
    if (!fs.existsSync(srcPath)) {
      // Optional content missing — skip silently. Required content (prompts/agents) is asserted by the caller.
      continue;
    }
    await copyRecursive(srcPath, destPath, overwrite, result, workspaceRoot);
  }

  return result;
}

async function copyRecursive(
  src: string,
  dest: string,
  overwrite: boolean,
  result: CopyResult,
  workspaceRoot: string
): Promise<void> {
  const stat = await fs.promises.stat(src);
  if (stat.isDirectory()) {
    await fs.promises.mkdir(dest, { recursive: true });
    const entries = await fs.promises.readdir(src);
    for (const entry of entries) {
      await copyRecursive(
        path.join(src, entry),
        path.join(dest, entry),
        overwrite,
        result,
        workspaceRoot
      );
    }
    return;
  }
  // File
  const rel = path.relative(workspaceRoot, dest);
  if (fs.existsSync(dest) && !overwrite) {
    result.skipped++;
    result.skippedFiles.push(rel);
    return;
  }
  await fs.promises.mkdir(path.dirname(dest), { recursive: true });
  await fs.promises.copyFile(src, dest);
  result.copied++;
  result.copiedFiles.push(rel);
}
