# Azure Migration Agent — GitHub Copilot prompts for Azure migration

> **Migrate any application to Azure** using a single GitHub Copilot agent definition plus 19 prompts, 85 skills, and 8 chat modes. Universal source/stack/workload coverage. Discovery-first. The agent **never decides major architecture for you** — it lays out options and waits.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/robertoborges.azure-migration-squad-vscode?label=VS%20Code%20Marketplace&color=blueviolet&logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository is the canonical source for the **Azure Migration Agent** (`.github/agents/Code-Migration-Modernization.agent.md`) and its supporting prompts, skills, chatmodes, and hooks.

## Supported languages, frameworks, and platforms

**Not just .NET and Java.** The agent handles any application in any of these stacks — with a dedicated skill file per stack that knows the modernization patterns, Azure hosting options, and common blockers:

| Category | Coverage |
|----------|----------|
| **Languages / frameworks (15 stack adapters)** | `.NET` (Framework 2.x → 10 LTS), `Java` (8/11 → 17/21 LTS + Spring Boot 3.x), `Python` (2.x → 3.12+, Django/Flask/FastAPI), `Node.js` (12/14/16 → 20/22 LTS, Express/NestJS/Next), `PHP` (5.x/7.x → 8.3+, Laravel/Symfony), `Ruby` (2.x → 3.3+, Rails), `Go` (≤ 1.19 → 1.22+), `Perl` (5.x), `Rust` (edition upgrades), `Scala/Kotlin`, `Oracle Forms` (→ APEX / Spring Boot rewrite), `PowerBuilder`, `Delphi/VB6`, `C++ Windows`, plus a `skill-creator` that authors a **new** stack adapter on the fly when the agent encounters something novel (Elixir, F#, Julia, Clojure, ABAP, etc.) |
| **Sources (10 source adapters)** | On-premise, AWS, GCP, Oracle Cloud, VMware / RVTools export, Kubernetes cluster, container registry (ACR / ECR / Docker Hub), GitHub repo, ZIP archive, and a catch-all escalation path for SaaS-embedded workloads (Salesforce Apex, ServiceNow, SharePoint on-prem, Power Platform, SAP ABAP extensions) or mainframe/midrange (z/OS, IBM i, COBOL/RPG/Natural) — routes to a specialist-partner playbook |
| **Workloads (8 patterns)** | Web app, API service, batch job, event-driven, serverless (Functions), data pipeline, desktop / client-server, packaged app |
| **Azure targets** | App Service, Container Apps, AKS, Functions, VMs, Azure VMware Solution, Azure SQL / PostgreSQL / MySQL / Cosmos / Data Factory / Databricks / Synapse, Entra ID, Key Vault, Application Insights, and more |

> **Out of scope as a first-class family:** mainframe / midrange code migration (z/OS, IBM i, COBOL / RPG / Natural / PL/I on CICS / IMS / VSAM). These workloads route to `.github/skills/source-unsupported-escalation.md`, which provides a specialist-partner playbook (Micro Focus / Astadia / Kyndryl / LzLabs / TCS / NTT DATA) instead of pretending we can migrate their code.

## How it's distributed

**One channel:** the [Azure Migration Agent VS Code extension](https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode). No npm CLI. Just install the extension, open a folder, click **Initialize**.

The extension bundles a copy of the canonical content from this repo and drops it into your workspace under `.github/`.

## Quick start

1. Install the extension: open VS Code, `Ctrl+Shift+X`, search **"Azure Migration Agent"**, click Install.
2. Open the folder you want to migrate.
3. Accept the welcome notification → click **Get started** (or run "Azure Migration: Initialize in this workspace" from the Command Palette).
4. Open GitHub Copilot Chat (`Ctrl+Alt+I`) → type `/assess-any-application`. This is step 1 of the main path — discovery.
5. Then `/Phase1-Plan` — produces `reports/Application-Assessment-Report.md`, `reports/Migration-Plan.md`, and `reports/Decisions-Required.md`.
6. Answer each decision in `reports/Decisions-Required.md`, then run Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 in order.

Phases 2-6 **hard-stop** until each required decision in `reports/Decisions-Required.md` is answered. See [`.github/skills/decision-hardstop.md`](./.github/skills/decision-hardstop.md) for the protocol.

> **Optional add-ons** — `/Build-Migration-Plan`, `/PortfolioStrategy`, `/DatabaseMigration`, `/SecurityHardening`, `/CostOptimization`, and more are available for specialized needs. They are **not part of the default flow**. See [`MIGRATION-START-HERE.md`](./MIGRATION-START-HERE.md) for the full add-ons catalog.

Full walkthrough: [docs/vscode-quickstart.md](./docs/vscode-quickstart.md).

## What gets installed in your workspace

| Path | Content |
|------|---------|
| `.github/agents/Code-Migration-Modernization.agent.md` | The one agent definition |
| `.github/prompts/` | 19 prompt files (Assess + Phase 1-6 main path, plus Portfolio, Database, Security, Cost, Interview, Rollback add-ons) |
| `.github/skills/` | 85 skill files — 15 stack adapters, 10 source adapters, 8 workload patterns, plus universal Azure / security / decision / logging / meta skills |
| `.github/skills/references/` | On-demand references consumed by `skill-creator` when authoring new skills |
| `.github/chatmodes/` | 8 specialized chat modes (Discovery-Intake, Migration-Orchestrator, Code-Migration, Cost-Optimization, Debug-Migration, Quick-Assessment, Security-Review, Azure-Infrastructure) |
| `.github/hooks/` | 11 orchestration files: `session-lifecycle.json`, `validation.json`, `phase-gates.md`, `decision-gates.md`, `quality-checklist.md`, and helper scripts (SessionStart context loader, Stop hook Action-Log writer, etc.) |
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
| ...and 14 more major decisions | Same pattern. See [`.github/skills/decision-catalog.md`](./.github/skills/decision-catalog.md) |

**Stay-as-is** is always option 1 in every option block, forcing an active choice. No silent defaults. No expert-mode bypass.

### 🧠 On-the-fly skill authoring (skill-creator)

If Discovery finds a stack / source / workload / integration the agent's 85 skills don't cover, the **skill-creator** meta-skill offers to author a new one on the spot — research 3-5 authoritative sources, draft the skill file, save it, and continue the migration using the fresh knowledge. Inspired by [Anthropic's skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator). See [`.github/skills/skill-creator.md`](./.github/skills/skill-creator.md).

### 📜 Action Log (trace memory + token accounting)

Every meaningful action (phase transitions, artifact production, decisions, gates, user inputs, rollbacks) writes one canonical line to `reports/Report-Status.md`. That log is:

- **Trace memory** — a new session can recover where the last one left off via the SessionStart hook that reads the last 5 log entries
- **Token accounting** — each entry carries a per-action `turn=<n>` counter plus a best-effort `tokens=~<bucket>` estimate. Users get authoritative counts from the Copilot Dashboard; the log provides live in-context signal

Full spec: [`.github/skills/action-log-format.md`](./.github/skills/action-log-format.md).

### ✅ Universal, stack-agnostic wording

Every prompt, skill, and hook was swept to remove ".NET or Java only" phrasing. The agent explicitly avoids rewriting to microservices / event-driven architectures unless the user picks a `rearchitect` or `rebuild` strategy — the default goal is **minimum viable Azure compatibility**, not architectural modernization.

## Repository structure (for contributors)

```
.github/
├── agents/                                       (✏️ EDIT — the one agent file)
├── prompts/                                      (✏️ EDIT — slash commands)
├── skills/                                       (✏️ EDIT — adapters & patterns)
│   └── references/                               (✏️ EDIT — on-demand refs for skill-creator)
├── chatmodes/                                    (✏️ EDIT — Copilot Chat modes)
├── hooks/                                        (✏️ EDIT — orchestration rules + scripts)
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
├── inject-action-log-contract.mjs                (gate injector — Action Log contract per prompt)
├── validate-decision-coverage.mjs                (CI guard)
└── validate-description-lengths.mjs              (CI guard)
MIGRATION-START-HERE.md                           (✏️ EDIT — user welcome doc)
```

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
- ✅ Decision-catalog coverage (every catalog ID referenced by ≥1 phase prompt)
- ✅ Templates sync from `.github/*` into the extension package
- ✅ Extension build via esbuild
- ✅ `.vsix` packaging via `vsce`
- ✅ Headless extension tests via `@vscode/test-electron`
- ✅ `.vsix` uploaded as build artifact

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
