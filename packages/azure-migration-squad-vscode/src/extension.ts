/**
 * Azure Migration Agent — VS Code extension.
 *
 * Self-contained: bundles all migration content under `templates/` and
 * copies it into the user's workspace on Initialize.
 *
 * COMPATIBILITY: This extension is **VS Code only**. It intentionally
 * does not activate on VS Code forks (VSCodium, Cursor, Windsurf,
 * Positron, Eclipse Theia-based IDEs, etc.) because it depends on
 * VS Code-specific behavior around GitHub Copilot Chat slash-command
 * registration and the Copilot Chat sidebar contract, and we cannot
 * validate against every fork's runtime differences.
 */

import * as vscode from 'vscode';
import { AgentsProvider } from './treeProviders/agentsProvider';
import { PromptsProvider } from './treeProviders/promptsProvider';
import { AddonsProvider } from './treeProviders/addonsProvider';
import { DecisionsProvider } from './treeProviders/decisionsProvider';
import { registerCommands } from './commands';
import { AmsStatusBar } from './statusBar';
import { maybeShowWelcome, showWelcomePanel, ensureCopilotChat } from './welcome';

/**
 * Whitelist of `vscode.env.appName` values that count as "real VS Code".
 * These are Microsoft-signed/-branded builds. Forks like VSCodium, Cursor,
 * Windsurf, Positron, and Theia-based IDEs will report different values
 * and get the friendly "not supported" message below.
 */
const SUPPORTED_APP_NAMES = new Set<string>([
  'Visual Studio Code',
  'Visual Studio Code - Insiders',
  'Visual Studio Code - Exploration',
  // The Microsoft-signed open-source build that ships from the vscode repo.
  // Same source code + Marketplace as branded VS Code; commonly used in
  // corporate environments that repackage but keep the Microsoft signature.
  'Code - OSS',
]);

const MARKETPLACE_URL =
  'https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode';

