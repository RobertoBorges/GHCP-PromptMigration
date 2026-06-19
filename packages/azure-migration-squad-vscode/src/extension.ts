/**
 * Azure Migration Squad — VS Code extension.
 *
 * This extension turns any VS Code workspace into a launchpad for migrating
 * applications to Azure using the @robertoborges/azure-migration-squad npm
 * package as the source of truth for prompts, skills, and agents.
 *
 * Phase 2: bootstrap activate/deactivate + smoke test command
 * Phase 3 (this file): tree view + commands + first useful UX
 */

import * as vscode from 'vscode';
import { AgentsProvider } from './treeProviders/agentsProvider';
import { PromptsProvider } from './treeProviders/promptsProvider';
import { SkillsProvider } from './treeProviders/skillsProvider';
import { registerCommands } from './commands';
import { AmsStatusBar } from './statusBar';
import { maybeShowWelcome, showWelcomePanel, ensureCopilotChat } from './welcome';

export function activate(context: vscode.ExtensionContext): void {
  console.log('[azure-migration-squad] extension activated');

  // Tree views — one per content type (agents / prompts / skills)
  const agentsProvider = new AgentsProvider();
  const promptsProvider = new PromptsProvider();
  const skillsProvider = new SkillsProvider();

  context.subscriptions.push(
    vscode.window.createTreeView('azureMigrationSquadAgents', {
      treeDataProvider: agentsProvider,
      showCollapseAll: true,
    }),
    vscode.window.createTreeView('azureMigrationSquadPrompts', {
      treeDataProvider: promptsProvider,
      showCollapseAll: true,
    }),
    vscode.window.createTreeView('azureMigrationSquadSkills', {
      treeDataProvider: skillsProvider,
      showCollapseAll: true,
    })
  );

  // Status bar widget showing current migration phase. Honors the
  // azureMigrationSquad.statusBar.enabled setting.
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

  // Refresh all trees when the workspace's AMS state may have changed.
  const refreshAll = () => {
    agentsProvider.refresh();
    promptsProvider.refresh();
    skillsProvider.refresh();
    statusBar.refresh();
  };

  // Auto-refresh when files in .squad/ or .github/ change.
  const watcher = vscode.workspace.createFileSystemWatcher(
    '**/{.squad,.github}/**/*.md'
  );
  context.subscriptions.push(
    watcher,
    watcher.onDidCreate(refreshAll),
    watcher.onDidDelete(refreshAll),
    watcher.onDidChange(refreshAll)
  );

  // Also refresh on workspace folder change (multi-root projects).
  context.subscriptions.push(
    vscode.workspace.onDidChangeWorkspaceFolders(refreshAll)
  );

  // Register all commands (Initialize, Upgrade, Doctor, Open Discovery, etc.)
  registerCommands(context, refreshAll);

  // Phase 5 commands: welcome page + Copilot install
  context.subscriptions.push(
    vscode.commands.registerCommand('azureMigrationSquad.showWelcome', () =>
      showWelcomePanel(context)
    ),
    vscode.commands.registerCommand('azureMigrationSquad.installCopilotChat', () =>
      ensureCopilotChat(context, /* userInitiated */ true)
    )
  );

  // Smoke test command kept from Phase 2 for backward compat / debugging.
  context.subscriptions.push(
    vscode.commands.registerCommand('azureMigrationSquad.hello', () => {
      vscode.window.showInformationMessage(
        'Azure Migration Squad extension is active — open the sidebar to browse agents, prompts, and skills.'
      );
    })
  );

  // First-run welcome: shown only if AMS isn't installed and user hasn't
  // already dismissed it for this workspace. Runs after activation completes
  // (don't block the activation path).
  setTimeout(() => maybeShowWelcome(context).catch(() => undefined), 1500);
}

export function deactivate(): void {
  // Subscriptions handle their own disposal.
}

