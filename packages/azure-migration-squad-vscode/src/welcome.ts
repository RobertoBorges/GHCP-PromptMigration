/**
 * First-run welcome WebView panel.
 *
 * Shows the first time the extension activates in a workspace that doesn't
 * have the migration agent installed. Provides one-click Initialize +
 * "Install Copilot Chat" buttons.
 */

import * as vscode from 'vscode';
import { findAmsWorkspace } from './util/workspace';

const SHOWN_KEY_PREFIX = 'azureMigrationSquad.welcomeShown.';

export async function maybeShowWelcome(context: vscode.ExtensionContext): Promise<void> {
  const ws = findAmsWorkspace();
  if (!ws) return;
  if (ws.isInstalled) {
    return;
  }
  const key = SHOWN_KEY_PREFIX + ws.root;
  if (context.globalState.get<boolean>(key)) {
    return;
  }

  const choice = await vscode.window.showInformationMessage(
    '👋 Welcome to the Azure Migration Agent! Want to set up the migration workflow in this workspace?',
    'Get started',
    'Show welcome page',
    'Not now',
    "Don't show again"
  );

  if (choice === "Don't show again") {
    await context.globalState.update(key, true);
    return;
  }
  if (choice === 'Not now' || !choice) {
    return;
  }
  if (choice === 'Get started') {
    await vscode.commands.executeCommand('azureMigrationSquad.initialize');
    return;
  }
  if (choice === 'Show welcome page') {
    showWelcomePanel(context);
  }
}

export function showWelcomePanel(context: vscode.ExtensionContext): void {
  const panel = vscode.window.createWebviewPanel(
    'azureMigrationSquadWelcome',
    'Welcome — Azure Migration Agent',
    vscode.ViewColumn.Active,
    {
      enableScripts: true,
      retainContextWhenHidden: true,
    }
  );

  panel.webview.html = renderWelcomeHtml();

  panel.webview.onDidReceiveMessage(
    async (msg: { command: string }) => {
      switch (msg.command) {
        case 'initialize':
          await vscode.commands.executeCommand('azureMigrationSquad.initialize');
          break;
        case 'openDiscovery':
          await vscode.commands.executeCommand('azureMigrationSquad.openDiscovery');
          break;
        case 'showCatalog':
          await vscode.commands.executeCommand('azureMigrationSquad.showCatalog');
          break;
        case 'installCopilotChat':
          await ensureCopilotChat(context, /* userInitiated */ true);
          break;
        case 'openSettings':
          await vscode.commands.executeCommand('azureMigrationSquad.openSettings');
          break;
      }
    },
    undefined,
    context.subscriptions
  );
}

/**
 * Check if GitHub Copilot Chat is installed; if not, honor the
 * `azureMigrationSquad.autoInstallCopilot` setting:
 *   - "auto":   install silently
 *   - "prompt": ask the user once per workspace
 *   - "never":  do nothing
 */
export async function ensureCopilotChat(
  context: vscode.ExtensionContext,
  userInitiated = false
): Promise<void> {
  const COPILOT_CHAT_ID = 'GitHub.copilot-chat';
  const ext = vscode.extensions.getExtension(COPILOT_CHAT_ID);
  if (ext) {
    if (userInitiated) {
      vscode.window.showInformationMessage(
        'GitHub Copilot Chat is already installed. You\'re all set!'
      );
    }
    return;
  }

  const cfg = vscode.workspace.getConfiguration('azureMigrationSquad');
  const mode = cfg.get<string>('autoInstallCopilot', 'prompt');

  if (mode === 'never' && !userInitiated) {
    return;
  }

  if (mode === 'auto' || userInitiated) {
    await installCopilotChat();
    return;
  }

  const consentKey = 'azureMigrationSquad.copilotChatPromptShown.workspace';
  if (context.globalState.get<boolean>(consentKey)) {
    return;
  }

  const choice = await vscode.window.showInformationMessage(
    'The Azure Migration Agent works best with GitHub Copilot Chat. Install it now?',
    'Install',
    'Not now',
    "Don't ask again"
  );

  if (choice === 'Install') {
    await installCopilotChat();
  } else if (choice === "Don't ask again") {
    await context.globalState.update(consentKey, true);
    await cfg.update(
      'autoInstallCopilot',
      'never',
      vscode.ConfigurationTarget.Global
    );
  }
}

async function installCopilotChat(): Promise<void> {
  const COPILOT_CHAT_ID = 'GitHub.copilot-chat';
  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: 'Installing GitHub Copilot Chat...',
      cancellable: false,
    },
    async () => {
      try {
        await vscode.commands.executeCommand(
          'workbench.extensions.installExtension',
          COPILOT_CHAT_ID
        );
        vscode.window.showInformationMessage(
          'GitHub Copilot Chat installed. You may need to reload the window for it to activate.'
        );
      } catch (err) {
        vscode.window.showErrorMessage(
          `Failed to install GitHub Copilot Chat: ${err}. Install manually from the marketplace.`
        );
      }
    }
  );
}

