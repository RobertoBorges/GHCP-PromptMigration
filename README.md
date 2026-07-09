# Azure Migration Agent — GitHub Copilot prompts for Azure migration

> **Migrate any application to Azure** using a single GitHub Copilot agent definition plus 26 prompts, 60+ skills, and 8 chat modes. Universal source/stack/workload coverage. Discovery-first. The agent **never decides major architecture for you** — it lays out options and waits.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/robertoborges.azure-migration-squad-vscode?label=VS%20Code%20Marketplace&color=blueviolet&logo=visualstudiocode)](https://marketplace.visualstudio.com/items?itemName=robertoborges.azure-migration-squad-vscode)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository is the canonical source for the **Azure Migration Agent** (`.github/agents/Code-Migration-Modernization.agent.md`) and its supporting prompts, skills, chatmodes, and hooks.

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
| `.github/prompts/` | 19 prompt files (Phase 1-6, DatabaseMigration, SecurityHardening, etc.) |
| `.github/skills/` | 113 skill files — source/stack/workload adapters + universal patterns |
| `.github/chatmodes/` | 8 specialized chat modes (Discovery-Intake, Migration-Orchestrator, etc.) |
| `.github/hooks/` | 11 orchestration files (phase-gates, decision-gates, quality-checklist) |
| `.github/copilot-instructions.md` | Top-level rules for Copilot |
| `MIGRATION-START-HERE.md` | 60-second quickstart |

## Supported tech

| Sources | Stacks | Workloads |
|---------|--------|-----------|
| On-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, GitHub repos, ZIPs, mainframes | .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows | Web app, API service, batch job, event-driven, serverless, data pipeline, desktop, packaged, mainframe transactional |

## The Decision Hardstop Protocol

The agent **does not decide major architecture on your behalf**. It surfaces options with tradeoffs and waits.

| When | What the agent does |
|------|---------------------|
| Target framework version unclear | Posts options (.NET 8 vs 10, Java 17 vs 21, Python 3.11 vs 3.12, Node 20 vs 22 LTS, PHP 8.2 vs 8.3, etc.) with tradeoffs, waits for your pick |
| Database engine unclear | Posts options (Azure SQL, PostgreSQL, Cosmos, etc.), waits |
| Hosting platform unclear | Posts options (App Service, Container Apps, AKS, Functions), waits |
| IaC tool unclear | Posts options (Bicep, Terraform, ARM, Pulumi), waits |
| ...and 14 more major decisions | Same pattern. See [`.github/skills/decision-catalog.md`](./.github/skills/decision-catalog.md) |

**Stay-as-is** is always option 1 in every option block, forcing an active choice. No silent defaults. No expert-mode bypass.

## Repository structure (for contributors)

```
.github/
├── agents/                                       (✏️ EDIT — the one agent file)
├── prompts/                                      (✏️ EDIT — slash commands)
├── skills/                                       (✏️ EDIT — adapters & patterns)
├── chatmodes/                                    (✏️ EDIT — Copilot Chat modes)
├── hooks/                                        (✏️ EDIT — orchestration rules)
├── copilot-instructions.md                       (✏️ EDIT — top-level rules)
└── workflows/                                    (✏️ EDIT — CI)
docs/                                             (✏️ EDIT — user docs)
packages/azure-migration-squad-vscode/
├── src/                                          (✏️ EDIT — TypeScript)
├── templates/                                    (❌ DO NOT EDIT — auto-synced)
├── package.json
└── ...
scripts/
├── inject-capability-matrix-gates.mjs            (gate injector)
├── inject-decision-gates.mjs                     (gate injector)
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
