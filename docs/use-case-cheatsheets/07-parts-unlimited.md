# 07-PartsUnlimited-aspnet45 Cheat Sheet — The Warehouse

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

> ⚠ The rows below are **candidates, not defaults.** `/phase1-plan` presents each option with tradeoffs and records your answer in `reports/Decisions-Required.md`. The agent never picks a target framework, hosting platform, or database engine on your behalf.

| Area | Candidate target (your decision) |
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

## Command sequence

> Steps marked 🟢 are the 7-step main path. Steps marked 🔵 are optional add-ons. Free-text lines are follow-up requests you type in the same thread.

1. `/assess-any-application`
2. `Assess #file:Use-cases/07-PartsUnlimited-aspnet45 as an ASP.NET MVC 5 / .NET Framework 4.5.1 app targeting .NET 8 on Azure App Service with Azure SQL. Highlight EF6, ASP.NET Identity, OWIN, deployment scripts, and test migration risk.`
3. `/phase1-plan`
4. `Map the MVC controllers, EF6 models, ASP.NET Identity/OWIN configuration, and deploy.cmd flow to ASP.NET Core MVC, EF Core, modern auth, and Azure deployment equivalents.`
5. `/database-migration`
6. `/phase2-migrate-code`
7. `/security-hardening`
8. `/phase3-generate-infra`
9. `/phase4-deploy-to-azure`
10. `/phase5-setup-cicd`
11. `/phase6-post-migration-ops`
12. `/get-status`

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

- [Full walkthrough for this app](../walkthroughs/07-parts-unlimited-walkthrough.md)
- [Skill catalog](../architecture/SKILL-CATALOG.md) — all 65 skills and 10 custom agents
- [Skills map](../guides/skills-map.md) — which skills load at which step
- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop reference walkthrough](../walkthroughs/05-bookshop-reference-walkthrough.md)

## Sample requests

- `Assess #file:Use-cases/07-PartsUnlimited-aspnet45 for ASP.NET MVC 5 to ASP.NET Core MVC migration and rank the EF6 and auth blockers.`
- `Create a migration plan for EF6, ASP.NET Identity, OWIN, deployment scripts, and test assets.`
- `Design the Azure App Service + Azure SQL target, including slots, Key Vault, Application Insights, and rollback readiness.`
- `Compare this plan against #file:Use-cases/05-BookShop and list the missing reference patterns we should copy.`
