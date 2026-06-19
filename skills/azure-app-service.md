# Azure App Service

Use this skill when the target workload is a web app or API that benefits from low-operations PaaS hosting on Azure App Service.

## Best fit

App Service is usually the default choice when the workload is:

- A monolithic web application or REST API
- A .NET or Java application that does not require Kubernetes-level control
- Best served by deployment slots, built-in TLS, easy diagnostics, and rapid PaaS deployment

Prefer Container Apps when the workload is fully container-centric or event-driven. Prefer AKS only when Kubernetes control is a hard requirement.

## Baseline architecture

The default App Service deployment pattern should include:

- Resource group scoped deployment
- App Service Plan sized to expected load
- Web App or API App
- Managed identity enabled
- Application Insights + Log Analytics
- Key Vault for secrets
- Deployment slot for staging when downtime matters
- VNet integration or private endpoints when private dependencies require it

## Application requirements

- Run statelessly; store session state outside the process when scale-out is needed.
- Listen on the platform-assigned port for Linux containers.
- Expose a health endpoint such as `/health`.
- Write logs to stdout/stderr or the standard logging pipeline.
- Read configuration from environment variables / app settings.

## `azure.yaml` pattern

```yaml
name: contoso-modernization
services:
  web:
    project: src/Contoso.Web
    language: dotnet
    host: appservice
```

## App Service deployment settings

Recommended app settings and platform settings:

- `ASPNETCORE_ENVIRONMENT` or `SPRING_PROFILES_ACTIVE`
- connection strings and service endpoints injected as app settings
- health check path configured in the resource
- Always On enabled for production workloads
- staging slot for zero-downtime swaps when supported by the SKU

## Bicep resource shape

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
      healthCheckPath: '/health'
      alwaysOn: true
      minTlsVersion: '1.2'
    }
  }
}
```

## Operational guidance

- Use deployment slots for blue/green style swaps.
- Use autoscale based on CPU, memory, or HTTP queue length when the plan supports it.
- Keep secrets out of app settings when the value should come from Key Vault references or managed identity flows.
- Add custom domains and certificates after baseline deployment is stable.

## Security defaults

- Enable HTTPS only.
- Disable public SCM access if organizational policy requires it.
- Use managed identity for Key Vault, database, and storage access where supported.
- Apply least-privilege RBAC and avoid embedding credentials in configuration.

## Validation checklist

Validate that:

- The application starts in App Service without machine-specific assumptions.
- Health checks pass.
- Logs and traces reach Application Insights.
- Auth redirects or bearer token validation work behind the App Service hostname.
- Slot swap, scale-out, and restart behavior are acceptable.

## Output expectations for the infrastructure prompt

- Generate App Service plan, site, identity, monitoring, and secret integration resources.
- Recommend staging slots when the workload is customer-facing.
- Document SKU rationale and any networking choices.
- Note when App Service is a poor fit and why another host should be used instead.
