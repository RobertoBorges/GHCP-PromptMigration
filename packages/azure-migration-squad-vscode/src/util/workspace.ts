/**
 * Workspace helpers — find the project root and detect install state.
 *
 * The extension supports multi-root workspaces, but for tree views we pick
 * the first workspace folder that contains a `.github/prompts/` directory
 * (the marker that the migration agent has been initialized). If none is
 * found, the user hasn't initialized yet.
 */

import * as path from 'path';
import * as fs from 'fs';
import * as vscode from 'vscode';

export interface AmsWorkspace {
  /** Root path of the workspace folder containing migration content. */
  root: string;
  /** True if `.github/agents/Code-Migration-Modernization.agent.md` exists. */
  hasAgent: boolean;
  /** True if `.github/prompts/` exists. */
  hasPrompts: boolean;
  /** True if `.github/skills/` exists. */
  hasSkills: boolean;
  /** True if `.github/copilot-instructions.md` exists. */
  hasCopilotInstructions: boolean;
  /** True if all the core surfaces are installed. */
  isInstalled: boolean;
}

export function findAmsWorkspace(): AmsWorkspace | null {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) {
    return null;
  }

  for (const folder of folders) {
    const root = folder.uri.fsPath;
    const ws = inspectWorkspace(root);
    if (ws.hasPrompts || ws.hasAgent || ws.hasSkills) {
      return ws;
    }
  }

  // No workspace folder has migration content — return the first folder so the
  // user can run "Initialize" against it.
  return inspectWorkspace(folders[0].uri.fsPath);
}

function inspectWorkspace(root: string): AmsWorkspace {
  const hasAgent = fs.existsSync(
    path.join(root, '.github', 'agents', 'Code-Migration-Modernization.agent.md')
  );
  const hasPrompts = fs.existsSync(path.join(root, '.github', 'prompts'));
  const hasSkills = fs.existsSync(path.join(root, '.github', 'skills'));
  const hasCopilotInstructions = fs.existsSync(
    path.join(root, '.github', 'copilot-instructions.md')
  );
  return {
    root,
    hasAgent,
    hasPrompts,
    hasSkills,
    hasCopilotInstructions,
    isInstalled: hasAgent && hasPrompts && hasSkills && hasCopilotInstructions,
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

    const fm = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (fm) {
      const desc = fm[1].match(/(?:^|\n)description\s*:\s*"?([^"\n]+)"?/);
      if (desc) {
        return desc[1].trim();
      }
    }

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
        return trimmed.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').slice(0, 200);
      }
    }
  } catch {
    // ignore — file unreadable
  }
  return '';
}
