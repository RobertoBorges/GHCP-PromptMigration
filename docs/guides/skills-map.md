# Ocean's Twelve Skills Map

Production-ready mapping for Roberto Borges' migration crew: which skills, prompts, and squad agents to use for each target in this repo.

> **Rule of thumb:** use the built-in slash commands for phase control, then use the exact natural-language prompts in this document to steer each use-case. This repo does **not** currently include use-case-specific slash commands like `/assess-wcf-migration`.

## Command legend

- `/quickassessment` — fast triage and complexity scoring
- `/phase1-planandassess` — full assessment and target-state plan
- `/phase2-migratecode` — code modernization
- `/databasemigration` — database schema/provider/data planning
- `/phase3-generateinfra` — Bicep/Terraform + `azure.yaml`
- `/phase4-deploytoazure` — Azure deployment
- `/phase5-setupcicd` — pipelines and release flow
- `/phase6-postmigrationops` — observability, runbooks, SRE readiness
- `/securityhardening` — focused security review
- `/costoptimization` — sizing and FinOps review
- `/phase-rollback` — rollback and recovery
- `/getstatus` — status and next-step summary

## Section A. Technology skills matrix

### 01-ASPClassicApp — The Antique
- **Language/framework skills:** VBScript, Classic ASP, IIS, `global.asa`, ADODB, Jet/Access connection patterns, session state
- **Migration pattern skills:** Classic ASP -> ASP.NET Core rewrite, include-file decomposition, Request/Response/session mapping, ADO/ADODB -> EF Core or repository pattern, `global.asa` -> middleware/startup/services
- **Azure target skills:** Azure App Service, Azure SQL, Key Vault, Application Insights, Entra ID, managed identity
- **Tool skills:** VS Code, GitHub Copilot chat, `az`, `azd`, `dotnet`, Bicep, SQL migration tooling, GitHub Actions
- **Skill files to compose:** `skills/asp-classic-to-dotnet.md`, `skills/config-transformation.md`, `skills/azure-app-service.md`, `skills/azure-sql-migration.md`, `skills/bicep-modules.md`, `skills/github-actions-cicd.md`, `skills/secret-management.md`

### 02-NetFramework30-ASPNET-WEB — The Fossil
- **Language/framework skills:** C#, ASP.NET WebForms, `.aspx`, code-behind, `Web.config`, Windows Authentication
- **Migration pattern skills:** WebForms -> Razor Pages/MVC, `System.Web` -> ASP.NET Core, `Web.config` -> `appsettings.json`, Windows Auth -> Entra ID/App Service auth, server controls/ViewState/postback removal
- **Azure target skills:** Azure App Service, Azure SQL, Key Vault, App Service auth, Application Insights
- **Tool skills:** `dotnet`, Upgrade Assistant, try-convert, `az`, `azd`, Bicep, GitHub Actions
- **Skill files to compose:** `skills/dotnet-framework-to-dotnet8.md`, `skills/webforms-to-razor.md`, `skills/config-transformation.md`, `skills/azure-app-service.md`, `skills/azure-entra-id.md`, `skills/azure-monitor-appinsights.md`, `skills/github-actions-cicd.md`

### 03-WCFNet35 — The Wire
- **Language/framework skills:** C#, .NET Framework 3.5, WCF, `ServiceContract`, `OperationContract`, SOAP, `basicHttpBinding`, `app.config`
- **Migration pattern skills:** WCF -> ASP.NET Core REST API, DTO contract flattening, SOAP endpoint inventory, `app.config` -> `appsettings.json`, self-hosted service -> containerized API, client proxy -> HTTP client/OpenAPI client
- **Azure target skills:** Azure Container Apps, Azure Container Registry, Key Vault, Application Insights, Entra ID for APIs
- **Tool skills:** `dotnet`, Docker, OpenAPI/Swagger, `az`, `azd`, Bicep or Terraform, GitHub Actions
- **Skill files to compose:** `skills/wcf-to-rest-api.md`, `skills/dotnet-framework-to-dotnet8.md`, `skills/config-transformation.md`, `skills/docker-containerize.md`, `skills/azure-container-apps.md`, `skills/azure-key-vault.md`, `skills/azure-monitor-appinsights.md`

