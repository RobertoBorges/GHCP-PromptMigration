/**
 * Commands exposed via the Command Palette.
 *
 * The extension is a SELF-CONTAINED distribution: it bundles all the
 * migration content under `templates/` and copies it into the user's
 * workspace on Initialize. No npm CLI dependency.
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { findAmsWorkspace } from '../util/workspace';
import { copyTemplatesToWorkspace } from '../util/templatesCopier';

let outputChannel: vscode.OutputChannel | undefined;

function getOutputChannel(): vscode.OutputChannel {
  if (!outputChannel) {
    outputChannel = vscode.window.createOutputChannel('Azure Migration Agent');
  }
  return outputChannel;
}

export function registerCommands(
  context: vscode.ExtensionContext,
  onRefresh: () => void
): void {
  context.subscriptions.push(
    vscode.commands.registerCommand('azureMigrationSquad.openFile', (uri: vscode.Uri) =>
      vscode.commands.executeCommand('vscode.open', uri)
    ),

    vscode.commands.registerCommand('azureMigrationSquad.initialize', () =>
      cmdInitialize(context, onRefresh, /* overwrite */ false)
    ),

    vscode.commands.registerCommand('azureMigrationSquad.upgrade', () =>
      cmdInitialize(context, onRefresh, /* overwrite */ true)
    ),

    vscode.commands.registerCommand('azureMigrationSquad.doctor', () =>
      cmdDoctor(context)
    ),

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

    vscode.commands.registerCommand('azureMigrationSquad.refreshTree', () => onRefresh())
  );
}

async function cmdInitialize(
  context: vscode.ExtensionContext,
  onRefresh: () => void,
  overwrite: boolean
): Promise<void> {
  const ws = findAmsWorkspace();
  if (!ws) {
    vscode.window.showErrorMessage(
      'Open a folder before initializing the Azure Migration Agent.'
    );
    return;
  }

  if (ws.isInstalled && !overwrite) {
    const choice = await vscode.window.showWarningMessage(
      'The Azure Migration Agent is already installed in this workspace. Overwrite with the latest extension contents?',
      'Overwrite',
      'Cancel'
    );
    if (choice !== 'Overwrite') return;
    overwrite = true;
  }

  const out = getOutputChannel();
  out.show(true);
  out.appendLine('');
  out.appendLine('─'.repeat(78));
  out.appendLine(`▶ ${overwrite ? 'Upgrading' : 'Initializing'} Azure Migration Agent`);
  out.appendLine(`  Workspace: ${ws.root}`);
  out.appendLine('─'.repeat(78));

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: overwrite
        ? 'Upgrading Azure Migration Agent…'
        : 'Initializing Azure Migration Agent…',
      cancellable: false,
    },
    async () => {
      try {
        const result = await copyTemplatesToWorkspace(context.extensionUri, ws.root, {
          overwrite,
        });
        out.appendLine(`  Copied: ${result.copied} file(s)`);
        out.appendLine(`  Skipped (already present): ${result.skipped} file(s)`);
        out.appendLine('◀ done');
        vscode.window.showInformationMessage(
          `Azure Migration Agent: ${result.copied} file(s) installed${
            result.skipped > 0 ? `, ${result.skipped} skipped` : ''
          }.`
        );
      } catch (err) {
        out.appendLine(`✗ ERROR: ${err}`);
        vscode.window.showErrorMessage(
          `Azure Migration Agent: install failed — ${err}`
        );
        return;
      }
    }
  );

  onRefresh();

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

  // Offer to reload the window so Copilot Chat picks up the new chatmodes
  // (VS Code only registers .github/chatmodes/* on workspace load).
  const reload = await vscode.window.showInformationMessage(
    'Reload the VS Code window now so Copilot Chat picks up the new prompts and chatmodes?',
    'Reload',
    'Later'
  );
  if (reload === 'Reload') {
    await vscode.commands.executeCommand('workbench.action.reloadWindow');
  }
}

async function cmdDoctor(context: vscode.ExtensionContext): Promise<void> {
  const ws = findAmsWorkspace();
  if (!ws) {
    vscode.window.showErrorMessage('Open a folder first.');
    return;
  }
  const out = getOutputChannel();
  out.show(true);
  out.appendLine('');
  out.appendLine('─'.repeat(78));
  out.appendLine(`▶ Azure Migration Agent: doctor`);
  out.appendLine('─'.repeat(78));
  out.appendLine(`  Workspace root:           ${ws.root}`);
  out.appendLine(`  .github/agents/...:        ${ws.hasAgent ? '✓' : '✗ missing'}`);
  out.appendLine(`  .github/prompts/:          ${ws.hasPrompts ? '✓' : '✗ missing'}`);
  out.appendLine(`  .github/skills/:           ${ws.hasSkills ? '✓' : '✗ missing'}`);
  out.appendLine(`  .github/copilot-instr...:  ${ws.hasCopilotInstructions ? '✓' : '✗ missing'}`);

  const copilotChat = vscode.extensions.getExtension('GitHub.copilot-chat');
  out.appendLine(`  GitHub Copilot Chat ext:   ${copilotChat ? '✓ installed' : '✗ NOT installed'}`);

  const decisionsExists = fs.existsSync(path.join(ws.root, 'reports', 'Decisions-Required.md'));
  out.appendLine(`  reports/Decisions-Req...:  ${decisionsExists ? '✓ generated' : '⏸ not yet (run /Phase1-PlanAndAssess)'}`);

  const extensionVersion = (() => {
    try {
      const pkg = JSON.parse(
        fs.readFileSync(path.join(context.extensionUri.fsPath, 'package.json'), 'utf-8')
      );
      return pkg.version;
    } catch {
      return 'unknown';
    }
  })();
  out.appendLine(`  Extension version:         ${extensionVersion}`);

  const ok = ws.isInstalled;
  out.appendLine(`◀ ${ok ? 'OK' : 'Needs attention — run Initialize'}`);
  vscode.window.showInformationMessage(
    ok
      ? 'Doctor: install looks good. See output for details.'
      : 'Doctor: workspace needs Initialize. See output for details.'
  );
}

async function cmdOpenDiscovery(): Promise<void> {
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
      'MIGRATION-START-HERE.md is missing. Initialize first?',
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
