# Changelog

All notable changes to the Azure Migration Squad VS Code extension are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