function renderWelcomeHtml(): string {
  return /* html */ `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
  <title>Welcome — Azure Migration Agent</title>
  <style>
    body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); background: var(--vscode-editor-background); padding: 24px 32px; max-width: 800px; margin: 0 auto; line-height: 1.55; }
    h1 { font-size: 1.7em; margin-bottom: 4px; }
    h2 { font-size: 1.15em; margin-top: 32px; border-bottom: 1px solid var(--vscode-panel-border); padding-bottom: 4px; }
    .tagline { color: var(--vscode-descriptionForeground); margin-top: 0; font-size: 1.05em; }
    .actions { display: flex; flex-wrap: wrap; gap: 12px; margin: 20px 0 8px; }
    button { background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; padding: 9px 16px; border-radius: 4px; cursor: pointer; font-size: 0.95em; font-weight: 500; }
    button:hover { background: var(--vscode-button-hoverBackground); }
    button.secondary { background: var(--vscode-button-secondaryBackground); color: var(--vscode-button-secondaryForeground); }
    button.secondary:hover { background: var(--vscode-button-secondaryHoverBackground); }
    code, kbd { background: var(--vscode-textBlockQuote-background); padding: 2px 6px; border-radius: 3px; font-family: var(--vscode-editor-font-family); font-size: 0.92em; }
    .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 16px; }
    .feature-card { padding: 12px 14px; background: var(--vscode-textBlockQuote-background); border-left: 3px solid var(--vscode-textLink-foreground); border-radius: 3px; }
    .feature-card strong { display: block; margin-bottom: 4px; }
    ol li { margin: 8px 0; }
    .badge { display: inline-block; background: var(--vscode-textLink-foreground); color: var(--vscode-editor-background); padding: 1px 8px; border-radius: 10px; font-size: 0.78em; font-weight: 600; margin-left: 6px; vertical-align: middle; }
  </style>
</head>
<body>
  <h1>🚀 Azure Migration Agent <span class="badge">VS Code</span></h1>
  <p class="tagline">Migrate any application to Azure — universal source/stack/workload adapters, Discovery-first workflow, hard-stop user-decision gates.</p>

  <div class="actions">
    <button onclick="send('initialize')">Initialize in this workspace</button>
    <button class="secondary" onclick="send('installCopilotChat')">Install GitHub Copilot Chat</button>
    <button class="secondary" onclick="send('showCatalog')">Show prompt catalog</button>
    <button class="secondary" onclick="send('openSettings')">Open settings</button>
  </div>

  <h2>What you get</h2>
  <div class="feature-grid">
    <div class="feature-card">
      <strong>One migration agent</strong>
      The Code Migration Modernization Agent reads .github/agents/Code-Migration-Modernization.agent.md and orchestrates Phase 0-6 plus utility prompts.
    </div>
    <div class="feature-card">
      <strong>Universal source adapters</strong>
      On-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, GitHub repos, ZIPs, mainframes.
    </div>
    <div class="feature-card">
      <strong>Stack adapters</strong>
      .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows.
    </div>
    <div class="feature-card">
      <strong>Decision Hardstop Protocol</strong>
      The agent NEVER decides framework, database, hosting, IaC tool, etc. It lays out options and waits for YOU.
    </div>
  </div>

  <h2>Your first migration in 3 steps</h2>
  <ol>
    <li><strong>Click "Initialize in this workspace"</strong> above — drops <code>.github/agents/</code>, <code>.github/prompts/</code>, <code>.github/skills/</code>, etc. into your project.</li>
    <li><strong>Open GitHub Copilot Chat</strong> (<kbd>Ctrl+Alt+I</kbd>). If you don't have it, click "Install GitHub Copilot Chat" above.</li>
    <li><strong>Type</strong> <code>/assess-any-application</code> — the agent will interview you about source, stack, workload, then produce a Capability Matrix.</li>
  </ol>

  <h2>Next steps after init</h2>
  <ul>
    <li>Browse the <strong>agent definition, prompts, skills, and decisions</strong> in the sidebar (look for the rocket icon 🚀 in the Activity Bar).</li>
    <li>Check the <strong>status bar</strong> for your current migration phase and pending decisions (bottom-left).</li>
    <li>Open <code>MIGRATION-START-HERE.md</code> in your project root for the full quickstart.</li>
    <li>Use the <strong>Command Palette</strong> (<kbd>Ctrl+Shift+P</kbd>) → type "Azure Migration:" to see all commands.</li>
  </ul>

  <script>
    const vscode = acquireVsCodeApi();
    function send(command) { vscode.postMessage({ command }); }
  </script>
</body>
</html>`;
}
