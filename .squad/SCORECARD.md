# Squad Governance Scorecard — Ocean's Twelve — The Azure Heist

> Canonical scoring framework for the 14-agent squad, 21 prompts, 8 chatmodes, 23 prompt-local skills, and 7 migration targets.

## Automated Baseline

Run the structural self-check before scoring anything manually:

```bash
node .squad/eval.mjs
```

Use the automated check as the floor, not the finish line. A passing script means the control surface is wired; it does **not** guarantee the operator journey is good.

## Scoring Model

| Dimension | Weight | Passing Bar | Evidence |
|-----------|--------|-------------|----------|
| Agent coverage per use-case | 30% | Every target has a lead plus critical support agents from `.squad/routing.md` | `.squad/team.md`, `.squad/routing.md`, use-case docs |
| Prompt quality metrics | 30% | Prompt metadata, routing, hooks, skills, and next-step guidance are current | `.github/prompts/`, `.github/chatmodes/`, `.squad/eval.mjs` |
| Skill coverage | 20% | Required `.github/skills/` modules exist for each guided workflow | `.github/skills/`, prompt `#file:` references |
| Phase gate compliance | 20% | Each migration phase has explicit exit criteria and evidence expectations | `.squad/routing.md`, walkthroughs, status docs |

### Overall Grade

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100 | Green | Ready for operator use |
| 75-89 | Yellow | Usable, but drift exists and should be corrected soon |
| 60-74 | Orange | Governance gaps will confuse routing or handoffs |
| <60 | Red | Do not treat squad assets as trustworthy until corrected |

## Agent Coverage per Use-Case

| Use-Case | Source → Target | Lead Path | Critical Agents | Coverage Check |
|----------|------------------|-----------|-----------------|----------------|
| `01-ASPClassicApp` | Classic ASP → App Service + Azure SQL | `QuickAssessment` → `Phase1-PlanAndAssess` | Architect, Azure Specialist, Coder, Database Specialist, Security Auditor, Tester | Legacy hosting, auth, and data migration risks are all explicitly owned |
| `02-NetFramework30-ASPNET-WEB` | .NET Framework 3.0 → App Service + Azure SQL | `QuickAssessment` → `Phase1` → `Phase2` | Architect, Coder, Azure Specialist, Database Specialist, DevOps Engineer, Tester | Modernization, deployment automation, and validation are covered |
| `03-WCFNet35` | WCF .NET 3.5 → Container Apps + REST API | `QuickAssessment` → `Phase2-MigrateCode` | Architect, Coder, Azure Specialist, Performance Engineer, Security Auditor, Tester | Service redesign, API security, and performance have named owners |
| `04-ContosoUniversityDiPS` | ASP.NET MVC → App Service + Azure SQL | `QuickAssessment` → `Phase1` → `Phase4` | Architect, Azure Specialist, Coder, Database Specialist, DevOps Engineer, Observability Engineer, Tester | Multi-component migration includes deployment and ops ownership |
| `05-BookShop` | .NET 3.5 WebForms → Container Apps + Azure SQL | `QuickAssessment` → `Phase2` → `Phase-Rollback` | Database Specialist, Coder, Azure Specialist, DevOps Engineer, Cutover Commander, Performance Engineer, Tester | Commerce/data-heavy flow includes cutover and perf accountability |
| `06-Java-API-BusReservation` | Java 8 API → Container Apps + PostgreSQL | `QuickAssessment` → `Phase1` → `Phase6` | Azure Specialist, Coder, Database Specialist, DevOps Engineer, Observability Engineer, Performance Engineer, Tester | Java runtime, PostgreSQL, deployment, and telemetry are all assigned |
| `07-PartsUnlimited-aspnet45` | ASP.NET 4.5 → App Service + Azure SQL | `QuickAssessment` → `Phase1` → `Phase5` | Architect, Coder, Azure Specialist, DevOps Engineer, Security Auditor, Observability Engineer, Tester | Mature app path includes security, ops, and release readiness |

## Prompt Quality Metrics

