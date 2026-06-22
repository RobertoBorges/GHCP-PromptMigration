/**
 * Base class for the AMS tree providers (Agents, Prompts, Skills).
 * Each subclass declares where its content lives and produces TreeItems.
 */

import * as path from 'path';
import * as vscode from 'vscode';
import { findAmsWorkspace, listMarkdownFiles, extractDescription } from '../util/workspace';

export class AmsTreeItem extends vscode.TreeItem {
  constructor(
    label: string,
    description: string,
    public readonly filePath: string,
    iconId: string
  ) {
    super(label, vscode.TreeItemCollapsibleState.None);
    this.description = description;
    this.tooltip = `${label}\n\n${description}\n\n${filePath}`;
    this.iconPath = new vscode.ThemeIcon(iconId);
    this.command = {
      command: 'azureMigrationSquad.openFile',
      title: 'Open',
      arguments: [vscode.Uri.file(filePath)],
    };
  }
}

export class NotInstalledItem extends vscode.TreeItem {
  constructor() {
    super(
      'Click to install Azure Migration Squad here',
      vscode.TreeItemCollapsibleState.None
    );
    this.iconPath = new vscode.ThemeIcon('rocket');
    this.tooltip =
      'Run "Azure Migration: Initialize" to scaffold prompts, skills, ' +
      'and 15 specialist agents into this workspace. Squad CLI is NOT ' +
      'required — the extension bundles everything needed for Copilot Chat.';
    this.command = {
      command: 'azureMigrationSquad.initialize',
      title: 'Initialize',
    };
  }
}

export abstract class AmsTreeProviderBase implements vscode.TreeDataProvider<vscode.TreeItem> {
  protected _onDidChangeTreeData = new vscode.EventEmitter<vscode.TreeItem | undefined | void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  abstract getRelativeDir(): string;
  abstract getIconId(): string;
  abstract isRecursive(): boolean;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  async getChildren(): Promise<vscode.TreeItem[]> {
    const ws = findAmsWorkspace();
    if (!ws || (!ws.hasSquad && !ws.hasPrompts && !ws.hasManifest)) {
      return [new NotInstalledItem()];
    }

    const dir = path.join(ws.root, this.getRelativeDir());
    const files = listMarkdownFiles(dir, this.isRecursive());
    if (files.length === 0) {
      const empty = new vscode.TreeItem('(none found)');
      empty.iconPath = new vscode.ThemeIcon('info');
      return [empty];
    }

    return files.map((file) => {
      const label = labelFromFile(file, this.getRelativeDir());
      const description = extractDescription(file);
      return new AmsTreeItem(label, description, file, this.getIconId());
    });
  }
}

/**
 * Convert a file path to a human-readable label.
 */
function labelFromFile(filePath: string, _relDir: string): string {
  const base = path.basename(filePath);
  const parent = path.basename(path.dirname(filePath));

  // Charter pattern: .../<agent>/charter.md → use parent dir name
  if (base === 'charter.md') {
    return parent;
  }
  // Skill folder pattern: .../<skill-name>/SKILL.md → use parent dir name
  if (base === 'SKILL.md') {
    return parent;
  }
  // Prompt pattern: <Name>.prompt.md → strip suffix
  if (base.endsWith('.prompt.md')) {
    return base.replace(/\.prompt\.md$/, '');
  }
  // Chatmode pattern: <Name>.chatmode.md → strip suffix
  if (base.endsWith('.chatmode.md')) {
    return base.replace(/\.chatmode\.md$/, '');
  }
  // Default: strip .md
  return base.replace(/\.md$/, '');
}
