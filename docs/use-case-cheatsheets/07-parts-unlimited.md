# 07-PartsUnlimited-aspnet45 Cheat Sheet — The Machine

## What is this app?

A fuller-featured ASP.NET MVC 5 commerce sample on .NET Framework 4.5.1 with EF6, ASP.NET Identity, OWIN-era auth components, deployment scripts, docs, and tests. It is the repo's most realistic “enterprise legacy web app” lab and the best advanced exercise after BookShop.

## Source stack

| Area | Current state |
|---|---|
| UI | ASP.NET MVC 5 / Razor views |
| Framework | .NET Framework 4.5.1 |
| Data | EF6 + SQL Server |
| Auth | ASP.NET Identity + OWIN |
| Delivery | `deploy.cmd`, Azure/IIS-era deployment assets |
| Tests | Unit tests and Selenium-style test assets |

## Target stack

| Area | Recommended target |
|---|---|
| UI | ASP.NET Core 8 MVC |
| Data | EF Core + Azure SQL |
| Hosting | Azure App Service |
| Security | Entra ID or modern ASP.NET Core Identity, Key Vault, managed identity |
| Delivery | Bicep + GitHub Actions or Azure DevOps |
| Ops | Deployment slots, Application Insights, rollback guidance |

## Top 5 risks

1. **EF6 migration risk** — provider and query behavior may change under EF Core.
2. **Identity/OWIN risk** — auth flows need a deliberate modernization plan.
3. **System.Web MVC risk** — MVC 5 and ASP.NET Core MVC are related, but not drop-in compatible.
4. **Deployment automation risk** — `deploy.cmd` and older Azure assumptions must be replaced.
5. **Scope risk** — this app has enough surface area to drift into an unbounded migration.

## Key migration patterns

- MVC 5 -> ASP.NET Core MVC with explicit routing and middleware updates
- EF6 -> EF Core with query and migration validation
- OWIN / ASP.NET Identity -> ASP.NET Core auth or Entra ID
- `packages.config` -> SDK-style project + PackageReference
- Legacy deployment scripts -> Bicep + CI/CD pipeline + staged deployment

## Prompt sequence

1. `/run quick assessment`
2. `Assess #file:Use-cases/07-PartsUnlimited-aspnet45 as an ASP.NET MVC 5 / .NET Framework 4.5.1 app targeting .NET 8 on Azure App Service with Azure SQL. Highlight EF6, ASP.NET Identity, OWIN, deployment scripts, and test migration risk.`
3. `/run Phase 1 plan and assess`
4. `Map the MVC controllers, EF6 models, ASP.NET Identity/OWIN configuration, and deploy.cmd flow to ASP.NET Core MVC, EF Core, modern auth, and Azure deployment equivalents.`
5. `/run database migration review`
6. `/run Phase 2 code migration`
7. `/run security hardening review`
8. `/run Phase 3 infrastructure generation`
9. `/run Phase 4 deploy to Azure`
10. `/run Phase 5 CI/CD setup`
11. `/run Phase 6 post-migration ops`
12. `@agent show migration status`

## Agent dispatch order

| Phase | Ocean's Twelve dispatch |
|---|---|
| Phase 1 | Architect -> Azure Specialist -> Security Auditor -> Database Specialist |
| Phase 2 | Coder -> Database Specialist -> Tester -> Security Auditor |
| Phase 3 | Azure Specialist -> DevOps Engineer -> Observability Engineer |
| Phase 4 | Cutover Commander -> Azure Specialist -> Coder |
| Phase 5 | DevOps Engineer -> Tester -> Evaluator |
| Phase 6 | Observability Engineer -> Performance Engineer -> Security Auditor -> Scribe |

## Estimated effort

**4-6 weeks** for a disciplined modernization with infra, CI/CD, and auth redesign.

## Reference

- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop modernization reference](../../Use-cases/05-BookShop/docs/Modernization-Prompts-Reference.md)

## Sample prompts

- `Assess #file:Use-cases/07-PartsUnlimited-aspnet45 for ASP.NET MVC 5 to ASP.NET Core MVC migration and rank the EF6 and auth blockers.`
- `Create a migration plan for EF6, ASP.NET Identity, OWIN, deployment scripts, and test assets.`
- `Design the Azure App Service + Azure SQL target, including slots, Key Vault, Application Insights, and rollback readiness.`
- `Compare this plan against #file:Use-cases/05-BookShop and list the missing reference patterns we should copy.`