| Metric | Pass Condition | How to Score |
|--------|----------------|--------------|
| Metadata integrity | Prompt/chatmode frontmatter is present and roster-aligned | 0 = missing metadata, 1 = partial, 2 = complete |
| Routing fidelity | Lead agent and support agents match `.squad/routing.md` | 0 = drift, 1 = partially aligned, 2 = aligned |
| Hook coverage | Required orchestration hooks are referenced where expected | 0 = missing, 1 = inconsistent, 2 = consistent |
| Skill reference hygiene | Prompt references point at authoritative `.github/skills/` assets | 0 = stale paths, 1 = mixed, 2 = canonical |
| CLI follow-through | Next-step guidance uses current CLI-first flow (`@squad`) when operator-facing | 0 = stale, 1 = mixed, 2 = current |
| Output contract quality | Required report sections, gates, and next commands are explicit | 0 = vague, 1 = partial, 2 = explicit |
| Roster alignment | Agent names reflect the live 14-agent squad | 0 = stale identity, 1 = partial, 2 = current |
| Regression evidence | A change was validated by `node .squad/eval.mjs` plus spot checks | 0 = no evidence, 1 = partial, 2 = verified |

**Prompt quality target:** 14/16 or better before treating prompt changes as complete.

## Skill Coverage

| Coverage Area | Required Skills | Primary Prompts / Chatmodes | Coverage Goal |
|---------------|-----------------|-----------------------------|---------------|
| Platform modernization | `asp-classic-to-dotnet`, `dotnet-framework-to-dotnet8`, `java8-to-java21`, `webforms-to-razor`, `wcf-to-rest-api` | Assessment prompts, `Phase2-MigrateCode`, `Code-Migration-Modernization` | Every legacy stack has a canonical migration skill |
| Hosting and infrastructure | `azure-app-service`, `azure-container-apps`, `bicep-modules`, `docker-containerize`, `config-transformation` | `Phase3-GenerateInfra`, `Azure-Infrastructure`, deployment phases | Every target landing zone has IaC and hosting guidance |
| Data, identity, and security | `ef-migration`, `azure-entra-id`, `managed-identity`, `rbac-least-privilege`, `azure-keyvault-secrets`, `azure-network-security`, `azure-defender-compliance`, `owasp-top10-review`, `secret-management` | `DatabaseMigration`, `SecurityHardening`, `Phase1`, `Phase5` | Data and security concerns are never implicit |
| Delivery and resilience | `migration-handoff`, `rollback-strategy`, `migration-report-template` | `GetStatus`, `Phase-Rollback`, walkthroughs | Operators can hand off, report status, and recover safely |
| Visual communication | `pptx-generation` | Presentation and stakeholder-facing workstreams | Presentation work has an explicit skill owner |

## Phase Gate Compliance

| Prompt / Phase | Gate Focus | Evidence Required |
|----------------|------------|-------------------|
| `QuickAssessment` | Go/no-go triage | Scope, complexity, landing zone, next command |
| `Phase0-Multi-repo-assessment` | Portfolio inventory | Repo inventory, blockers, priorities, ownership |
| `Phase1-PlanAndAssess` | Architecture readiness | Target platform, risks, success criteria |
| `Phase2-MigrateCode` | Code migration readiness | Build/validation status, config/auth changes, regression notes |
| `DatabaseMigration` | Data cutover readiness | Schema path, validation queries, backup/cutover plan |
| `Phase3-GenerateInfra` | IaC readiness | Runnable deployment instructions, identity/network choices |
| `SecurityHardening` | Security review completion | Auth, secrets, RBAC, network exposure, accepted risks |
| `Phase4-DeployToAzure` | Deployment readiness | Successful deployment, smoke tests, rollback path |
| `Phase5-SetupCICD` | Automation readiness | Repeatable pipeline, secure secrets flow, notifications |
| `Phase6-PostMigrationOps` | Operations readiness | Dashboards, alerts, runbooks, baseline, cost guardrails |
| `Phase-Rollback` | Recovery readiness | Trigger conditions, rehearsable rollback, validation checks |
| `CostOptimization` | Cost governance | Current drivers, right-sizing actions, budget guardrails |
| `GetStatus` | Operator visibility | Current blocker, owner, risk, next step |

## Review Cadence

- Re-run `node .squad/eval.mjs` after any prompt, chatmode, routing, roster, or governance-doc change.
- Re-score the four dimensions after any phase-definition change or new use-case addition.
- Treat any stale squad identity, missing use-case coverage, or broken prompt reference as a scorecard defect.
- Update this scorecard whenever the squad roster, prompt catalog, or phase gates change.

