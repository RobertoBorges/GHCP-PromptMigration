# Deploy infrastructure using Bicep
param(
    [string]$resourceGroupName = "rg-netframeworkwebapp-dev",
    [string]$location = "eastus",
    [string]$appName = "netframeworkwebapp",
    [string]$environmentName = "dev",
    [string]$appServicePlanSku = "B1"
)

# Create resource group if it doesn't exist
$rgExists = az group exists --name $resourceGroupName | ConvertFrom-Json
if (-not $rgExists) {
    Write-Host "Creating resource group $resourceGroupName in $location"
    az group create --name $resourceGroupName --location $location
}

# Deploy Bicep template
Write-Host "Deploying infrastructure to $resourceGroupName"
$deploymentOutput = az deployment group create `
    --resource-group $resourceGroupName `
    --template-file ./infrastructure/bicep/main.bicep `
    --parameters appName=$appName environmentName=$environmentName appServicePlanSku=$appServicePlanSku `
    --output json | ConvertFrom-Json

# Extract output values
$webAppName = $deploymentOutput.properties.outputs.webAppName.value
$webAppUrl = $deploymentOutput.properties.outputs.webAppUrl.value
$appInsightsName = $deploymentOutput.properties.outputs.appInsightsName.value
$keyVaultName = $deploymentOutput.properties.outputs.keyVaultName.value

Write-Host "Deployment completed successfully!"
Write-Host "Web App: $webAppName"
Write-Host "Web App URL: $webAppUrl"
Write-Host "Application Insights: $appInsightsName"
Write-Host "Key Vault: $keyVaultName"

# Return the deployment details
return @{
    WebAppName = $webAppName
    WebAppUrl = $webAppUrl
    AppInsightsName = $appInsightsName
    KeyVaultName = $keyVaultName
    ResourceGroupName = $resourceGroupName
}
