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

| Area | Recommended target |
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

## Prompt sequence

1. `@squad run quick assessment`
2. `Assess #file:Use-cases/01-ASPClassicApp as a Classic ASP + VBScript + ADODB application. Target .NET 8 on Azure App Service with Azure SQL, Bicep, and GitHub Actions. Call out session state, include files, COM/ADODB dependencies, and global.asa risks.`
3. `@squad run Phase 1 plan and assess`
4. `Create a page-by-page migration map for default.asp, products.asp, product-detail.asp, cart.asp, about.asp, and contact.asp. Show how includes, Session variables, and global.asa events map to ASP.NET Core.`
5. `@squad run database migration review`
6. `@squad run Phase 2 code migration`
7. `@squad run Phase 3 infrastructure generation`
8. `@squad run security hardening review`
9. `@squad run Phase 4 deploy to Azure`
10. `@squad run Phase 5 CI/CD setup`
11. `@squad run Phase 6 post-migration ops`
12. `@squad show migration status`

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

- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop modernization reference](../../Use-cases/05-BookShop/docs/Modernization-Prompts-Reference.md)

## Sample prompts

- `Assess #file:Use-cases/01-ASPClassicApp for a full rewrite to .NET 8 on Azure App Service with Azure SQL. Show the safest strangler path.`
- `Map Classic ASP includes, Session variables, and global.asa events to ASP.NET Core equivalents.`
- `Design the Azure App Service + Azure SQL target for this app, including Key Vault and Application Insights.`
- `Create a migration backlog that converts pages first, then cart/session, then data access, then deployment.`
