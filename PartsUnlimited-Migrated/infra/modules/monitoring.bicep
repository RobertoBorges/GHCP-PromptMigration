@description('Resource name prefix / token')
param resourceToken string
@description('Location for all resources')
param location string
param tags object = {}
@description('Principal IDs that receive Monitoring Metrics Publisher role on Application Insights')
param metricsPublisherPrincipalIds array = []

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${resourceToken}'
  location: location
  tags: tags
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
    features: { searchVersion: 1 }
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${resourceToken}'
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

output logAnalyticsId string = logAnalytics.id
output logAnalyticsCustomerId string = logAnalytics.properties.customerId
var metricsPublisherRoleId = '3913510d-42f4-4e42-8a64-420c390055eb'
resource metricsPublisherRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for pid in metricsPublisherPrincipalIds: {
  name: guid(appInsights.id, pid, metricsPublisherRoleId)
  scope: appInsights
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', metricsPublisherRoleId)
    principalId: pid
    principalType: 'ServicePrincipal'
  }
}]

output appInsightsConnectionString string = appInsights.properties.ConnectionString
output appInsightsName string = appInsights.name