### 04-ContosoUniversityDiPS — The Campus
- **Language/framework skills:** C#, ASP.NET Core 2.1, MVC, Razor, React SPA, REST API, EF Core 2.1, Identity 2.0, JWT, SendGrid, Twilio
- **Migration pattern skills:** ASP.NET Core 2.1 -> .NET 8, shared library cleanup, SPA/API/Web boundary preservation, EF Core provider review, auth/token refresh review, config split cleanup, package modernization
- **Azure target skills:** Azure App Service, Azure SQL, App Service deployment slots, Key Vault, App Insights, Entra ID, Static asset strategy for SPA
- **Tool skills:** `dotnet`, npm, `az`, `azd`, Bicep, GitHub Actions, Playwright/Selenium follow-up as needed
- **Skill files to compose:** `skills/dotnet-framework-to-dotnet8.md`, `skills/config-transformation.md`, `skills/ef-migration.md`, `skills/azure-app-service.md`, `skills/azure-entra-id.md`, `skills/azd-configuration.md`, `skills/github-actions-cicd.md`

### 05-BookShop — The Vault (reference)
- **Language/framework skills:** .NET 8, ASP.NET Core, Razor Pages, `Microsoft.Data.SqlClient`, DI, xUnit, Moq
- **Migration pattern skills:** WebForms -> ASP.NET Core reference patterns, SQL migration reference, deployment/runbook reference, `Legacy-Archive` preservation, report/status model
- **Azure target skills:** Azure App Service, Azure SQL, Key Vault, Application Insights, managed identity
- **Tool skills:** `dotnet`, `az`, Bicep, GitHub Actions, Docker, deployment scripts
- **Skill files to study:** `skills/azure-app-service.md`, `skills/azure-sql-migration.md`, `skills/bicep-modules.md`, `skills/azd-configuration.md`, `skills/github-actions-cicd.md`, `skills/rollback-strategy.md`
- **Reference note:** the implemented BookShop assets in this repo show **App Service + Azure SQL** and should be treated as the canonical reference architecture.

### 06-Java-API-BusReservation — The Express
- **Language/framework skills:** Java 8, Spring Boot 2.3, Spring Web, Spring Data JPA, Maven, H2, REST controllers
- **Migration pattern skills:** Java 8 -> Java 21, Spring Boot 2.x -> 3.x, `javax` -> `jakarta`, H2 -> PostgreSQL, containerization, actuator hardening, property migration
- **Azure target skills:** Azure Container Apps, Azure Database for PostgreSQL, Key Vault, Managed Identity/Workload Identity, Application Insights/Azure Monitor
- **Tool skills:** Maven, JDK 21, Docker, `az`, `azd`, Terraform or Bicep, GitHub Actions
- **Skill files to compose:** `skills/java8-to-java21.md`, `skills/docker-containerize.md`, `skills/azure-container-apps.md`, `skills/terraform-azure.md`, `skills/azure-key-vault.md`, `skills/azure-monitor-appinsights.md`, `skills/cost-optimization.md`

### 07-PartsUnlimited-aspnet45 — The Machine
- **Language/framework skills:** C#, ASP.NET MVC 5, .NET Framework 4.5.1, EF6, ASP.NET Identity, OWIN, SQL Server, deployment scripts, test projects
- **Migration pattern skills:** MVC5 -> ASP.NET Core MVC, EF6 -> EF Core, `packages.config` -> SDK-style `PackageReference`, OWIN auth -> ASP.NET Core auth/Entra ID, deployment script replacement, `Web.config` transformation
- **Azure target skills:** Azure App Service, Azure SQL, deployment slots, Key Vault, App Insights, managed identity
- **Tool skills:** Upgrade Assistant, try-convert, `dotnet`, `az`, `azd`, Bicep, GitHub Actions/Azure DevOps
- **Skill files to compose:** `skills/dotnet-framework-to-dotnet8.md`, `skills/ef-migration.md`, `skills/config-transformation.md`, `skills/azure-app-service.md`, `skills/azure-sql-migration.md`, `skills/azure-entra-id.md`, `skills/rollback-strategy.md`

