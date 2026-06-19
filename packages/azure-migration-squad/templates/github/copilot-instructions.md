# Azure Migration Project Guidelines

These instructions apply to all GitHub Copilot interactions within this repository.

## Project Purpose (Universal Mode — 2026-06-01)

This repository is a **universal application-to-Azure migration system**. It can assess, modernize, and migrate **any application** — regardless of source environment (on-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registry, GitHub repo, ZIP, mainframe) or stack (.NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows, and more) — into Azure.

The system supports **three complementary flows**:

1. **Universal Application Migration Flow (default)** — Starts with `/assess-any-application`. The **Discovery Engineer (Saul Bloom Jr.)** characterizes the application's source, stack, workload pattern, data, and integrations; produces a **Discovery Dossier** and a **Capability Matrix**; recommends a migration strategy (Rehost/Replatform/Refactor/Rearchitect/Rebuild/Retire/Retain) using the `migration-strategy-decision-tree` skill; and hands off to the Architect for execution via Phases 1–6.

2. **Portfolio Planning Flow (pre-engagement)** — Generates executive-ready Migration Strategy Reports from CMDB / RVTools / DMA / mixed customer artifacts. Produces a CIO-level HTML deck with CAF-aligned 6 Rs classification and Factory / ISD-Partner / Unknown execution ownership. Invoke with `/PortfolioStrategy` or use the `migration-strategy-report` skill.

3. **Per-Application Modernization Flow (Phases 1–5, optionally Phase 0)** — Guided execution of ONE application at a time. Now **stack-agnostic**: Phase prompts consume the Capability Matrix produced by Discovery and inject the right stack/source/workload-specific guidance via skills.

The seven legacy use-cases (`01-ASPClassicApp` … `07-PartsUnlimited`) remain in the repository as **reference walkthroughs**, not as a fixed catalog.

## How to Invoke the Squad (CLI vs Chat)

**This squad is invokable in two surfaces:**

| Surface | How to invoke |
|---------|---------------|
| **GitHub Copilot CLI** (the `copilot` terminal command) | **Use natural language.** Slash commands like `/assess-any-application` are NOT registered as CLI commands — they are reference labels. Just say what you want. |
| **VS Code Copilot Chat** | Slash commands ARE registered. Type `/assess-any-application` directly. |

### Natural-language → squad action mapping (for CLI users)

When the user says any of the phrases below, dispatch the matching action:

| User says (any of) | Action |
|---|---|
| "assess this application", "assess any application", "discover this app", "discover this application", "what is this app", "characterize this application", "scan this repo", "/assess-any-application", "azure migration of this app" | Dispatch **Discovery Engineer**. Read `.github/prompts/Assess-Any-Application.prompt.md` and follow it. Produce `reports/Discovery-Dossier.md` + `reports/Capability-Matrix.yaml`. |
| "build migration plan", "approve discovery", "build the plan", "make the migration plan", "/build-migration-plan" | Dispatch **Architect**. Read `.github/prompts/Build-Migration-Plan.prompt.md`. Produce `reports/Migration-Plan.md`. Requires Discovery Dossier + Capability Matrix to already exist. |
| "phase 1", "plan and assess", "/phase1-planandassess" | Read `.github/prompts/Phase1-PlanAndAssess.prompt.md` |
| "phase 2", "migrate code", "/phase2-migratecode" | Read `.github/prompts/Phase2-MigrateCode.prompt.md` |
| "phase 3", "generate infra", "/phase3-generateinfra" | Read `.github/prompts/Phase3-GenerateInfra.prompt.md` |
| "phase 4", "deploy to azure", "/phase4-deploytoazure" | Read `.github/prompts/Phase4-DeployToAzure.prompt.md` |
| "phase 5", "setup cicd", "/phase5-setupcicd" | Read `.github/prompts/Phase5-SetupCICD.prompt.md` |
| "phase 6", "post-migration ops", "/phase6-postmigrationops" | Read `.github/prompts/Phase6-PostMigrationOps.prompt.md` |
| "portfolio strategy", "/PortfolioStrategy", "analyze portfolio", "CMDB analysis", "RVTools analysis", "migration strategy report" | Read `.github/prompts/PortfolioStrategy.prompt.md` and the `migration-strategy-report` skill |
| "phase 0", "multi-repo assessment", "/phase0-multi-repo-assessment" | Read `.github/prompts/Phase0-Multi-repo-assessment.prompt.md` |
| "database migration", "/databasemigration", "migrate the database" | Read `.github/prompts/DatabaseMigration.prompt.md` |
| "security hardening", "/securityhardening", "harden security" | Read `.github/prompts/SecurityHardening.prompt.md` |
| "cost optimization", "/costoptimization", "optimize cost" | Read `.github/prompts/CostOptimization.prompt.md` |
| "quick assessment", "/quickassessment", "quick triage", "/quicktriage" | Read the matching prompt |
| "rollback", "phase rollback", "/phase-rollback" | Read `.github/prompts/Phase-Rollback.prompt.md` |
| "status", "/getstatus", "show migration status" | Read `.github/prompts/GetStatus.prompt.md` and consult `reports/Report-Status.md` |
| "interview me", "/InteractiveMigrationInterview" | Read `.github/prompts/InteractiveMigrationInterview.prompt.md` |
| "team skill assessment", "/TeamSkillAssessment" | Read `.github/prompts/TeamSkillAssessment.prompt.md` |

