/**
 * Shell out to `npx @robertoborges/azure-migration-squad@<channel> <command>` and
 * stream output into a VS Code OutputChannel so users can see what's happening.
 */

import * as vscode from 'vscode';
import { spawn } from 'child_process';

let outputChannel: vscode.OutputChannel | undefined;

export function getOutputChannel(): vscode.OutputChannel {
  if (!outputChannel) {
    outputChannel = vscode.window.createOutputChannel('Azure Migration Squad');
  }
  return outputChannel;
}

export interface RunNpxOptions {
  /** AMS subcommand: "init", "upgrade", "doctor", "list", etc. */
  subcommand: string;
  /** Extra flags to pass after the subcommand. */
  args?: string[];
  /** Working directory for the npx process. */
  cwd: string;
  /** Channel: "latest" or "insider". Defaults to user setting. */
  channel?: 'latest' | 'insider';
  /** Title shown on the progress notification. */
  progressTitle?: string;
}

/**
 * Runs the AMS CLI via npx and shows progress + output in VS Code.
 * Returns the exit code (0 = success).
 */
export async function runAmsCli(opts: RunNpxOptions): Promise<number> {
  const channel = opts.channel || getConfiguredChannel();
  const pkgSpec = `@robertoborges/azure-migration-squad@${channel}`;
  const args = ['-y', pkgSpec, opts.subcommand, ...(opts.args || [])];
  const out = getOutputChannel();

  out.show(true);
  out.appendLine('');
  out.appendLine('─'.repeat(78));
  out.appendLine(`▶ npx ${args.join(' ')}`);
  out.appendLine(`  cwd: ${opts.cwd}`);
  out.appendLine('─'.repeat(78));

  return new Promise<number>((resolve) => {
    vscode.window.withProgress(
      {
        location: vscode.ProgressLocation.Notification,
        title: opts.progressTitle || `Running AMS: ${opts.subcommand}`,
        cancellable: false,
      },
      async () => {
        return new Promise<void>((res) => {
          const proc = spawn('npx', args, {
            cwd: opts.cwd,
            shell: true,
            env: process.env,
          });

          proc.stdout.on('data', (data: Buffer) => {
            out.append(stripAnsi(data.toString()));
          });
          proc.stderr.on('data', (data: Buffer) => {
            out.append(stripAnsi(data.toString()));
          });
          proc.on('close', (code) => {
            const exit = code ?? -1;
            out.appendLine('');
            out.appendLine(`◀ exit ${exit}`);
            if (exit === 0) {
              vscode.window.showInformationMessage(
                `Azure Migration Squad: ${opts.subcommand} completed successfully.`
              );
            } else {
              vscode.window.showErrorMessage(
                `Azure Migration Squad: ${opts.subcommand} failed with exit ${exit}. See output for details.`
              );
            }
            resolve(exit);
            res();
          });
          proc.on('error', (err) => {
            out.appendLine(`ERROR: ${err.message}`);
            vscode.window.showErrorMessage(
              `Azure Migration Squad: failed to launch npx (${err.message}). Is Node.js installed?`
            );
            resolve(-1);
            res();
          });
        });
      }
    );
  });
}

function getConfiguredChannel(): 'latest' | 'insider' {
  const cfg = vscode.workspace.getConfiguration('azureMigrationSquad');
  const ch = cfg.get<string>('channel', 'latest');
  return ch === 'insider' ? 'insider' : 'latest';
}

/** Strip ANSI color codes from CLI output so the OutputChannel reads cleanly. */
function stripAnsi(s: string): string {
  // eslint-disable-next-line no-control-regex
  return s.replace(/\x1b\[[0-9;]*m/g, '');
}