## Section B. Agent dispatch per use-case

### 01-ASPClassicApp
| Phase | Dispatch exactly these agents |
|---|---|
| Phase 1: Assess and plan | Architect (Danny Ocean), Azure Specialist (Basher Tarr), Security Auditor (Frank Catton), Database Specialist (The Amazing Yen), Scribe (Roman Nagel) |
| Phase 2: Migrate code and data | Coder (Rusty Ryan), Database Specialist (The Amazing Yen), Tester (Linus Caldwell), Security Auditor (Frank Catton) |
| Phase 3: Generate infrastructure | Azure Specialist (Basher Tarr), DevOps Engineer (Turk Malloy), Observability Engineer (Livingston Dell), Database Specialist (The Amazing Yen) |
| Phase 4: Deploy and cut over | Cutover Commander (Reuben Tishkoff), Azure Specialist (Basher Tarr), Coder (Rusty Ryan), Security Auditor (Frank Catton) |
| Phase 5: CI/CD and validation | DevOps Engineer (Turk Malloy), Tester (Linus Caldwell), Evaluator (Saul Bloom), Cutover Commander (Reuben Tishkoff) |
| Phase 6: Operate and optimize | Observability Engineer (Livingston Dell), Performance Engineer (Virgil Malloy), Security Auditor (Frank Catton), Scribe (Roman Nagel) |

### 02-NetFramework30-ASPNET-WEB
| Phase | Dispatch exactly these agents |
|---|---|
| Phase 1: Assess and plan | Architect, Azure Specialist, Security Auditor, Tester, Scribe |
| Phase 2: Migrate code and auth | Coder, Tester, Security Auditor, Database Specialist |
| Phase 3: Generate infrastructure | Azure Specialist, DevOps Engineer, Security Auditor, Observability Engineer |
| Phase 4: Deploy and cut over | Cutover Commander, Azure Specialist, Coder, Tester |
| Phase 5: CI/CD and validation | DevOps Engineer, Tester, Evaluator, Cutover Commander |
| Phase 6: Operate and optimize | Observability Engineer, Performance Engineer, Security Auditor, Scribe |

### 03-WCFNet35
| Phase | Dispatch exactly these agents |
|---|---|
| Phase 1: Assess and plan | Architect, Azure Specialist, Security Auditor, Tester, Scribe |
| Phase 2: Convert WCF to REST | Coder, Tester, Security Auditor, Database Specialist |
| Phase 3: Generate infrastructure | Azure Specialist, DevOps Engineer, Observability Engineer, Security Auditor |
| Phase 4: Deploy and cut over | Cutover Commander, Azure Specialist, Coder, Tester |
| Phase 5: CI/CD and validation | DevOps Engineer, Tester, Evaluator, Cutover Commander |
| Phase 6: Operate and optimize | Observability Engineer, Performance Engineer, Security Auditor, Scribe |

### 04-ContosoUniversityDiPS
| Phase | Dispatch exactly these agents |
|---|---|
| Phase 1: Assess and plan | Architect, Azure Specialist, Security Auditor, Database Specialist, Scribe |
| Phase 2: Modernize app layers | Coder, Tester, Database Specialist, Security Auditor |
| Phase 3: Generate infrastructure | Azure Specialist, DevOps Engineer, Observability Engineer, Security Auditor |
| Phase 4: Deploy and cut over | Cutover Commander, Azure Specialist, Coder, Tester |
| Phase 5: CI/CD and validation | DevOps Engineer, Tester, Evaluator, Cutover Commander |
| Phase 6: Operate and optimize | Observability Engineer, Performance Engineer, Security Auditor, Scribe |

