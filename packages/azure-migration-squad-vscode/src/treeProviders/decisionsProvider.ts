/**
 * Tree view for reports/Decisions-Required.md.
 *
 * Shows each major architecture decision with its current status. Click an
 * entry to open the file at that decision's section.
 *
 * Renders helpful placeholders when:
 *   - Workspace not initialized at all → "Initialize first"
 *   - Initialized but no decisions file yet → "Run Phase 1 to generate decisions"
 *   - File exists but empty → "No decisions found — re-run Phase 1?"
 */

import * as vscode from 'vscode';
import { findAmsWorkspace } from '../util/workspace';
import { parseDecisionsFile, type Decision, type DecisionStatus } from '../util/decisionsParser';

const STATUS_ICON: Record<DecisionStatus, string> = {
  pending: 'circle-large-outline',
  decided: 'check',
  locked: 'lock',
  na: 'circle-slash',
  unknown: 'question',
};

const STATUS_COLOR: Record<DecisionStatus, vscode.ThemeColor | undefined> = {
  pending: new vscode.ThemeColor('charts.red'),
  decided: new vscode.ThemeColor('charts.green'),
  locked: new vscode.ThemeColor('charts.blue'),
  na: new vscode.ThemeColor('disabledForeground'),
  unknown: new vscode.ThemeColor('charts.yellow'),
};

const STATUS_LABEL: Record<DecisionStatus, string> = {
  pending: 'PENDING',
  decided: 'DECIDED',
  locked: 'LOCKED',
  na: 'N/A',
  unknown: '?',
};

class DecisionItem extends vscode.TreeItem {
  constructor(decision: Decision, filePath: string) {
    super(`${decision.id}. ${decision.name}`, vscode.TreeItemCollapsibleState.None);
    this.description = STATUS_LABEL[decision.status];
    this.iconPath = new vscode.ThemeIcon(STATUS_ICON[decision.status], STATUS_COLOR[decision.status]);

    const tooltip = new vscode.MarkdownString();
    tooltip.appendMarkdown(`**${decision.name}**\n\n`);
    tooltip.appendMarkdown(`Status: \`${decision.statusText || STATUS_LABEL[decision.status]}\`\n\n`);
    if (decision.requiredFor) {
      tooltip.appendMarkdown(`Required for: ${decision.requiredFor}\n\n`);
    }
    tooltip.appendMarkdown(`_Click to open this section in reports/Decisions-Required.md_`);
    this.tooltip = tooltip;

    // Use the open-at-line command we register below so we can jump to the
    // exact section instead of always opening at line 1.
    this.command = {
      command: 'azureMigrationSquad.openDecisionAtLine',
      title: 'Open decision',
      arguments: [vscode.Uri.file(filePath), decision.line],
    };
    this.contextValue = `decision:${decision.status}`;
  }
}

class PlaceholderItem extends vscode.TreeItem {
  constructor(label: string, iconId: string, tooltip: string, commandId?: string) {
    super(label, vscode.TreeItemCollapsibleState.None);
    this.iconPath = new vscode.ThemeIcon(iconId);
    this.tooltip = tooltip;
    if (commandId) {
      this.command = { command: commandId, title: label };
    }
  }
}

export class DecisionsProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<vscode.TreeItem | undefined | void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(): vscode.TreeItem[] {
    const ws = findAmsWorkspace();
    if (!ws) {
      return [
        new PlaceholderItem(
          'Open a folder to see decisions',
          'folder-opened',
          'The decisions view reads reports/Decisions-Required.md from the workspace folder.'
        ),
      ];
    }

    if (!ws.hasManifest && !ws.hasSquad && !ws.hasPrompts) {
      return [
        new PlaceholderItem(
          'Click to install Azure Migration Squad here',
          'rocket',
          'Run "Azure Migration: Initialize" first. The decisions file is produced by Phase 1.',
          'azureMigrationSquad.initialize'
        ),
      ];
    }

    const summary = parseDecisionsFile(ws.root);
    if (!summary.exists) {
      return [
        new PlaceholderItem(
          'Run Phase 1 to generate decisions',
          'play',
          'reports/Decisions-Required.md does not exist yet. Phase 1 (Plan & Assess) generates it from the canonical decision catalog.',
          'azureMigrationSquad.openDiscovery'
        ),
      ];
    }

    if (summary.parseError) {
      return [
        new PlaceholderItem(
          `Parse error: ${summary.parseError}`,
          'error',
          'Could not read reports/Decisions-Required.md. Check the file is well-formed Markdown.'
        ),
      ];
    }

    if (summary.decisions.length === 0) {
      return [
        new PlaceholderItem(
          'No decisions found — re-run Phase 1?',
          'warning',
          'The file exists but no "## Decision N: ..." sections were found. Re-running Phase 1 will regenerate it from the catalog.',
          'azureMigrationSquad.openDiscovery'
        ),
      ];
    }

    return summary.decisions.map((d) => new DecisionItem(d, summary.filePath));
  }
}
