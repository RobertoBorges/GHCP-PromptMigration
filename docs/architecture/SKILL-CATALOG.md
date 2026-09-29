# Skill Catalog

Verified against `.github/skills/` in this repository. This catalog covers all **36** skills currently on disk.

Everything the agent knows now lives in `.github/skills/`. There is no `.github/prompts/` folder and no `.github/chatmodes/` folder — VS Code deprecated prompt files for Agent Host sessions, so prompts became **workflow skills** and chat modes became **custom agents** in `.github/agents/`.

## Anatomy of a skill

```text
.github/skills/<skill-name>/
├─ SKILL.md              # always loaded when the skill matches — keep it short
└─ references/           # optional; loaded on demand (progressive disclosure)
   ├─ <topic-a>.md
   └─ <topic-b>.md
```

`SKILL.md` carries YAML frontmatter:

| Field | Meaning |
|---|---|
| `name` | Skill identifier. For workflow skills this is also the slash command. |
| `description` | When the skill applies. This is the only text the model sees before deciding to load the skill. |
| `user-invocable` | `true` → appears in the `/` menu. `false` → knowledge-only, auto-selected by description match. |
| `disable-model-invocation` | `true` on 19 of the 20 workflow skills so the model cannot silently start a phase the user did not ask for. |
| `argument-hint` | Optional placeholder text shown next to the slash command. |

`SKILL.md` stays small and routes to `references/` files only when they are needed. That progressive-disclosure pattern is why 36 skills and 71 reference files fit in a normal context window. (Three skills also ship a non-`references/` companion: an `examples/` template, a `templates/` guide, and a skill-level `README.md`.)

## Two skill classes

