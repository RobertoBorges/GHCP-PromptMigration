@description('Resource token')
param resourceToken string
param location string
param tags object = {}
@description('Principal IDs that receive AcrPull role')
param acrPullPrincipalIds array = []

resource acr 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {
  name: 'acr${replace(resourceToken,'-','')}'
  location: location
  tags: tags
  sku: { name: 'Basic' }
  properties: {
    adminUserEnabled: false
    publicNetworkAccess: 'Enabled'
    anonymousPullEnabled: false
  }
}

var acrPullRoleId = '7f951dda-4ed3-4680-a7ca-43fe172d538d'
resource acrPullRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for pid in acrPullPrincipalIds: {
  name: guid(acr.id, pid, acrPullRoleId)
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRoleId)
    principalId: pid
    principalType: 'ServicePrincipal'
  }
}]

output id string = acr.id
output name string = acr.name
output loginServer string = acr.properties.loginServer
