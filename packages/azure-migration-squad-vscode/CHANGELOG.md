# Changelog

All notable changes to the Azure Migration Agent VS Code extension are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — Drop Squad, ship via extension only

**Major reset.** Removed the entire Squad framework dependency. The project now ships as a **self-contained VS Code extension** that bundles a single agent definition (`.github/agents/Code-Migration-Modernization.agent.md`) plus 19 prompts, 113 skills, 8 chatmodes, and 11 hooks.

### Removed
- **Squad CLI / `@bradygaster/squad-cli` dependency** — Initialize no longer shells out to `npx`. The extension copies bundled templates directly into the workspace.
- **The npm package `@robertoborges/azure-migration-squad`** — no longer published. The extension is the sole distribution.
- **15 specialist agent charters** under `.squad/agents/*/charter.md` — replaced by the single `.github/agents/Code-Migration-Modernization.agent.md`.
- **Commands:**
  - `azureMigrationSquad.installSquadCli`
  - `azureMigrationSquad.registerAgents`
- **Settings:**
  - `azureMigrationSquad.channel` (npm dist-tag — no longer relevant)
  - `azureMigrationSquad.telemetry.enabled` (telemetry was an npm-package feature)
  - `azureMigrationSquad.language` (translations dropped)
  - `azureMigrationSquad.promptSquadInit` (no Squad CLI to prompt for)
- **Modules:** `src/util/runNpx.ts`, `src/util/squadDetection.ts` and their tests.

### Changed
- **Extension displayName:** "Azure Migration Squad" → **"Azure Migration Agent"**.
- **`Initialize` command:** Now copies from the extension's bundled `templates/` directory into the workspace. No `npx`, no network, no external dependency.
- **`Upgrade` command:** Now overwrites with the latest extension contents (no version-bump shenanigans).
- **`Doctor` command:** Inspects the workspace directly — checks for `.github/agents/`, `.github/prompts/`, etc., and `reports/Decisions-Required.md`. No CLI dependency.
- **Agents tree view:** Reads `.github/agents/*.agent.md` from the workspace (was `.squad/agents/<name>/charter.md`).
- **Welcome panel:** Rewritten to drop all Squad references.
- **`AmsWorkspace` interface:** `hasManifest`/`hasSquad` → `hasAgent`/`isInstalled`.

### Kept
- **Wave H Decision Hardstop Protocol** (all of it): `decision-hardstop.md`, `decision-catalog.md`, `decisions-required-template.md`, `decision-gates.md`, the injectors, the validator.
- **"🛑 Decisions Required" sidebar tree view** + status bar pending count (Wave I).
- **Auto-prompt for Copilot Chat install** with consent (existing behavior).
- **VS Code Walkthrough** (4 steps) — rephrased to drop Squad language.
- **Welcome notification + WebView panel** — same UX, new copy.

### Added
- **`templates/` folder + `scripts/sync-templates.mjs`** — bundles canonical `.github/*` content into the extension. Runs as `prepackage` and `pretest` so the `.vsix` always has fresh content.
- **`src/util/templatesCopier.ts`** — direct filesystem copy from extension install dir into workspace. No `npx`, no network.

### Tests
- **13 tests passing** (was 17 before; squadDetection tests removed):
  - 8 decisionsParser tests
  - 5 extension activation/commands tests
- Bundle: **27.8 KB** esbuild output. **.vsix: 461 KB (168 files)** — now ships ALL the prompts/skills/chatmodes/hooks/agent inside.

### Why
The Squad framework added complexity (15 specialist agents, eval scripts, governance rules, separate CLI) without proportional value for a migration-tool use case. The user wanted to return to the original architecture: one agent + prompts + skills, distributed through a VS Code extension. This release delivers exactly that.

## [0.1.3] — (legacy) Wave H surface

Previous releases used the Squad framework. See git history for details.
