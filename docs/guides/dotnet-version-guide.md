# .NET Version Upgrade Guide

Reference for choosing between an incremental upgrade and a rewrite when the discovered stack is **.NET**. This guide is the depth behind `stack-adapters/references/stack-dotnet.md` and `dotnet-modernization/references/`.

> ## ⚠ The target version is a decision, not a default
>
> This guide never tells you which .NET version to land on. **.NET 10 LTS and .NET 8 LTS are both valid**, and so is "stay on .NET Framework for now". The choice is recorded in `reports/Decisions-Required.md` during `/phase1-plan` and is enforced as a hard stop before `/phase2-migrate-code` runs.
>
> Wherever this page says *"the chosen LTS"*, it means the version **you** picked — not one this tool assumed. See `.github/skills/migration-decisions/references/decision-catalog.md`.
>
> This guide also covers only one of fourteen supported stacks. For Java, Python, Node.js, PHP, Ruby, Go, Perl, Rust, Scala/Kotlin, C++ (Windows), Delphi/VB6, PowerBuilder, or Oracle Forms, start at `/assess-any-application` and let `stack-adapters` route you.

## 1. At-a-glance migration paths

| Source | Recommended path | Typical landing pattern | Reference use-case | Commands |
|---|---|---|---|---|
| ASP Classic | Rewrite directly to ASP.NET Core on the chosen LTS | Razor Pages/MVC on App Service | 01 | `/quick-assessment`, `/phase1-plan`, `/phase2-migrate-code`, `/database-migration` |
| .NET Framework 2.0/3.0 WebForms | Assess directly for rewrite; optional short stabilization on 3.5/4.8 only if needed to inventory behavior | Razor Pages/MVC on App Service | 02 | `/quick-assessment`, `/phase1-plan`, `/phase2-migrate-code` |
| .NET Framework 3.5 WebForms | Rewrite the web tier; reuse business/data logic selectively | ASP.NET Core web app + managed SQL | 05 (reference path) | `/quick-assessment`, `/phase1-plan`, `/phase2-migrate-code`, `/database-migration` |
| .NET Framework 3.5 WCF | Prefer contract-first REST rewrite; keep SOAP only if external compatibility forces a bridge strategy | ASP.NET Core Web API on Container Apps | 03 | `/quick-assessment`, `/phase1-plan`, `/phase2-migrate-code` |
| .NET Framework 4.0-4.5.x MVC/Web API | Stabilize on 4.8 if package debt is high, then move to the chosen LTS | ASP.NET Core MVC/Web API on App Service | 07 | `/quick-assessment`, `/phase1-plan`, `/phase2-migrate-code`, `/database-migration` |
| .NET Framework 4.6-4.8 libraries/services | Upgrade Assistant + try-convert are viable; web UI still needs a `System.Web` rewrite | SDK-style projects, ASP.NET Core host, EF Core | 07-adjacent | `/quick-assessment`, `/phase1-plan`, `/phase2-migrate-code` |
| .NET Core 2.1 / 3.1 | Incremental package/runtime modernization; usually no rewrite | ASP.NET Core solution on App Service | 04 | `/quick-assessment`, `/phase1-plan`, `/phase2-migrate-code` |

## 2. Breaking changes by version jump

### ASP Classic → modern .NET
- No in-place upgrade path
- VBScript, `global.asa`, and include files must be re-modeled
- ADODB/Jet patterns usually become EF Core, Dapper, or repository abstractions
- IIS session/application events become middleware, DI services, or distributed cache

### .NET Framework 3.0/3.5 WebForms → modern .NET
- `System.Web` and WebForms do not exist on modern .NET
- ViewState, postbacks, server controls, and code-behind event models must be redesigned
- `Web.config` becomes `appsettings.json` + environment variables + Key Vault
- Windows Authentication often becomes Entra ID or App Service authentication

### .NET Framework 3.5 WCF → modern .NET
- Server-side WCF is not supported as-is
- SOAP endpoints, bindings, and config-based hosting must be redesigned
- `app.config` `serviceModel` sections become code-based ASP.NET Core hosting and OpenAPI metadata
- Generated client proxies typically become `HttpClient` or typed OpenAPI clients
- **Existing SOAP clients will need updates** — this is a rewrite, not a compatibility layer

### .NET Framework 4.5.x MVC / EF6 / OWIN → modern .NET
- `System.Web.Mvc`, OWIN middleware, and ASP.NET Identity wiring change significantly
- `packages.config` becomes SDK-style `PackageReference`
- EF6 LINQ, lazy loading, migrations, and provider behavior need review under EF Core
- `HttpContext`, filters, bundling, and startup patterns move to ASP.NET Core middleware and endpoint routing

### .NET Core 2.1 / 3.1 → modern .NET
- Package versions jump across unsupported releases
- Hosting model, endpoint routing, nullable reference types, and auth packages changed
- Older SPA, React build chains, and Node/npm assumptions often require refresh
- Deprecated APIs in EF Core 2.1, auth, and configuration need targeted rewrites

## 3. Which reference use-cases demonstrate each path

