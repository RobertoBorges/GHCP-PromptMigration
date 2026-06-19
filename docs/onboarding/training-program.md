# Ocean's Twelve Training Program

Production-ready training guide for Robert Borges' migration team. This document maps the 7 sample use-cases to the 12 squad agents, the exact repo skill files, the prompt flow, and the learning paths needed to build repeatable Azure migration capability.

## Who this is for
- **Migration team leads** deciding who should own each use-case
- **New team members** who need a clear first exercise and learning order
- **Squad coordinators** who need prompt and skill routing that matches the repo's current assets

## Training assumptions
- **BookShop (`05-BookShop`) is the reference implementation** because it already includes migrated code, infrastructure, deployment guidance, and reports.
- **Use-case 02 is the best starting lab** for new .NET teammates.
- **`/phase0-multirepoassessment` is only for multi-repo portfolios.** `04-ContosoUniversityDiPS` is multi-project, not multi-repo.
- **Default Azure baseline:** App Service for classic web monoliths, Container Apps for containerized API-first services, AKS only when Kubernetes control is explicitly required.
- **Default platform controls:** managed identity, Key Vault, App Insights, least-privilege RBAC, Bicep + AVM, and `azd`.
- **Skill-gap note:** the repo does **not** yet contain a dedicated Azure Database for PostgreSQL skill file, so Java/PostgreSQL training relies on `DatabaseMigration.prompt.md` plus Java/container/IaC/security skills.

## Prompt legend

### Core/original prompts
- `/phase0-multirepoassessment`
- `/phase1-planandassess`
- `/phase2-migratecode`
- `/phase3-generateinfra`
- `/phase4-deploytoazure`
- `/phase5-setupcicd`
- `/getstatus`

### New/supporting prompts
- `/quickassessment`
- `/databasemigration`
- `/phase6-postmigrationops`
- `/securityhardening`
- `/costoptimization`
- `/phase-rollback`

---

## 1) Use-Case × Agent Matrix

| Use-Case | Architect | Coder | Azure Spec | Security | DB Spec | Perf Eng | DevOps | Observ | Cutover | Evaluator | Tester | Scribe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01-ASPClassicApp | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | 🔴 | 🟡 |
| 02-NetFramework30-ASPNET-WEB | 🔴 | 🔴 | 🔴 | 🟡 | 🟡 | ⚪ | 🟡 | 🟡 | 🟡 | ⚪ | 🔴 | 🟡 |
| 03-WCFNet35 | 🔴 | 🔴 | 🔴 | 🟡 | 🟡 | 🟡 | 🔴 | 🔴 | 🟡 | 🟡 | 🔴 | 🟡 |
| 04-ContosoUniversityDiPS | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟡 | 🔴 | 🔴 | 🟡 | 🟡 | 🔴 | 🟡 |
| 05-BookShop (reference) | 🔴 | 🟡 | 🔴 | 🟡 | 🟡 | 🟡 | 🔴 | 🔴 | 🟡 | 🔴 | 🔴 | 🔴 |
| 06-Java-API-BusReservation | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟡 | 🔴 | 🔴 | 🟡 | 🟡 | 🔴 | 🟡 |
| 07-PartsUnlimited-aspnet45 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟡 | 🔴 | 🟡 | 🔴 | 🟡 | 🔴 | 🟡 |

### Matrix notes
- **🔴 Critical** = should be assigned early; decisions in this role materially change migration success.
- **🟡 Involved** = should review, validate, or support a specific phase.
- **⚪ Not needed** = usually unnecessary for the default training path.
- **BookShop is special:** it is less about discovery and more about learning from a mature reference, so Evaluator, Tester, DevOps, Observability, and Scribe matter more than greenfield migration roles.

---

## 2) Use-Case × Skill Map

### 01-ASPClassicApp — Classic ASP e-commerce
| Category | Exact skills from `skills/` |
|---|---|
| Technology | `skills/asp-classic-to-dotnet.md`, `skills/config-transformation.md`, `skills/ef-migration.md` |
| Azure | `skills/azure-app-service.md`, `skills/azure-sql-migration.md`, `skills/bicep-modules.md`, `skills/azd-configuration.md`, `skills/azure-monitor-appinsights.md` |
| Security / DevOps | `skills/managed-identity.md`, `skills/azure-key-vault.md`, `skills/rbac-least-privilege.md`, `skills/secret-management.md`, `skills/github-actions-cicd.md`, `skills/rollback-strategy.md`, `skills/cost-optimization.md` |
| Recommended learning order | 1) `asp-classic-to-dotnet` → 2) `config-transformation` → 3) `ef-migration` → 4) `azure-app-service` → 5) `azure-sql-migration` → 6) `bicep-modules` → 7) `azd-configuration` → 8) `managed-identity` → 9) `azure-key-vault` → 10) `azure-monitor-appinsights` → 11) `github-actions-cicd` → 12) `rollback-strategy` / `cost-optimization` |

