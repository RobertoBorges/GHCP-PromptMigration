# Skill: Stack Adapter — .NET (Framework + Core + 5+)

> Stack adapter for any .NET application: Classic ASP (yes, treated as a .NET-adjacent legacy stack), ASP.NET WebForms, ASP.NET MVC, ASP.NET Web API, WCF services, ASP.NET Core (any version), Console + Worker Services, WPF / WinForms (rare for migration), Blazor.

> This adapter consolidates the content from the legacy `Assess-DotNet-Upgrade`, `Assess-WCF-Migration`, `Assess-WebForms-Migration`, and `Assess-ClassicASP-Migration` prompts.

## When to Use

- `stack.primary_stack: dotnet` in the Capability Matrix
- File evidence: `*.sln`, `*.csproj`, `*.vbproj`, `*.cshtml`, `*.razor`, `*.aspx`, `*.svc`, `web.config`, `app.config`, `global.asax`

## Sub-Stack Detection

After confirming .NET is the primary stack, identify the **sub-stack** that drives Phase 2 effort:

| Sub-stack | Detection signal | Typical migration target |
|-----------|------------------|--------------------------|
| **.NET 8 / 9 / 10** (modern) | `TargetFramework=net8.0` (or later) in csproj | Stay current; minor upgrade or in-place LTS bump |
| **.NET Core 2.x / 3.x** | `netcoreapp2.1` / `netcoreapp3.1` | Upgrade to .NET 10 LTS |
| **.NET 5 / 6 / 7** (out of support) | `net5.0` / `net6.0` / `net7.0` | Upgrade to .NET 10 LTS |
| **.NET Framework 4.x** | `<TargetFrameworkVersion>v4.x</TargetFrameworkVersion>` | Port to .NET 10 (preferred); or rehost on Windows containers |
| **.NET Framework 2.x / 3.x** | `v2.0` / `v3.0` / `v3.5` | Heavy port to .NET 10; or rehost on Windows containers |
| **ASP.NET WebForms** | `*.aspx` + `*.ascx` + `<%@ Page %>` + Code-behind `.cs` | Rewrite to ASP.NET Core MVC or Razor Pages (no in-place upgrade) |
| **ASP.NET MVC 5 (System.Web)** | `Controllers/`, `Views/`, `RouteConfig.cs`, `Global.asax`, `System.Web.Mvc` | Port to ASP.NET Core MVC |
| **ASP.NET Web API 2 (System.Web)** | `ApiControllers`, `System.Web.Http` | Port to ASP.NET Core Web API |
| **ASP.NET Core MVC** | `Microsoft.AspNetCore.Mvc`, `Program.cs` (`WebApplication.CreateBuilder`) | Modernize within Core |
| **WCF** | `*.svc`, `[ServiceContract]`, `[OperationContract]`, `system.serviceModel` in config | Rewrite to ASP.NET Core REST API (preferred) or gRPC; or use CoreWCF if SOAP must stay |
| **Classic ASP** | `*.asp`, `global.asa`, `<%@ Language="VBScript" %>` | Full rewrite to ASP.NET Core (page-by-page strangler or feature-slice) |
| **Worker Service / Console** | `IHostedService`, `BackgroundService`, no web entry | Container Apps Jobs / Functions / Container Apps |
| **WPF / WinForms** | `*.xaml`, `App.xaml`, `Application.Run` | Rarely migrated to Azure; may go to Azure Virtual Desktop |
| **Blazor Server** | `_Imports.razor`, `App.razor`, `Microsoft.AspNetCore.Components.Server` | Stay current; deploy as web app |
| **Blazor WebAssembly** | `wwwroot/_framework/`, `Microsoft.AspNetCore.Components.WebAssembly` | Static Web Apps |

## Probes

### Csproj inspection

For each `*.csproj`:

1. `TargetFramework` / `TargetFrameworkVersion` / `TargetFrameworks`
2. `<OutputType>` → `Exe` / `WinExe` / `Library`
3. `<UseWPF>`, `<UseWindowsForms>` → desktop flag
4. `PackageReference` list → top NuGet dependencies
5. `Reference` list (Framework projects) → GAC + system references
6. `ProjectReference` list → internal project graph

### Configuration inspection

- `web.config` / `app.config`:
  - `<system.web>` → ASP.NET Framework only (vs ASP.NET Core)
  - `<system.serviceModel>` → WCF host / client
  - `<connectionStrings>` → DB engine + server (often hardcoded)
  - `<appSettings>` → secrets / endpoints
  - `<authentication mode="Forms" | "Windows" | "None">` → auth modernization scope
  - `<httpModules>`, `<modules>` → custom IIS modules (must replace)
  - `<bindings>` (WCF) → `wsHttp` / `basicHttp` / `netTcp` / `mex` → REST mapping

- `appsettings.json` (Core):
  - Connection strings, Entra ID config, logging config

### Code inspection (sample)

