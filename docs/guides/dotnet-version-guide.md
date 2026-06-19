# .NET Version Upgrade Guide

Quick reference for Robert Borges' Ocean's Twelve crew when choosing between incremental upgrades and a direct move to .NET 8.

## 1. At-a-glance migration paths

| Source | Recommended path to .NET 8 | Typical landing pattern | Use-cases in this repo | Primary prompts |
|---|---|---|---|---|
| ASP Classic | Rewrite directly to ASP.NET Core 8 | Razor Pages/MVC on App Service | 01 | `/quickassessment`, `/phase1-planandassess`, `/phase2-migratecode`, `/databasemigration` |
| .NET Framework 2.0/3.0 WebForms | Assess directly for rewrite; optional short stabilization on 3.5/4.8 only if needed to inventory behavior | Razor Pages/MVC on App Service | 02 | `/quickassessment`, `/phase1-planandassess`, `/phase2-migratecode` |
| .NET Framework 3.5 WebForms | Rewrite web tier; reuse business/data logic selectively | ASP.NET Core 8 web app + Azure SQL | 05 (reference path) | `/quickassessment`, `/phase1-planandassess`, `/phase2-migratecode`, `/databasemigration` |
| .NET Framework 3.5 WCF | Prefer contract-first REST rewrite; keep SOAP only if external compatibility requires bridge strategy | ASP.NET Core Web API on Container Apps | 03 | `/quickassessment`, `/phase1-planandassess`, `/phase2-migratecode` |
| .NET Framework 4.0-4.5.x MVC/Web API | Stabilize on 4.8 if package debt is high, then move to .NET 8 | ASP.NET Core MVC/Web API on App Service | 07 | `/quickassessment`, `/phase1-planandassess`, `/phase2-migratecode`, `/databasemigration` |
| .NET Framework 4.6-4.8 libraries/services | Upgrade Assistant + try-convert are more viable; web UI still needs System.Web rewrite | SDK-style projects, ASP.NET Core host, EF Core | 07-adjacent path | `/quickassessment`, `/phase1-planandassess`, `/phase2-migratecode` |
| ASP.NET Core 2.1 | Incremental package/runtime modernization to .NET 8; usually no rewrite | ASP.NET Core 8 App Service solution | 04 | `/quickassessment`, `/phase1-planandassess`, `/phase2-migratecode` |

## 2. Breaking changes by version jump

### ASP Classic -> .NET 8
- No in-place upgrade path
- VBScript, `global.asa`, and include files must be re-modeled
- ADODB/Jet patterns usually become EF Core, Dapper, or repository abstractions
- IIS session/application events become middleware, DI services, or distributed cache

### .NET Framework 3.0/3.5 WebForms -> .NET 8
- `System.Web` and WebForms do not exist in .NET 8
- ViewState, postbacks, server controls, and code-behind event models must be redesigned
- `Web.config` becomes `appsettings.json` + environment variables + Key Vault
- Windows Authentication often becomes Entra ID or App Service authentication

### .NET Framework 3.5 WCF -> .NET 8
- Server-side WCF is not supported as-is in .NET 8
- SOAP endpoints, bindings, and config-based hosting must be redesigned
- `app.config` serviceModel sections become code-based ASP.NET Core hosting and OpenAPI metadata
- Generated client proxies typically become `HttpClient` or typed OpenAPI clients

### .NET Framework 4.5.x MVC / EF6 / OWIN -> .NET 8
- `System.Web.Mvc`, OWIN middleware, and ASP.NET Identity wiring change significantly
- `packages.config` becomes SDK-style `PackageReference`
- EF6 LINQ, lazy loading, migrations, and provider behavior need review under EF Core
- `HttpContext`, filters, bundling, and startup patterns move to ASP.NET Core middleware and endpoint routing

### ASP.NET Core 2.1 -> .NET 8
- Package versions jump across unsupported releases
- Hosting model, endpoint routing, nullable reference types, and auth packages changed
- Older SPA, React build chains, and Node/npm assumptions often require refresh
- Deprecated APIs in EF Core 2.1, auth, and configuration need targeted rewrites

## 3. Which use-cases demonstrate each path