### 02-NetFramework30-ASPNET-WEB — .NET Framework 3.0 WebForms
| Category | Exact skills from `skills/` |
|---|---|
| Technology | `skills/dotnet-framework-to-dotnet8.md`, `skills/webforms-to-razor.md`, `skills/config-transformation.md` |
| Azure | `skills/azure-app-service.md`, `skills/azure-sql-migration.md`, `skills/azure-entra-id.md`, `skills/azure-monitor-appinsights.md`, `skills/bicep-modules.md`, `skills/azd-configuration.md` |
| Security / DevOps | `skills/managed-identity.md`, `skills/azure-key-vault.md`, `skills/rbac-least-privilege.md`, `skills/github-actions-cicd.md`, `skills/rollback-strategy.md`, `skills/cost-optimization.md` |
| Recommended learning order | 1) `dotnet-framework-to-dotnet8` → 2) `webforms-to-razor` → 3) `config-transformation` → 4) `azure-app-service` → 5) `azure-entra-id` → 6) `azure-sql-migration` → 7) `bicep-modules` → 8) `azd-configuration` → 9) `managed-identity` / `azure-key-vault` → 10) `azure-monitor-appinsights` → 11) `github-actions-cicd` |

### 03-WCFNet35 — WCF .NET 3.5 service estate
| Category | Exact skills from `skills/` |
|---|---|
| Technology | `skills/wcf-to-rest-api.md`, `skills/dotnet-framework-to-dotnet8.md`, `skills/config-transformation.md`, `skills/docker-containerize.md` |
| Azure | `skills/azure-container-apps.md`, `skills/azure-sql-migration.md`, `skills/azure-entra-id.md`, `skills/azure-key-vault.md`, `skills/azure-monitor-appinsights.md`, `skills/bicep-modules.md`, `skills/azd-configuration.md` |
| Security / DevOps | `skills/managed-identity.md`, `skills/rbac-least-privilege.md`, `skills/github-actions-cicd.md`, `skills/rollback-strategy.md`, `skills/cost-optimization.md` |
| Recommended learning order | 1) `wcf-to-rest-api` → 2) `dotnet-framework-to-dotnet8` → 3) `config-transformation` → 4) `docker-containerize` → 5) `azure-container-apps` → 6) `azure-entra-id` → 7) `azure-sql-migration` → 8) `managed-identity` / `azure-key-vault` → 9) `azure-monitor-appinsights` → 10) `bicep-modules` → 11) `azd-configuration` → 12) `github-actions-cicd` |

### 04-ContosoUniversityDiPS — API + Web + React + Data + Tests
| Category | Exact skills from `skills/` |
|---|---|
| Technology | `skills/dotnet-framework-to-dotnet8.md`, `skills/config-transformation.md`, `skills/ef-migration.md` |
| Azure | `skills/azure-app-service.md`, `skills/azure-sql-migration.md`, `skills/azure-entra-id.md`, `skills/azure-monitor-appinsights.md`, `skills/bicep-modules.md`, `skills/azd-configuration.md` |
| Security / DevOps | `skills/managed-identity.md`, `skills/azure-key-vault.md`, `skills/rbac-least-privilege.md`, `skills/github-actions-cicd.md`, `skills/rollback-strategy.md`, `skills/cost-optimization.md` |
| Recommended learning order | 1) `dotnet-framework-to-dotnet8` (selective modernization patterns) → 2) `config-transformation` → 3) `ef-migration` → 4) `azure-app-service` → 5) `azure-sql-migration` → 6) `azure-entra-id` → 7) `managed-identity` / `azure-key-vault` → 8) `bicep-modules` → 9) `azd-configuration` → 10) `azure-monitor-appinsights` → 11) `github-actions-cicd` |

### 05-BookShop — reference implementation
| Category | Exact skills from `skills/` |
|---|---|
| Technology | `skills/webforms-to-razor.md`, `skills/ef-migration.md`, `skills/migration-report-template.md` |
| Azure | `skills/azure-app-service.md`, `skills/azure-sql-migration.md`, `skills/bicep-modules.md`, `skills/azd-configuration.md`, `skills/azure-monitor-appinsights.md` |
| Security / DevOps | `skills/managed-identity.md`, `skills/azure-key-vault.md`, `skills/rbac-least-privilege.md`, `skills/github-actions-cicd.md`, `skills/rollback-strategy.md`, `skills/cost-optimization.md` |
| Recommended learning order | 1) Study `Use-cases/05-BookShop/reports/Report-Status.md` and project docs → 2) `migration-report-template` → 3) `webforms-to-razor` → 4) `ef-migration` → 5) `azure-app-service` → 6) `azure-sql-migration` → 7) `bicep-modules` → 8) `azd-configuration` → 9) `managed-identity` / `azure-key-vault` → 10) `azure-monitor-appinsights` → 11) `github-actions-cicd` → 12) `rollback-strategy` |

