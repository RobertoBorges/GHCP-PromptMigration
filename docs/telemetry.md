# Telemetry Policy — Azure Migration Squad

> Last updated: 2026-06-18 · Applies to: `@robertoborges/azure-migration-squad@0.1.0-insider.0` and later

## Summary

The `@robertoborges/azure-migration-squad` CLI collects **anonymous usage data** by default to help us:
- Understand which platforms/Node versions to prioritize for compatibility
- Identify the most-used commands so we can polish them first
- Spot error patterns we can fix proactively
- Measure adoption to justify continued investment

**You can opt out at any time** — see [Opt-out options](#opt-out-options) below. There is no penalty (the CLI works identically with or without telemetry).

## What we collect

When telemetry is enabled, the CLI sends a small JSON payload to [PostHog Cloud](https://posthog.com) (US region) on these events:

| Event | When fired | Properties |
|-------|-----------|------------|
| `cli.install` | After `init` completes | `result`, `forced`, `squad_detected`, `files_copied`, `files_skipped` |
| `cli.upgrade` | After `upgrade` completes | `from_version`, `to_version`, `files_copied` |
| `cli.command` | After `doctor` / `list` / `telemetry status` | `command_name`, `problems_found` (doctor only) |
| `cli.error` | When a command throws | `error_class` (e.g. `Error`, `TypeError`), `command` |
| `telemetry.disabled` | When user runs `telemetry off` | `disabled_by` (`user-command`) |

**Common properties on every event:**
- `distinct_id` — random UUID generated at first install (stored in `~/.config/azure-migration-squad/config.json`); not linked to any account
- `$lib` = `"azure-migration-squad"`
- `$lib_version` = the npm package version
- `os_platform` = `"darwin"` | `"linux"` | `"win32"`
- `node_major` = e.g. `"20"`, `"22"`
- `timestamp` = ISO8601

## What we NEVER collect

- ❌ File paths, file names, project names
- ❌ Source code, prompts, customer data
- ❌ Git remote URLs, branch names, commit hashes
- ❌ User emails, names, IPs (PostHog strips client IP at the edge)
- ❌ Anything inside `reports/Discovery-Dossier.md`, `reports/Capability-Matrix.yaml`, or `reports/Migration-Plan.md`
- ❌ Error messages or stack traces (only the error *class name*)
- ❌ Environment variable values
- ❌ npm package authoring info, organization details

**Defense in depth:** the telemetry sender (`lib/telemetry.js`) has a `FORBIDDEN_KEYS` allow-list-reject for property names like `path`, `file`, `cwd`, `email`, `token`, `secret`, `stack`, etc. Even if a future maintainer accidentally adds one, the sanitizer drops it before the network call. The CI pipeline also runs `scripts/lint.mjs` which greps for `track()` calls with forbidden keys and fails the build.

## Opt-out options

All options work — first match disables telemetry.

| Method | Scope | Command |
|--------|-------|---------|
| Per-invocation flag | Current command only | `azure-migration-squad init --no-telemetry` |
| Persistent — CLI subcommand | Forever, until re-enabled | `azure-migration-squad telemetry off` |
| Env var (this session) | This shell only | `export AZURE_MIGRATION_SQUAD_TELEMETRY=0` |
| Env var (persistent) | Add to `.bashrc`/`.zshrc`/`$PROFILE` | same as above |
| Industry-standard convention | Honored automatically | `export DO_NOT_TRACK=1` |
| CI environments | Auto-disabled when `CI=true` | (no action needed) |
| User config file | Forever, this user account | `~/.config/azure-migration-squad/config.json` → `{"telemetry": false}` |
| Project config file | Forever, this project | `<repo>/.azure-migration-squad/config.json` → `{"telemetry": false}` |

**Check current status anytime:** `azure-migration-squad telemetry status`

## Backend details

- **Provider:** [PostHog Cloud](https://posthog.com)
- **Region:** US (`https://us.i.posthog.com`)
- **Project:** `azure-migration-squad`
- **Org:** `robertoborges`
- **API Key in CLI:** A **write-only Project API Key** (`phc_...`) is shipped in the npm package. This key can only `capture` events — it cannot read or delete data. This pattern is standard for OSS CLIs (used by Vercel, Astro, Next.js, etc.)
- **Network behavior:** fail-silent. Telemetry POSTs have a 2-second timeout. If the network is unreachable or the API returns an error, the CLI continues working as if telemetry succeeded. **Telemetry NEVER blocks or slows the CLI.**
- **Public dashboard URL:** _(to be added with v0.1.1-insider.0 once dashboards are built)_

## First-run consent notice

On the very first invocation (per user account), the CLI prints a one-time notice describing what's collected and how to opt out. The user must press **Y** (or default-accept by pressing Enter) before any telemetry fires.

In CI environments (where `CI=true`), the notice is auto-acknowledged silently so pipelines aren't blocked.

The notice is shown only once. A flag is persisted to `~/.config/azure-migration-squad/config.json`.

## Your rights (GDPR / CCPA)

Even though we collect no PII, you have the right to:
- **Opt out at any time** (see above — multiple methods)
- **Request deletion of your `distinct_id`** — open an issue at https://github.com/RobertoBorges/GHCP-PromptMigration/issues with the install ID from your `~/.config/azure-migration-squad/config.json`; we'll remove it from PostHog within 7 days

You don't need to provide your name or email to request deletion.

## How the data is used

| What we do | Yes/No |
|-----------|--------|
| Use to prioritize bug fixes and new adapters | ✅ |
| Share aggregate trends in blog posts / talks | ✅ (anonymized only) |
| Share with vendors (PostHog stores it) | ✅ (necessary for the service) |
| Sell to third parties | ❌ |
| Use for ads / retargeting | ❌ |
| Combine with other datasets to deanonymize | ❌ |
| Use for legal action against you | ❌ |

## Auditing

This policy and the telemetry implementation are open source:
- Policy: [`docs/telemetry.md`](./telemetry.md) (this file)
- Privacy policy: [`docs/privacy-policy.md`](./privacy-policy.md)
- Telemetry sender source: [`packages/azure-migration-squad/lib/telemetry.js`](../packages/azure-migration-squad/lib/telemetry.js)
- Consent resolver source: [`packages/azure-migration-squad/lib/telemetry-consent.js`](../packages/azure-migration-squad/lib/telemetry-consent.js)
- PII-leak CI lint: [`packages/azure-migration-squad/scripts/lint.mjs`](../packages/azure-migration-squad/scripts/lint.mjs)

If you find something we collect that's not documented here, **that's a bug** — please open an issue.

## Changes to this policy

Material changes (new event types, new properties) will be:
1. Documented in the CHANGELOG with a `### Telemetry` section
2. Announced in the release notes
3. Reflected in this document with a "Last updated" bump

We will NEVER quietly add new properties to existing events without updating this document.

## Questions?

Open an issue: https://github.com/RobertoBorges/GHCP-PromptMigration/issues
