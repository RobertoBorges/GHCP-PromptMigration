# Configuration Transformation

Use this skill when moving legacy .NET configuration from `web.config` or `app.config` to `appsettings.json`, environment variables, and Azure-hosted secret/config providers.

## When to use

Apply this skill when the source contains:

- `appSettings`
- `connectionStrings`
- `system.web`, `system.serviceModel`, or custom XML config sections
- transform files such as `Web.Release.config`
- direct use of `ConfigurationManager`

## Target state

Default to this configuration stack:

1. `appsettings.json`
2. `appsettings.{Environment}.json`
3. environment variables
4. Azure Key Vault for secrets
5. optional Azure App Configuration for shared dynamic settings

## Migration workflow

1. Inventory all settings and classify them as config, secret, runtime, or legacy-only.
2. Move non-secret structured settings into `appsettings.json`.
3. Move secrets to Key Vault or deployment-time secret stores.
4. Replace `ConfigurationManager` calls with `IConfiguration` or `IOptions<T>`.
5. Replace XML transforms with environment-specific JSON files and environment variables.

## Mapping guide

| Legacy source | Modern target |
|---|---|
| `<appSettings>` | `appsettings.json` section or environment variable |
| `<connectionStrings>` | `ConnectionStrings` section + secret injection |
| `Web.Release.config` transforms | `appsettings.Production.json` + Azure settings |
| `ConfigurationManager.AppSettings["X"]` | `configuration["Section:Key"]` or `IOptions<T>` |
| `system.web/sessionState` | ASP.NET Core session middleware or distributed cache settings |
| `system.serviceModel` | Replace with REST/API configuration and typed options |

## Example conversion

### Legacy `web.config`

```xml
<configuration>
  <appSettings>
    <add key="CatalogBaseUrl" value="https://legacy.contoso.local" />
  </appSettings>
  <connectionStrings>
    <add name="DefaultConnection" connectionString="Server=.;Database=Store;Integrated Security=True" />
  </connectionStrings>
</configuration>
```

### Modern `appsettings.json`

```json
{
  "Catalog": {
    "BaseUrl": "https://api.contoso.com"
  },
  "ConnectionStrings": {
    "DefaultConnection": ""
  }
}
```

### Strongly typed options

```csharp
public sealed class CatalogOptions
{
    public const string SectionName = "Catalog";
    public string BaseUrl { get; init; } = string.Empty;
}
```

```csharp
builder.Services
    .AddOptions<CatalogOptions>()
    .Bind(builder.Configuration.GetSection(CatalogOptions.SectionName))
    .ValidateDataAnnotations();
```

### Reading configuration in code

```csharp
public sealed class CatalogClient(HttpClient httpClient, IOptions<CatalogOptions> options)
{
    public Task<HttpResponseMessage> GetAsync(CancellationToken cancellationToken) =>
        httpClient.GetAsync(options.Value.BaseUrl, cancellationToken);
}
```

## Environment variable conventions

Use double underscore separators for nested JSON:

```text
ConnectionStrings__DefaultConnection
Catalog__BaseUrl
AzureAd__TenantId
```

## Azure guidance

- Secrets do not belong in `appsettings.json` committed to source control.
- Prefer managed identity + Key Vault for production secrets.
- Prefer deployment-time app settings for host-specific values like URLs and connection strings.
- For App Service and Container Apps, keep the same logical setting names to reduce code branching.

## Validation checklist

Validate that:

- No runtime-critical setting was lost during conversion.
- The application starts with local development settings.
- Production secrets can be injected without code changes.
- Configuration values are bound through options or `IConfiguration`, not legacy static calls.

## Output expectations for the migration prompt

- Produce a settings inventory table.
- Show the exact JSON and options classes created.
- Identify secrets that must move to Key Vault or pipeline secret stores.
- Document any legacy configuration sections that require redesign instead of direct translation.
