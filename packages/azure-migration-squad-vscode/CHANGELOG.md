# Changelog

All notable changes to the Azure Migration Agent VS Code extension are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0](https://github.com/RobertoBorges/GHCP-PromptMigration/compare/vscode-v0.2.0...vscode-v0.3.0) (2026-07-23)


### Features

* **docs:** reorganize main path vs optional accessories ([b84dbeb](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/b84dbeba38ddd7d61a97084ac73c3d5cd0e69216))
* **logging:** add Action Log to Report-Status.md for trace memory + token accounting ([72bc956](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/72bc95613190ffca197b77f74b18c478c12ee48f))
* **prompts:** make phase prompts, agent, and add-ons stack-agnostic ([04384f6](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/04384f6e7a6b8a15c9350be8fc1408ea70970554))
* **release:** add release-please automation + local release script ([70d63cc](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/70d63cca301b0e1bd275e8f1a23162ee8ae1df4a))
* **scope:** remove mainframe / COBOL as first-class family; route via source-unsupported-escalation ([30e8118](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/30e81187fb92cef6afee5a79463854a27f7292cd))
* **skills:** add skill-creator meta-skill for on-the-fly skill authoring ([c582098](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/c582098fcd20ed4bedd5968f983023a76d08615c))
* **vscode-ext:** Phase 2 scaffold for azure-migration-squad-vscode extension ([82fd4b6](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/82fd4b60cb8cdd229c5fc5d7414c3fc25a2d70dc))
* **vscode-ext:** Phase 3 — tree view + 8 Command Palette commands ([612bba1](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/612bba12e695c8ee568826d4442a869e76a4567f))
* **vscode-ext:** Phase 4 + 5 — status bar, settings, welcome panel, walkthrough ([a9c79f4](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/a9c79f428e9f2619922bb0c1a158aa07b0b2c23c))
* **vscode-ext:** Phase 6 — publishing pipeline + docs refresh + reliability fix ([e3b3a95](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/e3b3a9516c196d484a8311e50689f1211af8b231))
* **vscode-ext:** v0.1.3 — surface Wave H decisions in sidebar + status bar ([45ea7ca](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/45ea7ca4aa4d6bc4a5572e3fcef097a017001682))


### Bug Fixes

* guard run() to only .trim() when execSync returned a string. ([af0bf4b](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/af0bf4b946f8507159e3093b55b0a93d3182413b))
* **prompts:** correct frontmatter agent field across all prompts + chatmodes ([75be393](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/75be393b338575a1ec6aa32ad8734102478eb131))
* **prompts:** rename Phase1 to Phase1-Plan and restore Assess as main-path step 1 ([dd031d7](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/dd031d7fb84c2b7410590a781b5432769c84d66d))
* **release:** handle null return from execSync when stdio is 'inherit' ([af0bf4b](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/af0bf4b946f8507159e3093b55b0a93d3182413b))
* **vscode-ext:** bypass Squad-CLI check on initialize (v0.1.1) ([71a3e06](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/71a3e06c59b40a4e9e85fb4657f2a01030bae4f7))
* **vscode-ext:** register AMS agents with Squad CLI after init (v0.1.2) ([6f10a04](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/6f10a04deac35f9117922e18932ca28aa80fec50))
* **vscode-ext:** rename status bar prefix AMS -&gt; AMA (Azure Migration Agent) ([8de5348](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/8de534887186501cbbd75289d1a6a5e4107a8050))

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
