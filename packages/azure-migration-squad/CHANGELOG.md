# Changelog

## 0.1.0-insider.7

### Patch Changes

- f70ce5b: CI hardening:

  - **Source-of-truth guard now line-ending-agnostic** — `scripts/check-templates-not-edited.mjs` normalizes CRLF/LF for text files before hashing, so it no longer fails when `templates/` is committed from Windows but synced on Linux.
  - **`.gitattributes` enforces LF** for all text files (PowerShell scripts kept as CRLF).
  - **CI matrix reduced to ubuntu-latest + Node 20 only** — package is pure Node.js with no native deps; cross-OS matrix wasted ~83% of CI minutes per push. macOS/Windows can be smoke-tested manually before releases.
  - **Squad eval no longer expects deprecated `Assess-*` prompts** at `.github/prompts/` — they were moved to `.github/prompts/legacy/` during the Universal Mode redesign. Eval now verifies the archive instead.
  - **Squad eval no longer requires `Use-cases/README.md`** — walkthroughs live under `docs/walkthroughs/` and `docs/use-case-cheatsheets/`.
  - **Prompt linter `model` and `tools` fields are now optional** — Copilot CLI prompts use `name` + `argument-hint` format, not VS Code chat format. Both formats are now accepted.
  - Phase / portfolio / status prompts added to lint hook-reference exemption list (they reference hooks indirectly through the Migration-Orchestrator chatmode).

## 0.1.0-insider.6

### Patch Changes

