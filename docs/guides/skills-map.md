# Skills Map

Which skills apply to which phase, which router resolves which evidence, and what to run for each reference use-case in this repo.

> **Rule of thumb:** use the slash commands for phase control, then use natural language to steer the specifics. This repo does **not** ship use-case-specific slash commands — there is no `/assess-wcf-migration`. Describe the app and the target, and the routers pick the right adapter.

---

## 1. How the skill system is shaped

`.github/skills/` holds **36 skills**. Each is a folder with a `SKILL.md`, and optionally a `references/` subfolder (**71 reference files** in total, plus three companion files: an `examples/` template, a `templates/` guide, and one skill-level `README.md`).

```text
.github/skills/<skill-name>/
├─ SKILL.md              # always loaded when the skill matches — short by design
└─ references/           # opened on demand, one file at a time
```

| Class | Count | `user-invocable` | Reached by |
|---|---:|---|---|
| Workflow skills | 20 | `true` | the user typing the slash command |
| Knowledge skills | 16 | `false` | description match while a workflow skill runs |

### Progressive disclosure

A knowledge skill's `SKILL.md` is a **selection table**, not a manual. It maps evidence → one reference file. The agent opens that one file and leaves the rest closed. This is why the `.NET`, `Java`, `Python`, `PHP`, `Delphi/VB6`, and `Oracle Forms` adapters can all coexist without making any single migration expensive.

Practical consequence: **never paste a whole `references/` folder into a prompt.** Name the evidence, let the router choose.

### Full skill inventory

| Workflow skills (20) | Knowledge skills (16) |
|---|---|
| `/assess-any-application` | `stack-adapters` (15 refs) |
| `/phase1-plan` | `source-adapters` (10 refs) |
| `/phase2-migrate-code` | `workload-adapters` (8 refs) |
| `/phase3-generate-infra` | `azure-security-baseline` (8 refs) |
| `/phase4-deploy-to-azure` | `migration-strategy-report` (7 refs) |
| `/phase5-setup-cicd` | `migration-artifacts` (6 refs) |
| `/phase6-post-migration-ops` | `migration-decisions` (4 refs) |
| `/build-migration-plan` | `dotnet-modernization` (4 refs) |
| `/quick-assessment` | `azure-infrastructure` (3 refs) |
| `/quick-triage` | `azure-containerization` (1 ref) |
| `/interactive-migration-interview` | `java-modernization` (1 ref) |
| `/team-skill-assessment` | `wcf-to-rest-migration` (1 ref) |
| `/portfolio-strategy` | `config-transformation` (1 ref) |
| `/phase0-multi-repo-assessment` | `business-logic-mapping` |
| `/database-migration` | `migration-unit-testing` |
| `/security-hardening` | `rollback-strategy` |
| `/cost-optimization` | |
| `/phase-rollback` | |
| `/get-status` | |
| `/skill-creator` | |

Full detail: [Skill catalog](../architecture/SKILL-CATALOG.md).

---

## 2. Main path — 7 steps

| Step | Command | Knowledge skills usually pulled in |
|---|---|---|
| 1 | `/assess-any-application` | `source-adapters`, `stack-adapters`, `workload-adapters`, `migration-artifacts`, `migration-decisions` |
| 2 | `/phase1-plan` | `migration-decisions`, `migration-artifacts`, the matched stack/workload adapters |
| 3 | `/phase2-migrate-code` | matched stack adapter, `config-transformation`, `business-logic-mapping`, `migration-unit-testing`, plus `dotnet-modernization` / `java-modernization` / `wcf-to-rest-migration` when they apply |
| 4 | `/phase3-generate-infra` | `azure-infrastructure`, `azure-containerization`, `azure-security-baseline` |
| 5 | `/phase4-deploy-to-azure` | `azure-infrastructure`, `azure-security-baseline`, `rollback-strategy` |
| 6 | `/phase5-setup-cicd` | `azure-infrastructure`, `azure-security-baseline`, `rollback-strategy` |
| 7 | `/phase6-post-migration-ops` | `azure-infrastructure`, `azure-security-baseline`, `rollback-strategy` |

### Optional add-ons