**If the user types a slash command that isn't in the table above, look for a matching file at `.github/prompts/<command-no-slash>.prompt.md` (case-insensitive) and read it.**



## Universal Discovery Contract

For any application that does not already have a Capability Matrix:

1. **Run discovery first.** Use `/assess-any-application` or the `Discovery-Intake` chatmode.
2. **Capture evidence with confidence labels.** Every classification (`source`, `stack`, `workload`, `data`, `integrations`) must have `evidence_confidence: high | medium | low`.
3. **Produce a Discovery Dossier.** Path: `reports/Discovery-Dossier.md`. Structure defined by `.github/skills/discovery-dossier-template.md`.
4. **Produce a Capability Matrix.** Path: `reports/Capability-Matrix.yaml`. Schema defined by `.github/skills/capability-matrix.md`.
5. **Recommend a migration strategy** using `.github/skills/migration-strategy-decision-tree.md` (6Rs is one output field; the decision tree weighs business priority, source constraints, code mutability, data gravity, integration complexity, target Azure options, cutover constraints, modernization depth, and team readiness).
6. **Hand off to Architect.** Architect approves/refines the strategy and finalizes the target Azure architecture and execution sequence.
7. **Phase prompts consume the Capability Matrix.** They do NOT re-do classification. If a Phase prompt cannot find a matrix, it must request one from Discovery before continuing.

## Migration Scope

### What This Project Does ✅
- **Universal intake & discovery** for applications from any source environment and any stack
- **Portfolio assessment** of customer estates (apps + databases + infrastructure)
- **Deterministic classification** via the migration-strategy-decision-tree (6 Rs strategy + Factory/Partner/Unknown ownership where applicable)
- **Code modernization** for any supported stack (see list above) to current Azure-compatible runtimes
- **Lift-and-shift (rehost)** when the decision tree says so — this is supported under Universal Mode for applications where modernization is out of scope or out of budget
- **Replatform / refactor / rearchitect / rebuild** as appropriate
- Converts WCF services to REST APIs (when stack is `dotnet` and workload is `api-service`)
- Transforms legacy configuration (web.config → appsettings.json, application.xml → application.yml, etc.)
- Generates Infrastructure as Code (Bicep / Terraform)
- Sets up CI/CD pipelines for Azure deployment
- Modernizes authentication to Entra ID
- Escalates **SaaS-embedded** apps (Salesforce Apex, ServiceNow, SharePoint, Power Platform, SAP extensions) to a `source-unsupported-escalation` path with a manual playbook

### What This Project Does NOT Do ❌
- **Data Migration tooling** itself — recommends and orchestrates Azure DMS / DMA but does not replace them
- **Binary/dependency scanning of compiled artifacts** — recommends .NET Upgrade Assistant or equivalent external tools for that
- **Wholesale replacement of SaaS-embedded code** — escalates to specialist (not a Copilot-only task)

## Always Apply These Rules

### Security
- Prefer managed identities over connection strings and keys
- Store secrets in Azure Key Vault with RBAC (no access policies)
- Do not query or modify Azure resources without explicit user consent
- Never store secrets in the repository

### Commands and Tools
- Use PowerShell (pwsh) for all shell commands
- Use Azure Developer CLI (azd) for deployments
- Use Azure Verified Modules (AVM) for Bicep templates

### Documentation
- Track migration progress in `reports/Report-Status.md`
- Generate assessment artifacts in `reports/Discovery-Dossier.md` + `reports/Capability-Matrix.yaml`
- Generate per-application reports in `reports/Application-Assessment-Report.md`
- Use Mermaid diagrams for architecture visualization
- Format reports with clear headings, tables, and checklists

### Code Changes
- Read 2000 lines of code at a time for sufficient context
- Make small, testable, incremental changes
- Validate changes with `get_errors` after each major step
- Do not modify code unless the change can be confidently verified

