# Azure App Service Deployment Patterns

Use this skill when the target workload is a web app or API that benefits from Azure App Service PaaS hosting.

## When App Service Is the Right Fit

Prefer App Service when the workload is:

- a monolithic web app, MVC app, Razor app, or REST API
- primarily HTTP-based and does not require Kubernetes-level control
- best served by deployment slots, managed identity, custom domains, TLS, and rapid PaaS operations

## App Service Plan Sizing

Use these as starting points, then validate with load and cost data.

| SKU | Best For | Guidance |
|---|---|---|
| `B1/B2/B3` | dev/test, low-traffic internal apps | No deployment slots, limited scale, not for production-critical workloads |
| `S1/S2/S3` | steady production apps with moderate traffic | Good default for many line-of-business apps |
| `P1v3/P2v3/P3v3` | production apps needing slots, scale, VNet, better perf | Default production recommendation for customer-facing apps |
| `I1v2+` | isolated/private workloads | Use only when network isolation requirements justify cost |

## Baseline Architecture

A production App Service pattern typically includes:

- App Service Plan
- Web App or API App
- system-assigned managed identity
- Application Insights + Log Analytics
- staging slot for low-risk releases
- Key Vault or App Configuration for externalized secrets/config
- health checks and autoscale policy

## Deployment Slots

Use slots when downtime matters.

- `production` slot: live traffic
- `staging` slot: warm-up and smoke tests
- slot swap only after validation passes
- keep slot-specific settings marked appropriately

### Slot Swap Procedure

1. Deploy to `staging`
2. Run smoke tests and health checks
3. Verify config and identity bindings
4. Swap `staging` -> `production`
5. Keep previous bits in the former production slot for fast rollback

## Custom Domains and SSL

- Bind custom domains only after the app is stable on the default hostname.
- Use managed certificates where supported or Key Vault-backed certificates when required.
- Enforce HTTPS-only and minimum TLS 1.2 or later.
- Validate redirect URI and cookie domain impacts for Entra-integrated apps.

## Managed Identity Setup

Enable system-assigned managed identity by default.

### Bicep example

```bicep
resource app 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    httpsOnly: true
    serverFarmId: plan.id
  }
}
```

Grant downstream access separately via RBAC or data-plane permissions.

## App Settings and Connection Strings

Use App Service settings for environment-specific values and Key Vault references for secrets.

```text
ASPNETCORE_ENVIRONMENT=Production
ConnectionStrings__DefaultConnection=@Microsoft.KeyVault(SecretUri=https://contoso-kv.vault.azure.net/secrets/default-connection/...)
AzureAd__TenantId=<tenant-id>
```

Prefer consistent logical setting names across local, CI/CD, staging, and prod.

## Health Checks

Expose a lightweight endpoint such as `/health`.

- configure the platform `healthCheckPath`
- ensure the endpoint verifies critical dependencies only when appropriate
- avoid leaking secrets or internal topology in health responses

## Auto-Scaling Rules

Start with conservative autoscale and tune with telemetry.

Recommended triggers:

- CPU > 70% for 10 minutes -> scale out by 1
- HTTP queue length or request latency sustained above threshold -> scale out
- CPU < 35% for 20-30 minutes -> scale in by 1
- schedule-based scale-down for predictable non-production idle windows

## Bicep Pattern

```bicep
resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: 'asp-${appName}-${environmentName}'
  location: location
  sku: {
    name: 'P1v3'
    tier: 'PremiumV3'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource app 'Microsoft.Web/sites@2023-12-01' = {
  name: 'app-${appName}-${environmentName}'
  location: location
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOTNETCORE|8.0'
      alwaysOn: true
      healthCheckPath: '/health'
      minTlsVersion: '1.2'
    }
  }
}
```

## Operational Defaults

- enable Always On for production web workloads
- send logs and traces to Application Insights
- externalize session state if scale-out is required
- validate slot swap, restart, and scale behaviors before go-live

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- justify App Service plan sizing
- include slots, managed identity, health checks, and scaling guidance
- document custom domain and certificate prerequisites
- produce an App Service-ready IaC or deployment plan
