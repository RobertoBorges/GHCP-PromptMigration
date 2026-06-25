# Changelog

All notable changes to the Azure Migration Squad VS Code extension are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] — Wave H surface: Decisions Required tree view + status bar enhancement

### Added

- **New "🛑 Decisions Required" tree view** in the sidebar (top entry, above Agents/Prompts/Skills). Reads `reports/Decisions-Required.md` and renders each major architecture decision with its current status:
  - ⏸ PENDING — needs user input (red icon)
  - ✅ DECIDED — answered (green checkmark)
  - 🔒 LOCKED — determined by another decision (blue lock)
  - 🚫 N/A — does not apply (gray slash)
  - ❓ Unknown — could not parse status (yellow)
- **Click a decision** → opens `reports/Decisions-Required.md` scrolled to that decision's section.
- **Auto-refresh on file change** (FileSystemWatcher on `**/reports/Decisions-Required.md`).
- **Status bar pending-count indicator.** When any decision is `⏸ PENDING`, the status bar widget switches from "AMS: Phase N" to **"🛑 AMS: 3/18 decisions pending"** with a warning-colored background. Click → opens the decisions file. Once all decisions are made, the widget reverts to the normal phase indicator.
- **New Command Palette commands:**
  - `Azure Migration: Show decisions required (open file)` — opens `reports/Decisions-Required.md` directly.
  - `Azure Migration: Open decision at line (internal)` — used by tree-item clicks.
- **8 new unit tests** for `decisionsParser` covering all status variants, line tracking, catalog-ID headings (`D-NN`), and empty/malformed files.
- **Placeholder states** for the new tree view:
  - "Open a folder to see decisions" — when no workspace.
  - "Click to install Azure Migration Squad here" — when AMS not installed.
  - "Run Phase 1 to generate decisions" — when AMS installed but no decisions file yet.
  - "No decisions found — re-run Phase 1?" — when file exists but unparseable.

### Why

Wave H (npm package `0.1.1.0-insider.0`) introduced the Decision Hardstop Protocol: the squad now generates `reports/Decisions-Required.md` with 18 major architecture decisions a user must answer before Phases 2-4 can run. Without surfacing this in the extension UI, users wouldn't see the new file unless they opened the file tree. With v0.1.3, the protocol is **visible at a glance**: open the sidebar, see which decisions are pending; or just look at the status bar.

### Architecture

- `src/util/decisionsParser.ts` — pure-logic markdown parser, exported types for `Decision`, `DecisionStatus`, `DecisionsFileSummary`. Tolerates emoji/no-emoji status text; supports both numeric (`1`) and catalog-ID (`D-04`) headings.
- `src/treeProviders/decisionsProvider.ts` — `TreeDataProvider` implementation. Uses theme icons + theme colors so it matches user's VS Code color scheme.
- `src/extension.ts` — registers the new tree view + FileSystemWatcher; wires `showDecisions` and `openDecisionAtLine` commands.
- `src/statusBar.ts` — pending-count check runs before phase inference; pending takes priority.

### Bundle size

`.vsix` is now 23.46 KB (up from 21 KB). esbuild bundle is 91 KB minified.

## [0.1.2] — Squad CLI integration follow-up

### Fixed

- **AMS agents weren't appearing in Copilot Chat's `@` dropdown** after `ams init`. Root cause: passing `--force` bypassed `squad init`, which is what registers agents with the Squad CLI's chat-participant registry. The agents existed on disk but Copilot Chat didn't know about them.

### Added

- **After-init follow-up flow.** When `ams init` succeeds, the extension now offers two more steps:
  1. **"Register agents with Squad CLI?"** — if `squad` is on PATH, opens a terminal with `squad init` pre-typed (not auto-executed; user reviews and presses Enter).
  2. **"Reload window?"** — VS Code only registers `.github/chatmodes/*` on workspace load, so the user needs to reload for new chatmodes to appear in Copilot Chat.
- If Squad CLI is **not** installed, the prompt becomes: "Install Squad CLI globally for @-agent dispatch?" — opens a terminal with `npm install -g @bradygaster/squad-cli` ready.
- New Command Palette entry **"Azure Migration: Register agents with Squad CLI (squad init)"** for users who skipped the prompt or want to re-register after adding custom agents.
- New setting `azureMigrationSquad.promptSquadInit` (default `true`). Disable to permanently silence the post-init Squad registration prompt — the Command Palette command remains available.

### Why this matters

The Squad CLI's @-agent integration with Copilot Chat is **not** triggered by file presence in `.squad/agents/`. It's triggered by `squad init` (or `squad agent add`). This release closes that loop without forcing every AMS user to install Squad CLI — slash-command users (`/assess-any-application` etc.) still get a full migration workflow without it.

