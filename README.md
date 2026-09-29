# Azure Migration Agent — GitHub Copilot agent skills for Azure migration

> **Migrate any application to Azure** using 36 agent skills and 8 custom agents — of which you only ever pick from **three**: migrate, assess, or debug. Universal source/stack/workload coverage. Discovery-first. The agent **never decides major architecture for you** — it lays out options and waits.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/robertoborges.azure-migration-squad-vscode?label=VS%20Code%20Marketplace&color=blueviolet&logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository is the canonical source for the **Azure Migration Agent** (`.github/agents/Code-Migration-Modernization.agent.md`) and its supporting agent skills, custom agents, and hooks.

## Supported languages, frameworks, and platforms

**Not just .NET and Java.** The agent handles any application in any of these stacks — each with a dedicated adapter file covering framework detection, Azure hosting targets, effort sizing, and common blockers:

| Category | Coverage |
|----------|----------|
| **Languages / frameworks (15 stack adapters)** | `.NET` (Framework 2.x → 10 LTS), `Java` (8/11 → 17/21 LTS + Spring Boot 3.x), `Python` (2.x → 3.12+, Django/Flask/FastAPI), `Node.js` (12/14/16 → 20/22 LTS, Express/NestJS/Next), `PHP` (5.x/7.x → 8.3+, Laravel/Symfony), `Ruby` (2.x → 3.3+, Rails), `Go` (≤ 1.19 → 1.22+), `Perl` (5.x), `Rust` (edition upgrades), `Scala/Kotlin`, `Oracle Forms` (→ APEX / Spring Boot rewrite), `PowerBuilder`, `Delphi/VB6`, `C++ Windows`, plus a `skill-creator` that authors a **new** stack adapter on the fly when the agent encounters something novel (Elixir, F#, Julia, Clojure, ABAP, etc.) |
| **Sources (10 source adapters)** | On-premise, AWS, GCP, Oracle Database, VMware / RVTools export, Kubernetes cluster, container registry (ACR / ECR / Docker Hub), GitHub repo, ZIP archive, and a catch-all escalation path for SaaS-embedded workloads (Salesforce Apex, ServiceNow, SharePoint on-prem, Power Platform, SAP ABAP extensions) or mainframe/midrange (z/OS, IBM i, COBOL/RPG/Natural) — routes to a specialist-partner playbook |
| **Workloads (8 patterns)** | Web app, API service, batch job, event-driven, serverless (Functions), data pipeline, desktop / client-server, packaged app |
| **Azure targets** | App Service, Container Apps, AKS, Functions, VMs, Azure VMware Solution, Azure SQL / PostgreSQL / MySQL / Cosmos / Data Factory / Databricks / Synapse, Entra ID, Key Vault, Application Insights, and more |

> **Adapter depth varies, by design.** Of the 33 adapters, 18 are full depth (.NET, Java, Python, Node.js, PHP, on-premise, AWS, the core workload patterns…) with step-by-step modernization guidance. The other 15 — Go, Ruby, Rust, Perl, Scala/Kotlin, C++ Windows, Delphi/VB6, PowerBuilder, GCP, Oracle DB, VMware/RVTools, and three workload patterns — are deliberately lighter: they classify the app, detect the sub-framework, pick Azure targets, size the effort, and flag risks, then hand off to the Architect. `skill-creator` deepens any of them on demand mid-migration.

> **Out of scope as a first-class family:** mainframe / midrange code migration (z/OS, IBM i, COBOL / RPG / Natural / PL/I on CICS / IMS / VSAM). These workloads route to `.github/skills/source-adapters/references/source-unsupported-escalation.md`, which provides a specialist-partner playbook (Micro Focus / Astadia / Kyndryl / LzLabs / TCS / NTT DATA) instead of pretending we can migrate their code.

## Where this tool fits alongside Microsoft's other migration options

Microsoft ships two first-party migration tools that are excellent when they cover your scenario. This tool complements them — use whatever combination fits your needs:

### 🔷 [GitHub Copilot Upgrade](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.upgrade-agent) *(`ms-dotnettools.upgrade-agent`)*
Great for **in-place .NET code upgrades and modernization**:
- .NET Framework / .NET Core → current .NET (8, 9, 10)
- .NET Framework 4.8.1 upgrades
- ASP.NET Web Forms → Blazor Server
- Azure Functions in-process → isolated worker
- Aspire integration + version upgrades
- SDK-style project conversion, VSIX/VSSDK modernization
- Newtonsoft.Json → System.Text.Json, System.Data.SqlClient → Microsoft.Data.SqlClient
- Semantic Kernel → Microsoft Agents framework

### 🔷 [Azure Migrate](https://learn.microsoft.com/en-us/azure/migrate/migrate-services-overview)
Great for **infrastructure discovery + lift-and-shift** of on-prem/other-cloud workloads to Azure IaaS:
- Server discovery (VMware, Hyper-V, physical, other clouds) → Azure VMs / AVS
- SQL Server assessment + migration → Azure SQL / Managed Instance / VMs (via **Data Migration Assistant** + **Azure Database Migration Service**)
- ASP.NET web apps on VMware → App Service (via **App Service Migration Assistant**)
- Business case analysis, dependency mapping, right-sizing, cost estimation
- Offline data movement via **Azure Data Box**
- Includes a preview **Azure Copilot migration agent** for planning inside the Azure portal

### 🟢 What THIS tool does differently

| Capability | This tool | Copilot Upgrade | Azure Migrate |
|------------|-----------|-----------------|---------------|
| **Non-.NET stacks** (Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, Scala/Kotlin, Oracle Forms, PowerBuilder, Delphi/VB6, C++ Windows) | ✅ 15 stack adapters | ❌ .NET only | ⚠ IaaS lift only, no code changes |
| **Universal source intake** (GitHub repo, ZIP archive, "describe-only" apps, mixed portfolios) | ✅ 10 source adapters + Discovery-first | ⚠ workspace-only | ✅ VMware / Hyper-V / physical / other cloud |
| **Decision Hardstop Protocol** — 18 major architecture decisions forced before code changes; user picks target framework, DB engine, hosting platform, IaC tool, etc. | ✅ | ❌ | ❌ |
| **On-the-fly skill authoring** (`skill-creator`) — mid-migration, agent researches + writes a new skill for any stack it hasn't seen (Elixir, F#, Clojure, ABAP, etc.) | ✅ | ❌ | ❌ |
| **Cross-session trace memory** — canonical Action Log in `Report-Status.md` for recovery + per-action token accounting | ✅ | ❌ | ❌ |
| **Portfolio 6Rs strategy report** — CIO-ready HTML deck with Microsoft / Partner / Unknown ownership across mixed-stack portfolios | ✅ | ❌ | ✅ (business case, different format) |
| **Universal Discovery Dossier + Capability Matrix** — a mechanical contract every downstream Phase skill consumes | ✅ | ❌ | ⚠ separate discovery report |
| **Never picks major architecture for you** — options + tradeoffs, waits for user pick, "stay-as-is" is always option 1 | ✅ | ⚠ some flows | ❌ |

**How to combine them:**
- Have a .NET app that needs an in-place code upgrade? Start with **GitHub Copilot Upgrade**.
- Have on-prem VMs / SQL / web apps to lift into Azure? Start with **Azure Migrate** for discovery + assessment.
- Have Java / Python / Node.js / PHP / Ruby / Go / other-stack apps to modernize? Use **this tool**.
- Have a mixed-stack portfolio needing a CIO plan? Use **this tool** for the 6Rs report, then hand off IaaS candidates to Azure Migrate and .NET candidates to GitHub Copilot Upgrade.

## How it's distributed

**One channel:** the [Azure Migration Agent VS Code extension](https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode). No npm CLI. Just install the extension, open a folder, click **Initialize**.

The extension bundles a copy of the canonical content from this repo and drops it into your workspace under `.github/`.

## Quick start

1. Install the extension: open VS Code, `Ctrl+Shift+X`, search **"Azure Migration Agent"**, click Install.
2. Open the folder you want to migrate.
3. Accept the welcome notification → click **Get started** (or run "Azure Migration: Initialize in this workspace" from the Command Palette).
4. Open GitHub Copilot Chat (`Ctrl+Alt+I`) and pick an agent from the agent dropdown. There are only three:

   | Pick | When |
   |---|---|
   | **Code Migration Modernization** | **Start here** — you want to migrate an app to Azure |
   | **Discovery Intake** | You are not yet sure what the app even is |
   | **Debug Migration** | A migration already in flight has broken |

   The five specialists (orchestrator, infrastructure, triage, security, cost) are dispatched for you automatically — you never have to pick the right one.

5. Type `/assess-any-application`. This is step 1 of the main path — discovery.
6. Then `/phase1-plan` — produces `reports/Application-Assessment-Report.md`, `reports/Migration-Plan.md`, and `reports/Decisions-Required.md`.
7. Answer each decision in `reports/Decisions-Required.md`, then run Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 in order.

Phases 2-6 **hard-stop** until each required decision in `reports/Decisions-Required.md` is answered. See [`.github/skills/migration-decisions/references/decision-hardstop.md`](./.github/skills/migration-decisions/references/decision-hardstop.md) for the protocol.

> **Optional add-ons** — `/build-migration-plan`, `/portfolio-strategy`, `/database-migration`, `/security-hardening`, `/cost-optimization`, and more are available for specialized needs. They are **not part of the default flow**. See [`MIGRATION-START-HERE.md`](./MIGRATION-START-HERE.md) for the full add-ons catalog.

Full walkthrough: [docs/vscode-quickstart.md](./docs/vscode-quickstart.md).

## What gets installed in your workspace

| Path | Content |
|------|---------|
| `.github/agents/` | 8 custom agents. 3 appear in the agent picker (see Quick start); the other 5 — Migration-Orchestrator, Azure-Infrastructure, Quick-Assessment, Security-Review, Cost-Optimization — set `user-invocable: false`, so they stay out of the dropdown while remaining dispatchable as subagents and reachable via their own slash commands |
| `.github/skills/` | 36 agent skills — 20 user-invocable workflow skills (`/assess-any-application`, Phase 1-6, Portfolio, Database, Security, Cost, Interview, Rollback…) and 16 auto-loaded knowledge skills bundling 74 reference files (15 stack adapters, 10 source adapters, 8 workload patterns, plus Azure / security / decision / artifact references) |
| `.github/hooks/` | Orchestration files: `session-lifecycle.json`, `validation.json`, `phase-gates.md`, `decision-gates.md`, `quality-checklist.md`, plus `scripts/` (SessionStart context loader, Stop-hook Action-Log writer, auto-validate — PowerShell and shell variants) |
| `.github/copilot-instructions.md` | Top-level rules for Copilot |
| `MIGRATION-START-HERE.md` | 60-second quickstart |

## Standout features

### 🎯 The Decision Hardstop Protocol

The agent **does not decide major architecture on your behalf**. It surfaces options with tradeoffs and waits.

| When | What the agent does |
|------|---------------------|
| Target framework version unclear | Posts options (.NET 8 vs 10, Java 17 vs 21, Python 3.11 vs 3.12, Node 20 vs 22 LTS, PHP 8.2 vs 8.3, etc.) with tradeoffs, waits for your pick |
| Database engine unclear | Posts options (Azure SQL, PostgreSQL, Cosmos, etc.), waits |
| Hosting platform unclear | Posts options (App Service, Container Apps, AKS, Functions), waits |
| IaC tool unclear | Posts options (Bicep, Terraform, ARM, Pulumi), waits |
| ...and 14 more major decisions | Same pattern. See [`.github/skills/migration-decisions/references/decision-catalog.md`](./.github/skills/migration-decisions/references/decision-catalog.md) |

**Stay-as-is** is always option 1 in every option block, forcing an active choice. No silent defaults. No expert-mode bypass.

### 🧠 On-the-fly skill authoring (skill-creator)

If Discovery finds a stack / source / workload / integration the agent's 36 skills don't cover, the **skill-creator** meta-skill offers to author a new one on the spot — research 3-5 authoritative sources, draft the skill file, save it, and continue the migration using the fresh knowledge. Inspired by [Anthropic's skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator). See [`.github/skills/skill-creator/SKILL.md`](./.github/skills/skill-creator/SKILL.md).

### 📜 Action Log (trace memory + token accounting)

Every meaningful action (phase transitions, artifact production, decisions, gates, user inputs, rollbacks) writes one canonical line to `reports/Report-Status.md`. That log is:

- **Trace memory** — a new session can recover where the last one left off via the SessionStart hook that reads the last 5 log entries
- **Token accounting** — each entry carries a per-action `turn=<n>` counter plus a best-effort `tokens=~<bucket>` estimate. Users get authoritative counts from the Copilot Dashboard; the log provides live in-context signal

Full spec: [`.github/skills/migration-artifacts/references/action-log-format.md`](./.github/skills/migration-artifacts/references/action-log-format.md).

### ✅ Universal, stack-agnostic wording

Every skill, agent, and hook was swept to remove ".NET or Java only" phrasing. The agent explicitly avoids rewriting to microservices / event-driven architectures unless the user picks a `rearchitect` or `rebuild` strategy — the default goal is **minimum viable Azure compatibility**, not architectural modernization.

## Repository structure (for contributors)

```
.github/
├── agents/                                       (✏️ EDIT — 8 custom agents, *.agent.md — 3 user-invocable)
├── skills/                                       (✏️ EDIT — 36 skills, each <name>/SKILL.md)
│   └── <skill>/references/                       (✏️ EDIT — 74 on-demand detail files)
├── hooks/                                        (✏️ EDIT — orchestration rules)
│   └── scripts/                                  (✏️ EDIT — .ps1 + .sh hook implementations)
├── copilot-instructions.md                       (✏️ EDIT — top-level rules)
└── workflows/                                    (✏️ EDIT — CI + release-please)
docs/                                             (✏️ EDIT — user docs)
packages/azure-migration-squad-vscode/
├── src/                                          (✏️ EDIT — TypeScript)
├── templates/                                    (❌ DO NOT EDIT — auto-synced)
├── package.json
└── ...
scripts/
├── inject-capability-matrix-gates.mjs            (gate injector — Phase 1-6 + DB/Sec/Cost)
├── inject-decision-gates.mjs                     (gate injector — decision-catalog coverage)
├── inject-action-log-contract.mjs                (gate injector — Action Log contract per skill)
├── validate-decision-coverage.mjs                (CI guard)
└── validate-description-lengths.mjs              (CI guard)
MIGRATION-START-HERE.md                           (✏️ EDIT — user welcome doc)
```

> **Why skills, not prompt files?** VS Code has
> [deprecated prompt files](https://code.visualstudio.com/docs/agent-customization/prompt-files)
> ("not loaded by Agent Host… the Local agent will be removed in a future release") and replaced chat
> modes with [custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents).
> Everything here follows the current
> [Agent Skills spec](https://code.visualstudio.com/docs/agent-customization/agent-skills): a skill is
> a **folder** containing `SKILL.md` with `name:` + `description:` frontmatter, and detail files in
> `references/` that load on demand. Skills are an [open standard](https://agentskills.io), so the same
> content works in VS Code Copilot Chat, the GitHub Copilot CLI, and the Copilot coding agent.

> **Important:** `packages/azure-migration-squad-vscode/templates/` is regenerated on every build by `scripts/sync-templates.mjs` (inside the extension package). Edit canonical files at `.github/*` and `MIGRATION-START-HERE.md`, then `npm run sync` to refresh.

## Local development

```powershell
# Install workspace deps
npm install

# Sync templates from .github/* into the extension
npm run sync

# Build + test extension
cd packages/azure-migration-squad-vscode
npm run build
npm run package          # produces .vsix
npm test                 # 13 headless tests

# Preview the next release locally (no push, no tag)
npm run release:local -- --dry-run
```

## CI

`.github/workflows/ci.yml` runs on every push/PR:

- ✅ Description lengths ≤1024 chars (Copilot listing constraint)
- ✅ Decision-catalog coverage (every catalog ID referenced by ≥1 phase skill)
- ✅ Templates sync from `.github/*` into the extension package
- ✅ Extension build via esbuild
- ✅ `.vsix` packaging via `vsce`
- ✅ Headless extension tests via `@vscode/test-electron`
- ✅ `.vsix` uploaded as build artifact
- ✅ Agent content pack (`.github/` skills, agents, hooks) staged, count-asserted, and uploaded as a portable artifact

## Publishing the extension

Versioning + changelog are automated via [release-please](https://github.com/googleapis/release-please). Use [Conventional Commits](./docs/conventional-commits.md) (`feat:` / `fix:` / `feat!:`) and merge to `main` — a Release PR opens automatically. Merge it and the marketplace publish workflow fires.

To preview a release locally (or ship an emergency hotfix):

```powershell
cd packages/azure-migration-squad-vscode
npm run release:local -- --dry-run
```

Full walkthrough: [`docs/publishing-vscode-extension.md`](./docs/publishing-vscode-extension.md).

## License

[MIT](./LICENSE)