### 06-Java-API-BusReservation — Java 8 Maven REST API
| Category | Exact skills from `skills/` |
|---|---|
| Technology | `skills/java8-to-java21.md`, `skills/docker-containerize.md`, `skills/config-transformation.md` |
| Azure | `skills/azure-container-apps.md`, `skills/terraform-azure.md`, `skills/bicep-modules.md`, `skills/azd-configuration.md`, `skills/azure-key-vault.md`, `skills/azure-monitor-appinsights.md` |
| Security / DevOps | `skills/managed-identity.md`, `skills/azure-entra-id.md`, `skills/rbac-least-privilege.md`, `skills/github-actions-cicd.md`, `skills/rollback-strategy.md`, `skills/cost-optimization.md` |
| Recommended learning order | 1) `java8-to-java21` → 2) `config-transformation` → 3) `docker-containerize` → 4) `azure-container-apps` → 5) choose one IaC standard: `terraform-azure` or `bicep-modules` → 6) `azd-configuration` → 7) `managed-identity` / `azure-key-vault` → 8) `azure-monitor-appinsights` → 9) `github-actions-cicd` → 10) `rollback-strategy` / `cost-optimization` |

> **Gap to teach explicitly:** use `/databasemigration` for PostgreSQL decisioning because the repo does not yet ship a dedicated PostgreSQL skill file.

### 07-PartsUnlimited-aspnet45 — ASP.NET MVC 5 e-commerce
| Category | Exact skills from `skills/` |
|---|---|
| Technology | `skills/dotnet-framework-to-dotnet8.md`, `skills/ef-migration.md`, `skills/config-transformation.md` |
| Azure | `skills/azure-app-service.md`, `skills/azure-sql-migration.md`, `skills/azure-entra-id.md`, `skills/azure-monitor-appinsights.md`, `skills/bicep-modules.md`, `skills/azd-configuration.md` |
| Security / DevOps | `skills/managed-identity.md`, `skills/azure-key-vault.md`, `skills/rbac-least-privilege.md`, `skills/github-actions-cicd.md`, `skills/azure-devops-pipelines.md`, `skills/rollback-strategy.md`, `skills/cost-optimization.md` |
| Recommended learning order | 1) `dotnet-framework-to-dotnet8` → 2) `ef-migration` → 3) `config-transformation` → 4) `azure-app-service` → 5) `azure-sql-migration` → 6) `azure-entra-id` → 7) `managed-identity` / `azure-key-vault` → 8) `bicep-modules` → 9) `azd-configuration` → 10) `azure-monitor-appinsights` → 11) `github-actions-cicd` (or `azure-devops-pipelines` if required) → 12) `rollback-strategy` |

---

## 3) Use-Case × Prompt Map

### Prompt-selection rule
1. Start with `/quickassessment` unless the app is already a known reference pattern.
2. Use `/phase1-planandassess` for the full architecture and migration plan.
3. Add `/databasemigration` whenever the database choice, schema portability, ORM rewrite, or provider change is a primary risk.
4. Use `/phase0-multirepoassessment` only for multi-repo portfolio work.
5. Use `/phase-rollback` as an exception-path rehearsal, not as a normal happy-path phase.

### 01-ASPClassicApp
- **Core/original prompts:** `/phase1-planandassess`, `/phase2-migratecode`, `/phase3-generateinfra`, `/phase4-deploytoazure`, `/phase5-setupcicd`, `/getstatus`
- **New prompts:** `/quickassessment`, `/databasemigration`, `/phase6-postmigrationops`, `/securityhardening`, `/costoptimization`, `/phase-rollback`
- **Recommended order:** `/quickassessment` → `/phase1-planandassess` → `/databasemigration` → `/phase2-migratecode` → `/phase3-generateinfra` → `/phase4-deploytoazure` → `/phase5-setupcicd` → `/phase6-postmigrationops` → `/securityhardening` → `/costoptimization` → `/phase-rollback` → `/getstatus`
- **Custom prompt modifications:** explicitly mention VBScript, include files, `global.asa`, session state, ADODB, and any COM dependencies.
- **Sample starter prompt:** `Assess #file:Use-cases/01-ASPClassicApp as a Classic ASP e-commerce app. Target a .NET 8 rewrite on Azure App Service with Azure SQL, Bicep, managed identity, Key Vault, and GitHub Actions. Call out global.asa, Session usage, include files, and ADODB risks.`