| Class | Count | `user-invocable` | How it is reached |
|---|---:|---|---|
| [Workflow skills](#workflow-skills-20) | 20 | `true` | The user types the slash command, or the agent recommends it as the next step |
| [Knowledge skills](#knowledge-skills-16) | 16 | `false` | Auto-selected by description match during a workflow skill's execution |

## The main path is 7 steps

Everything else in this catalog is an **optional add-on**. Run the main path in order:

```text
/assess-any-application  →  /phase1-plan  →  /phase2-migrate-code  →  /phase3-generate-infra
                         →  /phase4-deploy-to-azure  →  /phase5-setup-cicd  →  /phase6-post-migration-ops
```

---

## Workflow skills (20)

### 🟢 Main path (7)

| Slash command | Skill folder | What it does | Requires | Produces |
|---|---|---|---|---|
| `/assess-any-application` | `assess-any-application/` | Universal intake. Discovers any application — any source, any stack, any workload — and classifies it with evidence confidence labels. | Access to the app (repo, ZIP, inventory export, or interview) | `reports/Discovery-Dossier.md`<br>`reports/Capability-Matrix.yaml` |
| `/phase1-plan` | `phase1-plan/` | Produces the migration plan, the per-application assessment, and the list of architecture decisions the user must make. | Discovery Dossier + Capability Matrix | `reports/Migration-Plan.md`<br>`reports/Application-Assessment-Report.md`<br>`reports/Decisions-Required.md` |
| `/phase2-migrate-code` | `phase2-migrate-code/` | Applies the minimum code changes required to make the app Azure-compatible on the platform chosen in Phase 1. | Approved plan + all Phase 2 decisions `✅ DECIDED` | modernized source tree<br>`reports/Business-Logic-Mapping.md`<br>`reports/Media-Assets-Mapping.md` |
| `/phase3-generate-infra` | `phase3-generate-infra/` | Generates Bicep or Terraform infrastructure as code for the target architecture. | Modernized app + IaC/hosting decisions | `infra/`<br>`azure.yaml` |
| `/phase4-deploy-to-azure` | `phase4-deploy-to-azure/` | Deploys the validated project to Azure with the Azure Developer CLI and validates the release. | Reviewed `infra/` + deployment decisions | `reports/Deployment-Summary-Report.md` |
| `/phase5-setup-cicd` | `phase5-setup-cicd/` | Configures GitHub Actions or Azure DevOps pipelines for automated build and deploy. | Successful manual deployment | `.github/workflows/` or `azure-pipelines.yml`<br>`reports/cicd_setup_report.md` |
| `/phase6-post-migration-ops` | `phase6-post-migration-ops/` | Establishes monitoring, performance baselines, runbooks, and operational readiness. | Working pipeline | `reports/Post-Migration-Ops-Report.md`<br>`reports/Operational-Runbook.md` |

Every main-path skill also appends to `reports/Report-Status.md`, the migration's trace memory.

### 🔵 Alternative intakes (5)

| Slash command | Skill folder | What it does | Produces |
|---|---|---|---|
| `/build-migration-plan` | `build-migration-plan/` | Turns an approved Discovery Dossier + Capability Matrix into a finalized, evidence-backed plan with phase sequencing and quality gates. Use when you want the plan as a standalone artifact before Phase 1. | `reports/Migration-Plan.md` |
| `/quick-assessment` | `quick-assessment/` | Fast migration triage with a recommended next step. | `reports/Quick-Assessment-Report.md` |
| `/quick-triage` | `quick-triage/` | Stack-agnostic ~5-minute Go/No-Go: dominant stack, top blockers, complexity, next command. | `reports/Quick-Triage-Report.md` |
| `/interactive-migration-interview` | `interactive-migration-interview/` | Interviews you about the app, scans the codebase, and generates a phase-aware plan. Good when the source is not fully in a repo. | interview transcript + phased recommendation in `reports/Report-Status.md` |
| `/team-skill-assessment` | `team-skill-assessment/` | Scores team readiness and skill gaps against the stacks actually present in the target application(s). | `reports/Team-Skill-Assessment.md`<br>`reports/Training-Recommendations.md` |

### 🔵 Portfolio / multi-app (2)

| Slash command | Skill folder | What it does | Produces |
|---|---|---|---|
| `/portfolio-strategy` | `portfolio-strategy/` | Executive-ready Migration Strategy Report from CMDB exports, RVTools or Azure Migrate inventories, DMA output, vendor proposals, and architecture diagrams. Delegates rendering to the `migration-strategy-report` knowledge skill. | `<Customer>_Migration_Strategy_Report.html`<br>`reports/portfolio-handoff.json` |
| `/phase0-multi-repo-assessment` | `phase0-multi-repo-assessment/` | Cross-repo dependency and sequencing analysis for a business solution spanning several repositories. Run before the main path. Requires `codebase-repos.md` listing the repository URLs. | per-repo assessment notes<br>`reports/Report-Status.md` |

### 🔵 Specialized deep-dives (3)

| Slash command | Skill folder | What it does | Produces |
|---|---|---|---|
| `/database-migration` | `database-migration/` | Plans database migration, validation, and cutover for Azure targets. Hard-gated on the database-engine and data-migration-tool decisions. | `reports/Decision-Log.md`<br>`reports/Report-Status.md` |
| `/security-hardening` | `security-hardening/` | Applies security hardening guidance for Azure migration targets. Can be run between any two phases as a gate. | `reports/Security-Hardening-Report.md` |
| `/cost-optimization` | `cost-optimization/` | Identifies Azure cost risks and optimization opportunities through the Cost Engineer role. | `reports/Cost-Optimization-Report.md` |

### 🔵 Utility / recovery (2)

| Slash command | Skill folder | What it does | Produces |
|---|---|---|---|
| `/phase-rollback` | `phase-rollback/` | Defines rollback strategy, triggers, and recovery steps. Reads the `rollback-strategy` knowledge skill. | `reports/Rollback-Execution-Plan.md`<br>`reports/Rollback-Validation-Report.md`<br>`reports/Rollback-Communications.md`<br>`reports/Post-Mortem-Analysis.md` |
| `/get-status` | `get-status/` | Summarizes migration progress, blockers, and the next recommended command from `reports/Report-Status.md`. | refreshed `reports/Report-Status.md` |

### 🧠 Skill authoring (1)

| Slash command | Skill folder | What it does | References |
|---|---|---|---|
| `/skill-creator` | `skill-creator/` | Creates a new skill when discovery or planning finds an uncovered stack, source environment, workload pattern, integration, or risk. Also auto-invoked by `/assess-any-application` and `/phase1-plan` when the Capability Matrix contains a value with no matching adapter. | `skill-anatomy.md`<br>`skill-template.md` |

---

## Knowledge skills (16)

These never appear in the `/` menu. The agent loads them when their `description` matches the work in front of it, then opens individual `references/` files on demand.

### Routers — universal classification (3)

| Skill | References | Routes on |
|---|---:|---|
| `stack-adapters` | 15 | Language/runtime evidence. Start at `stack-detection.md` when the stack is unknown, conflicting, or polyglot. Adapters: `.NET`, `Java`, `Node.js`, `Python`, `PHP`, `Ruby`, `Go`, `Rust`, `Perl`, `Scala/Kotlin`, `C++ (Windows)`, `Delphi/VB6`, `PowerBuilder`, `Oracle Forms`. |
| `source-adapters` | 10 | Where the app lives today: `on-premise`, `aws`, `gcp`, `oracle-db`, `vmware-rvtools`, `kubernetes-cluster`, `container-registry`, `github-repo`, `zip-filesystem`, plus `unsupported-escalation`. |
| `workload-adapters` | 8 | How the app runs: `webapp`, `api-service`, `batch-job`, `data-pipeline`, `event-driven`, `serverless`, `desktop-client-server`, `packaged-app`. |

> **Out of scope, by design.** `source-unsupported-escalation.md` is the landing point for mainframe and midrange workloads (z/OS, z/VSE, IBM i / AS-400, COBOL, RPG, Natural, PL/I, CICS, IMS, VSAM) and for SaaS-embedded code (Salesforce Apex, ServiceNow, SharePoint, Power Platform, SAP extensions). This tool does not attempt code-level migration for those; the reference is a specialist-partner escalation playbook.

### Governance and artifacts (2)

| Skill | References | Purpose |
|---|---:|---|
| `migration-decisions` | 4 | The binding decision-gate router. `decision-hardstop.md` is the protocol, `decision-catalog.md` holds the 18 canonical decisions, `decisions-required-template.md` is the output shape, `migration-strategy-decision-tree.md` derives the recommended strategy. **Architecture decisions belong to the user, never the agent.** |
| `migration-artifacts` | 6 | Canonical output artifacts and handoffs: `discovery-dossier-template.md`, `capability-matrix.md`, `migration-plan-template.md`, `migration-report-template.md`, `action-log-format.md`, `migration-handoff.md`. |

### Azure platform (3)

| Skill | References | Purpose |
|---|---:|---|
| `azure-security-baseline` | 8 | Identity, secrets, network, RBAC, compliance, OWASP: `azure-entra-id.md`, `azure-keyvault-secrets.md`, `azure-network-security.md`, `azure-defender-compliance.md`, `managed-identity.md`, `rbac-least-privilege.md`, `secret-management.md`, `owasp-top10-review.md`. |
| `azure-infrastructure` | 3 | Bicep and Terraform patterns with Azure Verified Modules: `bicep-modules.md`, `azure-app-service.md`, `azure-container-apps.md`. |
| `azure-containerization` | 1 | Multi-stage Dockerfiles, compose, Container Apps config, health checks, resource limits: `docker-containerize.md`. |

### Stack-specific modernization (4)

| Skill | References | Applies when |
|---|---:|---|
| `dotnet-modernization` | 4 | Stack is `dotnet`: `asp-classic-to-dotnet.md`, `dotnet-framework-to-dotnet8.md`, `webforms-to-razor.md`, `ef-migration.md`. |
| `wcf-to-rest-migration` | 1 | Stack is `dotnet` **and** workload is `api-service` with `.svc` / `ServiceContract` evidence: `wcf-to-rest-api.md`. Also ships `templates/WcfMigrationGuide.md`. |
| `java-modernization` | 1 | Stack is `java`: `java8-to-java21.md`. |
| `config-transformation` | 1 | Legacy config files need cloud-native form: `config-transformation-patterns.md`. |

### Cross-cutting practice (4)

| Skill | References | Purpose |
|---|---:|---|
| `migration-strategy-report` | 7 | Renders the portfolio HTML deck: `classification-algorithm.md`, `style-guide.md`, `slides-common.md`, `slides-application-pillar.md`, `slides-database-pillar.md`, `slides-infrastructure-pillar.md`, `pptx-generation.md`. Also ships its own `README.md`. |
| `business-logic-mapping` | 0 | Extracts business rules and maps them source → target so nothing is silently lost. Stack-agnostic. Ships `examples/Business-Logic-Mapping-Template.md`. |
| `migration-unit-testing` | 0 | Test patterns that prove the migration preserved behavior. xUnit/NUnit, JUnit 5, and equivalents per stack. |
| `rollback-strategy` | 0 | Slot swaps, Container Apps revisions, database reversal, DNS cutover, and recovery ordering. |

---

## Custom agents

`.github/agents/` holds **9** `*.agent.md` custom agents. They set the persona, tool allow-list, and routing posture; skills supply the procedure.

| Agent | Leads | Typical entry skills |
|---|---|---|
| `Migration-Orchestrator` | End-to-end routing, gates, portfolio visibility | any workflow skill |
| `Discovery-Intake` | Universal intake and classification | `/assess-any-application`, `/quick-triage` |
| `Code-Migration-Modernization` | The general migration agent surface | any workflow skill |
| `Code-Modernization-Specialist` | Phase 2 code work only | `/phase2-migrate-code`, `/database-migration` |
| `Azure-Infrastructure` | Phase 3 IaC, identity, networking | `/phase3-generate-infra` |
| `Quick-Assessment` | Fast triage and effort sizing | `/quick-assessment` |
| `Security-Review` | Security posture as a phase gate | `/security-hardening` |
| `Cost-Optimization` | Spend, capacity, scaling | `/cost-optimization` |
| `Debug-Migration` | Root-cause across build, runtime, infra, deploy | `/get-status`, any failing phase |

## Notes

- **Slash commands are lowercase-hyphen** and match the skill folder name exactly. `/phase0-multi-repo-assessment` matches `phase0-multi-repo-assessment/`.
- **19 of the 20 workflow skills set `disable-model-invocation: true`.** The agent can recommend a phase but cannot silently start one. `/skill-creator` is the one exception, because discovery legitimately needs to fill an adapter gap mid-run.
- **Knowledge skills are never listed in the `/` menu.** If you want to read one, open the file — do not try to invoke it.
- **Reference files are not skills.** They have no frontmatter and are only opened by their parent `SKILL.md`.
- **Target framework versions are never defaults.** Every version target is a user decision recorded in `reports/Decisions-Required.md`. See `.github/skills/migration-decisions/references/decision-catalog.md`.

## See also

- [Architecture](./ARCHITECTURE.md) — how skills, agents, hooks, and artifacts fit together
- [Skills map](../guides/skills-map.md) — which skills apply to which phase and scenario
- [Handoff protocol](../guides/handoff-protocol.md) — artifact contracts between phases
- [VS Code quickstart](../vscode-quickstart.md) — install and run your first migration
