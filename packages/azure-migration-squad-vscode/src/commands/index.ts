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

    vscode.commands.registerCommand('azureMigrationSquad.registerAgents', () =>
      cmdRegisterAgentsWithSquadCli()
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

  // Help the user register the freshly-installed AMS agents with the Squad CLI
  // so they appear in Copilot Chat's @-agent dropdown. This is a no-op for
  // users who just want the slash-command UX (e.g. /assess-any-application
  // runs through the Migration-Orchestrator chatmode, which doesn't need
  // Squad CLI registration).
  await offerSquadCliRegistration(ws.root);

  // Chatmodes from .github/chatmodes/ register on workspace load. If we just
  // dropped them into a workspace that was already open, the user has to
  // reload the window for VS Code to pick them up.
  await offerReloadWindow();
}

async function offerSquadCliRegistration(workspaceRoot: string): Promise<void> {
  const cfg = vscode.workspace.getConfiguration('azureMigrationSquad');
  const shouldPrompt = cfg.get<boolean>('promptSquadInit', true);
  if (!shouldPrompt) {
    // User opted out — Command Palette → "Register agents with Squad CLI" still works.
    return;
  }

  const detection = detectSquadState(workspaceRoot);

  if (detection.hasGlobalSquadCli) {
    const choice = await vscode.window.showInformationMessage(
      'Register the AMS agents (Architect, Coder, Tester, etc.) with Squad CLI ' +
        "so they appear in Copilot Chat's @ dropdown? Opens a terminal with `squad init`.",
      'Run squad init',
      'Skip for now',
      "Don't ask again"
    );
    if (choice === 'Run squad init') {
      openSquadInitTerminal(workspaceRoot);
    } else if (choice === "Don't ask again") {
      await cfg.update('promptSquadInit', false, vscode.ConfigurationTarget.Global);
    }
    return;
  }

  // Squad CLI not on PATH — offer the optional install path.
  const choice = await vscode.window.showInformationMessage(
    "AMS works through slash commands like /assess-any-application without Squad CLI. " +
      "For native @-agent dispatch in Copilot Chat (e.g. @architect), install " +
      '@bradygaster/squad-cli globally and run squad init.',
    'Install Squad CLI',
    'Skip for now',
    'Learn more'
  );
  if (choice === 'Install Squad CLI') {
    openSquadInstallAndInitTerminal();
  } else if (choice === 'Learn more') {
    await vscode.env.openExternal(
      vscode.Uri.parse('https://github.com/bradygaster/squad')
    );
  }
}

async function offerReloadWindow(): Promise<void> {
  const choice = await vscode.window.showInformationMessage(
    'Reload the VS Code window now so the new chatmodes register with Copilot Chat?',
    'Reload',
    'Later'
  );
  if (choice === 'Reload') {
    await vscode.commands.executeCommand('workbench.action.reloadWindow');
  }
}

/**
 * Opens a VS Code terminal with `squad init` pre-typed (NOT executed).
 * Squad init can be interactive (preset picker, etc.) so we let the user
 * review and run it themselves. Once Squad CLI completes, the user reloads
 * the window and the AMS agents appear in Copilot Chat's @ dropdown.
 */
function openSquadInitTerminal(cwd: string): void {
  const terminal = vscode.window.createTerminal({
    name: 'Squad init',
    cwd,
  });
  terminal.show();
  terminal.sendText('squad init', false);
  vscode.window.showInformationMessage(
    'Terminal opened with `squad init` ready to run. Press Enter to start it. ' +
      'After it completes, reload the VS Code window so the new agents register.'
  );
}

/**
 * Opens a terminal that installs Squad CLI globally AND runs squad init.
 * The user reviews and presses Enter to execute.
 */
function openSquadInstallAndInitTerminal(): void {
  const cwd = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  const terminal = vscode.window.createTerminal({
    name: 'Install Squad CLI',
    cwd,
  });
  terminal.show();
  // npm install on its own line so users can see what they're agreeing to.
  // Then chained squad init on a second line — only runs if install succeeds.
  terminal.sendText('npm install -g @bradygaster/squad-cli', false);
  vscode.window.showInformationMessage(
    'Terminal opened with the install command ready. Press Enter to install. ' +
      'On macOS/Linux you may need to prefix with sudo. After install completes, ' +
      'run `squad init` in the same terminal to register the AMS agents.'
  );
}

async function cmdInstallSquadCli(): Promise<void> {
  // Squad CLI is OPTIONAL for AMS users. This command exists for power users
  // who want it. We open a VS Code terminal with the install command pre-typed
  // because `npm install -g` may require elevated permissions on some systems
  // and we want the user to review what's about to run.
  openSquadInstallAndInitTerminal();
}

async function cmdRegisterAgentsWithSquadCli(): Promise<void> {
  const ws = findAmsWorkspace();
  if (!ws) {
    vscode.window.showErrorMessage('Open a folder first.');
    return;
  }
  await offerSquadCliRegistration(ws.root);
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

