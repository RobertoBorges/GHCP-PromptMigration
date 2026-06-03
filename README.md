# GitHub Copilot Migration & Modernization for Azure

> **Universal Mode (v2 — 2026-06-01):** Migrate **any application** to Azure — regardless of where it runs today or what it's built in. Discovery-first, evidence-bound, squad-orchestrated.

This repository turns GitHub Copilot into a structured migration system: a Discovery Engineer characterizes any application; an Architect approves the strategy; specialist agents execute Phases 1–6 to land it on Azure. The Universal Discovery flow handles **on-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registries, GitHub repos, ZIPs, and mainframes** across **.NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, and C++ Windows** stacks.

## Table of Contents

- [Overview](#overview)
- [Three Ways to Start](#three-ways-to-start)
- [The Universal Migration Flow](#the-universal-migration-flow)
- [Requirements](#requirements)
- [What's in the Repository](#whats-in-the-repository)
- [Migration Phases](#migration-phases)
- [The Squad — 15 Specialists](#the-squad--15-specialists)
- [Source / Stack / Workload Adapters](#source--stack--workload-adapters)
- [Avoiding Hallucinations](#avoiding-hallucinations)
- [Status Tracking](#status-tracking)
- [Use-Case Walkthroughs](#use-case-walkthroughs)
- [Contributing](#contributing)
- [License](#license)

## Overview

The project provides a structured, evidence-bound approach to:

0. **Discover** any application — characterize source, stack, workload, data, integrations with confidence labels
1. **Plan & assess** with a Capability Matrix that every phase consumes
2. **Migrate code** to modern Azure-compatible runtimes (when modernization is in scope)
3. **Generate infrastructure as code** (Bicep / Terraform)
4. **Deploy to Azure** with managed identities, Key Vault, observability baked in
5. **Set up CI/CD** for automated, repeatable deployments
6. **Post-migration ops** — dashboards, alerts, runbooks, cost guardrails

Through a guided, AI-assisted workflow, developers and architects transform legacy applications into modern, cloud-native solutions running on Azure.

## Three Ways to Start

```
Got an unknown app and want the squad to figure it out?
  → /assess-any-application       (Universal Mode — recommended)

Got a customer portfolio (CMDB / RVTools / DMA / 10+ apps)?
  → /PortfolioStrategy            (Portfolio Planning flow)

Got multiple repos that form ONE business solution?
  → /Phase0-Multi-repo-assessment

Know the stack and target — just want execution?
  → /Phase1-PlanAndAssess         (skip discovery; accept risk in .squad/decisions.md)
```

The Universal Mode is the default for any new application. It auto-detects what the app is, where it lives, and recommends a migration strategy (Rehost / Replatform / Refactor / Rearchitect / Rebuild / Retire / Retain) using a 12-branch decision tree — not just a 6Rs label.

## The Universal Migration Flow

```
USER ──► /assess-any-application
            │
            ▼
   ┌──────────────────────────────┐
   │  Discovery Engineer          │  ← intake + classification + evidence
   │  (Saul Bloom Jr.)            │
   │                              │
   │  Outputs:                    │
   │   • Discovery Dossier        │  reports/Discovery-Dossier.md
   │   • Capability Matrix        │  reports/Capability-Matrix.yaml
   │   • Strategy recommendation  │
   └────────────┬─────────────────┘
                │ handoff (evidence-bound)
                ▼
   ┌──────────────────────────────┐
   │  Architect (Danny Ocean)     │  ← approves/refines strategy
   │  /build-migration-plan       │     finalizes target Azure architecture
   └────────────┬─────────────────┘     produces reports/Migration-Plan.md
                │
                ▼
   Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
   (each phase consumes the Capability Matrix and dispatches the right
    squad specialists per the source/stack/workload axes)
```

The **Capability Matrix** is the contract: every Phase 1–6 prompt reads it to know which source adapter, stack adapter, and workload pattern to load — and which specialists to dispatch.

## Requirements

- GitHub Copilot License
- Model **Claude Sonnet 4.5 or 4.6** (included in GitHub Copilot) — Sonnet 4.6 recommended for Discovery
- Azure MCP Server Extension
- GitHub Copilot for Azure Extension
- GitHub Copilot Extension 1.35+
- GitHub Copilot Chat Extension 0.30+
- Visual Studio Code 1.101+
- AZD CLI
- AZ CLI
- Development tools that fit your application's stack

## What's in the Repository

```
.
├── .github/
│   ├── chatmodes/              ← 9 chatmodes (Discovery-Intake, Migration-Orchestrator,
│   │                              Code-Migration-Modernization, Azure-Infrastructure,
│   │                              Security-Review, Cost-Optimization, Debug-Migration,
│   │                              Onboarding, Quick-Assessment)
│   ├── prompts/                ← Universal + Phase prompts (Phase 0–6, PortfolioStrategy,
│   │                              Assess-Any-Application, Build-Migration-Plan, …)
│   │   └── legacy/             ← Deprecated narrow Assess-* prompts (kept for reference)
│   ├── skills/                 ← 60+ reusable skills
│   │   ├── stack-detection.md
│   │   ├── migration-strategy-decision-tree.md
│   │   ├── capability-matrix.md
│   │   ├── discovery-dossier-template.md
│   │   ├── migration-plan-template.md
│   │   ├── source-*.md         ← 11 source adapters (on-premise, AWS, GCP, K8s, …)
│   │   ├── stack-*.md          ← 15 stack adapters (.NET, Java, Python, COBOL, …)
│   │   ├── workload-*.md       ← 9 workload patterns (webapp, api, batch, …)
│   │   └── (nested skill dirs with SKILL.md + templates)
│   ├── hooks/                  ← agent-dispatch, phase-gates, quality-checklist, …
│   ├── workflows/              ← GitHub Actions: pptx-generate, squad-health
│   └── copilot-instructions.md ← Universal Mode behavioral contract
│
├── .squad/                     ← Squad orchestration layer
│   ├── agents/                 ← 15 agent charters (incl. discovery-engineer)
│   ├── team.md                 ← Roster + targets
│   ├── routing.md              ← Capability-based routing rules
│   ├── decisions.md            ← Durable decision log
│   └── ...
│
├── docs/                       ← Architecture, guides, onboarding, walkthroughs,
│                                  PPTX decks, use-case cheatsheets
│
├── skills/                     ← Top-level mirror of flat skill files (for cross-mode access)
│
├── Use-cases/                  ← 7 reference applications (see Walkthroughs section)
│
├── README.md                   ← You are here
├── README-Squad.md             ← "Ocean's Fourteen" branded deep-dive on squad orchestration
├── AGENTS.md, CLAUDE.md,
│ JOURNAL.md, PORTFOLIO.md      ← Squad operating documents
└── .env.example
```

## Migration Phases

| Phase | Prompt | Lead Agent | Produces |
|-------|--------|-----------|----------|
| **Discovery** | `/assess-any-application` | Discovery Engineer | Discovery Dossier + Capability Matrix |
| **Plan** | `/build-migration-plan` | Architect | Migration Plan |
| **0** | `/Phase0-Multi-repo-assessment` | Discovery Engineer | Repo inventory + sequencing |
| **1** | `/Phase1-PlanAndAssess` | Architect | Application-Assessment-Report |
| **2** | `/Phase2-MigrateCode` | Coder | Modernized code + Migration-Change-Log |
| **DB** | `/DatabaseMigration` | Database Specialist | Database-Migration-Report |
| **3** | `/Phase3-GenerateInfra` | Azure Specialist | Bicep / Terraform IaC |
| **Sec** | `/SecurityHardening` | Security Auditor | Security-Review-Report |
| **4** | `/Phase4-DeployToAzure` | DevOps Engineer | Deployed environment |
| **5** | `/Phase5-SetupCICD` | DevOps Engineer | CI/CD pipelines |
| **6** | `/Phase6-PostMigrationOps` | Observability Engineer | Runbooks + dashboards + alerts |
| **Cost** | `/CostOptimization` | Cost Engineer | Cost-Optimization-Report |
| **Rollback** | `/Phase-Rollback` | Cutover Commander | Rollback execution |
| **Status** | `/GetStatus` | Tester | Status snapshot |

Each phase has a **quality gate** defined in `.squad/routing.md`. A phase does not advance until the gate is satisfied.

## The Squad — 15 Specialists

| # | Agent | Alias | Best for |
|---|-------|-------|----------|
| 1 | **Discovery Engineer** | Saul Bloom Jr. | Intake, classification, 6Rs recommendation, Capability Matrix |
| 2 | Architect | Danny Ocean | Migration strategy approval, target architecture, sequencing |
| 3 | Coder | Rusty Ryan | Code modernization, framework upgrades, refactoring |
| 4 | Tester | Linus Caldwell | Validation, smoke testing, prompt QA |
| 5 | Azure Specialist | Basher Tarr | Azure hosting, identity, landing zones |
| 6 | DevOps Engineer | Turk Malloy | CI/CD, deployment automation |
| 7 | Observability Engineer | Livingston Dell | Monitoring, App Insights, alerts |
| 8 | Database Specialist | The Amazing Yen | Schema migration, cutover, data validation |
| 9 | Performance Engineer | Virgil Malloy | Load, baselines, scaling |
| 10 | Security Auditor | Frank Catton | Auth, secrets, RBAC, compliance |
| 11 | Evaluator | Saul Bloom | Prompt quality, regression review |
| 12 | Cutover Commander | Reuben Tishkoff | Rollout, rollback, go-live |
| 13 | Scribe | Roman Nagel | Journal, decision log |
| 14 | Presentation Specialist | Tess Ocean | Status decks, executive summaries |
| 15 | Cost Engineer | The Accountant | Cost models, right-sizing, FinOps |

Full charters: `.squad/agents/<name>/charter.md`. Routing rules: `.squad/routing.md`.

## Source / Stack / Workload Adapters

The system characterizes any application along three orthogonal axes — every skill is a small, focused markdown file the Discovery Engineer loads dynamically based on what it detects.

**Source adapters (11)** — where the application lives today:

`source-github-repo`, `source-on-premise`, `source-aws`, `source-gcp`, `source-oracle-db`, `source-vmware-rvtools`, `source-mainframe`, `source-kubernetes-cluster`, `source-container-registry`, `source-zip-filesystem`, `source-unsupported-escalation` (Salesforce / SAP / Lotus Notes catch-all)

**Stack adapters (15)** — what the application is built in:

`stack-dotnet`, `stack-java`, `stack-python`, `stack-nodejs`, `stack-php`, `stack-ruby`, `stack-go`, `stack-perl`, `stack-rust`, `stack-cobol-mainframe`, `stack-oracle-forms`, `stack-powerbuilder`, `stack-delphi-vb6`, `stack-scala-kotlin`, `stack-cpp-windows`

**Workload patterns (9)** — runtime / architectural shape:

`workload-webapp`, `workload-api-service`, `workload-batch-job`, `workload-event-driven`, `workload-serverless`, `workload-data-pipeline`, `workload-desktop-client-server`, `workload-packaged-app`, `workload-mainframe-transactional`

Strategy is decided by the `migration-strategy-decision-tree` skill — a 12-branch decision engine that weighs business priority, source constraints, code mutability, data gravity, integration complexity, target Azure options, cutover constraints, and team readiness. The 6Rs label is **one output field**, not the whole engine.

## Avoiding Hallucinations

To keep migration grounded, the squad relies on **evidence-bound artifacts** in `reports/`:

| Artifact | Purpose |
|----------|---------|
| `reports/Discovery-Dossier.md` | Narrative discovery output with evidence + confidence labels |
| `reports/Capability-Matrix.yaml` | Machine-readable contract consumed by every Phase prompt |
| `reports/Migration-Plan.md` | Architect-approved execution plan |
| `reports/Application-Assessment-Report.md` | Phase 1 detailed assessment |
| `reports/Report-Status.md` | Overall status dashboard |

Every classification carries an `evidence_confidence: high | medium | low` label tied to a file path, command output, or quoted user statement. Low-confidence axes must list `unresolved_questions` with a recommended next probe. A Phase prompt that can't find a Capability Matrix refuses to proceed and routes back to Discovery.

**Pro tips:**

- For rewrite migrations, scaffolded files (`Class1.cs`, default templates) may be created. Clean them up before final check-in.
- Use the `@terminal` command to ask the agent to diagnose issues during tests.
- Don't assume — verify with documentation. Every Discovery Engineer recommendation lists alternatives considered.

## Status Tracking

Check progress at any time with:

- `/GetStatus` — current status snapshot
- `@squad show migration status` — squad-mode equivalent
- `reports/Report-Status.md` — durable status dashboard

The status report includes:

- Overall completion percentage and per-phase status
- Quality scores for each completed phase
- Timestamps for phase transitions
- Identified risks with severity
- Recommended next steps
- Resource links (architecture diagrams, IaC, runbooks)

## Use-Case Walkthroughs

The `Use-cases/` folder contains **seven reference applications** that demonstrate the universal flow against well-understood inputs. They are not a fixed catalog — the squad migrates anything — but they're the easiest way to see the system end-to-end.

| # | Use-Case | Source | Demonstrates |
|---|----------|--------|--------------|
| 1 | `01-ASPClassicApp` | Classic ASP | Strangler rewrite to ASP.NET Core |
| 2 | `02-NetFramework30-ASPNET-WEB` | .NET Framework 3.0 | Full-stack modernization to .NET 10 |
| 3 | `03-WCFNet35` | WCF .NET 3.5 | SOAP-to-REST API conversion |
| 4 | `04-ContosoUniversityDiPS` | ASP.NET MVC + multiple components | Multi-component App Service migration |
| 5 | `05-BookShop` | .NET 3.5 WebForms | Razor Pages + Container Apps + Bicep |
| 6 | `06-Java-API-BusReservation` | Java 8 + Spring | Spring Boot 3.x + PostgreSQL |
| 7 | `07-PartsUnlimited-aspnet45` | ASP.NET 4.5 | Mature .NET modernization + observability |

Step-by-step walkthroughs and cheatsheets live in `docs/walkthroughs/` and `docs/use-case-cheatsheets/`.

## See Also

- **`README-Squad.md`** — "Ocean's Fourteen" deep-dive on squad orchestration (the why behind multi-agent over single-prompt)
- **`.squad/team.md`** — full squad roster
- **`.squad/routing.md`** — capability-based routing rules
- **`.github/copilot-instructions.md`** — universal behavioral contract for GitHub Copilot
- **`AGENTS.md`** — universal squad instructions
- **`docs/onboarding/`** — onboarding guides and training exercises
- **`docs/architecture/`** — system architecture and prompt catalog
- **`.github/prompts/legacy/README.md`** — mapping from deprecated `Assess-*` prompts to current adapters

## Contributing

Contributions are welcome:

- Add a new source adapter, stack adapter, or workload pattern under `.github/skills/`
- Improve the `migration-strategy-decision-tree` with new branches
- Add use-case walkthroughs under `docs/walkthroughs/`
- Sharpen agent charters in `.squad/agents/`
- Add example `Capability-Matrix.yaml` fixtures for testing

Please open an issue or PR. The `Evaluator` agent reviews prompt/skill changes for consistency.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
