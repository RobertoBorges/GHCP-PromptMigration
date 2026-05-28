@description('Resource token')
param resourceToken string
param location string
param tags object = {}
@description('Principal IDs that receive Key Vault Secrets User role')
param secretsUserPrincipalIds array = []

resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-${resourceToken}'
  location: location
  tags: tags
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
    enablePurgeProtection: true
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      bypass: 'AzureServices'
    }
  }
}

// Key Vault Secrets User role
var secretsUserRoleId = '4633458b-17de-408a-b874-0445c86b69e6'
resource secretsUserRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for pid in secretsUserPrincipalIds: {
  name: guid(kv.id, pid, secretsUserRoleId)
  scope: kv
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', secretsUserRoleId)
    principalId: pid
    principalType: 'ServicePrincipal'
  }
}]

output id string = kv.id
output name string = kv.name
output uri string = kv.properties.vaultUri