### Squad Behavior
- For unknown applications, **dispatch the Discovery Engineer first** before any other specialist
- Honor the **Discovery Engineer / Architect boundary**: Discovery owns evidence and classification; Architect owns final target architecture and sequence
- Use `task` tool with `mode: "background"` to dispatch parallel sub-agents
- Read `.squad/team.md`, `.squad/routing.md`, and `.squad/decisions.md` on every substantive session

## Target Platforms

| Platform | Best For |
|----------|----------|
| Azure App Service | Web apps, APIs, quick deployment, PaaS simplicity |
| Azure Container Apps | Microservices, event-driven apps, serverless containers, batch jobs |
| Azure Kubernetes Service (AKS) | Complex orchestration, multi-container workloads, existing K8s sources |
| Azure Functions | Serverless, event-driven, low-traffic APIs |
| Azure VMs / AVS | Rehost when modernization is out of scope; Oracle/legacy Windows workloads |
| Azure Spring Apps | Java/Spring workloads with managed runtime |
| Azure Data Factory / Synapse / Databricks | Data pipelines, ETL/ELT |

## Framework Version Targets (when modernization is in scope)

| Source | Target |
|--------|--------|
| .NET Framework 2.x–4.x | .NET 10 LTS |
| .NET Core 2.1 / 3.1 | .NET 10 LTS |
| Java 8 / 11 | Java 21 LTS |
| Java EE 7 / 8 | Spring Boot 3.x |
| Spring 4.x / 5.x | Spring Boot 3.x |
| Python 2.x | Python 3.12+ |
| Node.js ≤ 16 | Node.js 20 LTS |
| PHP 5.x / 7.x | PHP 8.3+ |
| Ruby 2.x | Ruby 3.3+ |
| Go ≤ 1.19 | Go 1.22+ |
| COBOL / OpenCOBOL on z/OS | Java 21 on AKS via Micro Focus / Astadia, or rebuild |
| Oracle Forms | APEX / Spring Boot rewrite, or refactor to web UI |
| Delphi / VB6 / PowerBuilder | Rebuild on .NET 10 or modern web stack |

---

## Squad Orchestration (Optional, Additive)

> The repository has been augmented with a squad-orchestration layer derived from the [snap-squad](https://github.com/paulyuk/snap-squad) framework.
> The original prompt-based, phase-driven workflow above remains the **primary path**.
> The squad layer below is **opt-in** and provides multi-agent orchestration for teams that prefer it.

When operating in squad mode (i.e., when the user invokes .squad/ workflows, chatmodes, or routes through `Migration-Orchestrator`):

1. Read `AGENTS.md` at repo root for universal squad instructions
2. Read `CLAUDE.md` at repo root for session memory and project context
3. Read `.squad/team.md` for the full team roster
4. Read `.squad/routing.md` for work routing rules
5. Check `.squad/decisions.md` before starting work

### Squad-Aware Behavior

- Identify which squad member is best suited for the current task
- **Start every substantive response with a role tag:** `> **[AgentName]**` (see `AGENTS.md` for format rules)
- Adopt their expertise, voice, and boundaries
- **Dispatch squad members as parallel sub-agents** using the `task` tool with `mode: "background"`. Include charter context from `.squad/agents/<name>/charter.md`. See `AGENTS.md` "Squad Dispatch" section.
- Log significant decisions to `.squad/decisions.md` after completing work

### Proactive Quality Triggers (squad mode)

| Trigger | Action |
|---------|--------|
| Code changed | Run `npm test` before committing — never commit red |
| User-visible behavior changed | Dispatch DevRel — update docs and README |
| Prompt or agent behavior changed | Dispatch Evaluator — review eval baselines |
| Important trade-off made | Log decision to `.squad/decisions.md` |
| Meaningful milestone reached | Dispatch Scribe — update `JOURNAL.md` with what happened and why |
| Another role's expertise needed | Dispatch that role as a background sub-agent via `task` tool |
| New unknown application appears | Dispatch **Discovery Engineer** first |

### Squad Versioning

This squad was created with [snap-squad](https://github.com/paulyuk/snap-squad).
To switch presets or refresh:

```bash
npx snap-squad init --type <preset> --force    # switch to a different preset
npx snap-squad list                            # see available presets
```

Available presets: `default`, `fast`, `mentors`, `specialists`.

### When to use which mode

- **Universal Discovery flow (recommended)** — any new, unknown application. `/assess-any-application` → Discovery Dossier → Architect → Phase 1–6.
- **Portfolio flow** — customer engagement with 10+ apps.
- **Per-app prompt-based flow (legacy)** — single-developer workflows where the stack is well-known and the user explicitly wants the direct guided flow.
- **Squad orchestration** — multi-agent parallel execution, governed quality gates, complex migrations needing specialized expertise.

All modes share the same skills under `.github/skills/`, `skills/`, and the same Use-cases.

