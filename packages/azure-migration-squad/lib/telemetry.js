/**
 * Anonymous telemetry — PostHog Cloud, US region.
 *
 * Backend: https://us.i.posthog.com (project: azure-migration-squad, org: robertoborges)
 * Implementation: raw fetch, no SDK dependencies. ~60 lines.
 *
 * GUARANTEES:
 *   - Telemetry NEVER blocks CLI operations (timeout 2s, fail-silent)
 *   - Telemetry NEVER captures file paths, project content, prompts, customer data,
 *     IPs, emails, git remotes, branch names, or stack traces
 *   - Telemetry can be disabled at any time via env, flag, or config (see telemetry-consent.js)
 *
 * The POSTHOG_API_KEY is a write-only Project API Key — safe to ship publicly in OSS code.
 * It can only `capture` events; it cannot read or delete data. Same pattern used by
 * Vercel, Astro, Next.js, and many other open-source CLIs.
 */

import { resolveTelemetryEnabled, getInstallId } from './telemetry-consent.js';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Read package version once
let PKG_VERSION = 'unknown';
try {
  const pkg = JSON.parse(readFileSync(path.resolve(__dirname, '..', 'package.json'), 'utf-8'));
  PKG_VERSION = pkg.version;
} catch {
  /* ignore */
}

// ────────────────────────────────────────────────────────────────────────────
// Configuration
// ────────────────────────────────────────────────────────────────────────────

// PostHog Cloud Project API Key.
// This is a WRITE-ONLY project key — safe to ship in OSS code.
// It can only capture events; it cannot read or delete data.
// Project: azure-migration-squad (org: robertoborges, region: US)
// Public dashboard: https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/telemetry.md (link added in Wave E)
const POSTHOG_API_KEY =
  process.env['POSTHOG_API_KEY_OVERRIDE'] ||
  'phc_nYirVnEB6fX3FP6jVSRNb9zHJcLXyUQnFJgi8ipLgMta';
const POSTHOG_HOST = 'https://us.i.posthog.com';
const TELEMETRY_TIMEOUT_MS = 2000;

// ────────────────────────────────────────────────────────────────────────────
// Public API
// ────────────────────────────────────────────────────────────────────────────

/**
 * Track an anonymous event.
 *
 * @param {string} event — event name, e.g. 'cli.install', 'cli.command', 'cli.error'
 * @param {object} [props] — additional anonymous properties (NEVER include PII or paths)
 * @param {object} [opts]
 * @param {boolean} [opts.flagDisabled] — true if --no-telemetry was passed
 * @returns {Promise<void>} — always resolves; never throws
 */
export async function track(event, props = {}, opts = {}) {
  // Resolve consent
  const { enabled } = resolveTelemetryEnabled({ flagDisabled: opts.flagDisabled });
  if (!enabled) return;

  // No key configured (Wave A stub) — no-op
  if (!POSTHOG_API_KEY) return;

  try {
    // Build PostHog payload
    const payload = {
      api_key: POSTHOG_API_KEY,
      event,
      distinct_id: getInstallId(),
      properties: {
        ...sanitizeProps(props),
        $lib: 'azure-migration-squad',
        $lib_version: PKG_VERSION,
        os_platform: process.platform,           // 'darwin' | 'linux' | 'win32'
        node_major: process.versions.node.split('.')[0],
      },
      timestamp: new Date().toISOString(),
    };

    await fetch(`${POSTHOG_HOST}/i/v0/e/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(TELEMETRY_TIMEOUT_MS),
    });
  } catch {
    // Fail-silent. Telemetry NEVER breaks the CLI.
  }
}

// ────────────────────────────────────────────────────────────────────────────
// Property sanitization — defense-in-depth against accidental PII
// ────────────────────────────────────────────────────────────────────────────

const FORBIDDEN_KEYS = new Set([
  'path', 'paths', 'file', 'files', 'cwd', 'repo', 'repoName', 'projectName',
  'gitRemote', 'remote', 'branch', 'email', 'username', 'userName', 'user',
  'host', 'hostname', 'ip', 'token', 'apiKey', 'secret', 'password',
  'content', 'body', 'message', 'stack', 'stackTrace',
]);

function sanitizeProps(props) {
  const clean = {};
  for (const [key, value] of Object.entries(props)) {
    if (FORBIDDEN_KEYS.has(key)) continue;
    if (typeof value === 'string' && looksLikePath(value)) continue;
    if (typeof value === 'string' && looksLikeEmail(value)) continue;
    if (typeof value === 'object' && value !== null) continue; // no nested objects
    clean[key] = value;
  }
  return clean;
}

function looksLikePath(s) {
  return s.includes('/') || s.includes('\\') || /^[A-Z]:/.test(s);
}

function looksLikeEmail(s) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
}

// ────────────────────────────────────────────────────────────────────────────
// Convenience wrappers
// ────────────────────────────────────────────────────────────────────────────

export const trackInstall = (props, opts) => track('cli.install', props, opts);
export const trackUpgrade = (props, opts) => track('cli.upgrade', props, opts);
export const trackCommand = (commandName, props, opts) =>
  track('cli.command', { command_name: commandName, ...props }, opts);
export const trackError = (errorClass, props, opts) =>
  track('cli.error', { error_class: errorClass, ...props }, opts);
export const trackTelemetryDisabled = (source, opts) =>
  track('telemetry.disabled', { disabled_by: source }, opts);