| Category | Commands |
|---|---|
| Alternative intakes | `/build-migration-plan`, `/quick-assessment`, `/quick-triage`, `/interactive-migration-interview`, `/team-skill-assessment` |
| Portfolio / multi-app | `/portfolio-strategy`, `/phase0-multi-repo-assessment` |
| Specialized deep-dives | `/database-migration`, `/security-hardening`, `/cost-optimization` |
| Utility / recovery | `/phase-rollback`, `/get-status` |
| Skill authoring | `/skill-creator` |

---

## 3. Router selection tables

These are the three routers discovery uses. You do not invoke them — you supply the evidence.

### `stack-adapters` → `references/`

| Evidence | Reference |
|---|---|
| Unknown, conflicting, polyglot, or low-confidence | `stack-detection.md` |
| `*.sln`, `*.csproj`, `web.config`, `*.aspx`, `*.svc`, `System.Web` | `stack-dotnet.md` |
| `pom.xml`, `build.gradle`, `WEB-INF/`, `*.war`, Spring, Jakarta EE | `stack-java.md` |
| `package.json`, npm/yarn/pnpm lockfiles, Express, NestJS, Next.js | `stack-nodejs.md` |
| `requirements.txt`, `pyproject.toml`, Django, Flask, FastAPI, Airflow | `stack-python.md` |
| `composer.json`, Laravel, Symfony, WordPress, Magento | `stack-php.md` |
| `Gemfile`, Rails, Sinatra | `stack-ruby.md` |
| `go.mod`, `go.sum` | `stack-go.md` |
| `Cargo.toml` | `stack-rust.md` |
| `*.pl`, `*.pm`, `cpanfile` | `stack-perl.md` |
| `build.sbt`, `*.scala`, `*.kt`, Gradle Kotlin DSL | `stack-scala-kotlin.md` |
| `*.vcxproj`, MFC/ATL/Win32 sources | `stack-cpp-windows.md` |
| `*.dpr`, `*.pas`, `*.vbp`, `*.frm` | `stack-delphi-vb6.md` |
| `*.pbl`, `*.pbt`, `*.srw` | `stack-powerbuilder.md` |
| `*.fmb`, `*.fmx`, `*.rdf`, Forms/Reports runtime | `stack-oracle-forms.md` |

### `source-adapters` → `references/`

| Where the app lives today | Reference |
|---|---|
| GitHub repository | `source-github-repo.md` |
| ZIP or filesystem snapshot | `source-zip-filesystem.md` |
| On-premise servers | `source-on-premise.md` |
| AWS | `source-aws.md` |
| GCP | `source-gcp.md` |
| Oracle database estate | `source-oracle-db.md` |
| VMware / RVTools or Azure Migrate export | `source-vmware-rvtools.md` |
| Kubernetes cluster | `source-kubernetes-cluster.md` |
| Container registry image | `source-container-registry.md` |
| **Mainframe / midrange / SaaS-embedded** | `source-unsupported-escalation.md` |

> **Out of scope.** z/OS, z/VSE, IBM i / AS-400, COBOL, RPG, Natural, PL/I, CICS, IMS, and VSAM are **not** migrated code-level by this tool, and neither is SaaS-embedded code (Salesforce Apex, ServiceNow, SharePoint, Power Platform, SAP extensions). Both route to the specialist-partner escalation playbook.

### `workload-adapters` → `references/`

| How it runs | Reference |
|---|---|
| Browser-facing web app | `workload-webapp.md` |
| REST/SOAP/gRPC service | `workload-api-service.md` |
| Scheduled batch job | `workload-batch-job.md` |
| ETL / ELT data pipeline | `workload-data-pipeline.md` |
| Queue/topic/event consumer | `workload-event-driven.md` |
| Function-style serverless | `workload-serverless.md` |
| Desktop client-server | `workload-desktop-client-server.md` |
| Vendor-packaged application | `workload-packaged-app.md` |

---

## 4. Domain knowledge skills by reference file

