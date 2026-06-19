# 🛬 MIGRATION-START-HERE

> **Azure Migration Squad is installed in this repo.** This file is your 60-second quickstart.
> Once you've done your first migration, feel free to delete this file (or keep it for the team).

---

## ✅ What just got installed

Your repo now has **15 specialist migration agents**, **26 prompts**, **60+ skills**, and a **Discovery-first workflow** that can migrate almost any application to Azure:

```
.github/
├── chatmodes/         ← 9 chat modes (e.g., Migration-Orchestrator)
├── prompts/           ← 26 slash commands (try /assess-any-application)
├── skills/            ← 60+ migration skills (stack/source/workload adapters)
├── hooks/             ← orchestration rules
└── copilot-instructions.md
.squad/
├── agents/            ← 15 specialist charters (Ocean's Twelve theme)
├── team.md
└── routing.md
AGENTS.md              ← Squad operating instructions
```

---

## 🚀 Your first migration in 3 steps

### Step 1 — Open GitHub Copilot Chat

> 💡 **Easiest path:** Install the [**Azure Migration Squad VS Code extension**](https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad) — it gives you a sidebar tree view, status bar, and one-click "Open Discovery" command. *(coming soon)*

- **VS Code:** `Ctrl+Shift+P` → "Reload Window", then `Ctrl+Alt+I` to open Copilot Chat
- **Copilot CLI:** `gh copilot suggest` or `gh copilot explain`

### Step 2 — Run Discovery

Type this in Copilot Chat:

```
/assess-any-application
```

The **Discovery Engineer (Saul Bloom Jr.)** will walk you through intake:
- Where does your app live? (on-prem / AWS / GCP / Oracle / VMware / K8s / repo / ZIP / mainframe)
- What stack? (.NET / Java / Python / Node.js / PHP / Ruby / Go / Perl / Rust / COBOL / Oracle Forms / PowerBuilder / Delphi-VB6 / Scala-Kotlin / C++ Windows)
- What workload pattern? (web app / API / batch job / event-driven / serverless / data pipeline / desktop / packaged / mainframe transactional)
- What integrations? What data?

Output: `reports/Discovery-Dossier.md` + `reports/Capability-Matrix.yaml` with evidence-bound confidence labels.

### Step 3 — Build the migration plan

Once discovery completes, the Architect runs:

```
/build-migration-plan
```

It reads the Capability Matrix and recommends a strategy (Rehost / Replatform / Refactor / Rearchitect / Rebuild / Retire / Retain) via the **12-branch decision tree** in `.github/skills/migration-strategy-decision-tree.md`.

Output: `reports/Migration-Plan.md` ready for executive sign-off.

---

## 🗺️ Which prompt do I use? (decision flow)

```
Do you have ONE specific app to migrate?
├─ YES, but I don't know the stack/source ──→ /assess-any-application  ⭐ START HERE
├─ YES, and I know the stack ──────────────→ /Phase1-PlanAndAssess (skip discovery)
└─ NO ↓

Do you have a PORTFOLIO of 10+ apps (CMDB / RVTools / DMA)?
├─ YES ────────────────────────────────────→ /PortfolioStrategy
└─ NO ↓

Do you have MULTIPLE REPOS that form one solution?
├─ YES ────────────────────────────────────→ /Phase0-Multi-repo-assessment
└─ NO ────────────────────────────────────→ /QuickAssessment
```

---

## 📚 Full prompt catalog

| Prompt | What it does |
|--------|-------------|
| `/assess-any-application` ⭐ | Universal intake — Discovery Engineer characterizes any app |
| `/build-migration-plan` | Architect builds a migration plan from the Capability Matrix |
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

Each prompt lives at `.github/prompts/<Name>.prompt.md` — open and read for details.

---

## 🎭 Meet the squad

Read the full team in `.squad/team.md`. Highlights:

- **Saul Bloom Jr. (Discovery Engineer)** — owns intake and the Capability Matrix
- **Danny Ocean (Architect)** — picks the target Azure architecture
- **Rusty Ryan (Coder)** — does the actual code migration
- **Basher Tarr (Azure Specialist)** — Azure services, identity, networking
- **The Amazing Yen (Database Specialist)** — schema migration, data validation
- **Frank Catton (Security Auditor)** — Entra, Key Vault, secrets, compliance

Each charter is at `.squad/agents/<name>/charter.md`.

---

## 🛠️ Useful CLI commands (if you installed globally)

```bash
ams init           # add squad to a new repo
ams doctor         # verify install (you can run this now!)
ams list           # show all agents/prompts/skills
ams upgrade        # pull the latest migration squad
ams telemetry off  # opt out of anonymous usage data
```

If you used `npx`, you can run `npx @robertoborges/azure-migration-squad@latest <command>` instead.

---

## 🆘 Troubleshooting

| Problem | Fix |
|---------|-----|
| Slash commands don't show in Copilot Chat | **Reload VS Code window** (`Ctrl+Shift+P` → "Developer: Reload Window") |
| "Unknown command" in Copilot CLI | Copilot CLI doesn't auto-register slash commands. Type the request in natural language instead: *"assess this application"* |
| Init said "no squad detected" | Run `squad init` **before** `ams init`. Squad CLI: `npm install -g @bradygaster/squad-cli` |
| Wrong agent picked up the task | Check `.squad/routing.md` and `.github/chatmodes/Migration-Orchestrator.chatmode.md` |
| Want to start over | Delete `.github/`, `.squad/`, `AGENTS.md`, `MIGRATION-START-HERE.md`, `.azure-migration-squad/` and re-run `ams init` |

---

## 📖 Where to learn more

- **Project README** — high-level overview of how everything fits together
- **`.squad/team.md`** — full squad roster + roles
- **`.github/copilot-instructions.md`** — universal mode operating rules
- **`docs/vscode-quickstart.md`** — VS Code-specific walkthrough *(coming soon)*
- **[GitHub repo](https://github.com/RobertoBorges/GHCP-PromptMigration)** — source, issues, contributions

---

## 🤝 Contributing

The Squad ships **stack/source/workload adapters** — adding support for new technologies is a 1-file change. See `docs/contributing-adapters.md`.

---

## 📊 Telemetry

Anonymous usage data (which commands ran, install count) is **off by default**.
Opt in with: `ams telemetry on` — full policy at `docs/telemetry.md`.

---

> 💡 **Pro tip:** if you're new to Squad in general (not just AMS), check the upstream framework at https://github.com/bradygaster/squad — same patterns apply.

**Now go migrate something to Azure! 🚀**
