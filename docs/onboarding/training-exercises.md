# Ocean's Twelve Training Exercises

Hands-on drills using the actual use-cases in this repo. Each lab is designed so Robert Borges can hand it to a teammate and get a consistent result.

## Shared prerequisites for every exercise

- Visual Studio Code with GitHub Copilot Chat enabled
- This repository open locally
- Access to the prompt library in `.github/prompts/`
- Ability to reference files/folders in chat, for example `#file:Use-cases/02-NetFramework30-ASPNET-WEB`
- Recommended starting mode: App Modernization workflow or standard Copilot Chat with slash commands enabled

---

## Exercise 1 — Your First Assessment

- **Difficulty:** Beginner
- **Timebox:** 30 minutes
- **Use-case:** `02-NetFramework30-ASPNET-WEB`
- **Goal:** Run Phase 1 and produce a credible assessment report

### Exact prompts to use
1. `/quickassessment`
2. `Assess #file:Use-cases/02-NetFramework30-ASPNET-WEB as a .NET Framework 3.0 WebForms app targeting .NET 8 on Azure App Service with Azure SQL and Bicep. Call out WebForms, Secure.aspx, Web.config, and Windows Authentication risks.`
3. `/phase1-planandassess`
4. `Use Azure App Service, Bicep, Azure SQL, Entra ID/App Service authentication, and Application Insights as the target stack. Preserve the secure page behavior.`
5. `Inventory Default.aspx, About.aspx, Secure.aspx, and Web.config. Map each item to its Razor Pages or MVC equivalent.`
6. `/getstatus`

### Expected output
- A complexity score and go/no-go recommendation
- A phase plan with target Azure services
- A list of migration blockers, especially WebForms and Windows Authentication
- A page inventory and suggested target UI pattern
- A clear recommendation that Phase 2 is next

### Common mistakes and fixes
- **Mistake:** Running `/phase1-planandassess` without context
  - **Fix:** Reference the `Use-cases/02-...` folder and target stack explicitly
- **Mistake:** Forgetting Secure.aspx and Windows auth
  - **Fix:** Repeat the assessment with the security requirement called out
- **Mistake:** Asking for a direct package upgrade only
  - **Fix:** Reframe it as WebForms -> ASP.NET Core redesign

### Assessment criteria
- Mentions Windows Authentication and how to modernize it
- Mentions WebForms-to-Razor migration, not just package updates
- Names App Service, Azure SQL, Bicep, and Application Insights
- Recommends `/phase2-migratecode` as the next command

---

## Exercise 2 — WCF to REST

- **Difficulty:** Intermediate
- **Timebox:** 2 hours
- **Use-case:** `03-WCFNet35`
- **Goal:** Convert one WCF service contract into a REST-first migration plan and validation checklist

### Exact prompts to use
1. `/quickassessment`
2. `Assess #file:Use-cases/03-WCFNet35 for WCF .NET 3.5 to ASP.NET Core REST migration on Azure Container Apps. Focus on ServiceContract, OperationContract, basicHttpBinding, app.config, and client compatibility.`
3. `/phase1-planandassess`
4. `Map each operation in WCFDemo.Service to REST endpoints, request/response DTOs, status codes, and breaking changes. Recommend API versioning and authentication approach.`
5. `/phase2-migratecode`
6. `Convert one service flow end to end: contract -> DTO -> REST endpoint -> validation rules -> replacement client call. Preserve the business meaning of the original operation.`
7. `/securityhardening`
8. `/getstatus`

### Expected output
- A contract inventory showing SOAP-to-REST mappings
- A list of breaking changes and mitigation options
- A proposed API surface and deployment target (Container Apps)
- Validation guidance for the migrated endpoint
- A next-step recommendation for infrastructure and deployment

### Common mistakes and fixes
- **Mistake:** Treating WCF as a simple package update
  - **Fix:** Ask explicitly for contract and endpoint redesign
- **Mistake:** Ignoring the client application
  - **Fix:** Ask for replacement client strategy and compatibility notes
- **Mistake:** Skipping auth/security planning
  - **Fix:** Run `/securityhardening` before leaving the exercise

### Assessment criteria
- Lists at least one WCF contract-to-REST mapping
- Explains breaking changes clearly
- Recommends Container Apps, not IIS-style self-hosting
- Produces a validation or test checklist for the migrated endpoint

---

## Exercise 3 — Full Migration Runbook

- **Difficulty:** Advanced
- **Timebox:** 1 day
- **Use-case:** `07-PartsUnlimited-aspnet45`
- **Goal:** Complete Phases 1-5 and compare the outcome against BookShop (05)

### Exact prompts to use
1. `/quickassessment`
2. `Assess #file:Use-cases/07-PartsUnlimited-aspnet45 as an ASP.NET MVC 5 / .NET Framework 4.5.1 app targeting .NET 8 on Azure App Service with Azure SQL. Highlight EF6, ASP.NET Identity, OWIN, deployment scripts, and test migration risk.`
3. `/phase1-planandassess`
4. `Use Azure App Service, Azure SQL, Bicep, Key Vault, Application Insights, and GitHub Actions as the target stack. Require a rollback path and deployment slots.`
5. `/databasemigration`
6. `/phase2-migratecode`
7. `/securityhardening`
8. `/phase3-generateinfra`
9. `/phase4-deploytoazure`
10. `/phase5-setupcicd`
11. `Compare the resulting plan and artifacts against #file:Use-cases/05-BookShop and call out any missing reference patterns.`
12. `/getstatus`

