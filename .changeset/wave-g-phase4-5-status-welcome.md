---
"azure-migration-squad-vscode": minor
---

**Phase 4 + 5: Status bar, settings UI, welcome panel, walkthrough, Copilot install**

The extension is now feature-complete for v1. What's new:

### Phase 4 — Status bar widget

A dedicated status bar entry on the bottom-left shows your current migration phase:

| Icon | Label | When |
|------|-------|------|
| ⚠️ | AMS: not installed | No manifest.json present |
| 🔍 | AMS: Discovery | Capability-Matrix.yaml present |
| 🌳 | AMS: Phase 1 — Plan | Migration-Plan.md present |
| 📝 | AMS: Phase 2 — Migrate | Code-Migration-Plan.md present |
| 🖥️ | AMS: Phase 3 — Infra | Infrastructure-Plan.md present |
| 🚀 | AMS: Phase 4 — Deploy | Deployment-Report.md present |
| ⚙️ | AMS: Phase 5 — CI/CD | CICD-Setup.md present |
| 💓 | AMS: Phase 6 — Ops | Operations-Runbook.md present |
| ✅ | AMS: Complete | Phase-6-PostMigrationOps.md present |

Click the widget to jump to the next recommended action (Initialize / Open Discovery / Show Catalog).

Auto-refreshes when manifest.json or anything in `reports/` changes. Can be disabled via `azureMigrationSquad.statusBar.enabled`.

### Phase 4 — Settings UI contributions

5 settings now appear under VS Code Settings → Extensions → Azure Migration Squad:

| Setting | Default | Description |
|---------|---------|-------------|
| `azureMigrationSquad.channel` | `latest` | npm dist-tag (`latest` or `insider`) used by all CLI commands |
| `azureMigrationSquad.telemetry.enabled` | `false` | Opt-in anonymous usage data |
| `azureMigrationSquad.language` | `en` | Migration content language (`en`, `pt-BR`, `es-ES`) |
| `azureMigrationSquad.autoInstallCopilot` | `prompt` | `auto`/`prompt`/`never` for Copilot Chat install offers |
| `azureMigrationSquad.statusBar.enabled` | `true` | Show migration phase in status bar |

### Phase 5 — First-run welcome experience

The first time the extension activates in a workspace **without** AMS installed, the user sees a friendly notification:

> 👋 Welcome to Azure Migration Squad! Want to set up the migration agents in this workspace?
> [Get started] [Show welcome page] [Not now] [Don't show again]

"Get started" runs `Initialize` immediately. "Show welcome page" opens a polished WebView panel (themed to VS Code colors) with:
- 4 feature cards: 15 agents, universal sources, all stacks, Discovery-first
- 3-step quickstart with kbd shortcuts
- One-click buttons: Initialize, Install Copilot Chat, Show prompt catalog, Open settings

### Phase 5 — VS Code Walkthrough contribution

A 4-step walkthrough appears in **Help → Get Started** and after extension install:
1. Initialize the migration squad
2. Install GitHub Copilot Chat
3. Run Discovery
4. Explore the sidebar

Each step has a completion event so the walkthrough tracks progress automatically.

### Phase 5 — Copilot Chat auto-install (with consent)

When the extension detects `GitHub.copilot-chat` is missing, it honors the `azureMigrationSquad.autoInstallCopilot` setting:
- **`prompt`** (default): one notification per workspace with [Install] / [Not now] / [Don't ask again]
- **`auto`**: install silently
- **`never`**: do nothing

"Don't ask again" persists the setting to `never` so the prompt stays gone.

### New commands

- `Azure Migration: Show welcome page` — opens the WebView panel any time
- `Azure Migration: Install GitHub Copilot Chat` — runs the install flow on demand

### Tests

All 5 tests still passing in headless VS Code 1.95.0. The expanded command list (11 commands now) is verified.

Out of scope (Phase 6 only): marketplace publishing automation, real icon + screenshots, full docs refresh.
