# PowerShell script to set up Terraform backend storage with proper naming conventions
# This follows the Cloud Management Framework (CMF) Tenant Naming convention

param (
    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev",
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "eastus",
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectName = "storeapp",
    
    [Parameter(Mandatory=$false)]
    [string]$OrganizationPrefix = "contoso"
)

$ErrorActionPreference = "Stop"

# CMF naming convention formatting
$locationShort = switch ($Location) {
    "eastus" { "eus" }
    "westus" { "wus" }
    "northeurope" { "neu" }
    "westeurope" { "weu" }
    "eastasia" { "eas" }
    "southeastasia" { "seas" }
    default { $Location.Substring(0, 3).ToLower() }
}

$envShort = switch ($Environment) {
    "dev" { "d" }
    "test" { "t" }
    "qa" { "q" }
    "uat" { "u" }
    "prod" { "p" }
    default { $Environment.Substring(0, 1).ToLower() }
}

# CMF naming convention: <org>-<app/service>-<environment>-<region>-<instance>
$resourceGroupName = "$OrganizationPrefix-$ProjectName-tfstate-$envShort-$locationShort-01"
$storageAccountName = "$($OrganizationPrefix)$($ProjectName)tfst$($envShort)$($locationShort)01".ToLower().Replace("-", "")
$containerName = "tfstate"
$keyName = "$ProjectName-$Environment.tfstate"

Write-Host "Setting up Terraform backend storage with CMF naming conventions..." -ForegroundColor Green
Write-Host "Resource Group: $resourceGroupName" -ForegroundColor Yellow
Write-Host "Storage Account: $storageAccountName" -ForegroundColor Yellow
Write-Host "Container: $containerName" -ForegroundColor Yellow
Write-Host "State Key: $keyName" -ForegroundColor Yellow

# Create resource group
Write-Host "Creating resource group..." -ForegroundColor Cyan
az group create --name $resourceGroupName --location $Location

# Create storage account
Write-Host "Creating storage account..." -ForegroundColor Cyan
az storage account create --resource-group $resourceGroupName --name $storageAccountName --sku Standard_LRS --encryption-services blob --https-only true --min-tls-version TLS1_2

# Get storage account key
$accountKey = $(az storage account keys list --resource-group $resourceGroupName --account-name $storageAccountName --query [0].value -o tsv)

# Create blob container
Write-Host "Creating blob container..." -ForegroundColor Cyan
az storage container create --name $containerName --account-name $storageAccountName --account-key $accountKey

# Output configuration for Azure DevOps variable groups
Write-Host "`nConfiguration for Azure DevOps TerraformConfig variable group:" -ForegroundColor Green
Write-Host "TF_STATE_RESOURCE_GROUP_NAME: $resourceGroupName"
Write-Host "TF_STATE_STORAGE_ACCOUNT_NAME: $storageAccountName"
Write-Host "TF_STATE_CONTAINER_NAME: $containerName"
Write-Host "TF_STATE_KEY: $keyName"

# Create backend.tfvars file
$backendConfig = @"
resource_group_name  = "$resourceGroupName"
storage_account_name = "$storageAccountName"
container_name       = "$containerName"
key                  = "$keyName"
"@

$backendFilePath = Join-Path (Get-Location) "backend.tfvars"
$backendConfig | Out-File -FilePath $backendFilePath -Force

Write-Host "`nBackend configuration saved to: $backendFilePath" -ForegroundColor Green
Write-Host "Use this file with: terraform init -backend-config=backend.tfvars" -ForegroundColor Green

# Output for manual configuration if needed
Write-Host "`nTerraform backend configuration block:" -ForegroundColor Green
Write-Host @"
terraform {
  backend "azurerm" {
    resource_group_name  = "$resourceGroupName"
    storage_account_name = "$storageAccountName"
    container_name       = "$containerName"
    key                  = "$keyName"
  }
}
"@
