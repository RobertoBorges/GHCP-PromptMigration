# Changelog

All notable changes to the Azure Migration Agent VS Code extension are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0](https://github.com/RobertoBorges/GHCP-PromptMigration/compare/vscode-v0.5.0...vscode-v0.6.0) (2026-09-29)


### ⚠ BREAKING CHANGES

* **skills:** every slash command is now lowercase-hyphen, because the skills spec requires name to match ^[a-z0-9-]+$ and to equal its directory name. /Phase1-Plan becomes /phase1-plan, /PortfolioStrategy becomes /portfolio-strategy, and so on for all 19. Invalid characters cause a silent load failure rather than an error, so the old names simply stop resolving.

### Features

* **aws:** add AWS assessment and AWS-to-Azure migration tracks ([82cd160](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/82cd1607217e4f3512f2065a1985323be6736ab7))
* **aws:** add AWS assessment and AWS-to-Azure migration tracks ([784049b](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/784049b49e2bad5299d5675ab70a87938b804f66))
* **skills:** migrate .github to the VS Code agent skills spec ([e4586ed](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/e4586ed190ba9e09cded7999beda281d730b431f))


### Bug Fixes

* **agents:** repair dangling file refs, stale commands and Phase 2 routing ([b5791e1](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/b5791e1eca2e2b4ede24cf3d8f834da85eeece6f))
* **hooks:** make AWS read-only gates fire on every agent surface ([#39](https://github.com/RobertoBorges/GHCP-PromptMigration/issues/39)) ([75c5400](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/75c5400cdb1fde9a472f5269dda3ad13ef575331))


### Documentation

* correct both READMEs against the actual repo, and remove the last "Factory / ISD" leaks ([aad51ec](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/aad51ec55e9aa7e8bcdc1037cd60ac52bcee2904))
* **skills:** replace stale prompt-era wording across skills, agents and hooks ([bc3d21b](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/bc3d21bff95ae41489b77a03798642bfe6c0f818))


### Code Refactoring

* **agents:** collapse the agent picker to three front doors ([011e007](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/011e007c3af80797401b0f362481b2025e5e0825))
* **agents:** merge the Phase 2 specialist away and drop heist theming ([68baf11](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/68baf11d2f5e4191a920687b1de041edc5a0ced8))

## [0.5.0](https://github.com/RobertoBorges/GHCP-PromptMigration/compare/vscode-v0.4.0...vscode-v0.5.0) (2026-07-28)


### Features

* **portfolio:** rename Microsoft-internal Factory/ISD terms to customer-neutral labels ([95e0375](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/95e0375b1ea6edff8eb13dfae44d25529f3f774e))
* **portfolio:** rename Microsoft-internal Factory/ISD terms to customer-neutral labels ([eefb4e6](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/eefb4e6337c26d6e6f1785dfb1ae12967209f7eb))

## [0.4.0](https://github.com/RobertoBorges/GHCP-PromptMigration/compare/vscode-v0.3.2...vscode-v0.4.0) (2026-07-27)


### Features

* **compat:** lock extension to VS Code only (drop Open VSX + runtime host check) ([68d98b8](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/68d98b8bd1b884060fc6e552bd793e4703dcc7f4))

## [0.3.2](https://github.com/RobertoBorges/GHCP-PromptMigration/compare/vscode-v0.3.1...vscode-v0.3.2) (2026-07-27)


### Documentation

* **readme:** position this tool alongside GitHub Copilot Upgrade + Azure Migrate ([9e350e3](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/9e350e3a7f74c41063972e9026464cfb2603740b))

## [0.3.1](https://github.com/RobertoBorges/GHCP-PromptMigration/compare/vscode-v0.3.0...vscode-v0.3.1) (2026-07-23)


### Bug Fixes

* **ci:** produce two clean artifacts (agent content pack + .vsix) and slim the extension ([1843dbb](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/1843dbb5a5a0195d48a43fedbb3cd4ae64e6d6d2))
* **icon:** rename extension icon AMS -&gt; AMA to match new name ([5b61a14](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/5b61a14131ac7ef6dad598cb2aca821a14786cad))


### Documentation

* **readme:** update both READMEs with accurate counts + prominent language coverage ([b9495bb](https://github.com/RobertoBorges/GHCP-PromptMigration/commit/b9495bb0160884a337da2ad5c5443975cb592883))

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
- **Wave H Decision Hardstop Protocol** (all of it): `migration-decisions/references/decision-hardstop.md`, `migration-decisions/references/decision-catalog.md`, `migration-decisions/references/decisions-required-template.md`, `decision-gates.md`, the injectors, the validator.
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