## [0.1.1] — UX fix: no more "Squad runtime not detected" dead-end

### Fixed

- **Critical UX bug:** clicking "Azure Migration Squad not installed in this workspace" used to fail with `Squad runtime not detected in this directory` and exit 1, leaving users stuck. **Now Initialize succeeds even without Squad CLI installed** — the extension automatically passes `--force` to `ams init` when no `.squad/` directory is present. AMS bundles everything Copilot Chat needs (prompts, skills, chatmodes, agent charters) so a separate Squad CLI install isn't required.

### Added

- **`src/util/squadDetection.ts`** — detects Squad runtime state in 4 buckets:
  - `no-squad` — no `.squad/` here, no global `squad` binary → AMS init runs with `--force`
  - `cli-available` — global `squad` installed, but `.squad/` not yet here → AMS init runs with `--force`
  - `squad-initialized` — `.squad/` exists → AMS init runs cleanly
  - `ams-installed` — `.azure-migration-squad/manifest.json` exists → upgrade flow suggested
- **New optional command** `Azure Migration: Install Squad CLI globally (optional)` — opens a terminal pre-filled with `npm install -g @bradygaster/squad-cli` for power users who want it. Skipping this is fine.
- **Output channel now tells the user what's happening** — when `--force` is in play, the channel explains why and links to the optional global install command.
- **4 new unit tests** for `argsForAmsInit` covering each state transition.

### Changed

- Tree-view "Not installed" item: label updated from "Azure Migration Squad not installed in this workspace" → **"Click to install Azure Migration Squad here"**. Icon changed from ⚠️ warning to 🚀 rocket. Tooltip clarifies that Squad CLI is NOT required.

### Why this happened

The original implementation called `npx ams init` with no flags, which triggered the CLI's built-in Squad runtime guard. That guard makes sense for CLI users (it nudges them to set up Squad first), but in VS Code we already have full context — the user is using the extension, they want it to just work. The AMS templates include the entire `.squad/agents/` charter tree, so passing `--force` produces a fully-functional setup without requiring two separate global installs.

## [0.1.0] — Wave G v1 (initial marketplace release)

First marketplace release. Ships the full v1 feature set built across Phases 2-6 of Wave G.

### Added — Tree views (Phase 3)
- New "Azure Migration Squad" Activity Bar entry with a custom rocket icon
- Three tree views:
  - **Agents** — 15 specialist charters from `.squad/agents/<name>/charter.md`
  - **Prompts** — 26 prompts from `.github/prompts/*.prompt.md` (description from YAML frontmatter)
  - **Skills** — 60+ skills from `.github/skills/**/*.md` (flat files + `SKILL.md` folder skills)
- Click any item to open its source file
- "Not installed — click to initialize" item when AMS isn't present
- Auto-refresh on file changes under `.squad/` and `.github/`
- Refresh button on each tree title bar

### Added — Status bar (Phase 4)
- Dedicated status bar widget on bottom-left showing current migration phase
- Phase inferred from filesystem state: not-installed → discovery → phase-1 → … → phase-6 → complete
- Click the widget to jump to the next recommended action
- Auto-refreshes when `manifest.json` or `reports/*.md` change
- Can be disabled via `azureMigrationSquad.statusBar.enabled`

### Added — Settings UI (Phase 4)
Five settings under VS Code Settings → Extensions → Azure Migration Squad:
- `azureMigrationSquad.channel` (`latest` | `insider`) — npm dist-tag
- `azureMigrationSquad.telemetry.enabled` (default `false`) — opt-in usage data
- `azureMigrationSquad.language` (`en` | `pt-BR` | `es-ES`) — content language
- `azureMigrationSquad.autoInstallCopilot` (`prompt` | `auto` | `never`) — Copilot Chat install behavior
- `azureMigrationSquad.statusBar.enabled` (default `true`) — toggle phase widget

### Added — Welcome experience (Phase 5)
- First-run notification on activation in workspaces without AMS installed
- WebView welcome panel themed with VS Code CSS variables (4 feature cards, 3-step quickstart, action buttons)
- VS Code Walkthrough contribution (4 steps with completion tracking)
- Auto-prompt to install `GitHub.copilot-chat` (respects `autoInstallCopilot` setting)

### Added — Commands (Phases 3 + 5)
Eleven commands prefixed "Azure Migration:" in the Command Palette:
- Initialize in this workspace
- Upgrade to latest version
- Run health check (doctor)
- Open Discovery (`/assess-any-application`)
- Show prompt catalog
- Open settings
- Refresh
- Show welcome page
- Install GitHub Copilot Chat
- Hello (smoke test)
- Open file (internal)

