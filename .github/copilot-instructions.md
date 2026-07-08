# Azure Migration Project Guidelines

These instructions apply to all GitHub Copilot interactions within this repository.

## Project Purpose (Universal Mode)

This repository is a **universal application-to-Azure migration system**. It can assess, modernize, and migrate **any application** — regardless of source environment (on-premise, AWS, GCP, Oracle, VMware, Kubernetes, container registry, GitHub repo, ZIP, mainframe) or stack (.NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, COBOL, Oracle Forms, PowerBuilder, Delphi/VB6, Scala/Kotlin, C++ Windows, and more) — into Azure.

The system supports **three complementary flows**:

1. **Per-Application Modernization Flow (default, main path)** — Guided execution of ONE application at a time via **`/Phase1-PlanAndAssess` → `/Phase2-MigrateCode` → `/Phase3-GenerateInfra` → `/Phase4-DeployToAzure` → `/Phase5-SetupCICD` → `/Phase6-PostMigrationOps`**. Stack-agnostic: Phase prompts consume the Capability Matrix produced by Discovery and apply the right stack/source/workload-specific guidance via skills. Phase 1 will route to `/assess-any-application` and `/build-migration-plan` automatically if their artifacts are missing.

2. **Portfolio Planning Flow (pre-engagement, optional add-on)** — Generates executive-ready Migration Strategy Reports from CMDB / RVTools / DMA / mixed customer artifacts. Produces a CIO-level HTML deck with CAF-aligned 6 Rs classification and Factory / ISD-Partner / Unknown execution ownership. Invoke with `/PortfolioStrategy` or use the `migration-strategy-report` skill.

3. **Universal Discovery Preview (optional add-on)** — `/assess-any-application` runs standalone Discovery producing `reports/Discovery-Dossier.md` + `reports/Capability-Matrix.yaml` without committing to Phase 1's full assessment. Useful for a preview before the main path.

The seven legacy use-cases (`01-ASPClassicApp` … `07-PartsUnlimited`) remain in the repository as **reference walkthroughs**, not as a fixed catalog.

## Main path vs optional add-ons

The default migration flow is **6 phases** run in order. Everything else is an **optional add-on** offered when the user has a specific specialized need.

### 🟢 Main path (default — 6 phases)

Present these first. Run in order.

| # | Phase | Command |
|---|-------|---------|
| 1 | Plan & Assess | `/Phase1-PlanAndAssess` |
| 2 | Migrate Code | `/Phase2-MigrateCode` |
| 3 | Generate Infra | `/Phase3-GenerateInfra` |
| 4 | Deploy | `/Phase4-DeployToAzure` |
| 5 | Setup CI/CD | `/Phase5-SetupCICD` |
| 6 | Post-Migration Ops | `/Phase6-PostMigrationOps` |

### 🔵 Optional add-ons (offer only when relevant)

**Alternative intakes** — `/assess-any-application`, `/build-migration-plan`, `/QuickAssessment`, `/QuickTriage`, `/InteractiveMigrationInterview`, `/TeamSkillAssessment`
**Portfolio / multi-app** — `/PortfolioStrategy`, `/Phase0-Multi-repo-assessment`
**Specialized deep-dives** — `/DatabaseMigration`, `/SecurityHardening`, `/CostOptimization`
**Utility / recovery** — `/Phase-Rollback`, `/GetStatus`

**Agent behavior:**
- When a user starts a new migration, recommend the **main path** (Phase 1 first). Do NOT lead with `/assess-any-application` unless the user explicitly asks for a Discovery preview.
- Only surface add-ons when the user's question maps to one (e.g., "how do I move the DB?" → suggest `/DatabaseMigration`).
- The natural-language mapping table below still maps ALL commands so users can type any of them — but presentation should always foreground the main path.

## How to Invoke the Agent (CLI vs Chat)

**The Code Migration Modernization Agent (`.github/agents/Code-Migration-Modernization.agent.md`) is invokable on two surfaces:**

| Surface | How to invoke |
|---------|---------------|
| **GitHub Copilot CLI** (the `copilot` terminal command) | **Use natural language.** Slash commands like `/assess-any-application` are NOT registered as CLI commands — they are reference labels. Just say what you want. |
| **VS Code Copilot Chat** | Slash commands ARE registered. Type `/assess-any-application` directly. |

