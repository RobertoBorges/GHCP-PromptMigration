// =============================================================================
// App Service Module
// =============================================================================
// Deploys an App Service Plan and Web App with managed identity,
// Application Insights integration, and security best practices.
// Uses Azure Verified Modules (AVM) for reliability.
// =============================================================================

// =============================================================================
// Parameters
// =============================================================================

@description('Name of the workload (used for resource naming)')
@minLength(3)
@maxLength(20)
param workloadName string

@description('Environment name')
@allowed(['dev', 'staging', 'prod'])
param environmentName string

@description('Azure region for resources')
param location string

@description('Tags to apply to all resources')
param tags object = {}

@description('SKU name for the App Service Plan')
param skuName string = environmentName == 'prod' ? 'P1v3' : 'B1'

@description('Application Insights connection string')
param applicationInsightsConnectionString string = ''

@description('Key Vault name for secret references')
param keyVaultName string = ''

@description('Container Registry login server (for container-based deployments)')
param containerRegistryLoginServer string = ''

@description('Runtime stack for the web app')
@allowed(['dotnet', 'java', 'node', 'python'])
param runtimeStack string = 'dotnet'

@description('Runtime version')
param runtimeVersion string = '10.0'

@description('Enable VNet integration')
param enableVnetIntegration bool = false

@description('Subnet resource ID for VNet integration')
param vnetSubnetId string = ''

// =============================================================================
// Variables
// =============================================================================

var resourceToken = toLower(uniqueString(resourceGroup().id, workloadName, environmentName))
var appServicePlanName = 'asp-${workloadName}-${environmentName}'
var appServiceName = 'app-${workloadName}-${environmentName}'

var linuxFxVersion = {
  dotnet: 'DOTNETCORE|${runtimeVersion}'
  java: 'JAVA|${runtimeVersion}-java21'
  node: 'NODE|${runtimeVersion}'
  python: 'PYTHON|${runtimeVersion}'
}

// =============================================================================
// App Service Plan (using AVM)
// =============================================================================

module appServicePlan 'br/public:avm/res/web/serverfarm:0.2.0' = {
  name: 'asp-${resourceToken}'
  params: {
    name: appServicePlanName
    location: location
    skuName: skuName
    skuCapacity: environmentName == 'prod' ? 2 : 1
    kind: 'linux'
    reserved: true
    zoneRedundant: environmentName == 'prod'
    tags: tags
  }
}

// =============================================================================
// Web App (using AVM)
// =============================================================================

module appService 'br/public:avm/res/web/site:0.3.0' = {
  name: 'app-${resourceToken}'
  params: {
    name: appServiceName
    location: location
    kind: 'app,linux'
    serverFarmResourceId: appServicePlan.outputs.resourceId
    managedIdentities: {
      systemAssigned: true
    }
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: linuxFxVersion[runtimeStack]
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      http20Enabled: true
      alwaysOn: skuName != 'F1' && skuName != 'D1'
      healthCheckPath: '/health'
      appSettings: concat(
        [
          {
            name: 'WEBSITE_RUN_FROM_PACKAGE'
            value: '1'
          }
          {
            name: 'ASPNETCORE_ENVIRONMENT'
            value: environmentName == 'prod' ? 'Production' : 'Development'
          }
        ],
        !empty(applicationInsightsConnectionString) ? [
          {
            name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
            value: applicationInsightsConnectionString
          }
        ] : [],
        !empty(containerRegistryLoginServer) ? [
          {
            name: 'DOCKER_REGISTRY_SERVER_URL'
            value: 'https://${containerRegistryLoginServer}'
          }
        ] : []
      )
    }
    virtualNetworkSubnetId: enableVnetIntegration ? vnetSubnetId : ''
    tags: tags
  }
}

// =============================================================================
// Diagnostic Settings
// =============================================================================

resource diagnosticSettings 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = if (!empty(applicationInsightsConnectionString)) {
  name: '${appServiceName}-diagnostics'
  scope: appService
  properties: {
    logs: [
      {
        categoryGroup: 'allLogs'
        enabled: true
        retentionPolicy: {
          days: environmentName == 'prod' ? 90 : 30
          enabled: true
        }
      }
    ]
    metrics: [
      {
        category: 'AllMetrics'
        enabled: true
        retentionPolicy: {
          days: environmentName == 'prod' ? 90 : 30
          enabled: true
        }
      }
    ]
  }
}

// =============================================================================
// Key Vault Access - RBAC Role Assignment
// =============================================================================

module keyVaultRoleAssignment 'br/public:avm/ptn/authorization/resource-role-assignment:0.1.1' = if (!empty(keyVaultName)) {
  name: 'kv-role-${resourceToken}'
  params: {
    principalId: appService.outputs.systemAssignedMIPrincipalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6') // Key Vault Secrets User
    resourceId: resourceId('Microsoft.KeyVault/vaults', keyVaultName)
    principalType: 'ServicePrincipal'
  }
}

// =============================================================================
// Autoscale (production only)
// =============================================================================

resource autoscaleSettings 'Microsoft.Insights/autoscalesettings@2022-10-01' = if (environmentName == 'prod') {
  name: '${appServicePlanName}-autoscale'
  location: location
  properties: {
    enabled: true
    targetResourceUri: appServicePlan.outputs.resourceId
    profiles: [
      {
        name: 'Default'
        capacity: {
          minimum: '2'
          maximum: '10'
          default: '2'
        }
        rules: [
          {
            metricTrigger: {
              metricName: 'CpuPercentage'
              metricResourceUri: appServicePlan.outputs.resourceId
              timeGrain: 'PT1M'
              statistic: 'Average'
              timeWindow: 'PT5M'
              timeAggregation: 'Average'
              operator: 'GreaterThan'
              threshold: 70
            }
            scaleAction: {
              direction: 'Increase'
              type: 'ChangeCount'
              value: '1'
              cooldown: 'PT5M'
            }
          }
          {
            metricTrigger: {
              metricName: 'CpuPercentage'
              metricResourceUri: appServicePlan.outputs.resourceId
              timeGrain: 'PT1M'
              statistic: 'Average'
              timeWindow: 'PT10M'
              timeAggregation: 'Average'
              operator: 'LessThan'
              threshold: 30
            }
            scaleAction: {
              direction: 'Decrease'
              type: 'ChangeCount'
              value: '1'
              cooldown: 'PT10M'
            }
          }
        ]
      }
    ]
  }
  tags: tags
}

// =============================================================================
// Outputs
// =============================================================================

output appServicePlanId string = appServicePlan.outputs.resourceId
output appServiceId string = appService.outputs.resourceId
output appServiceName string = appService.outputs.name
output appServiceDefaultHostName string = appService.outputs.defaultHostname
output appServicePrincipalId string = appService.outputs.systemAssignedMIPrincipalId