### Architecture
- All AMS-modifying commands shell out to `npx @robertoborges/azure-migration-squad@<channel>` — single source of truth shared with the CLI
- Output streams to a dedicated "Azure Migration Squad" OutputChannel
- Progress notifications during long-running commands
- TypeScript + esbuild bundle (~30 KB), CJS, Node 20 target

### Testing
- `@vscode/test-electron` headless test runner
- Pinned VS Code stable 1.95.0 (avoids Insiders auto-update issues)
- 5 tests covering activation, command registration, tree view registration

### Publishing
- Marketplace listing with placeholder icon (replace before launch)
- `.github/workflows/release-vscode-extension.yml` — automated publish to VS Code Marketplace + Open VSX Registry
- Trigger via tag push (`vscode-vX.Y.Z`) or manual workflow_dispatch (with dry-run option)
- Full setup docs in `docs/publishing-vscode-extension.md`

## [0.0.0] — Phase 2 scaffold (unpublished)

Internal milestone. Established TypeScript + esbuild + test-electron foundation.
Never published — superseded by 0.1.0.


### Added — Tree views (Phase 3)
- New "Azure Migration Squad" Activity Bar entry with a custom rocket icon
- Three tree views:
  - **Agents** — 15 specialist charters from `.squad/agents/<name>/charter.md`
  - **Prompts** — 26 prompts from `.github/prompts/*.prompt.md` (description from YAML frontmatter)
  - **Skills** — 60+ skills from `.github/skills/**/*.md` (flat files + `SKILL.md` folder skills)
- Click any item to open its source file
- "Not installed — click to initialize" item when AMS isn't present
- Auto-refresh on file changes under `.squad/` and `.github/`
- Refresh button on each tree title bar

### Added — Status bar (Phase 4)
- Dedicated status bar widget on bottom-left showing current migration phase
- Phase inferred from filesystem state: not-installed → discovery → phase-1 → … → phase-6 → complete
- Click the widget to jump to the next recommended action
- Auto-refreshes when `manifest.json` or `reports/*.md` change
- Can be disabled via `azureMigrationSquad.statusBar.enabled`

### Added — Settings UI (Phase 4)
Five settings under VS Code Settings → Extensions → Azure Migration Squad:
- `azureMigrationSquad.channel` (`latest` | `insider`) — npm dist-tag
- `azureMigrationSquad.telemetry.enabled` (default `false`) — opt-in usage data
- `azureMigrationSquad.language` (`en` | `pt-BR` | `es-ES`) — content language
- `azureMigrationSquad.autoInstallCopilot` (`prompt` | `auto` | `never`) — Copilot Chat install behavior
- `azureMigrationSquad.statusBar.enabled` (default `true`) — toggle phase widget

### Added — Welcome experience (Phase 5)
- First-run notification on activation in workspaces without AMS installed
- WebView welcome panel themed with VS Code CSS variables (4 feature cards, 3-step quickstart, action buttons)
- VS Code Walkthrough contribution (4 steps with completion tracking)
- Auto-prompt to install `GitHub.copilot-chat` (respects `autoInstallCopilot` setting)

### Added — Commands (Phases 3 + 5)
Eleven commands prefixed "Azure Migration:" in the Command Palette:
- Initialize in this workspace
- Upgrade to latest version
- Run health check (doctor)
- Open Discovery (`/assess-any-application`)
- Show prompt catalog
- Open settings
- Refresh
- Show welcome page
- Install GitHub Copilot Chat
- Hello (smoke test)
- Open file (internal)

### Architecture
- All AMS-modifying commands shell out to `npx @robertoborges/azure-migration-squad@<channel>` — single source of truth shared with the CLI
- Output streams to a dedicated "Azure Migration Squad" OutputChannel
- Progress notifications during long-running commands
- TypeScript + esbuild bundle (~30 KB), CJS, Node 20 target

### Testing
- `@vscode/test-electron` headless test runner
- Pinned VS Code stable 1.95.0 (avoids Insiders auto-update issues)
- 5 tests covering activation, command registration, tree view registration

### Publishing
- Marketplace listing with placeholder icon (replace before launch)
- `.github/workflows/release-vscode-extension.yml` — automated publish to VS Code Marketplace + Open VSX Registry
- Trigger via tag push (`vscode-vX.Y.Z`) or manual workflow_dispatch (with dry-run option)
- Full setup docs in `docs/publishing-vscode-extension.md`

## [0.0.0] — Phase 2 scaffold (unpublished)

Internal milestone. Established TypeScript + esbuild + test-electron foundation.
Never published — superseded by 0.1.0.