| Skill | Reference files |
|---|---|
| `migration-decisions` | `decision-hardstop.md`, `decision-catalog.md`, `decisions-required-template.md`, `migration-strategy-decision-tree.md` |
| `migration-artifacts` | `discovery-dossier-template.md`, `capability-matrix.md`, `migration-plan-template.md`, `migration-report-template.md`, `action-log-format.md`, `migration-handoff.md` |
| `azure-security-baseline` | `azure-entra-id.md`, `azure-keyvault-secrets.md`, `azure-network-security.md`, `azure-defender-compliance.md`, `managed-identity.md`, `rbac-least-privilege.md`, `secret-management.md`, `owasp-top10-review.md` |
| `azure-infrastructure` | `bicep-modules.md`, `azure-app-service.md`, `azure-container-apps.md` |
| `azure-containerization` | `docker-containerize.md` |
| `dotnet-modernization` | `asp-classic-to-dotnet.md`, `dotnet-framework-to-dotnet8.md`, `webforms-to-razor.md`, `ef-migration.md` |
| `java-modernization` | `java8-to-java21.md` |
| `wcf-to-rest-migration` | `wcf-to-rest-api.md` *(plus `templates/WcfMigrationGuide.md`)* |
| `config-transformation` | `config-transformation-patterns.md` |
| `migration-strategy-report` | `classification-algorithm.md`, `style-guide.md`, `slides-common.md`, `slides-application-pillar.md`, `slides-database-pillar.md`, `slides-infrastructure-pillar.md`, `pptx-generation.md` *(plus a skill-level `README.md`)* |
| `skill-creator` | `skill-anatomy.md`, `skill-template.md` |
| `business-logic-mapping` | *(no `references/` — ships `examples/Business-Logic-Mapping-Template.md`)* |
| `migration-unit-testing` | *(none — single `SKILL.md`)* |
| `rollback-strategy` | *(none — single `SKILL.md`)* |

Full paths follow the pattern `.github/skills/<skill>/references/<file>`.

---

## 5. Reference use-cases

The seven applications under `Use-cases/` are worked examples, not a support matrix. Discovery accepts anything.

### 01-ASPClassicApp — The Antique

- **Source stack:** VBScript, Classic ASP, IIS, `global.asa`, ADODB, Jet/Access connection patterns, session state
- **Migration patterns:** Classic ASP → ASP.NET Core rewrite, include-file decomposition, `Request`/`Response`/session mapping, ADODB → EF Core or repository pattern, `global.asa` → middleware/startup/services
- **Routers resolve to:** `stack-dotnet.md`, `source-zip-filesystem.md` or `source-github-repo.md`, `workload-webapp.md`
- **Domain references:** `dotnet-modernization/references/asp-classic-to-dotnet.md`, `config-transformation/references/config-transformation-patterns.md`, `azure-infrastructure/references/azure-app-service.md`, `azure-infrastructure/references/bicep-modules.md`, `azure-security-baseline/references/secret-management.md`
- **Add-ons worth running:** `/database-migration`, `/security-hardening`
- **Target framework:** a **user decision** — the .NET LTS choice is recorded in `reports/Decisions-Required.md`, not assumed here

### 02-NetFramework30-ASPNET-WEB — The Fossil

- **Source stack:** C#, ASP.NET WebForms, `.aspx`, code-behind, `Web.config`, Windows Authentication
- **Migration patterns:** WebForms → Razor Pages/MVC, `System.Web` → ASP.NET Core, `Web.config` → `appsettings.json`, Windows Auth → Entra ID or App Service auth, ViewState/postback removal
- **Routers resolve to:** `stack-dotnet.md`, `workload-webapp.md`
- **Domain references:** `dotnet-modernization/references/webforms-to-razor.md`, `dotnet-modernization/references/dotnet-framework-to-dotnet8.md`, `config-transformation/references/config-transformation-patterns.md`, `azure-infrastructure/references/azure-app-service.md`, `azure-security-baseline/references/azure-entra-id.md`
- **Add-ons worth running:** `/security-hardening`

### 03-WCFNet35 — The Wire

