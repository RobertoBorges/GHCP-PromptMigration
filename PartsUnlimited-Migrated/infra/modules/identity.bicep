@description('Resource token')
param resourceToken string
param location string
param tags object = {}

resource uami 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'id-${resourceToken}'
  location: location
  tags: tags
}

output id string = uami.id
output clientId string = uami.properties.clientId
output principalId string = uami.properties.principalId
output name string = uami.name
