# PowerShell script to deploy the Store Application to Azure

param (
    [Parameter(Mandatory=$false)]
    [string]$Environment = "dev"
)

$ErrorActionPreference = "Stop"

# Set working directory to the terraform folder
$terraformDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $terraformDir

Write-Host "Deploying Store Application to Azure ($Environment environment)..." -ForegroundColor Green

# Initialize Terraform (if not already initialized)
Write-Host "Initializing Terraform..." -ForegroundColor Yellow
terraform init

# Create and save Terraform plan
Write-Host "Creating Terraform plan..." -ForegroundColor Yellow
terraform plan -var="environment=$Environment" -out="storeapp.tfplan"

# Apply Terraform configuration using the saved plan
Write-Host "Applying Terraform configuration..." -ForegroundColor Yellow
terraform apply "storeapp.tfplan"

# Get outputs from Terraform
$resourceGroupName = terraform output -raw resource_group_name
$appServiceName = terraform output -raw app_service_name
$appServiceUrl = terraform output -raw app_service_url

# Build and publish the .NET application
Write-Host "Building and publishing the application..." -ForegroundColor Yellow
$projectPath = "..\..\src\StoreApp"
$publishPath = "..\..\src\StoreApp\bin\Release\net8.0\publish"

dotnet publish $projectPath -c Release

# Zip the published files
$zipPath = "..\..\src\StoreApp\bin\Release\net8.0\publish.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($publishPath, $zipPath)

# Deploy to Azure App Service
Write-Host "Deploying to Azure App Service..." -ForegroundColor Yellow
az webapp deployment source config-zip -g "$resourceGroupName" -n $appServiceName --src $zipPath

Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "Application URL: $appServiceUrl" -ForegroundColor Cyan