- **Release auth migrated to npm Trusted Publisher (OIDC).** No more `NPM_TOKEN` rotation pain.

  The `.github/workflows/release.yml` now publishes via short-lived OIDC tokens (npm CLI 11.5.1+ auto-detects the GitHub Actions OIDC env vars). Benefits:

  - No `NPM_TOKEN` secret to rotate (npm's UI now caps Granular tokens at 365 days)
  - Workflow-scoped — only `release.yml` can publish; a leak in another workflow can't be used
  - Provenance attestation is auto-generated (the npm page will show "Built and signed on GitHub Actions")
  - 5-minute publish tokens minted on demand; no long-lived secret can leak

  **One-time maintainer action required:** configure Trusted Publisher in the npm UI at https://www.npmjs.com/package/@robertoborges/azure-migration-squad/access — full step-by-step in `docs/release-automation.md`.

  After enabling Trusted Publisher, you can also revoke the existing `NPM_TOKEN` GitHub secret and enable "disallow tokens" on the package for maximum hardening.

  This is a docs + workflow change only — no behavior change for end users of the package.

## 0.1.0-insider.5

### Patch Changes

- Source-of-truth clarity + edit-guard:

  **Docs**

  - Root `README.md` now opens with a "Source-of-truth rule" section + table mapping every editable area to its canonical location
  - Repository structure tree marks every directory as ✏️ EDIT or ❌ DO NOT EDIT
  - Package `README.md` gains a "For contributors — source-of-truth rule" section
  - New `packages/azure-migration-squad/templates/README.md` is a big DO-NOT-EDIT sign at the entry of the auto-generated folder
  - `docs/contributing-adapters.md` opens with a "Critical first rule — where to edit" section

  **CI guard**

  - New `scripts/check-templates-not-edited.mjs` snapshots `templates/`, re-runs sync, and fails the build if any file differs (i.e., someone edited `templates/` directly instead of the canonical root location)
  - Wired into both `azure-migration-squad-ci.yml` and `release.yml` as a step BEFORE sync/build
  - New root script: `npm run validate:templates-not-edited`
  - `validate:all` now includes the guard

  **Workflow comments**

  - Both GitHub Actions workflows (`azure-migration-squad-ci.yml` and `release.yml`) gain a prominent ASCII-bordered comment at the top describing the source-of-truth rule so anyone reading the workflow YAML sees it

  **Misc**

  - `clean-templates.mjs` now preserves `README.md` and `.npmignore` across syncs (in addition to `.gitkeep`) — they're intentional, not noise
  - `.npmignore` inside `templates/` excludes `README.md` from the published tarball (it's a repo-only warning sign, not user content)

## 0.1.0-insider.4

### Minor Changes

- Wave B/E/F shipping together:

  **B — Release automation**

  - Added Changesets (`@changesets/cli`) at monorepo root; pre-release mode entered with `insider` tag
  - New `.github/workflows/release.yml` runs on push to `main`: opens "version packages" PR or auto-publishes to npm when consumed
  - New `docs/release-automation.md` documents the NPM_TOKEN secret setup + day-to-day flow
  - New root scripts: `npm run changeset`, `npm run changeset:version`, `npm run changeset:publish`

  **E — Capability Matrix hard gates**

  - All 9 phase prompts (Phase 1–6 + Database Migration + Security Hardening + Cost Optimization) now have a mandatory opening check that refuses to proceed without `reports/Discovery-Dossier.md` + `reports/Capability-Matrix.yaml` + `reports/Migration-Plan.md`
  - Gate is auto-managed by `scripts/inject-capability-matrix-gates.mjs` (idempotent; re-run anytime; sentinel-bounded for safe in-place updates)
  - Eval suite extended with hard-gate enforcement test — fails CI if the gate sentinel goes missing from any of the 9 prompts

  **F — `ams` short alias polish**

  - README + package README now lead with `ams init` instead of the long `azure-migration-squad init`
  - CLI `help` output reordered: `ams` shown first, with `azure-migration-squad` as the equivalent long form
  - New EXAMPLES section in `help` showing the 5 most common invocations

All notable changes to `@robertoborges/azure-migration-squad` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Dist tags:

- `latest` — current stable release
- `insider` — preview / early-access builds (may break between minor versions)

## [0.1.0-insider.3] — 2026-06-18

### Fixed (user-reported)

- **`/assess-any-application` returned "Unknown command" in Copilot CLI.** Root cause: **GitHub Copilot CLI does not auto-register `.github/prompts/*.prompt.md` files as slash commands** — that's a VS Code Copilot Chat feature only. Copilot CLI loads instructions (`AGENTS.md`, `copilot-instructions.md`, agent files) but not prompts.

### Changed

- **`.github/copilot-instructions.md`** now opens with a clear "How to Invoke the Squad (CLI vs Chat)" section + a 20-row natural-language → action mapping table. The Squad agent uses this table to interpret user intent regardless of which surface they're on.
- **`AGENTS.md`** adds an explicit "CLI vs Chat — Important" section so any agent loaded by Copilot CLI knows to interpret natural-language commands AND treat `/assess-any-application`-style literal text as the natural-language equivalent.
- **Package README + repo README** both now show two install/use paths side-by-side: VS Code Chat (slash commands) AND Copilot CLI (natural language).

### Why this matters

In v0.1.0-insider.0/1/2, users who installed via Copilot CLI hit a dead-end when typing `/assess-any-application` — they'd see "Unknown command" with no actionable guidance. The Squad agent was loaded correctly, but it had no instruction to interpret slash-style commands. v0.1.0-insider.3 fixes this without changing any actual behavior — only docs + instruction text. Both VS Code Chat and Copilot CLI now produce identical outcomes.

## [0.1.0-insider.2] — 2026-06-18

### Added

- **`doctor` command now validates the Capability Matrix.** If `reports/Capability-Matrix.yaml` exists, doctor parses it (lightweight YAML reader, no extra deps) and validates required top-level keys (`schema_version`, `application`, `source`, `stack`, `workload`, `data`, `migration_strategy`), confidence labels (`high|medium|low` on each axis), and the 6Rs strategy enum. Failures are reported per-problem.
- **Evaluator-driven eval suite** (`test/eval-suite.test.mjs`) — 12 tests covering prompt/skill/charter content shape: Discovery Engineer routing, Architect handoff contract, Migration-Orchestrator references all 15 agents, decision tree has ≥10 branches and lists all 6Rs+, Capability Matrix skill covers all axes, charters enforce evidence + handoff, routing is capability-based, coverage check on source/stack/workload adapter counts.
- **CI workflow expanded** to run `validate:descriptions`, `validate:plugin-manifest`, install smoke tests, AND the eval suite on Ubuntu/macOS/Windows × Node 20/22.
- **Repository top-level docs:** [`docs/telemetry.md`](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/telemetry.md), [`docs/privacy-policy.md`](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/privacy-policy.md), [`docs/contributing-adapters.md`](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/contributing-adapters.md), and translations ([🇪🇸](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/translations/README.es-ES.md), [🇧🇷](https://github.com/RobertoBorges/GHCP-PromptMigration/blob/main/docs/translations/README.pt-BR.md)).
- **Squad plugin marketplace manifest** (`plugin.manifest.json` at repo root) — 81 file deployments declared. Auto-generated by `scripts/build-plugin-manifest.mjs`. Users can now register the repo as a Squad marketplace via `squad plugin marketplace add RobertoBorges/GHCP-PromptMigration`.
- **GitHub template starter** at `template-repo-starter/` — content ready to push to a separate GitHub repo so users can click "Use this template" for a one-step start.
- **Changesets-based release flow** at `.changeset/` for future versioning.

### Changed

- Test script (`npm test`) now runs both install smoke tests AND the eval suite. Individual scripts `npm run test:install` and `npm run test:eval` available.

## [0.1.0-insider.1] — 2026-06-18

### Fixed (HOTFIX)

- **`.github/skills/migration-strategy-report/SKILL.md` description was 1273 chars** — exceeded the 1024-char limit GitHub Copilot / Squad enforce when loading skills. Caused the squad loader to print: _"The following skills failed to load: .github\skills\migration-strategy-report\SKILL.md: Skill description must be at most 1024 characters."_ Trimmed to 955 chars while preserving all the trigger phrases and use-when content.

### Added

- New CI guard: `scripts/validate-description-lengths.mjs` (root) + integrated into the package's `scripts/validate-build.mjs`. The build now fails if ANY skill / chatmode / prompt YAML frontmatter `description` field exceeds 1024 chars across `.github/skills/`, `.github/chatmodes/`, `.github/prompts/` (recursive). New `npm run validate:descriptions` and `npm run validate:all` scripts at the monorepo root.

## [0.1.0-insider.0] — 2026-06-18

### Added

- Initial CLI scaffold (`init`, `upgrade`, `doctor`, `list`, `telemetry`, `help`, `version`)
- Monorepo packaging (npm workspaces) — content lives at repo root, sync-from-root build step copies into `templates/`
- Squad-first init flow — refuses to scaffold without `.squad/` present (use `--force` to bypass for testing)
- Bundled 15 agent charters, 60+ skills (source/stack/workload adapters + universal skills), Phase 0–6 prompts, chatmodes, hooks
- JSON Schemas for Capability Matrix v1.0 and Discovery Dossier front-matter
- **Telemetry — fully active** — opt-out by default, PostHog Cloud (US region, `robertoborges` org, `azure-migration-squad` project), zero runtime dependencies
  - Honors `--no-telemetry`, `AZURE_MIGRATION_SQUAD_TELEMETRY=0`, `DO_NOT_TRACK=1`, `CI=true`, user config, project config
  - First-run consent notice (one-time, non-blocking in CI)
  - Write-only Project API Key shipped publicly (industry-standard pattern; safe — cannot read or delete data)
- Installation manifest at `.azure-migration-squad/manifest.json`
- Short alias `ams` in addition to `azure-migration-squad`

### Known Limitations

- **No Squad plugin marketplace registration yet** — Wave B.
- **`upgrade` is a full re-overwrite** of squad-managed files (your `reports/` and `.squad/decisions.md` are never touched). A more granular diff/merge mode is on the roadmap.
- **No automated schema validation of installed `Capability-Matrix.yaml` files** during `doctor` — Wave E.
- **Cross-reference validation in CI** is a basic file-existence check, not a deep markdown parse.
- **Public telemetry dashboard URL not yet linked** in docs (PostHog dashboards to be created post-publish; URL will be added in 0.1.1-insider.0).

[0.1.0-insider.0]: https://github.com/RobertoBorges/GHCP-PromptMigration/releases/tag/azure-migration-squad-v0.1.0-insider.0