| Path | Best example in repo | Why it matters |
|---|---|---|
| Legacy script to modern web app | 01-ASPClassicApp | Pure rewrite pattern, session and ADO concerns |
| Earliest WebForms to .NET 8 | 02-NetFramework30-ASPNET-WEB | WebForms + Windows Auth modernization |
| WCF contract modernization | 03-WCFNet35 | SOAP to REST, config to code, API hosting |
| Early ASP.NET Core modernization | 04-ContosoUniversityDiPS | Multi-project, Identity/JWT, React SPA |
| Completed WebForms modernization | 05-BookShop | Reference implementation with .NET 8, App Service, Azure SQL |
| Mature MVC 5 / EF6 modernization | 07-PartsUnlimited-aspnet45 | MVC, EF6, Identity, deployment automation |

## 4. Prompt recipes by source version

### .NET Framework 3.0 / 3.5 WebForms
1. `/quickassessment`
2. `Assess this WebForms application for direct migration to .NET 8 on Azure App Service. Inventory .aspx pages, code-behind, ViewState, server controls, Windows Authentication, and config risks.`
3. `/phase1-planandassess`
4. `/phase2-migratecode`
5. `/securityhardening`

### .NET Framework 3.5 WCF
1. `/quickassessment`
2. `Assess this WCF solution for conversion to ASP.NET Core REST APIs on Azure Container Apps. Map ServiceContract and OperationContract items to REST endpoints and flag compatibility gaps.`
3. `/phase1-planandassess`
4. `/phase2-migratecode`
5. `/phase3-generateinfra`

### .NET Framework 4.5.x MVC / EF6
1. `/quickassessment`
2. `Assess this ASP.NET MVC / EF6 / Identity solution for modernization to .NET 8 on Azure App Service with Azure SQL. Identify EF6, OWIN, and deployment-script blockers.`
3. `/phase1-planandassess`
4. `/databasemigration`
5. `/phase2-migratecode`

### ASP.NET Core 2.1
1. `/quickassessment`
2. `Assess this ASP.NET Core 2.1 multi-project solution for in-place modernization to .NET 8 while preserving API, Web, SPA, Data, and test boundaries.`
3. `/phase1-planandassess`
4. `/phase2-migratecode`
5. `/phase5-setupcicd`

## 5. Tooling reference

| Tool | Best use | Notes |
|---|---|---|
| .NET Upgrade Assistant | Project analysis, SDK-style conversion, dependency guidance | Strongest for libraries and newer framework apps; still requires manual work for System.Web apps |
| try-convert | Convert old csproj to SDK-style | Useful for libraries and some non-web projects; not enough by itself for WebForms/WCF/MVC |
| dotnet-migration analyzer | Inventory unsupported APIs and packages | Good before `/phase1-planandassess`; use findings to scope rewrite vs incremental path |
| `dotnet` CLI | Build, test, restore, package validation | Core loop during Phase 2-5 |
| `az` + `azd` | Azure validation and deployment | Use once target architecture is approved |
| Bicep / Terraform | IaC generation | App Service-heavy migrations fit Bicep well; mixed Java/container estates may prefer Terraform |

## 6. Decision tree: incremental upgrade or rewrite?

```text
Does the app depend on System.Web, WebForms, WCF server hosting, or ASP Classic?
├─ Yes -> Rewrite the web/service host for .NET 8.
│        Reuse isolated business logic only after validation.
└─ No -> Continue.

Is the app already on ASP.NET Core or mostly class libraries?
├─ Yes -> Prefer incremental modernization with Upgrade Assistant + try-convert.
└─ No -> Continue.

Are auth, EF6, or deployment scripts tightly coupled to runtime behavior?
├─ Yes -> Consider a stabilization hop to .NET Framework 4.8 before the .NET 8 move.
└─ No -> Continue.

Is external contract compatibility mandatory (SOAP, binary clients, legacy auth)?
├─ Yes -> Use a strangler pattern, compatibility bridge, or phased cutover.
└─ No -> Prefer direct .NET 8 landing.
```

## 7. Recommended defaults for this repo

- **01** -> rewrite directly
- **02** -> rewrite directly; do not chase a WebForms-preserving path
- **03** -> rewrite contracts to REST unless a hard SOAP requirement exists
- **04** -> incremental modernization from ASP.NET Core 2.1 to .NET 8
- **05** -> study as the completed reference pattern
- **07** -> assess first; if EF6/OWIN/package debt is severe, stabilize on 4.8 in a branch, then modernize to .NET 8

## 8. Fast reminder

If the source app still depends on `System.Web`, ViewState, WebForms, WCF config hosting, or ASP Classic scripts, treat the move to .NET 8 as a **platform redesign**, not a package upgrade.