### 02-NetFramework30-ASPNET-WEB
- **Core/original prompts:** `/phase1-planandassess`, `/phase2-migratecode`, `/phase3-generateinfra`, `/phase4-deploytoazure`, `/phase5-setupcicd`, `/getstatus`
- **New prompts:** `/quickassessment`, `/databasemigration` (optional), `/phase6-postmigrationops`, `/securityhardening`, `/costoptimization`, `/phase-rollback`
- **Recommended order:** `/quickassessment` → `/phase1-planandassess` → `/phase2-migratecode` → `/phase3-generateinfra` → `/phase4-deploytoazure` → `/phase5-setupcicd` → `/phase6-postmigrationops` → `/securityhardening` → `/costoptimization` → `/phase-rollback` → `/getstatus`
- **Custom prompt modifications:** mention `Default.aspx`, `About.aspx`, `Secure.aspx`, `Web.config`, Windows/Forms authentication, ViewState, code-behind, and secure-page parity.
- **Sample starter prompt:** `Assess #file:Use-cases/02-NetFramework30-ASPNET-WEB as a .NET Framework 3.0 WebForms app. Target .NET 8 on Azure App Service with Azure SQL and Bicep. Preserve Secure.aspx behavior and flag WebForms, code-behind, Web.config, ViewState, and Windows Authentication blockers.`

### 03-WCFNet35
- **Core/original prompts:** `/phase1-planandassess`, `/phase2-migratecode`, `/phase3-generateinfra`, `/phase4-deploytoazure`, `/phase5-setupcicd`, `/getstatus`
- **New prompts:** `/quickassessment`, `/databasemigration`, `/phase6-postmigrationops`, `/securityhardening`, `/costoptimization`, `/phase-rollback`
- **Recommended order:** `/quickassessment` → `/phase1-planandassess` → `/databasemigration` → `/phase2-migratecode` → `/phase3-generateinfra` → `/phase4-deploytoazure` → `/phase5-setupcicd` → `/phase6-postmigrationops` → `/securityhardening` → `/costoptimization` → `/phase-rollback` → `/getstatus`
- **Custom prompt modifications:** require `ServiceContract` / `OperationContract` inventory, SOAP-to-REST mapping, client compatibility notes, `app.config` migration, and API versioning guidance.
- **Sample starter prompt:** `Assess #file:Use-cases/03-WCFNet35 for WCF .NET 3.5 to ASP.NET Core REST migration. Target Azure Container Apps, Azure SQL, Key Vault, and App Insights. Score SOAP contract risk, app.config migration risk, client breakage risk, and container boundary decisions.`

### 04-ContosoUniversityDiPS
- **Core/original prompts:** `/phase1-planandassess`, `/phase2-migratecode`, `/phase3-generateinfra`, `/phase4-deploytoazure`, `/phase5-setupcicd`, `/getstatus`
- **New prompts:** `/quickassessment`, `/databasemigration`, `/phase6-postmigrationops`, `/securityhardening`, `/costoptimization`, `/phase-rollback`
- **Recommended order:** `/quickassessment` → `/phase1-planandassess` → `/databasemigration` → `/phase2-migratecode` → `/phase3-generateinfra` → `/phase4-deploytoazure` → `/phase5-setupcicd` → `/phase6-postmigrationops` → `/securityhardening` → `/costoptimization` → `/phase-rollback` → `/getstatus`
- **Custom prompt modifications:** state clearly that this is **one repo with multiple projects**; preserve API/Web/SPA/Data/Test boundaries; mention JWT, Identity, SendGrid, Twilio, and React build chain.
- **Sample starter prompt:** `Assess #file:Use-cases/04-ContosoUniversityDiPS as one multi-project solution with API, Web, React SPA, Data, Common, and Tests. Target .NET 8 on Azure App Service with Azure SQL, Entra ID, managed identity, Key Vault, and App Insights. Do not treat this as a multi-repo assessment.`