export function activate(context: vscode.ExtensionContext): void {
  // ── Host compatibility check ─────────────────────────────────────────
  const appName = vscode.env.appName ?? '(unknown)';
  if (!SUPPORTED_APP_NAMES.has(appName)) {
    console.warn(
      `[azure-migration-agent] refusing to activate on non-VS Code host: "${appName}"`
    );
    void vscode.window
      .showErrorMessage(
        `Azure Migration Agent is only supported on Visual Studio Code. ` +
          `Detected host: "${appName}". The extension will not activate.`,
        'Open marketplace listing',
        'Dismiss'
      )
      .then((choice) => {
        if (choice === 'Open marketplace listing') {
          void vscode.env.openExternal(vscode.Uri.parse(MARKETPLACE_URL));
        }
      });
    return;
  }

  console.log(`[azure-migration-agent] extension activated (host: ${appName})`);

  const agentsProvider = new AgentsProvider();
  const promptsProvider = new PromptsProvider();
  const addonsProvider = new AddonsProvider();
  const decisionsProvider = new DecisionsProvider();

  context.subscriptions.push(
    vscode.window.createTreeView('azureMigrationSquadAgents', {
      treeDataProvider: agentsProvider,
      showCollapseAll: true,
    }),
    vscode.window.createTreeView('azureMigrationSquadPrompts', {
      treeDataProvider: promptsProvider,
      showCollapseAll: true,
    }),
    vscode.window.createTreeView('azureMigrationSquadAddons', {
      treeDataProvider: addonsProvider,
      showCollapseAll: true,
    }),
    vscode.window.createTreeView('azureMigrationSquadDecisions', {
      treeDataProvider: decisionsProvider,
      showCollapseAll: false,
    })
  );

  const statusBar = new AmsStatusBar(context);
  const updateStatusBarVisibility = () => {
    const enabled = vscode.workspace
      .getConfiguration('azureMigrationSquad')
      .get<boolean>('statusBar.enabled', true);
    if (enabled) {
      statusBar.start();
    } else {
      statusBar.dispose();
    }
  };
  updateStatusBarVisibility();

  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('azureMigrationSquad.statusBar.enabled')) {
        updateStatusBarVisibility();
      }
    })
  );

  const refreshAll = () => {
    agentsProvider.refresh();
    promptsProvider.refresh();
    addonsProvider.refresh();
    decisionsProvider.refresh();
    statusBar.refresh();
  };

  // Watch the workspace's .github/* for changes.
  const watcher = vscode.workspace.createFileSystemWatcher(
    '**/.github/**/*.md'
  );
  context.subscriptions.push(
    watcher,
    watcher.onDidCreate(refreshAll),
    watcher.onDidDelete(refreshAll),
    watcher.onDidChange(refreshAll)
  );

  // Watch reports/Decisions-Required.md for the Decisions tree + status bar.
  const decisionsWatcher = vscode.workspace.createFileSystemWatcher(
    '**/reports/Decisions-Required.md'
  );
  context.subscriptions.push(
    decisionsWatcher,
    decisionsWatcher.onDidCreate(refreshAll),
    decisionsWatcher.onDidDelete(refreshAll),
    decisionsWatcher.onDidChange(refreshAll)
  );

  context.subscriptions.push(
    vscode.workspace.onDidChangeWorkspaceFolders(refreshAll)
  );

  registerCommands(context, refreshAll);

  // Welcome + Copilot install commands
  context.subscriptions.push(
    vscode.commands.registerCommand('azureMigrationSquad.showWelcome', () =>
      showWelcomePanel(context)
    ),
    vscode.commands.registerCommand('azureMigrationSquad.installCopilotChat', () =>
      ensureCopilotChat(context, /* userInitiated */ true)
    )
  );

  // Wave I commands — Decisions Required.
  context.subscriptions.push(
    vscode.commands.registerCommand('azureMigrationSquad.showDecisions', async () => {
      const folders = vscode.workspace.workspaceFolders;
      if (!folders || folders.length === 0) {
        vscode.window.showErrorMessage('Open a folder first.');
        return;
      }
      const uri = vscode.Uri.joinPath(folders[0].uri, 'reports', 'Decisions-Required.md');
      try {
        const doc = await vscode.workspace.openTextDocument(uri);
        await vscode.window.showTextDocument(doc);
      } catch {
        const choice = await vscode.window.showWarningMessage(
          `reports/Decisions-Required.md doesn't exist yet. Phase 1 generates it.`,
          'Run Discovery',
          'Cancel'
        );
        if (choice === 'Run Discovery') {
          vscode.commands.executeCommand('azureMigrationSquad.openDiscovery');
        }
      }
    }),
    vscode.commands.registerCommand(
      'azureMigrationSquad.openDecisionAtLine',
      async (uri: vscode.Uri, line: number) => {
        try {
          const doc = await vscode.workspace.openTextDocument(uri);
          const editor = await vscode.window.showTextDocument(doc);
          const lineIdx = Math.max(0, (line ?? 1) - 1);
          const range = new vscode.Range(lineIdx, 0, lineIdx, 0);
          editor.selection = new vscode.Selection(range.start, range.start);
          editor.revealRange(range, vscode.TextEditorRevealType.AtTop);
        } catch (err) {
          vscode.window.showErrorMessage(`Could not open decision: ${err}`);
        }
      }
    )
  );

  // Smoke test command kept for backward compat / debugging.
  context.subscriptions.push(
    vscode.commands.registerCommand('azureMigrationSquad.hello', () => {
      vscode.window.showInformationMessage(
        'Azure Migration Agent extension is active — open the sidebar to browse the agent, prompts, skills, and decisions.'
      );
    })
  );

  // First-run welcome (non-blocking).
  setTimeout(() => maybeShowWelcome(context).catch(() => undefined), 1500);
}

export function deactivate(): void {
  // Subscriptions handle their own disposal.
}
