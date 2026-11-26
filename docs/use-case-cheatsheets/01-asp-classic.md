# 01-ASPClassicApp Cheat Sheet — The Antique

## What is this app?

A small Classic ASP storefront used as the repo's pure legacy baseline. It mixes `.asp` pages, include files, `global.asa`, ADODB access, and session state to model a simple catalog/cart experience. For Ocean's Twelve, this is the clearest example of a full-platform rewrite rather than a package upgrade.

## Source stack

| Area | Current state |
|---|---|
| UI | Classic ASP pages (`default.asp`, `products.asp`, `product-detail.asp`, `cart.asp`) |
| Language | VBScript |
| Data | ADODB / Jet-style connection string in `database.asp` |
| State | `Session(...)` and `Application(...)` in `global.asa` |
| Hosting | IIS / ASP Classic |
| Auth | None in sample; session/cart state only |

## Target stack

> ⚠ The rows below are **candidates, not defaults.** `/phase1-plan` presents each option with tradeoffs and records your answer in `reports/Decisions-Required.md`. The agent never picks a target framework, hosting platform, or database engine on your behalf.

| Area | Candidate target (your decision) |
|---|---|
| UI | ASP.NET Core 8 Razor Pages or MVC |
| Data | Azure SQL + EF Core or repository abstraction |
| Hosting | Azure App Service |
| Security | Entra ID or App Service auth, Key Vault, managed identity |
| Ops | Application Insights, Azure Monitor, GitHub Actions |

## Top 5 risks

1. **Platform rewrite risk** — there is no direct ASP Classic -> .NET 8 path.
2. **Session/global state risk** — `global.asa` and cart/session logic must be redesigned.
3. **ADODB provider risk** — `Microsoft.Jet.OLEDB.4.0` is not a cloud target.
4. **Include-file coupling risk** — shared layout and behavior may be scattered across includes.
5. **Hidden IIS assumptions** — local IIS behavior may hide path, permission, or session dependencies.

## Key migration patterns

- Replace Classic ASP pages with Razor Pages or MVC controllers/views
- Convert include files to layouts, partials, and shared services
- Map `Application(...)` startup values to configuration/services
- Replace ADODB/Jet with Azure SQL access via EF Core or a repository layer
- Move session/cart behavior to ASP.NET Core session, cache, or persistence

## Command sequence

> Steps marked 🟢 are the 7-step main path. Steps marked 🔵 are optional add-ons. Free-text lines are follow-up requests you type in the same thread.

1. `/assess-any-application`
2. `Assess #file:Use-cases/01-ASPClassicApp as a Classic ASP + VBScript + ADODB application. Target .NET 8 on Azure App Service with Azure SQL, Bicep, and GitHub Actions. Call out session state, include files, COM/ADODB dependencies, and global.asa risks.`
3. `/phase1-plan`
4. `Create a page-by-page migration map for default.asp, products.asp, product-detail.asp, cart.asp, about.asp, and contact.asp. Show how includes, Session variables, and global.asa events map to ASP.NET Core.`
5. `/database-migration`
6. `/phase2-migrate-code`
7. `/phase3-generate-infra`
8. `/security-hardening`
9. `/phase4-deploy-to-azure`
10. `/phase5-setup-cicd`
11. `/phase6-post-migration-ops`
12. `/get-status`

## Agent dispatch order

| Phase | Ocean's Twelve dispatch |
|---|---|
| Phase 1 | Architect -> Azure Specialist -> Security Auditor -> Database Specialist |
| Phase 2 | Coder -> Database Specialist -> Tester |
| Phase 3 | Azure Specialist -> DevOps Engineer -> Observability Engineer |
| Phase 4 | Cutover Commander -> Azure Specialist -> Coder |
| Phase 5 | DevOps Engineer -> Tester -> Evaluator |
| Phase 6 | Observability Engineer -> Performance Engineer -> Security Auditor -> Scribe |

## Estimated effort

**4-6 weeks** for a production-ready rewrite with basic storefront parity.

## Reference

- [Full walkthrough for this app](../walkthroughs/01-classic-asp-walkthrough.md)
- [Skill catalog](../architecture/SKILL-CATALOG.md) — all 65 skills and 10 custom agents
- [Skills map](../guides/skills-map.md) — which skills load at which step
- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop reference walkthrough](../walkthroughs/05-bookshop-reference-walkthrough.md)

## Sample requests

- `Assess #file:Use-cases/01-ASPClassicApp for a full rewrite to .NET 8 on Azure App Service with Azure SQL. Show the safest strangler path.`
- `Map Classic ASP includes, Session variables, and global.asa events to ASP.NET Core equivalents.`
- `Design the Azure App Service + Azure SQL target for this app, including Key Vault and Application Insights.`
- `Create a migration backlog that converts pages first, then cart/session, then data access, then deployment.`
