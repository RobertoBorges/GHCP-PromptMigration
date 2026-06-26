# 02-NetFramework30-ASPNET-WEB Cheat Sheet — The Fossil

## What is this app?

A compact ASP.NET WebForms sample on .NET Framework 3.0 with `Default.aspx`, `About.aspx`, `Secure.aspx`, and `Web.config` rules for Windows Authentication. It is the team's entry-level WebForms modernization lab: small enough to assess quickly, but realistic enough to surface the core problems of `System.Web`, page lifecycle, code-behind, and auth migration.

## Source stack

| Area | Current state |
|---|---|
| UI | ASP.NET WebForms (`.aspx` + code-behind) |
| Framework | .NET Framework 3.0 |
| Config | `Web.config`, debug/release transforms |
| Auth | Windows Authentication, `Secure.aspx` authorization rules |
| Hosting | IIS / ASP.NET |
| Data | No active DB in sample, but ADO.NET-style expansion is implied |

## Target stack

| Area | Recommended target |
|---|---|
| UI | ASP.NET Core 8 Razor Pages or MVC |
| Hosting | Azure App Service |
| Auth | Entra ID or App Service authentication |
| Data | Azure SQL when data access is introduced |
| Ops | Application Insights, Key Vault, GitHub Actions |

## Top 5 risks

1. **WebForms lifecycle risk** — postback, server controls, and page events do not translate directly.
2. **Windows Authentication risk** — App Service and Entra ID require a different auth model.
3. **Config conversion risk** — `Web.config` auth and custom errors must be re-expressed in ASP.NET Core.
4. **Secure page parity risk** — `Secure.aspx` behavior must remain explicit after migration.
5. **False simplicity risk** — small sample size can hide how disruptive the System.Web -> ASP.NET Core shift really is.

## Key migration patterns

- Map `.aspx` pages to Razor Pages or MVC actions/views
- Replace code-behind events with controllers/page handlers and services
- Convert `Web.config` to `appsettings.json`, middleware, and App Service settings
- Replace Windows Authentication with Entra ID/App Service auth and ASP.NET Core authorization policies
- Add observability and secret management during the move rather than after

## Prompt sequence

1. `/run quick assessment`
2. `Assess #file:Use-cases/02-NetFramework30-ASPNET-WEB as a .NET Framework 3.0 WebForms app targeting .NET 8 on Azure App Service with Azure SQL and Bicep. Call out WebForms, Secure.aspx, Web.config, and Windows Authentication risks.`
3. `/run Phase 1 plan and assess`
4. `Inventory Default.aspx, About.aspx, Secure.aspx, and Web.config. Map each page, server-side event, and auth rule to Razor Pages or MVC endpoints while preserving Secure.aspx behavior.`
5. `/run Phase 2 code migration`
6. `/run security hardening review`
7. `/run Phase 3 infrastructure generation`
8. `/run Phase 4 deploy to Azure`
9. `/run Phase 5 CI/CD setup`
10. `/run Phase 6 post-migration ops`
11. `@agent show migration status`

## Agent dispatch order

| Phase | Ocean's Twelve dispatch |
|---|---|
| Phase 1 | Architect -> Azure Specialist -> Security Auditor -> Tester |
| Phase 2 | Coder -> Tester -> Security Auditor |
| Phase 3 | Azure Specialist -> DevOps Engineer -> Observability Engineer |
| Phase 4 | Cutover Commander -> Azure Specialist -> Coder |
| Phase 5 | DevOps Engineer -> Tester -> Evaluator |
| Phase 6 | Observability Engineer -> Performance Engineer -> Security Auditor -> Scribe |

## Estimated effort

**3-5 weeks** for a clean migration with modern auth and deployment automation.

## Reference

- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop modernization reference](../../Use-cases/05-BookShop/docs/Modernization-Prompts-Reference.md)

## Sample prompts

- `Assess #file:Use-cases/02-NetFramework30-ASPNET-WEB for WebForms to Razor Pages migration and preserve Secure.aspx authorization behavior.`
- `Create a page-by-page WebForms to Razor Pages mapping for Default.aspx, About.aspx, and Secure.aspx.`
- `Show how Windows Authentication in Web.config should become Entra ID or App Service authentication on Azure.`
- `Design the Azure App Service target, deployment slots, Key Vault usage, and Application Insights setup for this app.`
