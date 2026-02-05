---
name: dotnet-modernization
description: |
  .NET Framework to .NET 8+ modernization patterns.
  **Use when:** User has a .NET Framework 4.x application and needs to upgrade to .NET 8 LTS.
  **Triggers on:** .csproj files with TargetFrameworkVersion, web.config files, System.Web references, Entity Framework 6.
  **Covers:** Project file transformation, web.config to appsettings.json, EF6 to EF Core, Windows/Forms auth to Entra ID.
---

# .NET Modernization Skill

Use this skill when modernizing .NET Framework applications to .NET 8+ for Azure compatibility.

## When to Use This Skill

- Upgrading .NET Framework 4.x to .NET 8+
- Converting web.config/app.config to appsettings.json
- Migrating Entity Framework 6 to EF Core
- Modernizing Windows/Forms authentication to Entra ID
- Replacing System.Web dependencies
- Updating NuGet packages for .NET 8+ compatibility

## Framework Version Mapping

| Legacy Version | Target Version | Notes |
|----------------|----------------|-------|
| .NET Framework 4.5-4.8 | .NET 8 LTS | Recommended for production |
| .NET Core 2.1/3.1 | .NET 8 LTS | Straightforward upgrade |
| .NET 5/6/7 | .NET 8 LTS | Minor breaking changes |

## Project File Transformation

### Legacy .csproj (SDK-style conversion)

```xml
<!-- Legacy format -->
<Project ToolsVersion="15.0">
  <PropertyGroup>
    <TargetFrameworkVersion>v4.8</TargetFrameworkVersion>
  </PropertyGroup>
  <ItemGroup>
    <Reference Include="System.Web" />
  </ItemGroup>
</Project>

<!-- Modern SDK-style -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

## Configuration Transformation

### web.config → appsettings.json

| web.config Element | appsettings.json Equivalent |
|--------------------|----------------------------|
| `<connectionStrings>` | `"ConnectionStrings": { }` |
| `<appSettings>` | `"AppSettings": { }` or custom section |
| `<system.web>` | Middleware configuration in Program.cs |
| `<system.webServer>` | Kestrel/IIS configuration |
| `<customErrors>` | Exception handling middleware |

See [appsettings.json template](./templates/appsettings.json) for a complete example.

## Authentication Migration

### Windows Authentication → Entra ID

```csharp
// Legacy Windows Auth
[Authorize]
public class SecureController : Controller
{
    var user = User.Identity.Name; // DOMAIN\username
}

// Modern Entra ID
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));

[Authorize]
public class SecureController : ControllerBase
{
    var user = User.FindFirst(ClaimTypes.Name)?.Value;
}
```

### Forms Authentication → ASP.NET Core Identity

```csharp
// Legacy Forms Auth in web.config
// <authentication mode="Forms">
//   <forms loginUrl="~/Account/Login" />
// </authentication>

// Modern ASP.NET Core Identity
builder.Services.AddIdentity<ApplicationUser, IdentityRole>()
    .AddEntityFrameworkStores<ApplicationDbContext>()
    .AddDefaultTokenProviders();

builder.Services.ConfigureApplicationCookie(options =>
{
    options.LoginPath = "/Account/Login";
});
```

## Entity Framework Migration

### EF6 → EF Core

| EF6 Pattern | EF Core Equivalent |
|-------------|-------------------|
| `DbContext` with `DbSet<T>` | Same pattern, different namespace |
| `Database.SetInitializer` | `DbContext.Database.EnsureCreated()` or migrations |
| `DbConfiguration` | `OnConfiguring` or `AddDbContext` |
| `ObjectContext` | Not supported - use `DbContext` |
| `EntityObject` | POCO entities only |
| `Code First Migrations` | EF Core Migrations (similar syntax) |

```csharp
// EF6
public class LegacyContext : DbContext
{
    public LegacyContext() : base("DefaultConnection") { }
    public DbSet<Product> Products { get; set; }
}

// EF Core
public class ModernContext : DbContext
{
    public ModernContext(DbContextOptions<ModernContext> options) 
        : base(options) { }
    public DbSet<Product> Products { get; set; }
}

// Registration in Program.cs
builder.Services.AddDbContext<ModernContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
```

## Package Mapping

| Legacy Package | Modern Replacement |
|----------------|-------------------|
| `System.Web` | `Microsoft.AspNetCore.*` |
| `System.Web.Mvc` | `Microsoft.AspNetCore.Mvc` |
| `EntityFramework` | `Microsoft.EntityFrameworkCore` |
| `Microsoft.Owin` | Built-in middleware |
| `Newtonsoft.Json` | `System.Text.Json` (or keep Newtonsoft) |
| `log4net` / `NLog` | `Microsoft.Extensions.Logging` + provider |
| `Unity` / `Ninject` | Built-in DI container |

## Common Breaking Changes

1. **HttpContext.Current** - Not available; inject `IHttpContextAccessor`
2. **ConfigurationManager** - Use `IConfiguration` injection
3. **Server.MapPath** - Use `IWebHostEnvironment.ContentRootPath`
4. **Session** - Configure session middleware explicitly
5. **Global.asax** - Move to Program.cs and middleware
6. **Bundling** - Use npm/webpack or LibMan

## Template Files

- [Program.cs](./templates/Program.cs) - Modern .NET 8 entry point
- [appsettings.json](./templates/appsettings.json) - Configuration template
- [Dockerfile](./templates/Dockerfile) - Container template for .NET 8

## Best Practices

1. **Use SDK-style projects** - Simpler, cleaner project files
2. **Enable nullable reference types** - Better null safety
3. **Use IConfiguration** - Never use ConfigurationManager
4. **Inject dependencies** - Use built-in DI container
5. **Use async/await** - For all I/O operations
6. **Configure middleware order** - Order matters in the pipeline
7. **Use ILogger** - Consistent logging abstraction