- Grep for `Server.CreateObject` (Classic ASP COM dependency)
- Grep for `On Error Resume Next` (VBScript pattern)
- Grep for `[OperationContract]`, `[DataContract]`, `[ServiceContract]` (WCF)
- Grep for `Session[` and `Application[` (state usage)
- Grep for `System.Web.HttpContext.Current` (System.Web-coupled code)
- Grep for `Newtonsoft.Json` (consider System.Text.Json in Core)
- Grep for `Microsoft.AspNet.Identity` / `Microsoft.Owin` → identity migration to ASP.NET Core Identity + Entra ID
- Grep for `EntityFramework` v6 → migrate to EF Core
- Grep for `System.Configuration.ConfigurationManager` → migrate to `IConfiguration`

### Data access

- ADO.NET (`SqlConnection`, `OleDbConnection`, `OdbcConnection`)
- Entity Framework 6 (System.Data.Entity)
- Entity Framework Core (Microsoft.EntityFrameworkCore)
- Dapper
- NHibernate
- LINQ to SQL

Captures Phase 2 + Database Migration scope.

### Tests

- xUnit / NUnit / MSTest → preserved
- Web tests (Selenium / Playwright .NET) → preserved

## Phase 2 Effort Mapping

| Sub-stack | Phase 2 effort | Notes |
|-----------|----------------|-------|
| .NET 8+ → .NET 10 | S (Small) | Trivial bump |
| .NET Core 2.x/3.x → .NET 10 | M | Some breaking changes |
| .NET 5/6/7 → .NET 10 | M | Out-of-support runtime upgrades |
| .NET Framework 4.x → .NET 10 (port) | L | API removals; `System.Web` is the biggest blocker |
| .NET Framework 2.x/3.x → .NET 10 | XL | Often rewrite scope |
| ASP.NET WebForms → ASP.NET Core MVC | XL | No in-place; full rewrite |
| WCF (SOAP) → REST API | L | Service contract redesign |
| Classic ASP → ASP.NET Core | XL | Full rewrite |
| ASP.NET MVC 5 → ASP.NET Core MVC | L | Pattern preserved; APIs differ |
| EF6 → EF Core | M | Migration path documented in `ef-migration` skill |

## Configuration Transformation (web.config → appsettings.json)

Use the `config-transformation` skill for the mechanical mapping. Highlights:

- `<appSettings>` → `appsettings.json` flat keys
- `<connectionStrings>` → `ConnectionStrings` section (then move to Key Vault references)
- `<system.web><authentication>` → ASP.NET Core authentication middleware
- `<httpModules>` → middleware in `Program.cs`
- `<httpHandlers>` → endpoint routing
- `<customErrors>` → exception-handling middleware
- IIS-specific `<system.webServer>` → mostly removed (Container Apps / App Service handle routing)

## Identity Modernization

| Today | Target |
|-------|--------|
| Forms Authentication | ASP.NET Core Identity + Entra ID (OIDC) |
| Windows Authentication (intranet) | Entra ID + workload identity (or stay Windows if behind App Service VNet integration) |
| ASP.NET Identity (Membership/Roles) | ASP.NET Core Identity + Entra ID B2C (for customer) or Entra ID (for workforce) |
| WS-Federation / WCF FederatedSecurity | Entra ID OIDC + JWT |

## Target Azure Mapping

| Sub-stack | Primary Azure target | Secondary |
|-----------|----------------------|-----------|
| ASP.NET Core (any) | App Service Linux | Container Apps |
| ASP.NET Core (containerized) | Container Apps | AKS (if complex) |
| ASP.NET Framework (4.x) | App Service Windows | Container Apps with Windows containers |
| WCF rewritten to REST | App Service / Container Apps | APIM in front |
| Worker / Console | Container Apps Jobs | Functions (if event-triggered) |
| Blazor WebAssembly | Static Web Apps | App Service (when paired with hosted API) |

## Anti-Patterns

- Don't claim "lift-and-shift" for ASP.NET Framework to Linux App Service — Linux App Service does not host `System.Web`. Use App Service Windows or containerize.
- Don't auto-replace `Newtonsoft.Json` with `System.Text.Json` without checking custom converters — behavior differences in serialization can break wire formats.
- Don't migrate WCF "as-is" by hosting it on Windows. The right answer is REST (or gRPC for internal use). Use CoreWCF only when SOAP contracts must be preserved for external clients.
- Don't keep Forms Auth on Azure. Modernize to Entra ID.
- Don't skip the `Configuration.Bind` step when porting `ConfigurationManager`-based code — strongly typed config is the Core idiom.

## Output Checklist

- [ ] Sub-stack identified (one of the 14 above)
- [ ] All csproj target frameworks captured
- [ ] Top NuGet dependencies inventoried
- [ ] System.Web coupling identified
- [ ] WCF service contracts inventoried (if applicable)
- [ ] Identity model captured
- [ ] Data access pattern captured (ADO/EF6/EF Core/Dapper)
- [ ] Tests inventory captured
- [ ] Configuration mapping plan drafted (web.config → appsettings.json)
- [ ] Phase 2 effort label assigned (S/M/L/XL)
- [ ] Target Azure compute candidate noted
