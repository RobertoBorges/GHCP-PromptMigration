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

  // Refresh all trees when the workspace's AMS state may have changed.
  const refreshAll = () => {
    agentsProvider.refresh();
    promptsProvider.refresh();
    skillsProvider.refresh();
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

  // Smoke test command kept from Phase 2 for backward compat / debugging.
  context.subscriptions.push(
    vscode.commands.registerCommand('azureMigrationSquad.hello', () => {
      vscode.window.showInformationMessage(
        'Azure Migration Squad extension is active — open the sidebar to browse agents, prompts, and skills.'
      );
    })
  );
}

export function deactivate(): void {
  // Subscriptions handle their own disposal.
}