### 05-BookShop
- **Core/original prompts:** `/getstatus`, `/phase1-planandassess`, `/phase2-migratecode`, `/phase3-generateinfra`, `/phase4-deploytoazure`, `/phase5-setupcicd`
- **New prompts:** `/phase6-postmigrationops`, `/securityhardening`, `/costoptimization`, `/phase-rollback`, `/quickassessment` (only if rehearsing from scratch)
- **Recommended order (reference mode):** `/getstatus` → `/phase6-postmigrationops` → `/securityhardening` → `/costoptimization` → `/phase-rollback` → `/getstatus`
- **Recommended order (rebuild practice mode):** `/quickassessment` → `/phase1-planandassess` → `/databasemigration` → `/phase2-migratecode` → `/phase3-generateinfra` → `/phase4-deploytoazure` → `/phase5-setupcicd` → `/phase6-postmigrationops` → `/securityhardening` → `/costoptimization` → `/phase-rollback` → `/getstatus`
- **Custom prompt modifications:** tell Copilot to use BookShop as a **benchmark**, extract reusable patterns, compare reports and infra, and note where another use-case still differs from the benchmark.
- **Sample starter prompt:** `Use #file:Use-cases/05-BookShop as the benchmark for .NET 8, Azure App Service, Azure SQL, Bicep, GitHub Actions, operations runbooks, and report structure. Extract the patterns that Use-cases 01, 02, and 07 should copy first.`

### 06-Java-API-BusReservation
- **Core/original prompts:** `/phase1-planandassess`, `/phase2-migratecode`, `/phase3-generateinfra`, `/phase4-deploytoazure`, `/phase5-setupcicd`, `/getstatus`
- **New prompts:** `/quickassessment`, `/databasemigration`, `/phase6-postmigrationops`, `/securityhardening`, `/costoptimization`, `/phase-rollback`
- **Recommended order:** `/quickassessment` → `/phase1-planandassess` → `/databasemigration` → `/phase2-migratecode` → `/phase3-generateinfra` → `/phase4-deploytoazure` → `/phase5-setupcicd` → `/phase6-postmigrationops` → `/securityhardening` → `/costoptimization` → `/phase-rollback` → `/getstatus`
- **Custom prompt modifications:** mention Java 8, Maven, REST controllers, `pom.xml`, `application.properties`, `javax` → `jakarta`, Docker, and PostgreSQL target choice.
- **Sample starter prompt:** `Assess #file:Use-cases/06-Java-API-BusReservation for Java 8 + Maven REST API modernization to Java 21 + Spring Boot 3 on Azure Container Apps with PostgreSQL. Flag javax-to-jakarta, property migration, Docker, and database portability risks.`

### 07-PartsUnlimited-aspnet45
- **Core/original prompts:** `/phase1-planandassess`, `/phase2-migratecode`, `/phase3-generateinfra`, `/phase4-deploytoazure`, `/phase5-setupcicd`, `/getstatus`
- **New prompts:** `/quickassessment`, `/databasemigration`, `/phase6-postmigrationops`, `/securityhardening`, `/costoptimization`, `/phase-rollback`
- **Recommended order:** `/quickassessment` → `/phase1-planandassess` → `/databasemigration` → `/phase2-migratecode` → `/phase3-generateinfra` → `/phase4-deploytoazure` → `/phase5-setupcicd` → `/phase6-postmigrationops` → `/securityhardening` → `/costoptimization` → `/phase-rollback` → `/getstatus`
- **Custom prompt modifications:** call out MVC5, EF6, ASP.NET Identity, OWIN, deployment scripts, staging slots, and production-hardening parity with BookShop.
- **Sample starter prompt:** `Assess #file:Use-cases/07-PartsUnlimited-aspnet45 as an ASP.NET MVC 5 / .NET Framework 4.5 e-commerce site. Target .NET 8 on Azure App Service with Azure SQL, Bicep, Key Vault, App Insights, GitHub Actions, and rollback slots. Flag EF6, Identity, OWIN, and deployment-script blockers.`

---

## 4) Training Paths by Role

### Path A — .NET Migration Specialist
- **Sequence:** 02 → 03 → 05 → 07
- **Prerequisites:** C#, ASP.NET basics, Git, Visual Studio or VS Code, basic Azure concepts
- **Estimated training time:** 4-6 weeks part-time
- **Key skills to acquire:** `dotnet-framework-to-dotnet8`, `webforms-to-razor`, `wcf-to-rest-api`, `config-transformation`, `ef-migration`, `azure-app-service`, `azure-container-apps`, `azure-sql-migration`, `github-actions-cicd`
- **Practice exercises:**
  1. Run `/quickassessment` and `/phase1-planandassess` on Use-case 02.
  2. Convert one WCF contract from Use-case 03 into REST endpoint mappings.
  3. Compare your outputs to BookShop reports and infra.
  4. Execute a full prompt chain for Use-case 07 with rollback and security included.
- **Assessment criteria:** ready when the trainee can explain WebForms vs WCF modernization differences, choose App Service vs Container Apps correctly, produce a realistic DB migration plan, and identify what Use-case 07 must copy from BookShop.

