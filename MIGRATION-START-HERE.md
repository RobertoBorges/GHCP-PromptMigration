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

## Your first migration in 3 steps

### 1. Open GitHub Copilot Chat
`Ctrl+Alt+I` (or `gh copilot suggest` in terminal)

### 2. Run Discovery
```
/assess-any-application
```
The agent interviews you about source/stack/workload/data/integrations and produces `reports/Discovery-Dossier.md` + `reports/Capability-Matrix.yaml`.

### 3. Build the plan + answer the decisions
```
/build-migration-plan
```
Produces `reports/Migration-Plan.md` and **`reports/Decisions-Required.md`** — a list of major architecture decisions YOU need to answer before Phases 2-6 can run:

- Target framework version
- UI architecture
- Database engine
- Hosting platform
- IaC tool
- ...and 13 more

The agent **shows options + tradeoffs** for each one and waits for your pick. No silent defaults.

Then run Phase 2 onward:
```
/Phase2-MigrateCode
/Phase3-GenerateInfra
/Phase4-DeployToAzure
/Phase5-SetupCICD
/Phase6-PostMigrationOps
```

## Full prompt catalog

| Prompt | What it does |
|--------|-------------|
| `/assess-any-application` ⭐ | Universal intake — characterize any app |
| `/build-migration-plan` | Build the migration plan + Decisions-Required from Capability Matrix |
| `/QuickAssessment` | Fast triage when you already know the basics |
| `/QuickTriage` | Suggest the next migration step in <5 minutes |
| `/InteractiveMigrationInterview` | Guided Q&A intake |
| `/TeamSkillAssessment` | Audit your team's readiness |
| `/PortfolioStrategy` | Executive CIO deck for 10+ apps |
| `/Phase0-Multi-repo-assessment` | Map multi-repo business solutions |
| `/Phase1-PlanAndAssess` | Plan + per-app assessment |
| `/Phase2-MigrateCode` | Modernize code to target framework |
| `/Phase3-GenerateInfra` | Generate Bicep / Terraform |
| `/Phase4-DeployToAzure` | Deploy to Azure (azd) |
| `/Phase5-SetupCICD` | GitHub Actions for the migrated app |
| `/Phase6-PostMigrationOps` | App Insights, alerts, runbooks |
| `/Phase-Rollback` | Rollback an in-flight migration |
| `/DatabaseMigration` | Schema + data move (DMS / DMA) |
| `/SecurityHardening` | Entra ID, Key Vault, managed identity |
| `/CostOptimization` | Right-sizing, savings plans, budgets |
| `/GetStatus` | Show current migration progress |

Each prompt lives at `.github/prompts/<Name>.prompt.md`.

## Useful extension commands

`Ctrl+Shift+P` → type **"Azure Migration:"**:

- Initialize in this workspace
- Upgrade to latest version
- Run health check (doctor)
- Open Discovery (`/assess-any-application`)
- Show prompt catalog (this file)
- Show decisions required

Or use the sidebar: rocket icon 🚀 in the Activity Bar shows Agent, Prompts, Skills, Decisions.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Slash commands don't show in Copilot Chat | **Reload VS Code window** (`Ctrl+Shift+P` → "Developer: Reload Window") |
| Status bar shows "AMS: N/M decisions pending" | Open `reports/Decisions-Required.md` and answer each PENDING decision |
| "Unknown command" in Copilot CLI | Copilot CLI doesn't auto-register slash commands. Type the request in natural language: *"assess this application"* |
| Want to start over | Delete `.github/agents/`, `.github/prompts/`, `.github/skills/`, `.github/chatmodes/`, `.github/hooks/`, `.github/copilot-instructions.md`, `MIGRATION-START-HERE.md` and re-run Initialize |

## Learn more

- **`.github/agents/Code-Migration-Modernization.agent.md`** — the agent's definition (read this!)
- **`.github/copilot-instructions.md`** — top-level rules for Copilot
- **`.github/skills/decision-hardstop.md`** — why the agent never decides for you
- **`.github/skills/decision-catalog.md`** — the 18 major decisions
- **[GitHub repo](https://github.com/RobertoBorges/GHCP-PromptMigration)** — source, issues, contributions

**Now go migrate something to Azure! 🚀**