### Natural-language → action mapping (for CLI users)

When the user says any of the phrases below, take the matching action. **Rows are ordered main-path first, then add-ons.**

| User says (any of) | Action |
|---|---|
| **🟢 Main path (Phase 1-6)** | |
| "phase 1", "plan and assess", "start migration", "assess this app", "/phase1-planandassess" | Read `.github/prompts/Phase1-PlanAndAssess.prompt.md`. Phase 1 will route to `/assess-any-application` + `/build-migration-plan` first if their artifacts are missing. |
| "phase 2", "migrate code", "/phase2-migratecode" | Read `.github/prompts/Phase2-MigrateCode.prompt.md` |
| "phase 3", "generate infra", "/phase3-generateinfra" | Read `.github/prompts/Phase3-GenerateInfra.prompt.md` |
| "phase 4", "deploy to azure", "/phase4-deploytoazure" | Read `.github/prompts/Phase4-DeployToAzure.prompt.md` |
| "phase 5", "setup cicd", "/phase5-setupcicd" | Read `.github/prompts/Phase5-SetupCICD.prompt.md` |
| "phase 6", "post-migration ops", "/phase6-postmigrationops" | Read `.github/prompts/Phase6-PostMigrationOps.prompt.md` |
| **🔵 Alternative intakes (add-ons)** | |
| "assess any application", "discover this app", "characterize this application", "scan this repo", "/assess-any-application", "run discovery" | Read `.github/prompts/Assess-Any-Application.prompt.md` and follow it. Produce `reports/Discovery-Dossier.md` + `reports/Capability-Matrix.yaml`. |
| "build migration plan", "approve discovery", "build the plan", "make the migration plan", "/build-migration-plan" | Read `.github/prompts/Build-Migration-Plan.prompt.md`. Produce `reports/Migration-Plan.md`. Requires Discovery Dossier + Capability Matrix to already exist. |
| "quick assessment", "/quickassessment", "quick triage", "/quicktriage" | Read the matching prompt |
| "interview me", "/InteractiveMigrationInterview" | Read `.github/prompts/InteractiveMigrationInterview.prompt.md` |
| "team skill assessment", "/TeamSkillAssessment" | Read `.github/prompts/TeamSkillAssessment.prompt.md` |
| **🔵 Portfolio / multi-app (add-ons)** | |
| "portfolio strategy", "/PortfolioStrategy", "analyze portfolio", "CMDB analysis", "RVTools analysis", "migration strategy report" | Read `.github/prompts/PortfolioStrategy.prompt.md` and the `migration-strategy-report` skill |
| "phase 0", "multi-repo assessment", "/phase0-multi-repo-assessment" | Read `.github/prompts/Phase0-Multi-repo-assessment.prompt.md` |
| **🔵 Specialized deep-dives (add-ons)** | |
| "database migration", "/databasemigration", "migrate the database" | Read `.github/prompts/DatabaseMigration.prompt.md` |
| "security hardening", "/securityhardening", "harden security" | Read `.github/prompts/SecurityHardening.prompt.md` |
| "cost optimization", "/costoptimization", "optimize cost" | Read `.github/prompts/CostOptimization.prompt.md` |
| **🔵 Utility / recovery (add-ons)** | |
| "rollback", "phase rollback", "/phase-rollback" | Read `.github/prompts/Phase-Rollback.prompt.md` |
| "status", "/getstatus", "show migration status" | Read `.github/prompts/GetStatus.prompt.md` and consult `reports/Report-Status.md` |

**If the user types a slash command that isn't in the table above, look for a matching file at `.github/prompts/<command-no-slash>.prompt.md` (case-insensitive) and read it.**

## Universal Discovery Contract

For any application that does not already have a Capability Matrix:

1. **Run discovery first.** Use `/assess-any-application` or the `Discovery-Intake` chatmode.
2. **Capture evidence with confidence labels.** Every classification (`source`, `stack`, `workload`, `data`, `integrations`) must have `evidence_confidence: high | medium | low`.
3. **Produce a Discovery Dossier.** Path: `reports/Discovery-Dossier.md`. Structure defined by `.github/skills/discovery-dossier-template.md`.
4. **Produce a Capability Matrix.** Path: `reports/Capability-Matrix.yaml`. Schema defined by `.github/skills/capability-matrix.md`.
5. **Recommend a migration strategy** using `.github/skills/migration-strategy-decision-tree.md` (6Rs is one output field; the decision tree weighs business priority, source constraints, code mutability, data gravity, integration complexity, target Azure options, cutover constraints, modernization depth, and team readiness).
6. **Phase prompts consume the Capability Matrix.** They do NOT re-do classification. If a Phase prompt cannot find a matrix, it must request one before continuing.

## Migration Scope

### What This Project Does ✅
- **Universal intake & discovery** for applications from any source environment and any stack
- **Portfolio assessment** of customer estates (apps + databases + infrastructure)
- **Deterministic classification** via the migration-strategy-decision-tree (6 Rs strategy + Factory/Partner/Unknown ownership where applicable)
- **Code modernization** for any supported stack (see list above) to current Azure-compatible runtimes
- **Lift-and-shift (rehost)** when the decision tree says so — supported for applications where modernization is out of scope or out of budget
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

### 🛑 Architecture decisions belong to the user — NEVER the agent

The agent does **not** decide major architecture on the user's behalf. It lays out options with tradeoffs and waits.

- Read [`.github/skills/decision-hardstop.md`](./skills/decision-hardstop.md) — the binding protocol
- Consult [`.github/skills/decision-catalog.md`](./skills/decision-catalog.md) — the 18 canonical decisions
- Phase 2-4 + DatabaseMigration prompts have hard-stop gates that block work until `reports/Decisions-Required.md` shows each required decision as `✅ DECIDED` (or `🚫 N/A`)
- **No silent defaults. No "newer is better." No expert-mode bypass.**
- Even when surfacing a recommendation, label it `⚠ Default guess` and acknowledge the user owns the choice
- Stay-as-is is always option 1 in every option block — force an active choice

Read [`.github/hooks/decision-gates.md`](./hooks/decision-gates.md) for the orchestration rules.

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

### Agent Behavior
- For unknown applications, **run discovery first** before any other work (see Universal Discovery Contract above)
- Each Phase prompt is self-contained — it reads the Capability Matrix and Decisions-Required file, applies the relevant skills, and produces named output artifacts
- When parallel work is possible (e.g., assessment + risk audit), use the `task` tool with `mode: "background"` to dispatch sub-agents

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

| Source | Common target (NOT a default) |
|--------|--------|
| .NET Framework 2.x–4.x | .NET 10 LTS or .NET 8 LTS — **user decides** |
| .NET Core 2.1 / 3.1 | .NET 10 LTS |
| Java 8 / 11 | Java 21 LTS or Java 17 LTS — **user decides** |
| Java EE 7 / 8 | Spring Boot 3.x |
| Spring 4.x / 5.x | Spring Boot 3.x |
| Python 2.x | Python 3.12+ |
| Node.js ≤ 16 | Node.js 20 LTS or Node.js 22 LTS — **user decides** |
| PHP 5.x / 7.x | PHP 8.3+ |
| Ruby 2.x | Ruby 3.3+ |
| Go ≤ 1.19 | Go 1.22+ |
| COBOL / OpenCOBOL on z/OS | Java 21 on AKS via Micro Focus / Astadia, or rebuild |
| Oracle Forms | APEX / Spring Boot rewrite, or refactor to web UI |
| Delphi / VB6 / PowerBuilder | Rebuild on .NET 10 or modern web stack |

> ⚠ The target framework is **not a default**. It is [a decision the user must make](./skills/decision-catalog.md). The table above shows common modernization targets, not a recommendation to silently apply.

## Distribution

This project ships as a **VS Code extension** at `packages/azure-migration-squad-vscode/`. The extension:

- Bundles all of `.github/{prompts,skills,chatmodes,hooks,agents,copilot-instructions.md}` into the user's workspace via the **Initialize** command
- Surfaces the prompt catalog, agent definition, skills, and pending decisions in a sidebar tree view
- Shows current migration phase in the status bar
- Auto-prompts to install GitHub Copilot Chat (with user consent)
- Reads `reports/Decisions-Required.md` to surface pending architecture decisions

There is no separate npm CLI — the extension is the only distribution path.