### 05-BookShop (reference)
| Phase | Dispatch exactly these agents |
|---|---|
| Phase 1: Extract reference patterns | Architect, Tester, Scribe, Azure Specialist |
| Phase 2: Validate code patterns | Coder, Tester, Evaluator, Database Specialist |
| Phase 3: Validate infrastructure patterns | Azure Specialist, DevOps Engineer, Observability Engineer, Security Auditor |
| Phase 4: Rehearse cutover guidance | Cutover Commander, Azure Specialist, Tester, Security Auditor |
| Phase 5: Rehearse CI/CD guidance | DevOps Engineer, Tester, Evaluator, Cutover Commander |
| Phase 6: Rehearse operations guidance | Observability Engineer, Performance Engineer, Security Auditor, Scribe |

### 06-Java-API-BusReservation
| Phase | Dispatch exactly these agents |
|---|---|
| Phase 1: Assess and plan | Architect, Azure Specialist, Database Specialist, Security Auditor, Scribe |
| Phase 2: Migrate Java and persistence | Coder, Database Specialist, Tester, Security Auditor |
| Phase 3: Generate infrastructure | Azure Specialist, DevOps Engineer, Observability Engineer, Security Auditor |
| Phase 4: Deploy and cut over | Cutover Commander, Azure Specialist, Coder, Tester |
| Phase 5: CI/CD and validation | DevOps Engineer, Tester, Evaluator, Cutover Commander |
| Phase 6: Operate and optimize | Observability Engineer, Performance Engineer, Security Auditor, Scribe |

### 07-PartsUnlimited-aspnet45
| Phase | Dispatch exactly these agents |
|---|---|
| Phase 1: Assess and plan | Architect, Azure Specialist, Security Auditor, Database Specialist, Scribe |
| Phase 2: Modernize MVC, EF, and auth | Coder, Database Specialist, Tester, Security Auditor |
| Phase 3: Generate infrastructure | Azure Specialist, DevOps Engineer, Observability Engineer, Security Auditor |
| Phase 4: Deploy and cut over | Cutover Commander, Azure Specialist, Coder, Tester |
| Phase 5: CI/CD and validation | DevOps Engineer, Tester, Evaluator, Cutover Commander |
| Phase 6: Operate and optimize | Observability Engineer, Performance Engineer, Security Auditor, Scribe |

## Section C. Prompt sequence per use-case

### 01-ASPClassicApp
1. `/quickassessment`
2. `Assess Use-cases/01-ASPClassicApp as a Classic ASP + VBScript + ADODB application. Target .NET 8 on Azure App Service with Azure SQL, Bicep, and GitHub Actions. Call out session state, include files, COM/ADODB dependencies, and global.asa risks.`
3. `/phase1-planandassess`
4. `Create a page-by-page migration map for default.asp, products.asp, product-detail.asp, cart.asp, about.asp, and contact.asp. Show how includes, Session variables, and global.asa events map to ASP.NET Core.`
5. `/databasemigration`
6. `/phase2-migratecode`
7. `/phase3-generateinfra`
8. `/securityhardening`
9. `/phase4-deploytoazure`
10. `/phase5-setupcicd`
11. `/phase6-postmigrationops`
12. `/costoptimization`
13. `/phase-rollback`
14. `/getstatus`

### 02-NetFramework30-ASPNET-WEB
1. `/quickassessment`
2. `Assess Use-cases/02-NetFramework30-ASPNET-WEB as a .NET Framework 3.0 WebForms app. Target .NET 8 on Azure App Service with Azure SQL and Bicep. Flag WebForms, code-behind, Web.config, and Windows Authentication blockers.`
3. `/phase1-planandassess`
4. `Inventory Default.aspx, About.aspx, Secure.aspx, and Web.config. Map each page, server-side event, and auth rule to Razor Pages or MVC endpoints while preserving Secure.aspx behavior.`
5. `/phase2-migratecode`
6. `/securityhardening`
7. `/phase3-generateinfra`
8. `/phase4-deploytoazure`
9. `/phase5-setupcicd`
10. `/phase6-postmigrationops`
11. `/costoptimization`
12. `/phase-rollback`
13. `/getstatus`

