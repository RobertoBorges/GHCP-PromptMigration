/**
 * Telemetry consent + opt-out resolution.
 *
 * Opt-out precedence (first match wins; any "off" disables):
 *   1. CLI flag --no-telemetry            (per-invocation)
 *   2. env AZURE_MIGRATION_SQUAD_TELEMETRY=0|false|off|no
 *   3. env DO_NOT_TRACK=1                  (industry-standard convention)
 *   4. env CI=true                          (auto-disable in CI by default)
 *   5. user config file                    (~/.config/azure-migration-squad/config.json)
 *   6. project config file                 (<cwd>/.azure-migration-squad/config.json)
 *
 * If none of the above disable telemetry, it is ENABLED by default (opt-out model).
 *
 * The user can persist their choice at any time via the `telemetry on|off` subcommand,
 * which writes to the user config file.
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';

const USER_CONFIG_DIR = path.join(
  process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'),
  'azure-migration-squad'
);
const USER_CONFIG_PATH = path.join(USER_CONFIG_DIR, 'config.json');
const PROJECT_CONFIG_PATH = path.join(process.cwd(), '.azure-migration-squad', 'config.json');

const FALSE_VALUES = new Set(['0', 'false', 'off', 'no']);

function isFalse(value) {
  if (value == null) return false;
  return FALSE_VALUES.has(String(value).trim().toLowerCase());
}

function readJsonSafe(p) {
  try {
    if (!existsSync(p)) return null;
    return JSON.parse(readFileSync(p, 'utf-8'));
  } catch {
    return null;
  }
}

/**
 * Resolve whether telemetry is currently enabled.
 *
 * @param {object} options
 * @param {boolean} [options.flagDisabled] — true if --no-telemetry was passed
 * @returns {{ enabled: boolean, source: string }}
 */
export function resolveTelemetryEnabled(options = {}) {
  if (options.flagDisabled) {
    return { enabled: false, source: 'cli-flag' };
  }

  const envValue = process.env['AZURE_MIGRATION_SQUAD_TELEMETRY'];
  if (envValue != null && isFalse(envValue)) {
    return { enabled: false, source: 'env-AZURE_MIGRATION_SQUAD_TELEMETRY' };
  }

  if (process.env['DO_NOT_TRACK'] === '1' || process.env['DO_NOT_TRACK'] === 'true') {
    return { enabled: false, source: 'env-DO_NOT_TRACK' };
  }

  // Auto-disable in CI unless explicitly enabled
  if (process.env['CI'] === 'true' && envValue !== '1' && envValue !== 'true') {
    return { enabled: false, source: 'env-CI' };
  }

  const userConfig = readJsonSafe(USER_CONFIG_PATH);
  if (userConfig && userConfig.telemetry === false) {
    return { enabled: false, source: 'user-config' };
  }

  const projectConfig = readJsonSafe(PROJECT_CONFIG_PATH);
  if (projectConfig && projectConfig.telemetry === false) {
    return { enabled: false, source: 'project-config' };
  }

  return { enabled: true, source: 'default' };
}

/**
 * Get or create a persistent anonymous install ID.
 * Stored in the user config file. A random UUID — no PII.
 */
export function getInstallId() {
  let config = readJsonSafe(USER_CONFIG_PATH) || {};
  if (!config.installId) {
    config.installId = crypto.randomUUID();
    writeUserConfig(config);
  }
  return config.installId;
}

/**
 * Has the user been shown the first-run consent notice?
 */
export function hasSeenFirstRunNotice() {
  const config = readJsonSafe(USER_CONFIG_PATH) || {};
  return config.firstRunNoticeShown === true;
}

export function markFirstRunNoticeShown() {
  const config = readJsonSafe(USER_CONFIG_PATH) || {};
  config.firstRunNoticeShown = true;
  config.firstRunAt = config.firstRunAt || new Date().toISOString();
  writeUserConfig(config);
}

/**
 * Persist telemetry on/off in the user config.
 */
export function setTelemetryEnabled(enabled) {
  const config = readJsonSafe(USER_CONFIG_PATH) || {};
  config.telemetry = !!enabled;
  config.telemetryChangedAt = new Date().toISOString();
  writeUserConfig(config);
}

function writeUserConfig(config) {
  if (!existsSync(USER_CONFIG_DIR)) {
    mkdirSync(USER_CONFIG_DIR, { recursive: true });
  }
  writeFileSync(USER_CONFIG_PATH, JSON.stringify(config, null, 2) + '\n', 'utf-8');
}

export function getUserConfigPath() {
  return USER_CONFIG_PATH;
}

export function getProjectConfigPath() {
  return PROJECT_CONFIG_PATH;
}

export function getTelemetryStatus() {
  const { enabled, source } = resolveTelemetryEnabled();
  return {
    enabled,
    source,
    installId: enabled ? getInstallId() : null,
    userConfigPath: USER_CONFIG_PATH,
    projectConfigPath: existsSync(PROJECT_CONFIG_PATH) ? PROJECT_CONFIG_PATH : null,
  };
}
