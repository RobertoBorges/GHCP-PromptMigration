/**
 * Status bar widget showing the current migration phase.
 *
 * Reads `.azure-migration-squad/manifest.json` from the workspace; falls back
 * to "Not installed" if AMS hasn't been initialized.
 *
 * The phase is inferred from manifest.lastPhase if present (set by future
 * CLI hooks), or from the presence of certain reports/ files.
 */

import * as path from 'path';
import * as fs from 'fs';
import * as vscode from 'vscode';
import { findAmsWorkspace } from './util/workspace';

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
    this.item.name = 'Azure Migration Squad';
    context.subscriptions.push(this.item);
  }

  start(): void {
    this.refresh();
    this.setupWatchers();

    // Refresh when workspace folders change (multi-root or open/close).
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

    // Watch manifest.json for version changes.
    this.watcher = vscode.workspace.createFileSystemWatcher(
      '**/.azure-migration-squad/manifest.json'
    );
    this.watcher.onDidCreate(() => this.refresh());
    this.watcher.onDidChange(() => this.refresh());
    this.watcher.onDidDelete(() => this.refresh());

    // Watch reports/ for phase inference signals.
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

    const phase = inferPhase(ws.root, !!ws.hasManifest);
    const icon = PHASE_ICON[phase] || PHASE_ICON.unknown;
    const label = PHASE_LABEL[phase] || PHASE_LABEL.unknown;
    const cmd = PHASE_PROMPT[phase] || PHASE_PROMPT.unknown;

    this.item.text = `${icon} ${label}`;
    this.item.tooltip = buildTooltip(ws.root, phase, ws.manifest?.version);
    this.item.command = cmd;
    this.item.show();
  }

  dispose(): void {
    this.watcher?.dispose();
    this.reportsWatcher?.dispose();
    this.item.dispose();
  }
}

/**
 * Heuristic: infer the current migration phase from filesystem state.
 *
 * Order matters — most-advanced phase wins.
 */
function inferPhase(root: string, hasManifest: boolean): string {
  if (!hasManifest) {
    return 'not-installed';
  }
  const reports = path.join(root, 'reports');
  const exists = (rel: string) => fs.existsSync(path.join(reports, rel));

  if (exists('Phase-6-PostMigrationOps.md') || exists('Cutover-Complete.md')) {
    return 'complete';
  }
  if (exists('Phase-6-PostMigrationOps-Plan.md') || exists('Operations-Runbook.md')) {
    return 'phase-6';
  }
  if (exists('Phase-5-CICD.md') || exists('CICD-Setup.md')) {
    return 'phase-5';
  }
  if (exists('Phase-4-Deployment.md') || exists('Deployment-Report.md')) {
    return 'phase-4';
  }
  if (exists('Phase-3-Infrastructure.md') || exists('Infrastructure-Plan.md')) {
    return 'phase-3';
  }
  if (exists('Phase-2-CodeMigration.md') || exists('Code-Migration-Plan.md')) {
    return 'phase-2';
  }
  if (exists('Migration-Plan.md')) {
    return 'phase-1';
  }
  if (exists('Capability-Matrix.yaml') || exists('Discovery-Dossier.md')) {
    return 'discovery';
  }
  return 'unknown';
}

function buildTooltip(root: string, phase: string, version?: string): string {
  const lines = [
    `Azure Migration Squad`,
    ``,
    `Phase: ${PHASE_LABEL[phase] || phase}`,
  ];
  if (version) lines.push(`Version: ${version}`);
  lines.push(`Workspace: ${root}`);
  lines.push(``);
  lines.push(`Click to open the next recommended action.`);
  return lines.join('\n');
}