### Path B — Java Migration Specialist
- **Sequence:** 06 → 04 cross-train → 05 reference review
- **Prerequisites:** Java, Maven, REST APIs, SQL basics, container basics
- **Estimated training time:** 3-4 weeks part-time
- **Key skills to acquire:** `java8-to-java21`, `docker-containerize`, `terraform-azure` or `bicep-modules`, `azure-container-apps`, `azure-key-vault`, `managed-identity`, `azure-monitor-appinsights`
- **Practice exercises:**
  1. Run a quick assessment and Phase 1 on Use-case 06.
  2. Produce a `javax` → `jakarta` impact summary from `pom.xml`.
  3. Write a PostgreSQL decision memo using `/databasemigration`.
  4. Cross-train by reviewing Contoso's API/auth/config patterns and mapping them to Java equivalents.
- **Assessment criteria:** ready when the trainee can justify Container Apps, explain Java 8 → 21 and Spring 2.x → 3.x breaking changes, define a Postgres migration approach, and choose one IaC standard without mixing Terraform and Bicep randomly.

### Path C — Legacy Migration Specialist
- **Sequence:** 01 → 02 → 05 reference review
- **Prerequisites:** IIS basics, SQL basics, comfort reading legacy code, willingness to redesign rather than patch-upgrade
- **Estimated training time:** 4-5 weeks part-time
- **Key skills to acquire:** `asp-classic-to-dotnet`, `webforms-to-razor`, `config-transformation`, `ef-migration`, `azure-app-service`, `azure-sql-migration`, `rollback-strategy`
- **Practice exercises:**
  1. Create a page inventory for Use-case 01.
  2. Map `global.asa` concepts to middleware/services.
  3. Repeat the exercise for Use-case 02 and compare which patterns carry over.
  4. Review BookShop to see what a finished rewrite looks like.
- **Assessment criteria:** ready when the trainee consistently treats ASP Classic and WebForms as redesigns, not package upgrades; can map session/config/data patterns to ASP.NET Core equivalents; and can name the safest first Azure landing zone.

### Path D — Full-Stack Cloud Engineer
- **Sequence:** 04 → 05 → 07
- **Prerequisites:** ASP.NET Core, JavaScript/React basics, API fundamentals, SQL, Azure fundamentals
- **Estimated training time:** 4-6 weeks part-time
- **Key skills to acquire:** `config-transformation`, `ef-migration`, `azure-app-service`, `azure-entra-id`, `managed-identity`, `azure-key-vault`, `azure-monitor-appinsights`, `bicep-modules`, `azd-configuration`, `github-actions-cicd`
- **Practice exercises:**
  1. Assess Contoso without misclassifying it as multi-repo.
  2. Produce a dependency map across API/Web/SPA/Data/Tests.
  3. Compare the resulting target architecture to BookShop's reference assets.
  4. Run PartsUnlimited through the full prompt chain and add rollback requirements.
- **Assessment criteria:** ready when the trainee can preserve project boundaries, design a coherent Azure topology, keep auth/secret handling explicit, and hand off an infra-ready solution with status evidence.

### Path E — Migration Team Lead
- **Sequence:** 05 first, then 02 + 03 + 06 + 07 portfolio view
- **Prerequisites:** delivery planning, basic Azure, comfort reading architecture docs and status reports
- **Estimated training time:** 2-3 weeks focused, then ongoing portfolio practice
- **Key skills to acquire:** `migration-report-template`, `bicep-modules`, `azd-configuration`, `rollback-strategy`, `cost-optimization`, plus enough of each technology skill to route work intelligently
- **Practice exercises:**
  1. Start with BookShop and extract the benchmark checklist.
  2. For each remaining use-case, choose the correct squad roles, core prompts, and top 5 skills.
  3. Run a mock portfolio triage: decide which app migrates first and why.
  4. Review a trainee's prompt order and identify missing security, database, or rollback steps.
- **Assessment criteria:** ready when the lead can route each use-case to the right roles, explain why a prompt is optional vs mandatory, spot when Phase0 is misused, and use BookShop as the benchmark without forcing every app into the exact same architecture.

---

## 5) Assessment / Evaluation Prompts for Team Leads

