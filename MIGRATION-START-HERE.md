# 🛬 Welcome — Azure Migration Agent

> **The Azure Migration Agent is installed in this workspace.** This file is your 60-second quickstart.

## What just got installed

```
.github/
├── agents/Code-Migration-Modernization.agent.md   ← The agent definition
├── prompts/                                          ← 19 slash commands
├── skills/                                           ← 113 stack/source/workload adapters
├── chatmodes/                                        ← 8 Copilot Chat modes
├── hooks/                                            ← Phase gates + decision protocol
└── copilot-instructions.md                           ← Top-level rules
```

---

## 🟢 The main path — Assess + 6 phases

**This is the migration flow.** Everything else (portfolio planning, database-specific work, cost tuning, etc.) is optional and listed under **Optional add-ons** below.

Open GitHub Copilot Chat (`Ctrl+Alt+I`) and run these commands in order:

| # | Step | Prompt | What it does |
|---|------|--------|--------------|
| **1** | 🔍 Assess | `/assess-any-application` | Discovery — interviews you about source/stack/workload/data/integrations, produces `reports/Discovery-Dossier.md` + `reports/Capability-Matrix.yaml` |
| **2** | 🚀 Plan | `/Phase1-Plan` | Reads the Capability Matrix; produces `reports/Application-Assessment-Report.md`, `reports/Migration-Plan.md`, and `reports/Decisions-Required.md` |
| **3** | ⚙️ Migrate Code | `/Phase2-MigrateCode` | Modernizes application code to your chosen target framework |
| **4** | 🏗️ Generate Infra | `/Phase3-GenerateInfra` | Generates Bicep or Terraform for Azure |
| **5** | ☁️ Deploy | `/Phase4-DeployToAzure` | Deploys via Azure Developer CLI (azd) |
| **6** | 🔄 Setup CI/CD | `/Phase5-SetupCICD` | Configures GitHub Actions (or Azure DevOps) |
| **7** | 📈 Post-Migration Ops | `/Phase6-PostMigrationOps` | App Insights, alerts, runbooks |

**How the phases coordinate:**

- After Phase 1, open `reports/Decisions-Required.md` — the agent listed the **major architecture decisions you must make** (target framework, database engine, hosting platform, IaC tool, etc.). Each one shows options with tradeoffs and **waits for your pick**. No silent defaults.
- Phases 2-6 **hard-stop** until each required decision is `✅ DECIDED`. The status bar (bottom-left) shows how many are still pending.

**That's the whole main flow.** Seven commands, in order.

---

## 🔵 Optional add-ons

These are **not part of the default flow**. Use them when you need a specific specialized task, a lightweight alternative entry point, or a utility.

### Alternative intakes

Use these instead of (or before) the main path if you have a specific need:

| Prompt | Use when |
|--------|----------|
| `/build-migration-plan` | You ran `/assess-any-application` and want the migration plan + `Decisions-Required.md` split into its own step, before running `/Phase1-Plan`. |
| `/QuickAssessment` | You already know the basics — fast triage without the full interview. |
| `/QuickTriage` | You want the agent to suggest the next migration step in **under 5 minutes**. |
| `/InteractiveMigrationInterview` | You'd like a **guided Q&A** rather than free-form intake. |
| `/TeamSkillAssessment` | You want to audit your team's readiness for the migration (skills gap analysis). |

### Portfolio / multi-app

| Prompt | Use when |
|--------|----------|
| `/PortfolioStrategy` | You have **10+ apps** (from CMDB / RVTools / DMA) and need an executive CIO deck classifying each app. Runs before per-app work. |
| `/Phase0-Multi-repo-assessment` | You have **multiple repos that form ONE business solution** and need cross-repo dependency + sequencing analysis before Phase 1. |

### Specialized deep-dives

Use during or between phases when a specific concern needs focused work:

| Prompt | Use when |
|--------|----------|
| `/DatabaseMigration` | You need a focused **schema + data move** plan using Azure DMS / DMA. |
| `/SecurityHardening` | You want a dedicated pass on **Entra ID, Key Vault, managed identity, and network security**. |
| `/CostOptimization` | You want **right-sizing, savings plans, and budget setup** for the migrated workload. |

### Utility / recovery

| Prompt | Use when |
|--------|----------|
| `/Phase-Rollback` | You need to **rollback an in-flight migration** to a safe state. |
| `/GetStatus` | You want to see the **current migration progress** at a glance. |

---

## Useful extension commands

`Ctrl+Shift+P` → type **"Azure Migration:"**:

- Initialize in this workspace
- Upgrade to latest version
- Run health check (doctor)
- Open Discovery (`/assess-any-application`)
- Show prompt catalog (this file)
- Show decisions required

Or use the sidebar: rocket icon 🚀 in the Activity Bar shows Agent, Main path, Add-ons, and Decisions.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Slash commands don't show in Copilot Chat | **Reload VS Code window** (`Ctrl+Shift+P` → "Developer: Reload Window") |
| Status bar shows "AMA: N/M decisions pending" | Open `reports/Decisions-Required.md` and answer each PENDING decision |
| `/Phase1-Plan` tells me it can't find a Discovery Dossier | Run `/assess-any-application` first (that's step 1 of the main path) |
| "Unknown command" in Copilot CLI | Copilot CLI doesn't auto-register slash commands. Type the request in natural language: *"assess this application"* / *"plan this migration"* |
| Want to start over | Delete `.github/agents/`, `.github/prompts/`, `.github/skills/`, `.github/chatmodes/`, `.github/hooks/`, `.github/copilot-instructions.md`, `MIGRATION-START-HERE.md` and re-run Initialize |

## Learn more

- **`.github/agents/Code-Migration-Modernization.agent.md`** — the agent's definition (read this!)
- **`.github/copilot-instructions.md`** — top-level rules for Copilot
- **`.github/skills/decision-hardstop.md`** — why the agent never decides for you
- **`.github/skills/decision-catalog.md`** — the 18 major decisions
- **[GitHub repo](https://github.com/RobertoBorges/GHCP-PromptMigration)** — source, issues, contributions

**Now go migrate something to Azure! 🚀**
