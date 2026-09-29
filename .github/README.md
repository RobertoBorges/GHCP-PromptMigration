# GitHub Copilot Customization for Azure Migration

This folder contains VS Code GitHub Copilot customization files for the **Code Migration Modernization Agent** — a guided workflow for migrating any legacy application (any language, any source environment) to Azure.

## 📁 Folder Structure

```
.github/
├── agents/                              # Custom agent definitions (.agent.md)
│   ├── Code-Migration-Modernization.agent.md   # Main universal migration agent
│   ├── Migration-Orchestrator.agent.md
│   ├── Discovery-Intake.agent.md
│   ├── Azure-Infrastructure.agent.md
│   ├── Security-Review.agent.md
│   ├── Cost-Optimization.agent.md
│   ├── Quick-Assessment.agent.md
│   └── Debug-Migration.agent.md
├── skills/                              # 36 agent skills (each a folder with SKILL.md)
│   │
│   │   ── Workflow skills (user-invocable via `/`) ──
│   ├── assess-any-application/         # Step 1 — universal discovery
│   ├── phase1-plan/ … phase6-post-migration-ops/
│   ├── portfolio-strategy/             # Portfolio Planning flow entry point
│   ├── phase0-multi-repo-assessment/
│   ├── build-migration-plan/  quick-assessment/  quick-triage/
│   ├── interactive-migration-interview/  team-skill-assessment/
│   ├── database-migration/  security-hardening/  cost-optimization/
│   ├── phase-rollback/  get-status/  skill-creator/
│   │
│   │   ── Knowledge skills (auto-loaded by the agent) ──
│   ├── stack-adapters/                 # 15 refs — .NET, Java, Python, Node, PHP, Go, …
│   ├── source-adapters/                # 10 refs — on-prem, AWS, GCP, Oracle, VMware, K8s, …
│   ├── workload-adapters/              # 8 refs  — web app, API, batch, event-driven, …
│   ├── azure-security-baseline/        # 8 refs  — Entra ID, Key Vault, RBAC, OWASP, …
│   ├── migration-decisions/            # 4 refs  — decision catalog + hardstop protocol
│   ├── migration-artifacts/            # 6 refs  — dossier, capability matrix, templates
│   ├── dotnet-modernization/  java-modernization/  wcf-to-rest-migration/
│   ├── azure-infrastructure/  azure-containerization/  config-transformation/
│   ├── business-logic-mapping/  migration-unit-testing/  migration-strategy-report/
│   └── rollback-strategy/
├── hooks/                               # Agent lifecycle hooks
│   ├── validation.json                 # PostToolUse: auto-validate after edits
│   ├── session-lifecycle.json          # SessionStart + Stop hooks
│   └── scripts/                        # Hook scripts (PowerShell + Bash)
│       ├── block-secrets.ps1/.sh       # Detect hardcoded credentials
│       ├── block-dangerous-commands.ps1/.sh  # Block destructive operations
│       ├── auto-validate.ps1/.sh       # Validation reminders after edits
│       ├── load-migration-state.ps1/.sh     # Inject migration + portfolio context
│       └── update-status-report.ps1/.sh     # Append session timestamps
├── copilot-instructions.md              # Repo-wide agent rules
└── README.md                            # This file
```

