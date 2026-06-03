---
title: Squad Routing Rules — Universal Migration Mode
version: 2.0
updated: 2026-06-01
mode: capability-based
---

# Routing Rules — Ocean's Twelve — The Azure Heist (Universal Mode)

> Fifteen specialists. Any source. Any stack. Route by capability, not by use-case.

> **Version 2.0 (2026-06-01):** This file was refactored from use-case-pinned routing to **capability-based routing**. The original use-case-1–7 tables are preserved at the bottom under [Legacy Examples](#legacy-examples) as a reference. Routing decisions now flow from the **Capability Matrix** produced by the Discovery Engineer.

## Routing Principles

1. **Discovery is the universal entry point.** No app gets routed to a Phase prompt until the Discovery Engineer has produced a **Discovery Dossier** + **Capability Matrix** (or the user explicitly skipped discovery and accepted the risk).
2. **One lead agent owns the outcome.** Support agents run in parallel. The lead consolidates.
3. **Route by capability, not by use-case.** The Capability Matrix has fields (`source_adapter`, `stack_adapters`, `workload_patterns`, `migration_strategy`, `risk_flags`). Each field maps to a routing rule.
4. **Exact asset names win.** Route by the real prompt / chatmode / skill name. Do not invent aliases mid-run.
5. **Dispatch early.** If the matrix obviously touches platform, data, security, deployment, or quality, launch those specialists immediately.
6. **Utility prompts do not replace phase gates.** `QuickAssessment`, `GetStatus`, and `Debug-Migration` help steer work, but they do not waive entry or exit criteria.
7. **Escalate by trigger, not by preference.** Secondary agents join automatically when their trigger conditions appear in the matrix.
8. **Scribe records milestones; Evaluator guards prompt quality.** Neither should be skipped when their trigger conditions are met.

## Universal Migration Flow

```
USER ──► /assess-any-application  (or @squad assess any application)
            │
            ▼
   ┌────────────────────────────┐
   │  Discovery Engineer        │  ← intake + classification + evidence
   │  (Saul Bloom Jr.)          │
   │                            │
   │  Outputs:                  │
   │   • Discovery Dossier      │
   │   • Capability Matrix      │
   │   • Strategy recommendation│
   └────────────┬───────────────┘
                │ handoff (evidence-bound)
                ▼
   ┌────────────────────────────┐
   │  Architect (Danny Ocean)   │  ← approves/refines strategy, finalizes
   │                            │   target Azure architecture + sequence
   └────────────┬───────────────┘
                │ executes via Migration-Orchestrator
                ▼
   Phase 1 → 2 → 3 → 4 → 5 → 6  (capability-matrix-driven)
   with cross-cutting specialists dispatched per matrix
```

## Discovery-to-Phase Handoff Contract

The Discovery Engineer hands the Architect a **Capability Matrix** with this shape (see `.github/skills/capability-matrix.md`):

```yaml
application:
  name: <discovered or user-provided>
  business_priority: <speed | modernize | cost | risk>

source:
  primary_adapter: <source-aws | source-on-premise | source-github-repo | ...>
  access_method: <git-url | ssh | aws-profile | rvtools-export | filesystem-path | ...>
  evidence_confidence: <high | medium | low>

stack:
  primary_stack: <dotnet | java | python | nodejs | php | cobol | ...>
  secondary_stacks: [...]
  build_system: <msbuild | maven | gradle | npm | pip | composer | make | ...>
  evidence_confidence: <high | medium | low>

workload:
  primary_pattern: <webapp | api | batch | event-driven | serverless | data-pipeline | ...>
  secondary_patterns: [...]

data:
  primary_datastore: <sql-server | oracle | postgresql | mysql | mongo | dynamodb | files | ...>
  data_gravity: <none | small | medium | large | very-large>

integrations:
  - <queue | api | file-share | scheduler | identity-provider>

migration_strategy:
  recommendation: <rehost | replatform | refactor | rearchitect | rebuild | retire | retain>
  target_azure_candidates: [...]
  rationale: <evidence + decision-tree path>
  alternatives_considered: [...]

risk_flags: [...]
required_specialists: [...]
unresolved_questions: [...]
```

Routing reads this matrix. Every rule below maps from a matrix field.

## Capability-Based Routing

### Source Adapter → Lead Engagement (first specialist after Discovery)

| `source.primary_adapter` | First-engaged specialist after Discovery |
|--------------------------|-------------------------------------------|
| `source-github-repo`, `source-zip-filesystem` | Architect (scope + sequence) |
| `source-on-premise` | Architect + Azure Specialist (landing-zone fit) |
| `source-aws`, `source-gcp` | Azure Specialist (service-mapping) |
| `source-vmware-rvtools` | Architect (portfolio sequencing) |
| `source-oracle-db` | Database Specialist + Architect |
| `source-mainframe` | Architect + Database Specialist (high-risk path) |
| `source-kubernetes-cluster` | Azure Specialist + DevOps Engineer |
| `source-container-registry` | DevOps Engineer + Azure Specialist |
| `source-unsupported-escalation` | Architect (define escalation + manual path) |

### Stack Adapter → Code-Phase Lead

| `stack.primary_stack` | Phase 2 / code-migration lead | Cross-cutting partners |
|-----------------------|-------------------------------|------------------------|
| `dotnet` | Coder | Azure Specialist, Tester |
| `java` | Coder | Azure Specialist, Tester |
| `python` | Coder | DevOps Engineer (packaging), Tester |
| `nodejs` | Coder | Azure Specialist, Tester |
| `php` | Coder | Azure Specialist, Database Specialist |
| `ruby` | Coder | Azure Specialist, Tester |
| `go` | Coder | DevOps Engineer (build), Tester |
| `perl` | Coder | Architect (often retire/rewrite), Tester |
| `rust` | Coder | DevOps Engineer (build), Tester |
| `cobol-mainframe` | Architect → Coder | Database Specialist, Cutover Commander |
| `oracle-forms` | Architect → Coder | Database Specialist, Security Auditor |
| `powerbuilder`, `delphi-vb6`, `cpp-windows` | Architect (rewrite path) | Coder, Cutover Commander |
| `scala-kotlin` | Coder | Performance Engineer, Tester |

### Workload Pattern → Architecture Lead

| `workload.primary_pattern` | Azure target tendency | Architecture lead |
|----------------------------|----------------------|-------------------|
| `webapp` | App Service, Container Apps | Azure Specialist |
| `api-service` | App Service, Container Apps, Functions | Azure Specialist |
| `batch-job` | Container Apps Jobs, Container Instances, Batch | Azure Specialist + DevOps Engineer |
| `event-driven` | Functions, Event Grid, Service Bus | Azure Specialist + Performance Engineer |
| `serverless` | Functions, Static Web Apps | Azure Specialist |
| `desktop-client-server` | App Service + Win VM hybrid, or rewrite | Architect (rewrite likely) |
| `packaged-app` | Container Apps, AVS, or retire | Architect + Azure Specialist |
| `data-pipeline` | Data Factory, Synapse, Databricks | Database Specialist + Azure Specialist |
| `mainframe-transactional` | AKS + replatform, or modernize incrementally | Architect (escalation path) |

### Migration Strategy → Phase Emphasis

| `migration_strategy.recommendation` | Phases emphasized | Phases lightened |
|-------------------------------------|-------------------|------------------|
| `rehost` (lift-and-shift) | Phase 3 (infra), Phase 4 (deploy) | Phase 2 (code) is mostly packaging |
| `replatform` | Phase 2 (config/runtime), Phase 3, Phase 4 | — |
| `refactor` | Phase 2 (heavy code work) | — |
| `rearchitect` | Phase 1 (re-design), Phase 2, Phase 3 (new IaC) | — |
| `rebuild` | All phases; treat as greenfield | Phase 0 (multi-repo) usually skipped |
| `retire` | None — feed into portfolio decision | All |
| `retain` (keep on-source) | Phase 3 (integration only) | Phase 2, Phase 4 |

### Risk Flag → Auto-Dispatch

When the Capability Matrix has any of these `risk_flags`, the listed specialist is added automatically.

| Risk flag | Auto-added specialist |
|-----------|----------------------|
| `regulated-data` (PII, PCI, HIPAA, GDPR) | Security Auditor + Architect |
| `production-only-system` (no test env) | Cutover Commander + Tester |
| `large-data-gravity` | Database Specialist + Performance Engineer |
| `no-source-code-available` | Architect (rehost path) |
| `unsupported-runtime` (out-of-support OS or framework) | Architect + Security Auditor |
| `vendor-licensed-runtime` (Oracle, IBM, SAP, etc.) | Architect + Cost Engineer |
| `tight-cutover-window` | Cutover Commander + Performance Engineer |
| `mainframe` or `saas-embedded` | Architect (escalation path) |
| `high-integration-fanout` | Architect + Azure Specialist |
| `low-evidence-confidence` | Discovery Engineer re-run before Phase 1 |

## Work Type → Agent (capability-agnostic baseline)

| Work Type | Lead Agent | Support Agents |
|-----------|------------|----------------|
| intake / discovery / classification | Discovery Engineer | Architect |
| architecture | Architect | Azure Specialist |
| azure-services | Azure Specialist | Architect |
| implementation | Coder | Database Specialist |
| database | Database Specialist | Coder |
| infrastructure | Azure Specialist | DevOps Engineer |
| deployment | DevOps Engineer | Cutover Commander |
| cutover | Cutover Commander | DevOps Engineer |
| security | Security Auditor | Azure Specialist |
| performance | Performance Engineer | Observability Engineer |
| monitoring | Observability Engineer | Performance Engineer |
| testing | Tester | Evaluator |
| documentation | Tester | Scribe |
| prompt-quality | Evaluator | Tester |
| cost | Cost Engineer | Azure Specialist, Architect |
| journal | Scribe | — |
| presentation | Presentation Specialist | Scribe, Architect |

## Prompt & Chatmode → Agent Dispatch Map

> Universal entry points first, then phase prompts.

| Prompt | Lead | Parallel Agents |
|--------|------|-----------------|
| **Assess-Any-Application** | **Discovery Engineer** | **Architect (review)** |
| **Build-Migration-Plan** | **Architect** | **Discovery Engineer, Azure Specialist** |
| QuickAssessment | Discovery Engineer | Architect |
| Phase0-Multi-repo-assessment | Discovery Engineer | Architect, Azure Specialist, Security Auditor |
| Phase1-PlanAndAssess | Architect | Azure Specialist, Security Auditor, Database Specialist |
| Phase2-MigrateCode | Coder | per `stack_adapters` and `workload_patterns` |
| DatabaseMigration | Database Specialist | Coder, Security Auditor |
| Phase3-GenerateInfra | Azure Specialist | DevOps Engineer, Security Auditor |
| SecurityHardening | Security Auditor | Azure Specialist, Observability Engineer |
| Phase4-DeployToAzure | DevOps Engineer | Cutover Commander, Tester |
| Phase5-SetupCICD | DevOps Engineer | Tester, Security Auditor |
| Phase6-PostMigrationOps | Observability Engineer | Performance Engineer |
| Phase-Rollback | Cutover Commander | Coder, Database Specialist |
| CostOptimization | Cost Engineer | Azure Specialist, Architect |
| GetStatus | Tester | — |
| Debug-Migration (chatmode) | Coder | Azure Specialist |
| Discovery-Intake (chatmode) | Discovery Engineer | Architect |
| Migration-Orchestrator (chatmode) | Architect | per matrix |

## Phase Quality Gates

> A phase only advances when the gate is true AND the relevant artifacts are updated.

| Phase | Gate — all must be true |
|-------|-------------------------|
| **Discovery** | Discovery Dossier produced; Capability Matrix populated; `evidence_confidence` recorded per axis; `unresolved_questions` listed; escalation path defined for any low-confidence axis. |
| Phase 0 — Multi-Repo Assessment | Repository inventory complete; candidate apps prioritized; shared dependencies documented; each repo has a recommended migration path and next-step owner. |
| Phase 1 — Plan & Assess | Capability Matrix loaded; target Azure platform chosen; assessment report updated; risks recorded; success criteria explicit. |
| Phase 2 — Migrate Code | Per `stack_adapters`: core paths compile/validate; breaking changes addressed or logged; config and auth changes documented; regression checks pass; DB-impacting changes handed to Database Specialist. |
| Database Migration | Target database choice confirmed; schema/data migration path documented; validation queries exist; backup/restore/cutover expectations clear. |
| Phase 3 — Generate Infra | IaC generated and reviewed; parameters/secrets externalized; network/identity/hosting explicit; security baseline present; deployment instructions runnable. |
| Security Hardening | Auth validated; secrets externalized; RBAC/network exposure reviewed; compliance checks documented; risks accepted or assigned. |
| Phase 4 — Deploy to Azure | Deployment succeeds in target env; smoke tests pass; app config verified in Azure; rollback path ready; status reflects deployed state. |
| Phase 5 — Setup CI/CD | Pipeline runs end-to-end; promotion gates defined; secrets handled securely; deployment repeatable; failure handling configured. |
| Phase 6 — Post-Migration Ops | Dashboards/alerts/runbooks exist; health signals connected; perf baseline captured; cost guardrails defined; operational ownership clear. |
| Phase-Rollback | Trigger conditions defined; rollback steps rehearsable; data integrity checks specified; communications plan exists; post-rollback validation documented. |
| QuickAssessment | Scope, complexity, recommended landing zone summarized; go/no-go explicit; next command identified. |
| CostOptimization | Cost drivers identified; right-sizing actions prioritized; every recommendation includes $/month savings; no recommendation violates reliability or security. |
| GetStatus | Report-Status current enough to guide next action; blockers/risks/owners/next-step visible. |
| Debug-Migration | Repro steps, failing phase, likely root cause, recommended fix path captured. |

## Auto-Routing Triggers (universal)

| Trigger | Auto-Dispatch |
|---------|---------------|
| New application enters the system without a Discovery Dossier | **Discovery Engineer** |
| Scope is ambiguous or multiple prompts compete after discovery | Architect |
| Azure service selection / landing-zone / IaC design needed | Azure Specialist |
| Cost, budget, savings questions | Cost Engineer |
| Application code, API contracts, framework upgrades, config transformation must change | Coder |
| Schema evolution, data validation, migration tooling, cutover data sequencing | Database Specialist |
| Pipelines, environments, release automation, promotion flow | DevOps Engineer |
| Go-live windows, slot swaps, rollback drills, production release | Cutover Commander |
| Authentication, secret management, RBAC, perimeter exposure, compliance | Security Auditor |
| Latency, throughput, load profile, scaling | Performance Engineer |
| Dashboards, alerts, KQL, runbooks, SLOs | Observability Engineer |
| Smoke tests, validation, acceptance, regression | Tester |
| Any prompt, chatmode, routing, or skill changes | Evaluator |
| Milestone reached, significant handoff, decision needs durable context | Scribe |
| Deck / PPTX / slides / executive summary / visual reporting | Presentation Specialist |
| Application source/stack/workload cannot be classified at high confidence | **Discovery Engineer** re-run |

## Cross-Cutting Rules

- **Discovery is non-negotiable** for unknown applications. Skipping it requires the user's explicit acceptance logged in `.squad/decisions.md`.
- **Evaluator is critical** whenever prompts, chatmodes, routing rules, or skill composition changes.
- **Scribe is critical** at every milestone, decision, or meaningful handoff.
- **Tester remains the default documentation lead** for README, handoff guides, and operator-facing instructions, with Scribe supporting milestone narrative.
- **Capability Matrix is the contract.** If a Phase prompt cannot find a matrix, it must request one from the Discovery Engineer before continuing.
- Before closing any task, ask: **"Which specialist should already be in this room but isn't?"**

---

## Legacy Examples

> These are the original use-case-pinned routing tables from version 1.x. They are kept for reference and as walkthrough material. Universal Mode routing supersedes them.

### Legacy Use-Case Routing (reference)

| Use-Case | Critical Agents | Why they are critical |
|----------|-----------------|-----------------------|
| `01-ASPClassicApp` | Architect, Azure Specialist, Coder, Database Specialist, Security Auditor, Tester | Legacy platform triage, App Service + Azure SQL landing zone, code/config rewrite, data migration, auth modernization, final validation. |
| `02-NetFramework30-ASPNET-WEB` | Architect, Coder, Azure Specialist, Database Specialist, DevOps Engineer, Tester | Full-stack modernization needs architectural scoping, framework migration, App Service/Azure SQL mapping, deployment automation, validation. |
| `03-WCFNet35` | Architect, Coder, Azure Specialist, Performance Engineer, Security Auditor, Tester | WCF-to-REST conversion needs service redesign, Container Apps fit, API perf validation, security review, regression testing. |
| `04-ContosoUniversityDiPS` | Architect, Azure Specialist, Coder, Database Specialist, DevOps Engineer, Observability Engineer, Tester | Multi-component app migration needs platform decomposition, data handling, deployment orchestration, operational visibility. |
| `05-BookShop` | Database Specialist, Coder, Azure Specialist, DevOps Engineer, Cutover Commander, Performance Engineer, Tester | Data-heavy commerce flow makes schema safety, app modernization, deployment, cutover, perf, checkout-path validation critical. |
| `06-Java-API-BusReservation` | Azure Specialist, Coder, Database Specialist, DevOps Engineer, Observability Engineer, Performance Engineer, Tester | Java API modernization depends on platform fit, runtime changes, PostgreSQL migration, deployment, telemetry, throughput. |
| `07-PartsUnlimited-aspnet45` | Architect, Coder, Azure Specialist, DevOps Engineer, Security Auditor, Observability Engineer, Tester | Mature modernization needs architectural steering, app upgrade, landing zone, pipeline hardening, security review, production observability. |

These rows are a useful starting point for any **classic .NET web app migration**, but Universal Mode will derive equivalent routing automatically from the Capability Matrix.
