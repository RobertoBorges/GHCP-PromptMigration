# .NET Framework to .NET 8

Use this skill when modernizing a .NET Framework application to .NET 8 for Azure hosting.

## When to use

Apply this skill when the source solution contains one or more of the following:

- `<TargetFrameworkVersion>` such as `v3.5`, `v4.6.2`, or `v4.8`
- `packages.config`
- `System.Web`, `Global.asax`, `HttpContext.Current`, or `OWIN`
- ASP.NET MVC 5, Web API 2, Windows Services, console apps, or class libraries on .NET Framework
- Legacy configuration in `web.config` or `app.config`

If the application also contains WCF or Web Forms, combine this skill with `skills/wcf-to-rest-api.md` or `skills/webforms-to-razor.md`.

## Target state

Default to these modernization targets unless the assessment report says otherwise:

- SDK-style projects
- `net8.0` or `net8.0-windows` only when Windows-specific APIs are still required
- `PackageReference` instead of `packages.config`
- Generic Host / ASP.NET Core hosting model
- Centralized configuration through `appsettings.json`, environment variables, and Key Vault
- Built-in dependency injection, logging, health checks, and OpenAPI where applicable

## Migration workflow

1. Inventory solution types and external dependencies.
2. Convert each project file to SDK style.
3. Upgrade packages to versions compatible with .NET 8.
4. Replace `System.Web` hosting and pipeline concepts with ASP.NET Core equivalents.
5. Move configuration to the modern configuration stack.
6. Add Azure-ready observability, authentication, and health endpoints.
7. Build and test after each project conversion.

## Project file conversion pattern

### Legacy `.csproj` example

```xml
<Project ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup>
    <TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>
    <OutputType>Library</OutputType>
  </PropertyGroup>
  <ItemGroup>
    <Reference Include="System" />
    <Reference Include="System.Web" />
  </ItemGroup>
  <Import Project="$(MSBuildToolsPath)\Microsoft.CSharp.targets" />
</Project>
```

### Modern SDK-style target

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.ApplicationInsights.AspNetCore" Version="2.*" />
    <PackageReference Include="Microsoft.Identity.Web" Version="2.*" />
  </ItemGroup>
</Project>
```

## Hosting and startup migration

Replace `Global.asax`, `Startup.cs`, OWIN bootstrapping, and `HttpApplication` events with `Program.cs`.

```csharp
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.Identity.Web;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();
builder.Services.AddHealthChecks();
builder.Services.AddApplicationInsightsTelemetry();

builder.Services
    .AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"));

builder.Services.AddAuthorization();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();

app.MapHealthChecks("/health");
app.MapControllers();
app.MapDefaultControllerRoute();

app.Run();
```

## Common API replacements

| Legacy pattern | .NET 8 target pattern |
|---|---|
| `System.Web.HttpContext.Current` | Inject `IHttpContextAccessor` or use `HttpContext` in controllers/endpoints |
| `ConfigurationManager.AppSettings` | `IConfiguration` or strongly typed `IOptions<T>` |
| `packages.config` | `PackageReference` |
| `Global.asax` lifecycle events | Middleware pipeline and hosted services |
| `HttpModules` / `HttpHandlers` | Middleware and endpoint routing |
| `BinaryFormatter` | `System.Text.Json` or a supported serializer |
| `WebRequest` / `HttpWebRequest` | `HttpClient` via `IHttpClientFactory` |
| `log4net` / `System.Diagnostics` only | `ILogger<T>` plus Application Insights / OpenTelemetry |
| Machine-level IIS config assumptions | App-local config plus App Service settings |

## Library compatibility guidance

- Replace unsupported libraries first; do not try to force incompatible .NET Framework-only packages into .NET 8.
- Favor modern Microsoft or actively maintained packages.
- If a project is only a utility library, target `Microsoft.NET.Sdk` instead of the Web SDK.
- Use `net8.0-windows` only for code that truly requires Windows-only APIs such as registry, EventLog, or GDI+.

## Configuration and data access

- Move `connectionStrings` and `appSettings` into `appsettings.json`.
- Externalize secrets to Key Vault or deployment settings.
- Replace direct `SqlConnection` usage where practical with EF Core or repository abstractions.
- If EF6 or ADO.NET is significant, combine with `skills/ef-migration.md`.

## Azure-ready defaults

Add these during modernization rather than as a final cleanup step:

- `AddApplicationInsightsTelemetry()`
- `/health` endpoint for probes
- `UseForwardedHeaders()` when behind reverse proxies if needed
- Entra ID authentication for interactive apps or APIs
- Key Vault and managed identity for secrets and connections

## Commands and validation

Run these after each meaningful change:

```bash
dotnet restore
dotnet build
dotnet test
dotnet list package --outdated
```

Validate that:

- All converted projects build on the .NET 8 SDK.
- Unsupported APIs are either removed or replaced.
- Authentication, configuration, logging, and database access still work.
- Generated containers or deployment artifacts target supported runtime images.

## Output expectations for the migration prompt

When applying this skill, the prompt should:

- Describe each incompatible dependency and replacement.
- Produce SDK-style project files.
- Document framework-specific breaking changes.
- Call out remaining Windows-only blockers explicitly.
- Recommend the next composed skill when the app includes WCF, Web Forms, or EF6.
