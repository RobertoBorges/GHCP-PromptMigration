/**
 * Base class for the AMA tree providers (Agents, Prompts, Add-ons).
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
      'Click to install the Azure Migration Agent here',
      vscode.TreeItemCollapsibleState.None
    );
    this.iconPath = new vscode.ThemeIcon('rocket');
    this.tooltip =
      'Run "Azure Migration: Initialize" to scaffold the agent definition, ' +
      'prompts, skills, chatmodes, and hooks into this workspace.';
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
  /** Optional file suffix filter (e.g., '.agent.md'). Default: any .md file. */
  getFileSuffix(): string {
    return '.md';
  }
  /** Subclasses can filter files further (e.g., only main-path phases). Default: include all. */
  filterFile(_absolutePath: string): boolean {
    return true;
  }

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  async getChildren(element?: vscode.TreeItem): Promise<vscode.TreeItem[]> {
    // Flat providers ignore `element` — parent items only exist in grouped providers
    // (like AddonsProvider) which override this method.
    if (element) {
      return [];
    }
    const ws = findAmsWorkspace();
    if (!ws || !ws.isInstalled) {
      return [new NotInstalledItem()];
    }

    const dir = path.join(ws.root, this.getRelativeDir());
    const files = listMarkdownFiles(dir, this.isRecursive())
      .filter((f) => f.endsWith(this.getFileSuffix()))
      .filter((f) => this.filterFile(f));
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

  // Agent pattern: <Name>.agent.md → strip suffix
  if (base.endsWith('.agent.md')) {
    return base.replace(/\.agent\.md$/, '');
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