### A. Quick knowledge checks
| Area | Exact assessment prompt | What good looks like |
|---|---|---|
| WebForms | `In 10 bullets, explain how #file:Use-cases/02-NetFramework30-ASPNET-WEB maps from WebForms + Web.config + Windows Authentication to .NET 8 on Azure App Service. Name the first 3 skills and first 3 prompts you would use.` | Mentions `webforms-to-razor`, config migration, auth modernization, App Service, `/quickassessment`, `/phase1-planandassess`, `/phase2-migratecode`. |
| WCF | `Using #file:Use-cases/03-WCFNet35, explain why this is not an in-place upgrade. Map ServiceContract/OperationContract to REST concepts and list the first 3 prompts you would run.` | Mentions REST rewrite, client compatibility, Container Apps, `/databasemigration` when data matters. |
| Java | `Using #file:Use-cases/06-Java-API-BusReservation, summarize the Java 8 -> 21, Spring 2.x -> 3.x, javax -> jakarta, and H2 -> PostgreSQL changes that matter most. Name the repo skills that teach them.` | Mentions `java8-to-java21`, `docker-containerize`, `/databasemigration`, Container Apps. |
| Data migration | `Compare the data migration risk in Use-cases 01, 04, 06, and 07. Which ones require /databasemigration by default and why?` | Identifies provider/schema/ORM shifts and justifies prompt selection. |
| Azure platform selection | `For Use-cases 02, 03, 06, and 07, justify App Service vs Container Apps vs AKS in one table.` | Avoids overusing AKS, matches platform to workload shape. |

### B. Migration simulation exercises
| Exercise | Exact assessment prompt | Ready when |
|---|---|---|
| Starter simulation | `You are planning the first migration for a new teammate. Use #file:Use-cases/02-NetFramework30-ASPNET-WEB. Pick the squad agents, skill order, prompt order, and first deliverable. Keep it to one screen.` | Trainee selects Use-case 02, routes to Architect/Coder/Azure/Tester, and produces a sensible first deliverable. |
| Service simulation | `Create a migration plan for #file:Use-cases/03-WCFNet35 that preserves business behavior but changes the interface contract from SOAP to REST. Include rollback and cutover rehearsal.` | Includes contract mapping, client impact, Container Apps, rollback path. |
| Full-stack simulation | `Plan #file:Use-cases/04-ContosoUniversityDiPS without using /phase0-multirepoassessment. Include API, SPA, data, auth, and test impacts.` | Keeps it as one repo, includes project-boundary and auth/secret concerns. |
| Java simulation | `Design the first two weeks of migration work for #file:Use-cases/06-Java-API-BusReservation, including database and infrastructure decisions.` | Produces Java/runtime/DB/container/IaC workstreams. |
| Portfolio simulation | `You can only start two migrations this quarter: 02, 03, 06, or 07. Choose them, justify the order, and name the benchmark artifacts from 05 that de-risk the plan.` | Uses 05 as benchmark, explains sequence, identifies reusable assets. |

### C. Code review exercises
| Exercise | Exact assessment prompt | Evidence expected |
|---|---|---|
| WebForms rewrite review | `Review a proposed migration approach for #file:Use-cases/02-NetFramework30-ASPNET-WEB. List the 5 most important risks if someone tries to preserve WebForms behavior too literally.` | Calls out ViewState/postbacks/server controls/System.Web/auth/config issues. |
| WCF review | `Review a draft WCF -> REST design for #file:Use-cases/03-WCFNet35. What compatibility notes must appear before Phase 2 starts?` | Mentions DTO changes, status codes, endpoint shape, client rewrite, auth/versioning. |
| MVC/EF review | `Review the likely code migration hotspots in #file:Use-cases/07-PartsUnlimited-aspnet45. Focus on MVC, EF6, OWIN, and deployment script assumptions.` | Identifies MVC5 -> Core, EF6 -> EF Core, OWIN/Identity rewrite, config/scripts. |

### D. Infrastructure review exercises
| Exercise | Exact assessment prompt | Evidence expected |
|---|---|---|
| BookShop benchmark | `Use #file:Use-cases/05-BookShop as the benchmark. What should another team copy first from its reports, Bicep, deployment guidance, and CI/CD setup?` | Calls out reports, infra shape, deployment docs, status tracking, operations guidance. |
| App Service review | `Design the minimum secure App Service landing zone for Use-case 07. Include identity, secret handling, telemetry, slots, and rollback controls.` | Mentions App Service, Azure SQL, Key Vault, App Insights, slots, rollback. |
| Container Apps review | `Design the minimum secure Container Apps landing zone for Use-case 03 or 06. Include image flow, secrets, telemetry, auth, and rollback controls.` | Mentions container registry/image flow, Key Vault, managed identity, App Insights, revision rollback. |

### Readiness rubric
- **Ready:** chooses the right start prompt, lists the right skills in order, names the correct Azure landing zone, includes security/database/rollback where needed, and produces a handoff-ready next step.
- **Not ready:** mixes multi-repo and multi-project guidance, treats WebForms/WCF/Classic ASP as package upgrades, skips `/databasemigration` on data-heavy scenarios, or prescribes AKS without justification.

