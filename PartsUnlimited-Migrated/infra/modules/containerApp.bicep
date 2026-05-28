@description('Resource token')
param resourceToken string
param location string
param tags object = {}

@description('Log Analytics workspace customer id')
param logAnalyticsCustomerId string
@description('Log Analytics workspace resource id (for diagnostics)')
param logAnalyticsId string
@description('Application Insights connection string')
param appInsightsConnectionString string

@description('User-assigned managed identity resource id')
param userAssignedIdentityId string
@description('User-assigned managed identity client id (for AcrPull + SQL AAD auth)')
param userAssignedIdentityClientId string

@description('ACR login server')
param acrLoginServer string

@description('Full image reference (login server/repository:tag). For first deploy, can be a placeholder; azd will rebuild and update.')
param containerImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

@description('SQL connection string (managed identity auth)')
param sqlConnectionString string

@description('Service name tag value used by azd to map service to resource')
param serviceTag string = 'web'

@description('Min replicas')
param minReplicas int = 1
@description('Max replicas')
param maxReplicas int = 3

resource lawSecret 'Microsoft.OperationalInsights/workspaces@2023-09-01' existing = {
  name: split(logAnalyticsId, '/')[8]
}

resource cae 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'cae-${resourceToken}'
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsCustomerId
        sharedKey: lawSecret.listKeys().primarySharedKey
      }
    }
    zoneRedundant: false
  }
}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'ca-${resourceToken}'
  location: location
  tags: union(tags, { 'azd-service-name': serviceTag })
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentityId}': {}
    }
  }
  properties: {
    managedEnvironmentId: cae.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: true
        targetPort: 8080
        transport: 'auto'
        allowInsecure: false
        traffic: [
          { weight: 100, latestRevision: true }
        ]
      }
      registries: [
        {
          server: acrLoginServer
          identity: userAssignedIdentityId
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'web'
          image: containerImage
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
          env: [
            { name: 'ASPNETCORE_ENVIRONMENT',                  value: 'Production' }
            { name: 'ASPNETCORE_URLS',                          value: 'http://+:8080' }
            { name: 'ApplicationInsights__ConnectionString',    value: appInsightsConnectionString }
            { name: 'ConnectionStrings__DefaultConnection',     value: sqlConnectionString }
            { name: 'AZURE_CLIENT_ID',                          value: userAssignedIdentityClientId }
            { name: 'AppSettings__ShowRecommendations',         value: 'false' }
            { name: 'AppSettings__ImagePath',                   value: '/Images' }
          ]
          probes: [
            {
              type: 'Liveness'
              httpGet: { path: '/', port: 8080 }
              initialDelaySeconds: 20
              periodSeconds: 30
            }
            {
              type: 'Readiness'
              httpGet: { path: '/', port: 8080 }
              initialDelaySeconds: 10
              periodSeconds: 15
            }
          ]
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
        rules: [
          {
            name: 'http-scale'
            http: { metadata: { concurrentRequests: '50' } }
          }
        ]
      }
    }
  }
}

output environmentId string = cae.id
output containerAppName string = app.name
output fqdn string = app.properties.configuration.ingress.fqdn
output url string = 'https://${app.properties.configuration.ingress.fqdn}'
