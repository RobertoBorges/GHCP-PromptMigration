/**
 * Workspace helpers — find the AMS root folder and detect install state.
 *
 * The extension supports multi-root workspaces, but for tree views we pick
 * the first workspace folder that contains a .squad/ or .github/prompts/
 * directory. If none is found, the user hasn't initialized AMS yet.
 */

import * as path from 'path';
import * as fs from 'fs';
import * as vscode from 'vscode';

export interface AmsWorkspace {
  /** Root path of the workspace folder containing AMS content. */
  root: string;
  /** True if `.azure-migration-squad/manifest.json` exists. */
  hasManifest: boolean;
  /** True if `.squad/agents/` exists. */
  hasSquad: boolean;
  /** True if `.github/prompts/` exists. */
  hasPrompts: boolean;
  /** Parsed manifest if present. */
  manifest?: {
    package: string;
    version: string;
    installedAt: string;
    filesCopied: number;
    filesSkipped: number;
    squadDetected: boolean;
  };
}

export function findAmsWorkspace(): AmsWorkspace | null {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) {
    return null;
  }

  for (const folder of folders) {
    const root = folder.uri.fsPath;
    const squadAgents = path.join(root, '.squad', 'agents');
    const ghPrompts = path.join(root, '.github', 'prompts');
    const manifestPath = path.join(root, '.azure-migration-squad', 'manifest.json');

    const hasSquad = fs.existsSync(squadAgents);
    const hasPrompts = fs.existsSync(ghPrompts);
    const hasManifest = fs.existsSync(manifestPath);

    if (hasSquad || hasPrompts || hasManifest) {
      let manifest;
      if (hasManifest) {
        try {
          manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
        } catch {
          // Malformed manifest — treat as not-installed.
        }
      }
      return { root, hasManifest, hasSquad, hasPrompts, manifest };
    }
  }

  // No workspace folder has AMS content — return the first folder so the
  // user can run "Initialize" against it.
  const first = folders[0];
  return {
    root: first.uri.fsPath,
    hasManifest: false,
    hasSquad: false,
    hasPrompts: false,
  };
}

/**
 * List all markdown files in a directory (optionally recursive).
 */
export function listMarkdownFiles(dir: string, recursive = false): string[] {
  if (!fs.existsSync(dir)) {
    return [];
  }
  const out: string[] = [];
  function walk(d: string) {
    const entries = fs.readdirSync(d, { withFileTypes: true });
    for (const e of entries) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) {
        if (recursive) walk(p);
      } else if (e.name.endsWith('.md')) {
        out.push(p);
      }
    }
  }
  walk(dir);
  return out.sort((a, b) => path.basename(a).localeCompare(path.basename(b)));
}

/**
 * Extract a brief description from a markdown file.
 * Strategy: pull YAML frontmatter `description:` if present, else use the
 * first non-empty paragraph after any heading.
 */
export function extractDescription(filePath: string): string {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');

    // Try YAML frontmatter description
    const fm = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (fm) {
      const desc = fm[1].match(/(?:^|\n)description\s*:\s*"?([^"\n]+)"?/);
      if (desc) {
        return desc[1].trim();
      }
    }

    // Fall back to first non-blank, non-heading line after frontmatter
    const body = fm ? content.slice(fm[0].length) : content;
    const lines = body.split(/\r?\n/);
    for (const line of lines) {
      const trimmed = line.trim();
      if (
        trimmed &&
        !trimmed.startsWith('#') &&
        !trimmed.startsWith('>') &&
        !trimmed.startsWith('```') &&
        !trimmed.startsWith('<!--')
      ) {
        // Strip markdown link syntax for cleaner display
        return trimmed.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').slice(0, 200);
      }
    }
  } catch {
    // ignore — file unreadable
  }
  return '';
}
