---
"azure-migration-squad-vscode": minor
---

**Phase 3: Tree view + 8 Command Palette commands**

The VS Code extension now provides a real working UX inside the editor:

### New sidebar — "Azure Migration Squad"

Adds an Activity Bar entry with a custom rocket icon. Opens to a sidebar containing 3 tree views:

- **Agents** — all 15 specialist charters from `.squad/agents/<name>/charter.md`. Click any agent to open their charter file.
- **Prompts** — all prompts from `.github/prompts/*.prompt.md`. Description from YAML frontmatter shown next to the name.
- **Skills** — all skills from `.github/skills/**/*.md`, including both flat `.md` files and `<skill>/SKILL.md` folder skills.

If AMS is not yet installed in the workspace, each tree view shows a "Not installed — click to initialize" item.

Each tree view has a refresh button in the title bar. The extension also auto-refreshes on file changes under `.squad/` and `.github/`.

### 8 new Command Palette commands

All prefixed with **"Azure Migration:"** in the palette:

| Command | What it does |
|---------|--------------|
| Initialize in this workspace | Runs `npx @robertoborges/azure-migration-squad@<channel> init` |
| Upgrade to latest version | Runs `npx ... upgrade` |
| Run health check (doctor) | Runs `npx ... doctor` |
| Open Discovery (`/assess-any-application`) | Opens Copilot Chat with the slash command pre-filled (falls back to clipboard if Chat APIs aren't available) |
| Show prompt catalog | Opens `MIGRATION-START-HERE.md` in markdown preview |
| Open settings | Jumps to VS Code Settings filtered to this extension |
| Refresh | Refreshes all three tree views |
| Hello (smoke test) | Diagnostic ping kept from Phase 2 |

### How it works

The extension shells out to `npx` for all AMS-modifying commands so the extension and the CLI share **one** source of truth. Output streams into a dedicated "Azure Migration Squad" OutputChannel. A progress notification appears while commands run.

Channel selection respects the `azureMigrationSquad.channel` setting (defaults to `latest`).

### Tests

5 headless tests passing:
- Extension is present
- Extension activates without errors
- All 9 commands are registered
- Hello smoke-test runs without throwing
- Agents tree view is registered and focusable

Now pinned to VS Code stable `1.95.0` for tests (avoids Insiders auto-update churn).

Out of scope (coming in Phases 4-6): status bar widget, settings UI contributions, first-run welcome WebView, walkthrough, Copilot Chat install prompts, marketplace publishing.