### 03-WCFNet35
1. `/quickassessment`
2. `Assess Use-cases/03-WCFNet35 for WCF .NET 3.5 to ASP.NET Core REST migration. Target Azure Container Apps. Score SOAP contract risk, app.config migration risk, and client compatibility risk.`
3. `/phase1-planandassess`
4. `Map every ServiceContract and OperationContract in WCFDemo.Service to REST endpoints, DTOs, status codes, and breaking changes. Recommend container boundaries and API versioning.`
5. `/phase2-migratecode`
6. `/securityhardening`
7. `/phase3-generateinfra`
8. `/phase4-deploytoazure`
9. `/phase5-setupcicd`
10. `/phase6-postmigrationops`
11. `/costoptimization`
12. `/phase-rollback`
13. `/getstatus`

### 04-ContosoUniversityDiPS
1. `/quickassessment`
2. `Assess Use-cases/04-ContosoUniversityDiPS as one multi-project solution with API, Web, React SPA, Data, Common, and Tests. Keep project boundaries explicit. Target .NET 8 on Azure App Service with Azure SQL.`
3. `/phase1-planandassess`
4. `Produce a dependency map across ContosoUniversity.Api, .Web, .Spa.React, .Data, .Common, and test projects. Flag JWT, Identity, SendGrid, Twilio, EF Core provider, and SPA build risks.`
5. `/databasemigration`
6. `/phase2-migratecode`
7. `/securityhardening`
8. `/phase3-generateinfra`
9. `/phase4-deploytoazure`
10. `/phase5-setupcicd`
11. `/phase6-postmigrationops`
12. `/costoptimization`
13. `/phase-rollback`
14. `/getstatus`

### 05-BookShop (reference)
1. `/getstatus`
2. `Use Use-cases/05-BookShop as the reference implementation for .NET 8, ASP.NET Core, Azure App Service, Azure SQL, Bicep, GitHub Actions, and migration reporting. Extract reusable patterns for use-cases 01, 02, and 07.`
3. `/phase6-postmigrationops`
4. `/securityhardening`
5. `/costoptimization`
6. `/phase-rollback`
7. `/getstatus`

### 06-Java-API-BusReservation
1. `/quickassessment`
2. `Assess Use-cases/06-Java-API-BusReservation for Java 8 + Spring Boot 2.3 modernization to Java 21 + Spring Boot 3 on Azure Container Apps with PostgreSQL. Flag javax->jakarta, H2->PostgreSQL, and Docker risks.`
3. `/phase1-planandassess`
4. `Review RestApi.java, pom.xml, and application.properties. Produce an endpoint inventory, dependency upgrade plan, and H2-to-PostgreSQL migration plan.`
5. `/databasemigration`
6. `/phase2-migratecode`
7. `/securityhardening`
8. `/phase3-generateinfra`
9. `/phase4-deploytoazure`
10. `/phase5-setupcicd`
11. `/phase6-postmigrationops`
12. `/costoptimization`
13. `/phase-rollback`
14. `/getstatus`

### 07-PartsUnlimited-aspnet45
1. `/quickassessment`
2. `Assess Use-cases/07-PartsUnlimited-aspnet45 as an ASP.NET MVC 5 / .NET Framework 4.5.1 e-commerce site. Target .NET 8 on Azure App Service with Azure SQL. Flag EF6, ASP.NET Identity, OWIN, deployment scripts, and test migration risk.`
3. `/phase1-planandassess`
4. `Map the MVC controllers, EF6 models, ASP.NET Identity/OWIN configuration, and deploy.cmd flow to ASP.NET Core MVC, EF Core, modern auth, and Azure deployment equivalents.`
5. `/databasemigration`
6. `/phase2-migratecode`
7. `/securityhardening`
8. `/phase3-generateinfra`
9. `/phase4-deploytoazure`
10. `/phase5-setupcicd`
11. `/phase6-postmigrationops`
12. `/costoptimization`
13. `/phase-rollback`
14. `/getstatus`

## Fast dispatch notes

- Use **05-BookShop** as the benchmark for reporting format, `infra/` shape, deployment docs, and production hardening.
- Use `/phase0-multirepoassessment` only when several repositories are involved. **04-ContosoUniversityDiPS is multi-project, not multi-repo.**
- When a cheat sheet says “natural-language prompt,” paste the line exactly after the slash-command output or as the opening message in Copilot chat.
