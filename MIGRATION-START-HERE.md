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

## 🟢 The main path — 6 phases

**This is the migration flow.** Everything else (Discovery previews, portfolio planning, database-specific work, cost tuning, etc.) is optional and listed under **Optional add-ons** below.

Open GitHub Copilot Chat (`Ctrl+Alt+I`) and run the phases in order:

| # | Phase | Prompt | What it does |
|---|-------|--------|--------------|
| **1** | 🚀 Plan & Assess | `/Phase1-PlanAndAssess` | Interviews you about source/stack/workload, produces `reports/Application-Assessment-Report.md` + `reports/Decisions-Required.md` |
| **2** | ⚙️ Migrate Code | `/Phase2-MigrateCode` | Modernizes application code to your chosen target framework |
| **3** | 🏗️ Generate Infra | `/Phase3-GenerateInfra` | Generates Bicep or Terraform for Azure |
| **4** | ☁️ Deploy | `/Phase4-DeployToAzure` | Deploys via Azure Developer CLI (azd) |
| **5** | 🔄 Setup CI/CD | `/Phase5-SetupCICD` | Configures GitHub Actions (or Azure DevOps) |
| **6** | 📈 Post-Migration Ops | `/Phase6-PostMigrationOps` | App Insights, alerts, runbooks |

**How the phases coordinate:**

- After Phase 1, open `reports/Decisions-Required.md` — the agent listed the **major architecture decisions you must make** (target framework, database engine, hosting platform, IaC tool, etc.). Each one shows options with tradeoffs and **waits for your pick**. No silent defaults.
- Phases 2-6 **hard-stop** until each required decision is `✅ DECIDED`. The status bar (bottom-left) shows how many are still pending.
- If Phase 1 doesn't find a Discovery Dossier + Capability Matrix, it'll route you through `/assess-any-application` and `/build-migration-plan` automatically. You can also run those two separately from the add-ons list if you prefer to preview.

**That's the whole main flow.** Six commands, in order, one per phase.

---

## 🔵 Optional add-ons

These are **not part of the default flow**. Use them when you need a specific specialized task, a lightweight alternative entry point, or a utility.

### Alternative intakes

Use these instead of (or before) Phase 1 if you have a specific need:

| Prompt | Use when |
|--------|----------|
| `/assess-any-application` | You want a **standalone discovery** — produces the Capability Matrix + Discovery Dossier without committing to Phase 1's full assessment. Useful for previewing before deciding. |
| `/build-migration-plan` | You already ran `/assess-any-application` and want the migration plan + `Decisions-Required.md` split into its own step. |
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
| Status bar shows "AMS: N/M decisions pending" | Open `reports/Decisions-Required.md` and answer each PENDING decision |
| Phase 1 tells me it can't find a Discovery Dossier | Either let Phase 1 run Discovery inline, OR run `/assess-any-application` first (add-on), then re-run Phase 1 |
| "Unknown command" in Copilot CLI | Copilot CLI doesn't auto-register slash commands. Type the request in natural language: *"plan and assess this application"* |
| Want to start over | Delete `.github/agents/`, `.github/prompts/`, `.github/skills/`, `.github/chatmodes/`, `.github/hooks/`, `.github/copilot-instructions.md`, `MIGRATION-START-HERE.md` and re-run Initialize |

## Learn more

- **`.github/agents/Code-Migration-Modernization.agent.md`** — the agent's definition (read this!)
- **`.github/copilot-instructions.md`** — top-level rules for Copilot
- **`.github/skills/decision-hardstop.md`** — why the agent never decides for you
- **`.github/skills/decision-catalog.md`** — the 18 major decisions
- **[GitHub repo](https://github.com/RobertoBorges/GHCP-PromptMigration)** — source, issues, contributions

**Now go migrate something to Azure! 🚀**
