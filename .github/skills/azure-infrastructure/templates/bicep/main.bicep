// =============================================================================
// Azure Bicep Main Template
// =============================================================================
// Infrastructure as Code for Azure Application Deployment
// Uses Azure Verified Modules for reliability
// =============================================================================

targetScope = 'subscription'

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
param location string = 'eastus2'

@description('Tags to apply to all resources')
param tags object = {}

// =============================================================================
// Variables
// =============================================================================

var resourceToken = toLower(uniqueString(subscription().id, workloadName, environmentName))
var resourceGroupName = 'rg-${workloadName}-${environmentName}'

var defaultTags = union(tags, {
  Environment: environmentName
  Workload: workloadName
  ManagedBy: 'Bicep'
})

// =============================================================================
// Resource Group
// =============================================================================

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: defaultTags
}

// =============================================================================
// Monitoring (Log Analytics + Application Insights)
// =============================================================================

module monitoring 'br/public:avm/ptn/azd/monitoring:0.1.0' = {
  scope: rg
  name: 'monitoring-${resourceToken}'
  params: {
    applicationInsightsName: 'appi-${workloadName}-${environmentName}'
    logAnalyticsName: 'log-${workloadName}-${environmentName}'
    location: location
    tags: defaultTags
  }
}

// =============================================================================
// Container Registry
// =============================================================================

module containerRegistry 'br/public:avm/res/container-registry/registry:0.4.0' = {
  scope: rg
  name: 'acr-${resourceToken}'
  params: {
    name: 'acr${resourceToken}'
    location: location
    acrSku: environmentName == 'prod' ? 'Premium' : 'Basic'
    acrAdminUserEnabled: false
    tags: defaultTags
  }
}

// =============================================================================
// Container Apps Environment
// =============================================================================

module containerAppsEnvironment 'br/public:avm/res/app/managed-environment:0.5.2' = {
  scope: rg
  name: 'cae-${resourceToken}'
  params: {
    name: 'cae-${workloadName}-${environmentName}'
    location: location
    logAnalyticsWorkspaceResourceId: monitoring.outputs.logAnalyticsWorkspaceResourceId
    zoneRedundant: environmentName == 'prod'
    tags: defaultTags
  }
}

// =============================================================================
// Key Vault
// =============================================================================

module keyVault 'br/public:avm/res/key-vault/vault:0.6.1' = {
  scope: rg
  name: 'kv-${resourceToken}'
  params: {
    name: 'kv-${workloadName}-${resourceToken}'
    location: location
    sku: 'standard'
    enableRbacAuthorization: true
    enablePurgeProtection: environmentName == 'prod'
    softDeleteRetentionInDays: 7
    tags: defaultTags
  }
}

// =============================================================================
// SQL Database (if needed)
// =============================================================================

module sqlServer 'br/public:avm/res/sql/server:0.4.1' = {
  scope: rg
  name: 'sql-${resourceToken}'
  params: {
    name: 'sql-${workloadName}-${environmentName}'
    location: location
    administratorLoginPassword: '' // Use managed identity or Key Vault
    databases: [
      {
        name: '${workloadName}db'
        skuName: environmentName == 'prod' ? 'S1' : 'Basic'
        maxSizeBytes: 2147483648
      }
    ]
    tags: defaultTags
  }
}

// =============================================================================
// Outputs
// =============================================================================

output resourceGroupName string = rg.name
output containerRegistryName string = containerRegistry.outputs.name
output containerRegistryLoginServer string = containerRegistry.outputs.loginServer
output containerAppsEnvironmentId string = containerAppsEnvironment.outputs.resourceId
output keyVaultName string = keyVault.outputs.name
output applicationInsightsConnectionString string = monitoring.outputs.applicationInsightsConnectionString
output sqlServerFqdn string = sqlServer.outputs.fullyQualifiedDomainName