- **Source stack:** C#, .NET Framework 3.5, WCF, `ServiceContract`, `OperationContract`, SOAP, `basicHttpBinding`, `app.config`
- **Migration patterns:** WCF → ASP.NET Core REST API, DTO contract flattening, SOAP endpoint inventory, `app.config` → `appsettings.json`, self-hosted service → container, client proxy → typed HTTP/OpenAPI client
- **Routers resolve to:** `stack-dotnet.md`, `workload-api-service.md`
- **Domain references:** `wcf-to-rest-migration/references/wcf-to-rest-api.md`, `dotnet-modernization/references/dotnet-framework-to-dotnet8.md`, `config-transformation/references/config-transformation-patterns.md`, `azure-containerization/references/docker-containerize.md`, `azure-infrastructure/references/azure-container-apps.md`, `azure-security-baseline/references/azure-keyvault-secrets.md`
- **Note:** this is a **rewrite, not a compatibility layer**. Existing SOAP clients will need updates — that tradeoff is a recorded decision.

### 04-ContosoUniversityDiPS — The Campus

- **Source stack:** C#, ASP.NET Core 2.1, MVC, Razor, React SPA, REST API, EF Core 2.1, Identity 2.0, JWT, SendGrid, Twilio
- **Migration patterns:** runtime and package modernization, shared-library cleanup, SPA/API/Web boundary preservation, EF Core provider review, auth/token refresh review, config split cleanup
- **Routers resolve to:** `stack-dotnet.md` (+ `stack-nodejs.md` for the SPA build chain), `workload-webapp.md` and `workload-api-service.md`
- **Domain references:** `dotnet-modernization/references/dotnet-framework-to-dotnet8.md`, `dotnet-modernization/references/ef-migration.md`, `config-transformation/references/config-transformation-patterns.md`, `azure-infrastructure/references/azure-app-service.md`, `azure-security-baseline/references/azure-entra-id.md`
- **Add-ons worth running:** `/database-migration`, `/security-hardening`
- **Note:** multi-project, **not** multi-repo. Do not reach for `/phase0-multi-repo-assessment`.

### 05-BookShop — The Bestseller (reference)

- **Current state:** already-modernized ASP.NET Core solution with Azure-ready infrastructure, tests, deployment guidance, and runbooks
- **Use it for:** the reporting format, the `infra/` shape, deployment docs, and production hardening standard
- **Domain references to study:** `azure-infrastructure/references/azure-app-service.md`, `azure-infrastructure/references/bicep-modules.md`, `rollback-strategy/SKILL.md`, `migration-artifacts/references/migration-report-template.md`
- **Commands worth running:** `/get-status`, `/phase6-post-migration-ops`, `/security-hardening`, `/cost-optimization`

### 06-Java-API-BusReservation — The Duke

- **Source stack:** Java 8, Spring Boot 2.3, Spring Web, Spring Data JPA, Maven, H2, REST controllers
- **Migration patterns:** Java LTS upgrade, Spring Boot 2.x → 3.x, `javax` → `jakarta`, H2 → a managed database, containerization, actuator hardening, property migration
- **Routers resolve to:** `stack-java.md`, `workload-api-service.md`
- **Domain references:** `java-modernization/references/java8-to-java21.md`, `azure-containerization/references/docker-containerize.md`, `azure-infrastructure/references/azure-container-apps.md`, `azure-security-baseline/references/azure-keyvault-secrets.md`, `azure-security-baseline/references/managed-identity.md`
- **Add-ons worth running:** `/database-migration`, `/cost-optimization`
- **Target Java LTS:** a **user decision** — Java 21 and Java 17 are both valid landings

### 07-PartsUnlimited-aspnet45 — The Warehouse

- **Source stack:** C#, ASP.NET MVC 5, .NET Framework 4.5.1, EF6, ASP.NET Identity, OWIN, SQL Server, deployment scripts, test projects
- **Migration patterns:** MVC5 → ASP.NET Core MVC, EF6 → EF Core, `packages.config` → SDK-style `PackageReference`, OWIN auth → ASP.NET Core auth/Entra ID, deployment script replacement, `Web.config` transformation
- **Routers resolve to:** `stack-dotnet.md`, `workload-webapp.md`
- **Domain references:** `dotnet-modernization/references/dotnet-framework-to-dotnet8.md`, `dotnet-modernization/references/ef-migration.md`, `config-transformation/references/config-transformation-patterns.md`, `azure-infrastructure/references/azure-app-service.md`, `azure-security-baseline/references/azure-entra-id.md`, `rollback-strategy/SKILL.md`
- **Add-ons worth running:** `/database-migration`, `/phase-rollback`

---

