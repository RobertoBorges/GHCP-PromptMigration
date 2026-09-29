# Configuration Transformation

Use this skill when modernizing legacy application configuration from any format (XML `web.config` / `app.config`, Java properties, `.env`, YAML, INI, Python `settings.py`, PHP `.htaccess` + `php.ini`, Ruby YAML, etc.) into cloud-friendly configuration providers.

## When to Use

Apply this skill when the source contains:

- `web.config`, `app.config`, `Web.Release.config`, or custom XML sections
- `connectionStrings`, `appSettings`, `ConfigurationManager`, or `NameValueCollection`
- Spring `application.properties` with environment-specific overrides that need modernization
- hard-coded connection strings, service URLs, or secrets

## Target Configuration Stack

Use this order of precedence unless the project needs a different override model:

1. `appsettings.json` or `application.yml`
2. environment-specific files such as `appsettings.Production.json`
3. environment variables
4. user secrets for local development
5. Azure Key Vault for secrets
6. optional Azure App Configuration for shared dynamic settings

## Migration Workflow

1. Inventory every setting and classify it as config, secret, environment-specific, or legacy-only.
2. Move structured non-secret settings into JSON/YAML files.
3. Move secrets to user secrets (dev) and Key Vault/App Configuration (shared/prod).
4. Replace direct `ConfigurationManager` or XML section parsing with options binding or typed config properties.
5. Replace transform files with environment-specific config files and environment variables.

## `web.config` to `appsettings.json`

### Before - `web.config`

```xml
<configuration>
  <appSettings>
    <add key="CatalogBaseUrl" value="https://legacy.contoso.local" />
    <add key="FeatureFlag:BetaCheckout" value="false" />
  </appSettings>
  <connectionStrings>
    <add name="DefaultConnection"
         connectionString="Server=.;Database=Store;Integrated Security=True"
         providerName="System.Data.SqlClient" />
  </connectionStrings>
</configuration>
```

### After - `appsettings.json`

```json
{
  "Catalog": {
    "BaseUrl": "https://api.contoso.com"
  },
  "FeatureFlags": {
    "BetaCheckout": false
  },
  "ConnectionStrings": {
    "DefaultConnection": ""
  }
}
```

## Connection String Modernization

- Keep connection string keys stable across environments.
- Remove embedded credentials where managed identity or Entra ID can be used.
- For Azure SQL, prefer `Authentication=Active Directory Default` where supported.

### Example - Azure SQL with managed identity

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=tcp:contoso-sql.database.windows.net,1433;Database=Store;Authentication=Active Directory Default;Encrypt=True;TrustServerCertificate=False;"
  }
}
```

## Custom Config Sections to Options Pattern

### Before - custom XML section access

```csharp
var section = (CatalogSection)ConfigurationManager.GetSection("catalog");
var timeout = section.TimeoutSeconds;
```

### After - strongly typed options

```csharp
public sealed class CatalogOptions
{
    public const string SectionName = "Catalog";
    public string BaseUrl { get; init; } = string.Empty;
    public int TimeoutSeconds { get; init; }
}
```

```csharp
builder.Services
    .AddOptions<CatalogOptions>()
    .Bind(builder.Configuration.GetSection(CatalogOptions.SectionName))
    .ValidateDataAnnotations();
```

```csharp
public sealed class CatalogClient(HttpClient httpClient, IOptions<CatalogOptions> options)
{
    public Task<HttpResponseMessage> GetAsync(CancellationToken cancellationToken) =>
        httpClient.GetAsync(options.Value.BaseUrl, cancellationToken);
}
```

## Environment-Specific Configuration

### Before - transform file

```xml
<!-- Web.Release.config -->
<appSettings>
  <add key="CatalogBaseUrl" value="https://prod.contoso.com" xdt:Transform="SetAttributes" xdt:Locator="Match(key)" />
</appSettings>
```

### After - environment-specific JSON

```json
{
  "Catalog": {
    "BaseUrl": "https://prod.contoso.com"
  }
}
```

Use environment variables for last-mile overrides:

```text
Catalog__BaseUrl
ConnectionStrings__DefaultConnection
AzureAd__TenantId
```

## User Secrets for Development

Use local secrets for dev-time only.

```bash
dotnet user-secrets init
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=(localdb)\\MSSQLLocalDB;Database=Store;Trusted_Connection=True;"
```

## Azure App Configuration Integration

Use App Configuration when multiple services must share non-secret feature flags or operational settings.

```csharp
builder.Configuration.AddAzureAppConfiguration(options =>
{
    options.Connect(new Uri(builder.Configuration["AppConfig:Endpoint"]!), new DefaultAzureCredential())
           .Select("Contoso:*")
           .TrimKeyPrefix("Contoso:");
});

builder.Services.AddAzureAppConfiguration();
```

## Java Configuration Modernization

### Before - `application.properties`

```properties
catalog.base-url=https://legacy.contoso.local
db.password=hardcoded
```

### After - `application.yml`

```yaml
catalog:
  base-url: ${CATALOG_BASE_URL:https://api.contoso.com}

spring:
  datasource:
    password: ${DB_PASSWORD:}
```

## Validation Checklist

- No secret remains committed to source control.
- Every runtime-critical setting has a modern source of truth.
- Local development works via user secrets or `.env`-style injection.
- Production settings can be provided without code changes.
- Legacy transform files are either retired or explicitly documented as transitional.

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- Produce a setting inventory table
- Show exact target JSON/YAML and option classes
- Identify which values belong in Key Vault, App Configuration, or environment variables
- Call out any XML sections that require redesign instead of direct translation
