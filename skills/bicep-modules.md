# Bicep Modules

Use this skill when generating Azure infrastructure with Bicep and Azure Verified Modules (AVM).

## Design goals

The generated Bicep should be:

- Modular
- Environment-aware
- Idempotent
- Safe to review through `what-if`
- Consistent with Azure naming, tagging, identity, and monitoring standards

## Recommended folder structure

```text
infra/
  main.bicep
  main.parameters.json
  modules/
    appService.bicep
    containerApps.bicep
    aks.bicep
    monitoring.bicep
    database.bicep
    identity.bicep
    keyvault.bicep
    networking.bicep
```

## Module rules

- One responsibility per module.
- Pass in values through parameters; return IDs, endpoints, and names through outputs.
- Keep resource names deterministic and environment-scoped.
- Centralize tags in `main.bicep` and pass them into modules.
- Avoid embedding secrets in parameters or outputs.

## Main file pattern

```bicep
targetScope = 'resourceGroup'

@description('Deployment environment name such as dev, test, or prod')
param environmentName string

@description('Primary Azure region')
param location string = resourceGroup().location

@description('Base application name used in resource naming')
param appName string

var tags = {
  environment: environmentName
  workload: appName
  managedBy: 'bicep'
}

module monitoring './modules/monitoring.bicep' = {
  name: 'monitoring-${environmentName}'
  params: {
    location: location
    appName: appName
    tags: tags
  }
}

module app './modules/appService.bicep' = {
  name: 'app-${environmentName}'
  params: {
    location: location
    appName: appName
    environmentName: environmentName
    tags: tags
    logAnalyticsWorkspaceId: monitoring.outputs.logAnalyticsWorkspaceId
    appInsightsConnectionString: monitoring.outputs.applicationInsightsConnectionString
  }
}

output appHostname string = app.outputs.hostname
```

## AVM guidance

Prefer AVM for common resources when it reduces boilerplate and the module version can be pinned explicitly.

Example pattern:

```bicep
module appServicePlan 'br/public:avm/res/web/serverfarm:<version>' = {
  name: 'plan-${environmentName}'
  params: {
    name: 'asp-${appName}-${environmentName}'
    location: location
    skuName: 'P1v3'
    tags: tags
  }
}
```

Use placeholders like `<version>` until the repo standardizes the exact tested AVM release.

## Parameter rules

Keep parameters focused on deploy-time choices:

- environment name
- location
- SKU or scale settings
- principal IDs for RBAC
- feature toggles such as private networking enablement

Do not parameterize every string in the template; keep modules opinionated.

## Security rules

- Use managed identity by default.
- Prefer Key Vault with RBAC only.
- Keep secrets out of parameter files.
- Emit only safe outputs.
- Use private endpoints and VNet integration when the assessment requires them.

## Validation commands

```bash
az bicep build --file infra/main.bicep
az deployment group validate --resource-group <rg> --template-file infra/main.bicep --parameters @infra/main.parameters.json
az deployment group what-if --resource-group <rg> --template-file infra/main.bicep --parameters @infra/main.parameters.json
```

## Output expectations for the infrastructure prompt

- Generate `infra/main.bicep` and supporting modules.
- Explain how modules compose and what each module owns.
- Keep host-specific resources separate from shared identity, monitoring, and networking concerns.
- Include outputs needed by deployment steps, but avoid exposing secrets.