### Expected output
- Phase 1 assessment report with risks, scope, and target architecture
- Database migration plan for EF6/SQL Server -> EF Core/Azure SQL
- Phase 2 modernization approach for MVC, auth, and deployment scripts
- Infra and deployment recommendations for App Service + Azure SQL
- CI/CD design with validation, approvals, and rollback guidance
- BookShop comparison notes

### Common mistakes and fixes
- **Mistake:** Under-scoping EF6 and auth migration
  - **Fix:** Re-run `/databasemigration` and ask for Identity/OWIN mapping explicitly
- **Mistake:** Skipping rollback planning
  - **Fix:** Add `/phase-rollback` if the first plan is weak
- **Mistake:** Not using BookShop as the benchmark
  - **Fix:** Ask for a gap analysis against `Use-cases/05-BookShop`

### Assessment criteria
- Identifies EF6, Identity, OWIN, and deployment scripts as major workstreams
- Produces a realistic App Service + Azure SQL plan
- Includes CI/CD, security, and rollback elements
- Calls out differences from BookShop rather than assuming parity

---

## Exercise 4 — Multi-Project Assessment

- **Difficulty:** Advanced
- **Timebox:** 2 hours
- **Use-case:** `04-ContosoUniversityDiPS`
- **Goal:** Assess a multi-project solution with API + SPA + data + tests without treating it as multi-repo

### Exact prompts to use
1. `/quickassessment`
2. `Assess #file:Use-cases/04-ContosoUniversityDiPS as one multi-project solution with API, Web, React SPA, Data, Common, and Tests. Target .NET 8 on Azure App Service with Azure SQL. Do not treat this as a multi-repo assessment.`
3. `/phase1-planandassess`
4. `Produce a dependency map across the projects. Highlight JWT, Identity, SendGrid, Twilio, EF Core provider choices, SPA build pipeline, and test-suite impact.`
5. `/databasemigration`
6. `/getstatus`

### Expected output
- A dependency matrix across projects
- A recommended target topology for API, web app, SPA assets, and database
- A list of auth, provider, and package risks
- A phased modernization order for API/Web/SPA/Data/tests

### Common mistakes and fixes
- **Mistake:** Using `/phase0-multirepoassessment`
  - **Fix:** Start over with `/quickassessment` and note it is one repo
- **Mistake:** Treating the SPA as an afterthought
  - **Fix:** Ask explicitly for build, packaging, and hosting guidance
- **Mistake:** Missing SendGrid/Twilio secrets
  - **Fix:** Ask for Key Vault and secret management recommendations

### Assessment criteria
- Keeps the repo as a single solution with multiple projects
- Mentions JWT, Identity, SPA build tooling, EF Core providers, and secrets
- Produces a workstream-based plan rather than a single flat estimate

---

## Exercise 5 — Java Migration

- **Difficulty:** Intermediate
- **Timebox:** 2 hours
- **Use-case:** `06-Java-API-BusReservation`
- **Goal:** Assess and plan Java 8 -> Java 21 modernization with database and container implications

### Exact prompts to use
1. `/quickassessment`
2. `Assess #file:Use-cases/06-Java-API-BusReservation for Java 8 + Spring Boot 2.3 modernization to Java 21 + Spring Boot 3 on Azure Container Apps with PostgreSQL. Highlight H2, javax->jakarta, Docker, and Maven risks.`
3. `/phase1-planandassess`
4. `Review pom.xml, application.properties, and RestApi.java. Produce an endpoint inventory, dependency upgrade plan, and target architecture using Container Apps and PostgreSQL.`
5. `/databasemigration`
6. `/getstatus`

### Expected output
- A Java and Spring upgrade path
- A database migration plan from H2 to PostgreSQL
- Container and runtime recommendations for Container Apps
- A prioritized backlog of compatibility issues

### Common mistakes and fixes
- **Mistake:** Assuming H2 can remain unchanged in production
  - **Fix:** Ask explicitly for PostgreSQL migration steps
- **Mistake:** Forgetting `javax` -> `jakarta`
  - **Fix:** Ask for a package/import impact summary
- **Mistake:** Skipping containerization details
  - **Fix:** Ask for Dockerfile/runtime changes before Phase 3

### Assessment criteria
- Mentions Java 21, Spring Boot 3, and `jakarta`
- Produces a real H2 -> PostgreSQL plan
- Chooses Container Apps as the hosting target
- Leaves a clean next-step recommendation for `/phase2-migratecode`

---

## Scoring guide for team leads

| Score | Meaning |
|---|---|
| 5/5 | Output is ready to hand to the next squad member with no clarification |
| 4/5 | Solid output with one or two gaps to tighten |
| 3/5 | Usable, but missing key risks or target-state details |
| 2/5 | Too generic; trainee likely did not ground the prompts in the use-case |
| 1/5 | Wrong prompt flow or wrong migration target |

## Debrief questions

1. Which risks were found early because the prompt named the exact framework or auth pattern?
2. Which outputs were stronger after adding natural-language steering prompts?
3. Where did BookShop help as the reference implementation?
4. What would you hand off to the next Ocean's Twelve role?