| Path | Best example in repo | Why it matters |
|---|---|---|
| Legacy script to modern web app | 01-ASPClassicApp | Pure rewrite pattern, session and ADO concerns |
| Earliest WebForms to modern .NET | 02-NetFramework30-ASPNET-WEB | WebForms + Windows Auth modernization |
| WCF contract modernization | 03-WCFNet35 | SOAP to REST, config to code, API hosting |
| Early ASP.NET Core modernization | 04-ContosoUniversityDiPS | Multi-project, Identity/JWT, React SPA |
| Completed WebForms modernization | 05-BookShop | Reference implementation with App Service + managed SQL |
| Mature MVC 5 / EF6 modernization | 07-PartsUnlimited-aspnet45 | MVC, EF6, Identity, deployment automation |

## 4. Command recipes by source version

Every recipe starts with discovery. `/assess-any-application` is what produces the Capability Matrix the phases depend on — `/quick-assessment` is a triage shortcut, not a substitute.

### .NET Framework 3.0 / 3.5 WebForms
1. `/assess-any-application`
2. *Steer:* `Inventory .aspx pages, code-behind, ViewState, server controls, Windows Authentication, and config risks. Do not assume a target framework version — surface the options.`
3. `/phase1-plan` → answer the target-framework decision
4. `/phase2-migrate-code`
5. `/security-hardening`

### .NET Framework 3.5 WCF
1. `/assess-any-application`
2. *Steer:* `Map every ServiceContract and OperationContract to REST endpoints and flag client compatibility gaps.`
3. `/phase1-plan` → answer the target-framework and hosting decisions
4. `/phase2-migrate-code`
5. `/phase3-generate-infra`

### .NET Framework 4.5.x MVC / EF6
1. `/assess-any-application`
2. *Steer:* `Identify EF6, OWIN, and deployment-script blockers. Score whether a 4.8 stabilization hop is worth it.`
3. `/phase1-plan`
4. `/database-migration`
5. `/phase2-migrate-code`

### .NET Core 2.1 / 3.1
1. `/assess-any-application`
2. *Steer:* `Assess this multi-project solution for in-place modernization while preserving API, Web, SPA, Data, and test boundaries.`
3. `/phase1-plan`
4. `/phase2-migrate-code`
5. `/phase5-setup-cicd`

## 5. Tooling reference

The tool recommends these; it does not replace them. Binary and dependency scanning of compiled artifacts is explicitly out of scope.

| Tool | Best use | Notes |
|---|---|---|
| .NET Upgrade Assistant | Project analysis, SDK-style conversion, dependency guidance | Strongest for libraries and newer framework apps; still requires manual work for `System.Web` apps |
| try-convert | Convert old `.csproj` to SDK-style | Useful for libraries and some non-web projects; not enough by itself for WebForms/WCF/MVC |
| .NET API analyzers | Inventory unsupported APIs and packages | Run before `/phase1-plan`; use findings to scope rewrite vs incremental |
| `dotnet` CLI | Build, test, restore, package validation | Core loop during Phase 2-5 |
| `az` + `azd` | Azure validation and deployment | Use once the target architecture decision is recorded |
| Bicep / Terraform | IaC generation | IaC tool is itself a recorded decision — see `decision-catalog.md` |
| Azure DMS / DMA | Database assessment and data movement | Orchestrated by `/database-migration`, not reimplemented |

## 6. Decision tree: incremental upgrade or rewrite?

```text
Does the app depend on System.Web, WebForms, WCF server hosting, or ASP Classic?
├─ Yes -> Rewrite the web/service host onto the chosen LTS.
│        Reuse isolated business logic only after validation.
└─ No -> Continue.

Is the app already on ASP.NET Core or mostly class libraries?
├─ Yes -> Prefer incremental modernization with Upgrade Assistant + try-convert.
└─ No -> Continue.

Are auth, EF6, or deployment scripts tightly coupled to runtime behavior?
├─ Yes -> Consider a stabilization hop to .NET Framework 4.8 before the LTS move.
└─ No -> Continue.

Is external contract compatibility mandatory (SOAP, binary clients, legacy auth)?
├─ Yes -> Use a strangler pattern, compatibility bridge, or phased cutover.
└─ No -> Prefer a direct landing on the chosen LTS.
```

This tree narrows the **shape** of the work. It does not pick the version. The full strategy call — rehost, replatform, refactor, rearchitect, rebuild, or retire — comes from `.github/skills/migration-decisions/references/migration-strategy-decision-tree.md`.

## 7. Starting posture per reference use-case

These are **starting hypotheses for the reference apps in this repo**, not recommendations for your application and not defaults the agent may apply on its own.

| Use-case | Starting hypothesis |
|---|---|
| 01 | Rewrite directly — there is no in-place path |
| 02 | Rewrite directly; do not chase a WebForms-preserving path |
| 03 | Rewrite contracts to REST unless a hard SOAP requirement exists |
| 04 | Incremental modernization from ASP.NET Core 2.1 |
| 05 | Study as the completed reference pattern |
| 07 | Assess first; if EF6/OWIN/package debt is severe, stabilize on 4.8 in a branch, then modernize |

Each one still has to survive `/phase1-plan` and the decision gate before any code changes.

## 8. Fast reminder

If the source app still depends on `System.Web`, ViewState, WebForms, WCF config hosting, or ASP Classic scripts, treat the move as a **platform redesign**, not a package upgrade — and treat the destination version as an open question until the user answers it.

## See also

- [Skills map](./skills-map.md)
- [Skill catalog](../architecture/SKILL-CATALOG.md)
- [Handoff protocol](./handoff-protocol.md)
