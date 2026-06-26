/**
 * Status bar widget — shows pending decisions OR current migration phase.
 *
 * Priority order:
 *   1. If reports/Decisions-Required.md has PENDING items → "⏸ AMS: N/M decisions pending"
 *   2. If reports/ has phase artifacts → infer phase from filesystem
 *   3. If workspace not initialized → "AMS: not installed"
 *
 * Click → opens the most relevant next action.
 */

import * as path from 'path';
import * as fs from 'fs';
import * as vscode from 'vscode';
import { findAmsWorkspace } from './util/workspace';
import { parseDecisionsFile } from './util/decisionsParser';

const PHASE_ICON: Record<string, string> = {
  'not-installed': '$(warning)',
  discovery: '$(search)',
  'phase-1': '$(list-tree)',
  'phase-2': '$(code)',
  'phase-3': '$(server)',
  'phase-4': '$(rocket)',
  'phase-5': '$(github-action)',
  'phase-6': '$(pulse)',
  complete: '$(check)',
  unknown: '$(squirrel)',
};

const PHASE_LABEL: Record<string, string> = {
  'not-installed': 'AMS: not installed',
  discovery: 'AMS: Discovery',
  'phase-1': 'AMS: Phase 1 — Plan',
  'phase-2': 'AMS: Phase 2 — Migrate',
  'phase-3': 'AMS: Phase 3 — Infra',
  'phase-4': 'AMS: Phase 4 — Deploy',
  'phase-5': 'AMS: Phase 5 — CI/CD',
  'phase-6': 'AMS: Phase 6 — Ops',
  complete: 'AMS: Complete',
  unknown: 'AMS: Ready',
};

const PHASE_PROMPT: Record<string, string> = {
  'not-installed': 'azureMigrationSquad.initialize',
  discovery: 'azureMigrationSquad.openDiscovery',
  'phase-1': 'azureMigrationSquad.openDiscovery',
  'phase-2': 'azureMigrationSquad.openDiscovery',
  'phase-3': 'azureMigrationSquad.openDiscovery',
  'phase-4': 'azureMigrationSquad.openDiscovery',
  'phase-5': 'azureMigrationSquad.openDiscovery',
  'phase-6': 'azureMigrationSquad.openDiscovery',
  complete: 'azureMigrationSquad.showCatalog',
  unknown: 'azureMigrationSquad.showCatalog',
};

export class AmsStatusBar {
  private item: vscode.StatusBarItem;
  private watcher?: vscode.FileSystemWatcher;
  private reportsWatcher?: vscode.FileSystemWatcher;

  constructor(private context: vscode.ExtensionContext) {
    this.item = vscode.window.createStatusBarItem(
      vscode.StatusBarAlignment.Left,
      100
    );
    this.item.name = 'Azure Migration Agent';
    context.subscriptions.push(this.item);
  }

  start(): void {
    this.refresh();
    this.setupWatchers();

    this.context.subscriptions.push(
      vscode.workspace.onDidChangeWorkspaceFolders(() => {
        this.setupWatchers();
        this.refresh();
      })
    );
  }

  private setupWatchers(): void {
    this.watcher?.dispose();
    this.reportsWatcher?.dispose();

    // Watch the marker file for install state.
    this.watcher = vscode.workspace.createFileSystemWatcher(
      '**/.github/agents/Code-Migration-Modernization.agent.md'
    );
    this.watcher.onDidCreate(() => this.refresh());
    this.watcher.onDidDelete(() => this.refresh());

    // Watch reports/ for phase + decision signals.
    this.reportsWatcher = vscode.workspace.createFileSystemWatcher(
      '**/reports/*.md'
    );
    this.reportsWatcher.onDidCreate(() => this.refresh());
    this.reportsWatcher.onDidChange(() => this.refresh());
    this.reportsWatcher.onDidDelete(() => this.refresh());

    this.context.subscriptions.push(this.watcher, this.reportsWatcher);
  }

  refresh(): void {
    const ws = findAmsWorkspace();
    if (!ws) {
      this.item.hide();
      return;
    }

    // Pending decisions take priority — block work indicator.
    const decisions = parseDecisionsFile(ws.root);
    if (decisions.exists && decisions.pending > 0) {
      const total = decisions.decisions.length;
      this.item.text = `$(circle-large-outline) AMS: ${decisions.pending}/${total} decisions pending`;
      this.item.tooltip = buildDecisionsTooltip(decisions);
      this.item.command = 'azureMigrationSquad.showDecisions';
      this.item.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
      this.item.show();
      return;
    }

    const phase = inferPhase(ws.root, ws.isInstalled);
    const icon = PHASE_ICON[phase] || PHASE_ICON.unknown;
    const label = PHASE_LABEL[phase] || PHASE_LABEL.unknown;
    const cmd = PHASE_PROMPT[phase] || PHASE_PROMPT.unknown;

    this.item.text = `${icon} ${label}`;
    this.item.tooltip = buildTooltip(ws.root, phase);
    this.item.command = cmd;
    this.item.backgroundColor = undefined;
    this.item.show();
  }

  dispose(): void {
    this.watcher?.dispose();
    this.reportsWatcher?.dispose();
    this.item.dispose();
  }
}

function buildDecisionsTooltip(summary: ReturnType<typeof parseDecisionsFile>): string {
  const lines = ['Azure Migration Agent — Decisions Required', ''];
  lines.push(`⏸ PENDING:  ${summary.pending}`);
  lines.push(`✅ DECIDED:  ${summary.decided}`);
  if (summary.locked > 0) lines.push(`🔒 LOCKED:   ${summary.locked}`);
  if (summary.na > 0) lines.push(`🚫 N/A:      ${summary.na}`);
  lines.push('');
  lines.push('Click to open reports/Decisions-Required.md.');
  lines.push('Phases 2-4 + DatabaseMigration will not run until all required decisions are made.');
  return lines.join('\n');
}

function inferPhase(root: string, isInstalled: boolean): string {
  if (!isInstalled) return 'not-installed';
  const reports = path.join(root, 'reports');
  const exists = (rel: string) => fs.existsSync(path.join(reports, rel));

  if (exists('Phase-6-PostMigrationOps.md') || exists('Cutover-Complete.md')) return 'complete';
  if (exists('Phase-6-PostMigrationOps-Plan.md') || exists('Operations-Runbook.md')) return 'phase-6';
  if (exists('Phase-5-CICD.md') || exists('CICD-Setup.md')) return 'phase-5';
  if (exists('Phase-4-Deployment.md') || exists('Deployment-Report.md')) return 'phase-4';
  if (exists('Phase-3-Infrastructure.md') || exists('Infrastructure-Plan.md')) return 'phase-3';
  if (exists('Phase-2-CodeMigration.md') || exists('Code-Migration-Plan.md')) return 'phase-2';
  if (exists('Migration-Plan.md')) return 'phase-1';
  if (exists('Capability-Matrix.yaml') || exists('Discovery-Dossier.md')) return 'discovery';
  return 'unknown';
}

function buildTooltip(root: string, phase: string): string {
  return [
    `Azure Migration Agent`,
    ``,
    `Phase: ${PHASE_LABEL[phase] || phase}`,
    `Workspace: ${root}`,
    ``,
    `Click to open the next recommended action.`,
  ].join('\n');
}
