# Quickstart in VS Code

> **Get from "never heard of Azure Migration Squad" to "running your first `/assess-any-application`" in under 2 minutes.**

There are **two ways** to use Azure Migration Squad in VS Code:

| Path | Best for | What you install |
|------|----------|------------------|
| 🚀 **Extension** (recommended) | Anyone using VS Code | One marketplace install — get sidebar, status bar, and Command Palette commands |
| 💻 **CLI only** | Teams who prefer terminal-first workflows or who use Copilot CLI primarily | `npm install -g` once, then `ams init` per project |

This guide covers both. Pick one.

---

## Path 1 — VS Code extension (easiest)

### Prerequisites (one-time)

| Tool | Why | How |
|------|-----|-----|
| **VS Code** ≥ 1.85 | The extension runs here | https://code.visualstudio.com |
| **Node.js** ≥ 20 | The CLI runs in Node under the hood | https://nodejs.org |
| **GitHub Copilot Chat** | Slash commands (`/assess-any-application`) work here | The extension offers to install it for you |

### Step 1 — Install the extension

1. Open VS Code
2. **`Ctrl+Shift+X`** → search **"Azure Migration Squad"**
3. Click **Install** on the entry by `robertoborges`

   *Or install from CLI:*

   ```bash
   code --install-extension robertoborges.azure-migration-squad-vscode
   ```

4. Reload VS Code if prompted

### Step 2 — Open your project

Open the folder you want to migrate. The extension activates automatically and shows a friendly welcome notification:

> 👋 Welcome to Azure Migration Squad! Want to set up the migration agents in this workspace?
> [Get started] [Show welcome page] [Not now] [Don't show again]

Click **Get started**.

### Step 3 — Watch it set up your workspace

The extension runs `npx @robertoborges/azure-migration-squad init` in your project. After ~30 seconds (longer on first run while npm fetches the package), you'll have:

- `.github/prompts/` — 26 slash commands
- `.github/skills/` — 60+ migration skills
- `.squad/agents/` — 15 specialist charters
- `MIGRATION-START-HERE.md` — your 60-second quickstart

A notification offers to open the welcome doc — click **Open**.

### Step 4 — Run Discovery

In **Copilot Chat** (open with `Ctrl+Alt+I`):

```
/assess-any-application
```

The **Discovery Engineer (Saul Bloom Jr.)** interviews you about your application's source, stack, and workload, then produces a Capability Matrix the rest of the squad consumes.

### Step 5 — Explore the sidebar 🚀

Look for the **rocket icon** in the Activity Bar (left edge of VS Code). Open it to see:

- **Agents** — 15 specialist charters (click to read each)
- **Prompts** — 26 prompts with their descriptions
- **Skills** — 60+ migration skills

The **status bar** (bottom-left) shows your current migration phase. Click it to jump to the next recommended action.

---

## Path 2 — CLI only

### Prerequisites

| Tool | Why |
|------|-----|
| Node.js ≥ 20 | Runs `ams` |
| [Squad CLI](https://github.com/bradygaster/squad) | Base framework AMS extends |

### Install

```bash
# 1. Squad (one-time, global)
npm install -g @bradygaster/squad-cli

# 2. Initialize Squad in your project
cd your-project
squad init

# 3. Add the Azure Migration Squad
npx @robertoborges/azure-migration-squad@latest init

# Optional: install globally for the `ams` shortcut
npm install -g @robertoborges/azure-migration-squad@latest
ams doctor
```

### Daily use

```bash
ams init           # add squad to a new repo
ams doctor         # verify install
ams list           # show all agents/prompts/skills
ams upgrade        # pull latest version
ams telemetry off  # opt out of anonymous data
```

In Copilot Chat or Copilot CLI:

```
/assess-any-application          ← VS Code Copilot Chat (slash command)
assess this application          ← Copilot CLI (natural language, slash commands aren't supported)
```

---

## Which approach should I pick?

| Question | Answer |
|----------|--------|
| "I want zero terminal commands." | **Extension.** |
| "I want a sidebar that lists everything." | **Extension.** |
| "I want a status bar showing what phase I'm in." | **Extension.** |
| "I'm scripting this in CI." | **CLI.** |
| "I prefer Copilot CLI (terminal) over Copilot Chat." | **CLI.** |
| "I want both." | Install both — they share state via the same `.azure-migration-squad/manifest.json`. |

---

## Common tasks

### Open the prompt catalog

- **Extension:** Command Palette → "Azure Migration: Show prompt catalog"
- **CLI:** open `MIGRATION-START-HERE.md` in your project root

### Update to the newest squad

- **Extension:** Command Palette → "Azure Migration: Upgrade to latest version"
- **CLI:** `ams upgrade`

### Check install health

- **Extension:** Command Palette → "Azure Migration: Run health check (doctor)"
- **CLI:** `ams doctor`

### Switch to insider builds

- **Extension:** Settings → Extensions → Azure Migration Squad → Channel → `insider`
- **CLI:** `npm install -g @robertoborges/azure-migration-squad@insider`

### Opt in to anonymous telemetry

- **Extension:** Settings → `azureMigrationSquad.telemetry.enabled` → `true`
- **CLI:** `ams telemetry on`

(Telemetry is **off by default** in both. We never collect file paths, code, or personal data. Full policy: [docs/telemetry.md](./telemetry.md).)

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Slash commands don't show in Copilot Chat | **Reload VS Code window** (`Ctrl+Shift+P` → "Developer: Reload Window") |
| Welcome notification keeps showing every time | Click **"Don't show again"** — it persists per workspace |
| Status bar doesn't update | The status bar polls `manifest.json` + `reports/`. Try `Azure Migration: Refresh` from the Command Palette |
| Sidebar shows "Not installed" | Click the entry — it offers to run Initialize |
| Tree views are empty after init | Reload VS Code window OR click the refresh button on each tree title |
| Init fails with "no squad detected" | Run `squad init` first: `npx @bradygaster/squad-cli init` |
| `npx` not found | Install Node.js: https://nodejs.org |

---

## Next steps

After your first migration:

- Read `MIGRATION-START-HERE.md` (in your project root) for the full prompt catalog
- Browse `.squad/agents/<name>/charter.md` files to understand each specialist's role
- Try `Phase 0 (Multi-repo)`, `Portfolio Strategy`, or `Database Migration` prompts for advanced scenarios
- Star the [GitHub repo](https://github.com/RobertoBorges/GHCP-PromptMigration) to follow updates

Happy migrating! 🚀
