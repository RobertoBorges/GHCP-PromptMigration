/**
 * Detect Squad runtime state for a workspace.
 *
 * AMS init by default requires Squad's `.squad/` directory to exist (created
 * by `squad init`). But the AMS package's own content already includes a
 * `.squad/agents/` folder full of charters, so passing `--force` to AMS init
 * makes it install everything in one shot without requiring a separate
 * Squad CLI install.
 *
 * This module gives callers a way to decide whether to:
 *   - call `ams init` cleanly (Squad runtime present)
 *   - call `ams init --force` (Squad runtime missing, but extension users
 *     don't need it — Copilot Chat doesn't depend on the `squad` CLI binary)
 *   - call `squad init` first (rare; only if the user wants the full Squad
 *     CLI experience and we detect they have it globally installed)
 *
 * Calls to `isSquadCliInstalled()` are cached for the process lifetime
 * because `which`/`where` is expensive and the answer rarely changes.
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import { execSync } from 'node:child_process';

export type SquadState =
  /** No Squad scaffolding in this workspace; Squad CLI not on PATH. AMS works fine with --force. */
  | 'no-squad'
  /** No Squad scaffolding in this workspace; Squad CLI IS on PATH. Could run `squad init` first if desired. */
  | 'cli-available'
  /** Squad's .squad/ directory exists here but AMS isn't installed yet. AMS init will succeed without --force. */
  | 'squad-initialized'
  /** AMS is already installed in this workspace. */
  | 'ams-installed';

export interface SquadDetectionResult {
  state: SquadState;
  /** True if `.squad/` exists in the workspace. */
  hasLocalSquad: boolean;
  /** True if `.azure-migration-squad/manifest.json` exists. */
  hasAmsManifest: boolean;
  /** True if `squad` is on the user's global PATH. */
  hasGlobalSquadCli: boolean;
}

export function detectSquadState(workspaceRoot: string): SquadDetectionResult {
  const hasAmsManifest = fs.existsSync(
    path.join(workspaceRoot, '.azure-migration-squad', 'manifest.json')
  );
  const hasLocalSquad = fs.existsSync(path.join(workspaceRoot, '.squad'));
  const hasGlobalSquadCli = isSquadCliInstalled();

  let state: SquadState;
  if (hasAmsManifest) {
    state = 'ams-installed';
  } else if (hasLocalSquad) {
    state = 'squad-initialized';
  } else if (hasGlobalSquadCli) {
    state = 'cli-available';
  } else {
    state = 'no-squad';
  }

  return { state, hasLocalSquad, hasAmsManifest, hasGlobalSquadCli };
}

let cliCheckCache: boolean | null = null;

/**
 * Returns true if the global `squad` binary is on the PATH.
 * Result is cached for the lifetime of the extension host process.
 */
function isSquadCliInstalled(): boolean {
  if (cliCheckCache !== null) return cliCheckCache;
  try {
    execSync('squad --version', {
      stdio: 'ignore',
      timeout: 5000,
      shell: process.platform === 'win32' ? true : '/bin/sh',
    } as Parameters<typeof execSync>[1]);
    cliCheckCache = true;
  } catch {
    cliCheckCache = false;
  }
  return cliCheckCache;
}

/**
 * Returns the args to pass to `ams init` based on detected Squad state.
 *
 * - `no-squad` / `cli-available` → pass `--force` so AMS init bypasses its
 *   "Squad runtime not detected" check and installs the content directly.
 *   The AMS templates include the `.squad/agents/` structure anyway, so the
 *   user gets a fully-functional setup either way.
 * - `squad-initialized` → no flags needed; AMS init runs cleanly.
 * - `ams-installed` → callers should NOT call init; use upgrade instead.
 */
export function argsForAmsInit(state: SquadState): string[] {
  if (state === 'no-squad' || state === 'cli-available') {
    return ['--force'];
  }
  return [];
}

/**
 * For tests: reset the cached squad-cli detection result so the next call
 * re-probes the environment.
 */
export function _resetSquadCliCache(): void {
  cliCheckCache = null;
}
