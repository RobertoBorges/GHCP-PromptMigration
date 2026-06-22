/**
 * Commands exposed via the Command Palette.
 *
 * All AMS-modifying commands shell out to the npm package via npx so the
 * extension and the CLI share a single source of truth.
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { findAmsWorkspace } from '../util/workspace';
import { runAmsCli, getOutputChannel } from '../util/runNpx';
import { detectSquadState, argsForAmsInit } from '../util/squadDetection';

export function registerCommands(
  context: vscode.ExtensionContext,
  onRefresh: () => void
): void {
  context.subscriptions.push(
    vscode.commands.registerCommand('azureMigrationSquad.openFile', (uri: vscode.Uri) =>
      vscode.commands.executeCommand('vscode.open', uri)
    ),

    vscode.commands.registerCommand('azureMigrationSquad.initialize', () =>
      cmdInitialize(onRefresh)
    ),

    vscode.commands.registerCommand('azureMigrationSquad.upgrade', () =>
      cmdUpgrade(onRefresh)
    ),

    vscode.commands.registerCommand('azureMigrationSquad.doctor', () => cmdDoctor()),

    vscode.commands.registerCommand('azureMigrationSquad.openDiscovery', () =>
      cmdOpenDiscovery()
    ),

    vscode.commands.registerCommand('azureMigrationSquad.showCatalog', () => cmdShowCatalog()),

    vscode.commands.registerCommand('azureMigrationSquad.openSettings', () =>
      vscode.commands.executeCommand(
        'workbench.action.openSettings',
        '@ext:robertoborges.azure-migration-squad-vscode'
      )
    ),

    vscode.commands.registerCommand('azureMigrationSquad.refreshTree', () => onRefresh()),

    vscode.commands.registerCommand('azureMigrationSquad.installSquadCli', () =>
      cmdInstallSquadCli()
    ),
  );
}

async function cmdInitialize(onRefresh: () => void): Promise<void> {
  const ws = findAmsWorkspace();
  if (!ws) {
    vscode.window.showErrorMessage(
      'Open a folder before initializing the Azure Migration Squad.'
    );
    return;
  }

  if (ws.hasManifest) {
    const choice = await vscode.window.showWarningMessage(
      'Azure Migration Squad is already installed. Run upgrade instead?',
      'Upgrade',
      'Re-init anyway',
      'Cancel'
    );
    if (choice === 'Cancel' || !choice) return;
    if (choice === 'Upgrade') {
      await cmdUpgrade(onRefresh);
      return;
    }
  }

  // Detect Squad state and pick the right ams init flags. The extension does
  // NOT require the user to install Squad CLI separately — AMS bundles all
  // the .squad/agents/ content it needs. When .squad/ is missing we pass
  // --force so ams init skips its "Squad runtime not detected" guard.
  const detection = detectSquadState(ws.root);
  const initArgs = argsForAmsInit(detection.state);

  const out = getOutputChannel();
  if (detection.state === 'no-squad') {
    out.appendLine('');
    out.appendLine('ℹ Squad CLI not detected on PATH — that\'s OK!');
    out.appendLine('  Azure Migration Squad ships all the .squad/ content it needs.');
    out.appendLine('  Running ams init with --force to skip the Squad runtime check.');
    out.appendLine('  (If you want the squad CLI for advanced commands, run:');
    out.appendLine('     npm install -g @bradygaster/squad-cli');
    out.appendLine('   — but it is optional for Copilot Chat usage.)');
  } else if (detection.state === 'cli-available') {
    out.appendLine('');
    out.appendLine('ℹ Squad CLI is installed globally, but .squad/ is not in this workspace.');
    out.appendLine('  Installing AMS content directly (it includes the .squad/ scaffolding).');
    out.appendLine('  After init, you can also run `squad init` for richer Squad metadata.');
  }

  const exitCode = await runAmsCli({
    subcommand: 'init',
    args: initArgs,
    cwd: ws.root,
    progressTitle: 'Initializing Azure Migration Squad...',
  });
  onRefresh();

  if (exitCode !== 0) {
    // Error already shown by runAmsCli; nothing more to do.
    return;
  }

  // Offer to open the welcome doc if it was just created.
  const welcomePath = path.join(ws.root, 'MIGRATION-START-HERE.md');
  if (fs.existsSync(welcomePath)) {
    const open = await vscode.window.showInformationMessage(
      'Open MIGRATION-START-HERE.md for your 60-second quickstart?',
      'Open',
      'Not now'
    );
    if (open === 'Open') {
      const doc = await vscode.workspace.openTextDocument(welcomePath);
      await vscode.window.showTextDocument(doc, { preview: false });
      await vscode.commands.executeCommand('markdown.showPreview', vscode.Uri.file(welcomePath));
    }
  }
}

async function cmdInstallSquadCli(): Promise<void> {
  // Squad CLI is OPTIONAL for AMS users. This command exists for power users
  // who want it. We open a VS Code terminal with the install command pre-typed
  // because `npm install -g` may require elevated permissions on some systems
  // and we want the user to review what's about to run.
  const terminal = vscode.window.createTerminal({
    name: 'Install Squad CLI',
    cwd: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath,
  });
  terminal.show();
  terminal.sendText('npm install -g @bradygaster/squad-cli');
  vscode.window.showInformationMessage(
    'A terminal opened with the install command. Press Enter to run it. ' +
      'On macOS/Linux you may need to prefix with sudo.'
  );
}

async function cmdUpgrade(onRefresh: () => void): Promise<void> {
  const ws = findAmsWorkspace();
  if (!ws) {
    vscode.window.showErrorMessage('Open a folder first.');
    return;
  }
  if (!ws.hasManifest) {
    vscode.window.showWarningMessage(
      'Azure Migration Squad is not installed in this workspace. Run Initialize first.'
    );
    return;
  }
  await runAmsCli({
    subcommand: 'upgrade',
    cwd: ws.root,
    progressTitle: 'Upgrading Azure Migration Squad...',
  });
  onRefresh();
}

async function cmdDoctor(): Promise<void> {
  const ws = findAmsWorkspace();
  if (!ws) {
    vscode.window.showErrorMessage('Open a folder first.');
    return;
  }
  await runAmsCli({
    subcommand: 'doctor',
    cwd: ws.root,
    progressTitle: 'Running ams doctor...',
  });
}

async function cmdOpenDiscovery(): Promise<void> {
  // Try the chat APIs that VS Code Copilot Chat exposes.
  // Different VS Code/Copilot Chat versions expose different command IDs;
  // we try a sequence and fall back to a clipboard + open-chat approach.
  const query = '/assess-any-application';
  const attempts: Array<() => Thenable<unknown>> = [
    () => vscode.commands.executeCommand('workbench.action.chat.open', { query }),
    () => vscode.commands.executeCommand('workbench.action.chat.openInSidebar', { query }),
    () => vscode.commands.executeCommand('github.copilot.openChat'),
  ];

  for (const attempt of attempts) {
    try {
      await attempt();
      vscode.window.showInformationMessage(
        `Opened Copilot Chat. Type "${query}" if it wasn't pre-filled.`
      );
      return;
    } catch {
      // Try next.
    }
  }

  // Fallback: copy to clipboard and tell the user.
  await vscode.env.clipboard.writeText(query);
  vscode.window.showInformationMessage(
    `Couldn't auto-open Copilot Chat. The discovery command "${query}" is on your clipboard — paste it into the chat.`
  );
}

async function cmdShowCatalog(): Promise<void> {
  const ws = findAmsWorkspace();
  if (!ws) {
    vscode.window.showErrorMessage('Open a folder first.');
    return;
  }
  const welcomePath = path.join(ws.root, 'MIGRATION-START-HERE.md');
  if (!fs.existsSync(welcomePath)) {
    const init = await vscode.window.showWarningMessage(
      'MIGRATION-START-HERE.md is missing. Initialize the migration squad first?',
      'Initialize',
      'Cancel'
    );
    if (init === 'Initialize') {
      await vscode.commands.executeCommand('azureMigrationSquad.initialize');
    }
    return;
  }
  await vscode.commands.executeCommand(
    'markdown.showPreview',
    vscode.Uri.file(welcomePath)
  );
}

// Export for tests
export { getOutputChannel };