---

## 6) .NET Version Upgrade Guide

| Source | Target | Key challenges | Prompts | Skills | Breaking changes | Tools | Estimated effort | Risk |
|---|---|---|---|---|---|---|---|---|
| .NET Framework 2.0/3.0 | .NET 8 | WebForms, `System.Web`, `web.config`, Windows/Forms auth | `/quickassessment` → `/phase1-planandassess` → `/phase2-migratecode` → `/phase3-generateinfra` | `skills/dotnet-framework-to-dotnet8.md`, `skills/webforms-to-razor.md`, `skills/config-transformation.md`, `skills/azure-app-service.md` | No in-place WebForms path; config/auth/page model redesign required | Upgrade Assistant, try-convert (limited), `dotnet`, Bicep, `azd` | M-L | High |
| .NET Framework 3.5 | .NET 8 | WCF, ASMX-style patterns, old configs, legacy data access | `/quickassessment` → `/phase1-planandassess` → `/databasemigration` → `/phase2-migratecode` | `skills/dotnet-framework-to-dotnet8.md`, `skills/wcf-to-rest-api.md`, `skills/ef-migration.md`, `skills/config-transformation.md` | WCF hosting does not port directly; SOAP contracts and config-based hosting must be redesigned | Upgrade Assistant, try-convert, `dotnet`, OpenAPI tools, Docker | L | High |
| .NET Framework 4.5 | .NET 8 | MVC5 → MVC Core, EF6 → EF Core, Identity/OWIN, `packages.config` | `/quickassessment` → `/phase1-planandassess` → `/databasemigration` → `/phase2-migratecode` | `skills/dotnet-framework-to-dotnet8.md`, `skills/ef-migration.md`, `skills/config-transformation.md`, `skills/azure-entra-id.md` | `System.Web` removal, OWIN/auth rewrite, project format/package changes | Upgrade Assistant, try-convert, `dotnet`, Bicep, `azd` | M-L | Medium-High |
| .NET Framework 4.8 | .NET 8 | Easier package path, but `System.Web` apps still require host rewrite | `/quickassessment` → `/phase1-planandassess` → `/phase2-migratecode` | `skills/config-transformation.md`, `skills/ef-migration.md`, `skills/azure-app-service.md` | Libraries migrate more easily; WebForms/MVC5 hosts still need ASP.NET Core patterns | Upgrade Assistant, try-convert, `dotnet` | S-M | Medium |
| .NET 6 | .NET 8 | Mostly package/API updates, hosting package changes, auth/package drift | `/quickassessment` (optional) → `/phase2-migratecode` → `/phase5-setupcicd` | `skills/dotnet-framework-to-dotnet8.md` (selective use), `skills/config-transformation.md` | Usually incremental; focus on package/API/runtime compatibility | `dotnet`, package upgrade tooling, CI pipelines | XS-S | Low |
| .NET 8 | .NET 9/10 | LTS → STS/LTS planning, package alignment, runtime support strategy | `/quickassessment` or targeted review only | No dedicated repo skill required; use targeted review plus existing CI/CD and config skills as needed | Usually not architectural; mostly runtime/package validation and support-policy planning | `dotnet`, release notes, CI validation | XS | Low |

### Practical guide by source family
- **If the app depends on `System.Web`, ViewState, WebForms, or WCF hosting, treat the move as a redesign.**
- **If the app is already ASP.NET Core, treat the move as an incremental modernization.**
- **If data access is provider-heavy, add `/databasemigration` before Phase 2.**
- **If auth is custom, Windows-based, or OWIN-based, add `skills/azure-entra-id.md` and `/securityhardening` early.**
- **If the app is customer-facing, practice `/phase-rollback` before sign-off.**

---

## Recommended first 30 days for a new team member
1. Read `docs/onboarding/onboarding.md`, this document, and `docs/onboarding/team-guide.md`.
2. Start with **Use-case 02**.
3. Study **BookShop (05)** immediately after Use-case 02.
4. Choose your specialization path from Section 4.
5. Run one assessment exercise and one review exercise from Section 5.
6. Only then move to WCF, Java, or full-stack portfolio work.

## What good looks like
A trained teammate should be able to:
- pick the right use-case as their next lab,
- choose the correct start prompt,
- name the exact skill files to study next,
- explain why the target Azure platform fits the workload,
- identify when `/databasemigration`, `/securityhardening`, or `/phase-rollback` become mandatory,
- and compare their outputs against BookShop without forcing every app into the same architecture.
