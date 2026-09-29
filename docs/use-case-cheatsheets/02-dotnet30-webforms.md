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

> ⚠ The rows below are **candidates, not defaults.** `/phase1-plan` presents each option with tradeoffs and records your answer in `reports/Decisions-Required.md`. The agent never picks a target framework, hosting platform, or database engine on your behalf.

| Area | Candidate target (your decision) |
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

## Command sequence

> Steps marked 🟢 are the 7-step main path. Steps marked 🔵 are optional add-ons. Free-text lines are follow-up requests you type in the same thread.

1. `/assess-any-application`
2. `Assess #file:Use-cases/02-NetFramework30-ASPNET-WEB as a .NET Framework 3.0 WebForms app targeting .NET 8 on Azure App Service with Azure SQL and Bicep. Call out WebForms, Secure.aspx, Web.config, and Windows Authentication risks.`
3. `/phase1-plan`
4. `Inventory Default.aspx, About.aspx, Secure.aspx, and Web.config. Map each page, server-side event, and auth rule to Razor Pages or MVC endpoints while preserving Secure.aspx behavior.`
5. `/phase2-migrate-code`
6. `/security-hardening`
7. `/phase3-generate-infra`
8. `/phase4-deploy-to-azure`
9. `/phase5-setup-cicd`
10. `/phase6-post-migration-ops`
11. `/get-status`

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

- [Full walkthrough for this app](../walkthroughs/02-dotnet30-webforms-walkthrough.md)
- [Skill catalog](../architecture/SKILL-CATALOG.md) — all 36 skills and 9 custom agents
- [Skills map](../guides/skills-map.md) — which skills load at which step
- [BookShop reference cheat sheet](05-bookshop-reference.md)
- [BookShop reference walkthrough](../walkthroughs/05-bookshop-reference-walkthrough.md)

## Sample requests

- `Assess #file:Use-cases/02-NetFramework30-ASPNET-WEB for WebForms to Razor Pages migration and preserve Secure.aspx authorization behavior.`
- `Create a page-by-page WebForms to Razor Pages mapping for Default.aspx, About.aspx, and Secure.aspx.`
- `Show how Windows Authentication in Web.config should become Entra ID or App Service authentication on Azure.`
- `Design the Azure App Service target, deployment slots, Key Vault usage, and Application Insights setup for this app.`
