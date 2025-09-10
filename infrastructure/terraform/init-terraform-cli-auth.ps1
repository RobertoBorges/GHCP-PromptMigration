# PowerShell script to initialize Terraform with Azure CLI authentication
# This addresses the issue with key-based authentication being disabled on the storage account

param (
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName = "rg-infra-app-emea-vpmamidi-demo",
    
    [Parameter(Mandatory=$false)]
    [string]$StorageAccountName = "contosotfdwus01",
    
    [Parameter(Mandatory=$false)]
    [string]$ContainerName = "tfstate",
    
    [Parameter(Mandatory=$false)]
    [string]$KeyName = "storeapp-dev.tfstate",
    
    [Parameter(Mandatory=$false)]
    [string]$WorkingDirectory = "."
)

$ErrorActionPreference = "Stop"

Write-Host "Initializing Terraform with Azure CLI authentication..." -ForegroundColor Green
Write-Host "Resource Group: $ResourceGroupName" -ForegroundColor Yellow
Write-Host "Storage Account: $StorageAccountName" -ForegroundColor Yellow
Write-Host "Container: $ContainerName" -ForegroundColor Yellow
Write-Host "State Key: $KeyName" -ForegroundColor Yellow

# Check if Azure CLI is logged in
Write-Host "Checking Azure CLI login status..." -ForegroundColor Cyan
$loginStatus = az account show --query name -o tsv 2>$null
if (-not $loginStatus) {
    Write-Host "You are not logged in to Azure CLI. Please login first." -ForegroundColor Red
    az login
}

# Verify login was successful
$loginStatus = az account show --query name -o tsv 2>$null
if (-not $loginStatus) {
    Write-Host "Azure CLI login failed. Please try again manually with 'az login'." -ForegroundColor Red
    exit 1
}

Write-Host "Logged in to Azure as: $loginStatus" -ForegroundColor Green

# Verify that the resource group and storage account exist
Write-Host "Verifying resource group and storage account..." -ForegroundColor Cyan
$resourceGroup = az group show --name $ResourceGroupName --query name -o tsv 2>$null
if (-not $resourceGroup) {
    Write-Host "Resource group $ResourceGroupName does not exist. Please create it first with setup-terraform-backend.ps1" -ForegroundColor Red
    exit 1
}

$storageAccount = az storage account show --name $StorageAccountName --resource-group $ResourceGroupName --query name -o tsv 2>$null
if (-not $storageAccount) {
    Write-Host "Storage account $StorageAccountName does not exist. Please create it first with setup-terraform-backend.ps1" -ForegroundColor Red
    exit 1
}

# Verify that the container exists
Write-Host "Verifying blob container..." -ForegroundColor Cyan
$container = az storage container exists --name $ContainerName --account-name $StorageAccountName --auth-mode login --query exists -o tsv 2>$null
if ($container -ne "true") {
    Write-Host "Container $ContainerName does not exist. Creating it now..." -ForegroundColor Yellow
    az storage container create --name $ContainerName --account-name $StorageAccountName --auth-mode login
}

# Initialize Terraform with backend configuration
Write-Host "Initializing Terraform..." -ForegroundColor Cyan
Set-Location $WorkingDirectory

# Create temporary backend config file
$backendConfig = @"
resource_group_name  = "$ResourceGroupName"
storage_account_name = "$StorageAccountName"
container_name       = "$ContainerName"
key                  = "$KeyName"
use_azuread_auth     = true
"@

$backendFilePath = Join-Path (Get-Location) "backend-azure.tfvars"
$backendConfig | Out-File -FilePath $backendFilePath -Force -Encoding utf8

# Run terraform init
terraform init -reconfigure -backend-config="$backendFilePath"

# Clean up
Remove-Item $backendFilePath -Force

Write-Host "`nTerraform initialized successfully with Azure CLI authentication." -ForegroundColor Green
Write-Host "You can now run terraform plan, terraform apply, etc." -ForegroundColor Green
