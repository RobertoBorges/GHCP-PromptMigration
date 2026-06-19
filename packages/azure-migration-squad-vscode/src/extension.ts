/**
 * Azure Migration Squad — VS Code extension.
 *
 * This extension turns any VS Code workspace into a launchpad for migrating
 * applications to Azure using the @robertoborges/azure-migration-squad npm
 * package as the source of truth for prompts, skills, and agents.
 *
 * Phase 2 (this file): bootstrap activate/deactivate + one hello command
 * so the rest of the package can be built and validated incrementally.
 *
 * Phases 3-5 add: tree view, status bar, settings, welcome WebView,
 * first-run detector, walkthrough, auto-prompt for Copilot Chat install.
 */

import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext): void {
  console.log('[azure-migration-squad] extension activated');

  // Smoke test command — proves the extension loads. Will be removed in Phase 3
  // once we have real commands (Initialize, Open Discovery, etc.).
  const helloCommand = vscode.commands.registerCommand(
    'azureMigrationSquad.hello',
    () => {
      vscode.window.showInformationMessage(
        'Azure Migration Squad is loaded! 🎉  Phase 3 commands coming soon.'
      );
    }
  );

  context.subscriptions.push(helloCommand);
}

export function deactivate(): void {
  // Nothing to clean up in Phase 2.
}