> **Why folders, not loose files?** Agent skills follow the
> [VS Code Agent Skills spec](https://code.visualstudio.com/docs/agent-customization/agent-skills):
> a skill is a **directory** containing `SKILL.md` with `name:` + `description:` frontmatter.
> Detail files live in `references/` and are pulled in on demand (progressive disclosure), so the
> agent only pays context cost for what it actually needs.
>
> Prompt files (`.prompt.md`) and chat modes (`.chatmode.md`) are **deprecated** by VS Code and have
> been converted to skills and `.agent.md` custom agents respectively.

## 🚀 Quick Start

### Using the Agent

1. Open Copilot Chat in VS Code
2. Pick **Code Migration Modernization Agent** from the agent picker
3. Describe your migration scenario, or run the main path in order:
   - **Assess** — characterize the app (any stack, any source)
   - **Phase 1: Plan** — assessment report + migration plan + decisions
   - **Phase 2: Migrate Code** — modernize the codebase
   - **Phase 3: Generate Infrastructure** — Bicep or Terraform
   - **Phase 4: Deploy to Azure** — deploy with `azd`
   - **Phase 5: Setup CI/CD** — configure pipelines
   - **Phase 6: Post-Migration Ops** — App Insights, alerts, runbooks

### Using skills directly

Type `/` in Copilot Chat followed by the skill name. Skill names are **lowercase-hyphen**.

**🟢 Main path (run in order):**
- `/assess-any-application` — universal discovery; produces the Discovery Dossier + Capability Matrix
- `/phase1-plan`
- `/phase2-migrate-code`
- `/phase3-generate-infra`
- `/phase4-deploy-to-azure`
- `/phase5-setup-cicd`
- `/phase6-post-migration-ops`

**🔵 Optional add-ons:**
- `/portfolio-strategy` — Portfolio Planning flow — executive Migration Strategy Report from CMDB / RVTools / DMA artifacts
- `/phase0-multi-repo-assessment` — cross-repo dependency + sequencing analysis
- `/build-migration-plan`, `/quick-assessment`, `/quick-triage`, `/interactive-migration-interview`, `/team-skill-assessment`
- `/database-migration`, `/security-hardening`, `/cost-optimization`
- `/phase-rollback`, `/get-status`, `/skill-creator`

Because agent skills are an [open standard](https://agentskills.io), the same commands work in
VS Code Copilot Chat, the GitHub Copilot CLI, and the Copilot coding agent.

## 📚 Skills Reference

Skills are auto-loaded based on context. Each skill is a folder containing:
- **`SKILL.md`** — the router: what it does, when to use it, and links to detail files
- **`references/`** — detail files pulled in on demand
- **`templates/`** — ready-to-use code templates (where applicable)

### Knowledge skills (auto-loaded, not in the `/` menu)

| Skill | Refs | Purpose |
|-------|------|---------|
| `stack-adapters` | 15 | Per-language migration guidance — .NET, Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, Scala/Kotlin, C++ Windows, Delphi/VB6, PowerBuilder, Oracle Forms + stack detection |
| `source-adapters` | 10 | Per-source-environment extraction — on-premise, AWS, GCP, Oracle DB, VMware/RVTools, Kubernetes, container registry, GitHub repo, ZIP/filesystem, unsupported-source escalation |
| `workload-adapters` | 8 | Per-workload-shape targeting — web app, API service, batch job, data pipeline, event-driven, serverless, desktop client/server, packaged app |
| `azure-security-baseline` | 8 | Entra ID, Key Vault, managed identity, RBAC least-privilege, network security, Defender/compliance, secret management, OWASP Top 10 review |
| `migration-decisions` | 4 | Decision catalog (18 canonical decisions), hardstop protocol, decisions-required template, 6 Rs strategy decision tree |
| `migration-artifacts` | 6 | Canonical output formats — Discovery Dossier, Capability Matrix, migration plan, status report, action log, handoff |
| `dotnet-modernization` | 4 | .NET Framework → .NET 10+ LTS, ASP Classic, WebForms → Razor, EF6 → EF Core |
| `migration-strategy-report` | 7 | Portfolio-level Migration Strategy Report generator (HTML executive deck) |
| `azure-infrastructure` | 3 | Bicep/Terraform via Azure Verified Modules, App Service, Container Apps |
| `java-modernization` | 1 | Java EE → Spring Boot 3.x with Java 21 |
| `azure-containerization` | 1 | Multi-stage Dockerfiles, Container Apps, AKS |
| `wcf-to-rest-migration` | 1 | WCF service → ASP.NET Core REST API |
| `config-transformation` | 1 | web.config → appsettings.json, XML → YAML/properties |
| `business-logic-mapping` | — | Track and preserve business logic during migration |
| `migration-unit-testing` | — | xUnit/NUnit/JUnit 5 patterns for post-migration validation |
| `rollback-strategy` | — | Safe rollback procedures per phase |

### Workflow skills (user-invocable via `/`)

The 20 workflow skills listed under [Using skills directly](#using-skills-directly) above.
They set `disable-model-invocation: true` so they only run when *you* ask — the agent never
fires a migration phase mid-conversation on its own.

## 🎯 Supported Migration Paths

This agent is **stack-agnostic and source-agnostic**. Discovery characterizes the application
first, then the relevant adapters are loaded.

### Source environments
On-premise · AWS · GCP · Oracle · VMware (RVTools) · Kubernetes clusters · container registries ·
GitHub repos · ZIP/filesystem drops

### Language / runtime stacks
.NET Framework & .NET Core · Java / Java EE · Python · Node.js · PHP · Ruby · Go · Perl · Rust ·
Scala / Kotlin · C++ (Windows) · Delphi / VB6 · PowerBuilder · Oracle Forms

> **Out of scope:** mainframe and midrange workloads (z/OS, IBM i / AS-400, COBOL, RPG, Natural,
> PL/I, CICS/IMS, VSAM) and SaaS-embedded code (Salesforce Apex, ServiceNow, Power Platform).
> Discovery routes these to a specialist-partner escalation playbook instead of attempting
> code-level conversion.

### Common modernization targets
> ⚠ These are **not defaults** — the target framework is always a user decision.

- .NET Framework 3.0–4.8 → .NET 10 LTS or .NET 8 LTS
- ASP.NET Web Forms / MVC → ASP.NET Core MVC / Razor Pages
- WCF Services → ASP.NET Core Web APIs
- Entity Framework 6 → Entity Framework Core
- Java EE 6–8 → Spring Boot 3.x with Java 21 (EJB → Spring Beans, JSP/Servlets → Spring MVC, JAAS → Spring Security OAuth2)
- Python 2.x → 3.12+ · Node.js ≤16 → 20/22 LTS · PHP 5/7 → 8.3+ · Ruby 2.x → 3.3+ · Go ≤1.19 → 1.22+

### Azure hosting targets
Azure App Service · Azure Container Apps · Azure Kubernetes Service · Azure Functions ·
Azure Spring Apps · Azure VMs / AVS (rehost) · Azure Data Factory / Synapse / Databricks (data pipelines)

## 📊 Reports

The agent creates and maintains reports in the `reports/` folder:
- `Report-Status.md` - Migration progress tracking
- `Application-Assessment-Report.md` - Comprehensive assessment

## 🪝 Agent Hooks

Hooks enforce guardrails deterministically at the OS level, running shell scripts at key lifecycle points. Located in `.github/hooks/`.

| Hook | Event | What It Does | Context Cost |
|------|-------|-------------|-------------|
| **Auto-Validate** | `PostToolUse` | Provides validation reminders after edits to `.bicep`, `.tf`, `.csproj`, or `Dockerfile` files | ~80 chars |
| **Load Migration State** | `SessionStart` | Reads `reports/Report-Status.md` and detects project type (`.csproj`, `pom.xml`, `web.config`, `.svc`) AND any Migration Strategy Report decks to inject concise context | ~200 chars |
| **Update Status Report** | `Stop` | Appends a session-end timestamp to `reports/Report-Status.md` for audit trail | Zero |

**Prerequisites:** Bash scripts require [`jq`](https://jqlang.github.io/jq/) for JSON parsing. PowerShell scripts use built-in `ConvertFrom-Json`.

## 🔒 Agent Guardrails

- Requires user consent before modifying Azure resources
- Prefers managed identities over connection strings
- Stores secrets in Azure Key Vault
- Uses PowerShell (pwsh) for commands
- Never stores secrets in repository

## 📖 Documentation

- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [VS Code Custom Agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Azure Verified Modules](https://azure.github.io/Azure-Verified-Modules/)
