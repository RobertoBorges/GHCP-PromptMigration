# Azure Migration Agent — VS Code quickstart

> Get from "never heard of the agent" to running your first migration in under 2 minutes.

## Prerequisites (one-time)

| Tool | Why | How |
|------|-----|-----|
| **VS Code** ≥ 1.85 | The extension runs here | https://code.visualstudio.com |
| **GitHub Copilot Chat** extension | Slash commands (`/assess-any-application`) work here | The extension offers to install it for you |

Note: **Node.js is NOT required** to run the extension. It bundles all migration content internally.

## Step 1 — Install the extension

1. Open VS Code
2. `Ctrl+Shift+X` → search **"Azure Migration Agent"**
3. Click **Install** on the entry by `robertoborges`

   *Or from CLI:*

   ```bash
   code --install-extension robertoborges.azure-migration-squad-vscode
   ```

4. Reload VS Code if prompted.

## Step 2 — Open your project

Open the folder you want to migrate. The extension activates automatically and shows:

> 👋 Welcome to the Azure Migration Agent! Want to set up the migration workflow in this workspace?
> [Get started] [Show welcome page] [Not now] [Don't show again]

Click **Get started**.

## Step 3 — Watch it set up your workspace

The extension copies bundled templates into your project. After a few seconds you'll have:

- `.github/agents/Code-Migration-Modernization.agent.md` — the agent definition
- `.github/prompts/` — 19 slash commands
- `.github/skills/` — 113 stack/source/workload adapters
- `.github/chatmodes/` — 8 specialized chat modes
- `.github/hooks/` — orchestration rules + Wave H decision protocol
- `.github/copilot-instructions.md` — top-level rules for Copilot
- `MIGRATION-START-HERE.md` — your 60-second quickstart at the project root

A notification offers to open the welcome doc — click **Open**.

A second notification offers to **reload the VS Code window** so Copilot Chat picks up the new prompts and chatmodes. Click **Reload**.

## Step 4 — Run the main path — Step 1: Discovery

In **Copilot Chat** (open with `Ctrl+Alt+I`):

```
/assess-any-application
```

The agent interviews you about source, stack, workload, data, and integrations. It produces:

- `reports/Discovery-Dossier.md` — narrative + evidence
- `reports/Capability-Matrix.yaml` — structured classification

## Step 5 — Run the main path — Step 2: Plan

```
/Phase1-Plan
```

Phase 1 reads the Capability Matrix and produces:

- `reports/Application-Assessment-Report.md` — the per-app assessment
- `reports/Migration-Plan.md` — the migration plan (if not already produced via `/build-migration-plan`)
- `reports/Decisions-Required.md` — **major architecture decisions you need to answer** before later phases can run

## Step 6 — Answer the decisions

Open `reports/Decisions-Required.md`. For each decision (Target framework, Database engine, Hosting platform, IaC tool, etc.), the agent shows options + tradeoffs. Pick one and fill in your rationale.

The **status bar** (bottom-left) shows **"⚠ AMA: N/M decisions pending"** with a warning background until all are answered.

The **🛑 Decisions Required tree view** in the sidebar (rocket icon 🚀 in the Activity Bar) shows each decision's status. Click any entry to jump to that section of the file.

## Step 7 — Run Phase 2 through Phase 6

Once all required decisions are `✅ DECIDED`:

```
/Phase2-MigrateCode
/Phase3-GenerateInfra
/Phase4-DeployToAzure
/Phase5-SetupCICD
/Phase6-PostMigrationOps
```

Each phase **hard-stops** if any decision it depends on is still `⏸ PENDING`. The agent will tell you which decisions block its work.

## Optional add-ons

These are **not part of the default flow**. Use them when you need a specific specialized task:

- **Alternative intakes:** `/build-migration-plan`, `/QuickAssessment`, `/QuickTriage`, `/InteractiveMigrationInterview`, `/TeamSkillAssessment`
- **Portfolio / multi-app:** `/PortfolioStrategy`, `/Phase0-Multi-repo-assessment`
- **Specialized deep-dives:** `/DatabaseMigration`, `/SecurityHardening`, `/CostOptimization`
- **Utility / recovery:** `/Phase-Rollback`, `/GetStatus`

## Useful Command Palette commands

`Ctrl+Shift+P` → type **"Azure Migration:"**:

| Command | What |
|---------|------|
| Initialize in this workspace | Bundle the agent + content into the project |
| Upgrade to latest version | Overwrite with the latest extension contents |
| Run health check (doctor) | Verify install + show extension version |
| Open Discovery (`/assess-any-application`) | Jump-start the agent in Copilot Chat |
| Show prompt catalog | Open MIGRATION-START-HERE.md |
| Show decisions required | Open `reports/Decisions-Required.md` |
| Install GitHub Copilot Chat | If you don't have it yet |
| Show welcome page | The WebView welcome panel |
| Refresh | Refresh the sidebar trees |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Slash commands don't show in Copilot Chat | **Reload VS Code window** (`Ctrl+Shift+P` → "Developer: Reload Window") |
| Welcome notification keeps showing every time | Click **"Don't show again"** — it persists per workspace |
| Status bar shows "AMA: N/M decisions pending" | Open `reports/Decisions-Required.md` and answer each PENDING decision |
| Sidebar shows "Click to install Azure Migration Agent here" | Click the entry — it runs Initialize |
| Tree views are empty after init | Reload VS Code window OR click the refresh button on each tree title |

## Settings

`Ctrl+,` → search **"Azure Migration"**:

| Setting | Default | Description |
|---------|---------|-------------|
| `azureMigrationSquad.autoInstallCopilot` | `prompt` | `prompt` / `auto` / `never` — Copilot Chat install behavior |
| `azureMigrationSquad.statusBar.enabled` | `true` | Show migration phase + pending decisions in the status bar |

## Next steps

- Read `.github/agents/Code-Migration-Modernization.agent.md` to understand the agent's responsibilities
- Read `.github/skills/decision-hardstop.md` to understand why the agent never decides for you
- Read `.github/skills/decision-catalog.md` to see all 18 major decisions
- Star the [GitHub repo](https://github.com/RobertoBorges/GHCP-PromptMigration) for updates

Happy migrating! 🚀