## 6. Role dispatch per phase

Roles come from the custom agents in `.github/agents/`. The same pattern applies to every use-case; only the domain references change.

| Phase | Lead | Assists |
|---|---|---|
| Discovery | Discovery Engineer | Architect, Scribe |
| Phase 1: plan | Architect | Azure Specialist, Security Auditor, Database Specialist |
| Phase 2: migrate code | Coder | Tester, Database Specialist, Security Auditor |
| Phase 3: generate infra | Azure Specialist | DevOps Engineer, Observability Engineer, Security Auditor |
| Phase 4: deploy | DevOps Engineer | Cutover Commander, Azure Specialist, Tester |
| Phase 5: CI/CD | DevOps Engineer | Tester, Evaluator, Security Auditor |
| Phase 6: operate | Observability Engineer | Performance Engineer, Cost Engineer, Security Auditor, Scribe |

`Migration-Orchestrator` owns routing across all of them. `Debug-Migration` takes over on any failure. `Security-Review` and `Cost-Optimization` can be invoked between any two phases.

---

## 7. Command sequences

The sequence is the same for every application. What changes is the natural-language steer in between.

### Standard sequence

```text
/assess-any-application
  → (steer: describe the source environment and any constraint that matters)
/phase1-plan
  → answer every 🛑 DECISION REQUIRED block in reports/Decisions-Required.md
/phase2-migrate-code
/phase3-generate-infra
/phase4-deploy-to-azure
/phase5-setup-cicd
/phase6-post-migration-ops
```

Insert `/database-migration` after `/phase1-plan` whenever the app owns a database. Insert `/security-hardening` before `/phase4-deploy-to-azure`. Finish with `/cost-optimization` and, if a cutover is planned, `/phase-rollback`. Use `/get-status` at any point.

### Steering examples

Paste these after the slash-command output, or as the opening message.

| Use-case | Steer |
|---|---|
| 01 | `Treat this as a Classic ASP + VBScript + ADODB storefront. Call out session state, include files, COM/ADODB dependencies, and global.asa risks. Then map default.asp, products.asp, product-detail.asp, cart.asp, about.asp, and contact.asp page by page.` |
| 02 | `Inventory Default.aspx, About.aspx, Secure.aspx, and Web.config. Map each page, server-side event, and auth rule to Razor Pages or MVC endpoints while preserving Secure.aspx behavior.` |
| 03 | `Map every ServiceContract and OperationContract in WCFDemo.Service to REST endpoints, DTOs, and status codes. List the breaking changes existing SOAP clients will hit, and recommend container boundaries and API versioning.` |
| 04 | `Produce a dependency map across ContosoUniversity.Api, .Web, .Spa.React, .Data, .Common, and the test projects. Flag JWT, Identity, SendGrid, Twilio, EF Core provider, and SPA build risks. Keep the project boundaries explicit.` |
| 05 | `Use this as the reference implementation for reporting format, infra/ shape, deployment docs, and production hardening. Extract reusable patterns for use-cases 01, 02, and 07.` |
| 06 | `Review RestApi.java, pom.xml, and application.properties. Produce an endpoint inventory, a dependency upgrade plan, and an H2-to-managed-database migration plan. Flag javax→jakarta and container risks.` |
| 07 | `Map the MVC controllers, EF6 models, ASP.NET Identity/OWIN configuration, and deploy.cmd flow to ASP.NET Core MVC, EF Core, modern auth, and Azure deployment equivalents. Flag test-project migration risk.` |

### Dispatch notes

- Use `05-BookShop` as the benchmark for reporting format, `infra/` shape, deployment docs, and production hardening.
- Use `/phase0-multi-repo-assessment` only when several **repositories** are involved. `04-ContosoUniversityDiPS` is multi-project, not multi-repo.
- If discovery classifies a stack, source, or workload with no matching adapter, it calls `/skill-creator` instead of guessing.
- Never let a phase start with a `⏸ PENDING` decision it depends on. The gate exists for a reason.

## See also

- [Skill catalog](../architecture/SKILL-CATALOG.md)
- [Architecture](../architecture/ARCHITECTURE.md)
- [Handoff protocol](./handoff-protocol.md)
- [.NET version guide](./dotnet-version-guide.md)
