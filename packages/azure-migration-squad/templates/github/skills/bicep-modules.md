# Bicep Modules and Azure Verified Modules

Use this skill when generating Azure infrastructure with modular Bicep and Azure Verified Modules (AVM).

## Design Goals

The generated Bicep should be:

- modular
- environment-aware
- idempotent
- easy to validate with `what-if`
- consistent in naming, tagging, identity, and monitoring

## Module Composition Pattern

Recommended structure:

```text
infra/
  main.bicep
  main.parameters.json
  modules/
    appService.bicep
    containerApps.bicep
    monitoring.bicep
    database.bicep
    identity.bicep
    networking.bicep
    keyvault.bicep
```

Rules:

- one responsibility per module
- pass inputs through parameters and return IDs/endpoints as outputs
- keep resource naming deterministic
- centralize tags and naming tokens in `main.bicep`
- never output secrets

## AVM Usage

Prefer Azure Verified Modules when they reduce boilerplate and the version can be pinned.

```bicep
module appServicePlan 'br/public:avm/res/web/serverfarm:<version>' = {
  name: 'plan-${environmentName}'
  params: {
    name: 'asp-${nameToken}-${environmentName}'
    location: location
    skuName: 'P1v3'
    tags: tags
  }
}
```

Replace `<version>` with the repo-approved tested version.

## Main Composition Example

```bicep
targetScope = 'resourceGroup'

param environmentName string
param location string = resourceGroup().location
param workloadName string

var nameToken = toLower(replace('${workloadName}-${environmentName}', ' ', ''))
var tags = {
  environment: environmentName
  workload: workloadName
  managedBy: 'bicep'
}

module monitoring './modules/monitoring.bicep' = {
  name: 'monitoring-${environmentName}'
  params: {
    location: location
    nameToken: nameToken
    tags: tags
  }
}

module app './modules/appService.bicep' = {
  name: 'app-${environmentName}'
  params: {
    location: location
    nameToken: nameToken
    tags: tags
    appInsightsConnectionString: monitoring.outputs.applicationInsightsConnectionString
  }
}
```

## Parameter Files

Keep parameter files focused on deploy-time choices:

- `environmentName`
- `location`
- SKUs and scale settings
- principal IDs for RBAC
- feature toggles such as private networking

Avoid parameterizing every string; keep modules opinionated.

## Resource Naming with Tokens

Use stable naming tokens so the same workload deploys predictably across environments.

Recommended pattern:

```text
rg-{workload}-{env}
app-{workload}-{env}
asp-{workload}-{env}
kv-{workload}-{env}
log-{workload}-{env}
```

Apply truncation rules only when platform limits require it.

## RBAC Assignment Pattern

Use explicit role assignments for managed identities and deployment principals.

```bicep
resource appIdentityRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, principalId, 'Storage Blob Data Contributor')
  scope: storageAccount
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
    )
    principalType: 'ServicePrincipal'
  }
}
```

## Private Endpoint Pattern

Use private endpoints when the assessment requires private connectivity to services such as SQL, Storage, Key Vault, or App Configuration.

Pattern:

1. provision or reference VNet/subnet
2. deploy the service with public access restricted as appropriate
3. add private endpoint in a dedicated subnet
4. link private DNS zone
5. update app configuration so runtime uses the private endpoint path transparently

## Validation Commands

```bash
az bicep build --file infra/main.bicep
az deployment group validate --resource-group <rg> --template-file infra/main.bicep --parameters @infra/main.parameters.json
az deployment group what-if --resource-group <rg> --template-file infra/main.bicep --parameters @infra/main.parameters.json
```

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- generate `main.bicep`, parameter files, and focused modules
- show how AVM modules are composed
- justify naming tokens, RBAC, and private endpoint usage
- keep shared concerns separate from host-specific resources
