# .NET Framework to .NET 8 Migration

Use this skill when a legacy ASP.NET, MVC, Web API, service, or class library built on .NET Framework must move to .NET 8 for Azure.

## When to Use

Apply this skill when the source contains one or more of the following:

- `<TargetFrameworkVersion>` values such as `v3.5`, `v4.0`, `v4.6.2`, or `v4.8`
- `System.Web`, `Global.asax`, `HttpContext.Current`, `HttpModules`, or `HttpHandlers`
- `packages.config`, `ConfigurationManager`, `BundleConfig`, or `RouteConfig`
- OWIN startup classes, ASP.NET MVC 5, Web API 2, or IIS-only assumptions

Combine with:

- `#file:.github/skills/wcf-to-rest-api.md` for WCF services
- `#file:.github/skills/webforms-to-razor.md` for Web Forms UI
- `#file:.github/skills/config-transformation.md` for config modernization
- `#file:.github/skills/ef-migration.md` for data access modernization

## Target Architecture

Default to these targets unless the assessment report says otherwise:

- SDK-style projects
- `net8.0` or `net8.0-windows` only when Windows-specific APIs are unavoidable
- ASP.NET Core hosting model with `Program.cs`
- Built-in dependency injection, logging, health checks, and configuration providers
- `appsettings.json` + environment variables + Key Vault/App Configuration
- Controllers/Razor Pages/minimal APIs instead of `System.Web` pipeline primitives

## Migration Workflow

1. Inventory projects, framework versions, NuGet packages, IIS assumptions, and Windows-only APIs.
2. Convert each `.csproj` to SDK style and move from `packages.config` to `PackageReference`.
3. Replace `System.Web` and `HttpApplication` concepts with ASP.NET Core middleware and endpoint routing.
4. Move app startup logic into `Program.cs`.
5. Replace `ConfigurationManager` and XML transforms with modern configuration providers.
6. Add Azure-ready health checks, structured logging, and identity integration.
7. Build and test after each project conversion.

## System.Web Replacement Map

| Legacy API / Pattern | .NET 8 Replacement |
|---|---|
| `System.Web.HttpContext.Current` | Controller `HttpContext`, `IHttpContextAccessor`, or endpoint context |
| `HttpApplication` | ASP.NET Core middleware pipeline |
| `HttpModules` | Custom middleware |
| `HttpHandlers` | Minimal APIs, controllers, or endpoint handlers |
| `Server.MapPath()` | `IWebHostEnvironment.ContentRootPath` / `WebRootPath` |
| `Request.Params` | Model binding, `Request.Query`, `Request.Form`, `Request.RouteValues` |
| `Session` | `AddSession()` with distributed cache only if required |
| `FormsAuthentication` | Cookie auth or Entra ID via `Microsoft.Identity.Web` |
| `Url.RouteUrl()` / route tables | Endpoint routing via `MapControllerRoute()` / attribute routing |
| `BundleConfig` | Static files, bundler pipeline (Vite/Webpack/esbuild), or build-time bundling |
| `Global.asax` events | Middleware, hosted services, startup code in `Program.cs` |

## Project File Conversion

### Before - .NET Framework `.csproj`

```xml
<Project ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>
    <OutputType>Library</OutputType>
    <RootNamespace>Contoso.Web</RootNamespace>
  </PropertyGroup>
  <ItemGroup>
    <Reference Include="System.Web" />
    <Reference Include="System.Configuration" />
  </ItemGroup>
  <Import Project="$(MSBuildToolsPath)\Microsoft.CSharp.targets" />
</Project>
```

### After - SDK-style `.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.ApplicationInsights.AspNetCore" Version="2.*" />
    <PackageReference Include="Microsoft.Identity.Web" Version="3.*" />
  </ItemGroup>
</Project>
```

## Startup.cs / Program.cs Patterns

### Before - OWIN or `Startup.cs`

```csharp
public class Startup
{
    public void Configuration(IAppBuilder app)
    {
        app.UseCookieAuthentication(new CookieAuthenticationOptions
        {
            AuthenticationType = "Cookies"
        });
    }
}
```

### After - `.NET 8 Program.cs`

```csharp
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.HttpOverrides;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();
builder.Services.AddHttpContextAccessor();
builder.Services.AddHealthChecks();
builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddCookie();
builder.Services.AddAuthorization();

var app = builder.Build();

app.UseForwardedHeaders(new ForwardedHeadersOptions
{
    ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto
});

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();

app.MapHealthChecks("/health");
app.MapDefaultControllerRoute();

app.Run();
```

## Middleware Pipeline Conversion

### Before - `Global.asax`

```csharp
public class MvcApplication : HttpApplication
{
    protected void Application_Start()
    {
        AreaRegistration.RegisterAllAreas();
        FilterConfig.RegisterGlobalFilters(GlobalFilters.Filters);
        RouteConfig.RegisterRoutes(RouteTable.Routes);
        BundleConfig.RegisterBundles(BundleTable.Bundles);
    }

    protected void Application_BeginRequest()
    {
        Response.Headers.Add("X-App", "Legacy");
    }
}
```

### After - middleware and endpoint registration

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllersWithViews();

var app = builder.Build();

app.Use(async (context, next) =>
{
    context.Response.Headers.Append("X-App", "Modernized");
    await next();
});

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
```

## HttpContext Migration

### Before

```csharp
public static class TenantResolver
{
    public static string GetTenant()
    {
        return HttpContext.Current?.Request.Headers["X-Tenant"] ?? "default";
    }
}
```

### After

```csharp
public sealed class TenantResolver(IHttpContextAccessor accessor)
{
    public string GetTenant()
    {
        return accessor.HttpContext?.Request.Headers["X-Tenant"].ToString() ?? "default";
    }
}
```

## Global.asax Event Migration

| `Global.asax` Event | .NET 8 Target |
|---|---|
| `Application_Start` | Service registration + startup code in `Program.cs` |
| `Application_BeginRequest` | Early middleware |
| `Application_Error` | `UseExceptionHandler`, exception middleware, `IExceptionHandler` |
| `Session_Start` | Explicit session middleware or remove stateful dependency |
| `Application_End` | Hosted service shutdown hooks / disposal |

## Bundling and Minification Changes

Legacy bundling APIs do not exist in ASP.NET Core.

### Before - `BundleConfig.cs`

```csharp
bundles.Add(new ScriptBundle("~/bundles/app")
    .Include("~/Scripts/jquery-{version}.js")
    .Include("~/Scripts/app.js"));
```

### After - static assets or frontend build pipeline

```html
<link rel="stylesheet" href="~/dist/site.css" asp-append-version="true" />
<script src="~/dist/app.js" asp-append-version="true"></script>
```

Use one of these modernization patterns:

- Preserve static assets under `wwwroot/`
- Introduce Vite/Webpack/esbuild for non-trivial assets
- Use `asp-append-version="true"` for cache busting

## Azure-Ready Defaults

Add these during migration, not as a cleanup pass:

- `AddApplicationInsightsTelemetry()`
- `MapHealthChecks("/health")`
- `UseForwardedHeaders()` when behind App Service or reverse proxies
- Entra ID for user auth or API auth where applicable
- Key Vault/App Configuration for secrets and shared settings

## Validation Commands

```bash
dotnet restore
dotnet build
dotnet test
dotnet list package --outdated
```

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- Produce before/after mappings for every unsupported framework pattern
- Generate SDK-style project files and modern `Program.cs` wiring
- Call out Windows-only blockers explicitly
- Recommend follow-on skills for WCF, Web Forms, config, and EF migration
