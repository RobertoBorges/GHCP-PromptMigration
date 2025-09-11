# Setup-AzureDevOpsPipeline.ps1
# This script helps set up the Azure DevOps pipeline and required resources

param (
    [string]$AzureDevOpsOrg,
    [string]$AzureDevOpsProject,
    [string]$RepositoryName = "GHCP-PromptMigration",
    [string]$BranchName = "pipeline-branch",
    [string]$AzureSubscriptionId,
    [string]$ResourceGroupName = "rg-infra-winmig-emea-vpmamidi-demo",
    [string]$Location = "eastus",
    [switch]$CreateInfrastructure = $false
)

$ErrorActionPreference = "Stop"

# Function to display section headers
function Show-Header {
    param ([string]$Title)
    Write-Host "`n===== $Title =====" -ForegroundColor Cyan
}

# Check if Azure CLI is installed
Show-Header "Checking Prerequisites"
try {
    $azVersion = az --version
    Write-Host "Azure CLI is installed: $($azVersion[0])" -ForegroundColor Green
}
catch {
    Write-Host "Azure CLI is not installed. Please install it from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Check if Azure DevOps extension is installed
$azExtensions = az extension list --output json | ConvertFrom-Json
if (-not ($azExtensions | Where-Object { $_.name -eq "azure-devops" })) {
    Write-Host "Installing Azure DevOps extension..." -ForegroundColor Yellow
    az extension add --name azure-devops
}
else {
    Write-Host "Azure DevOps extension is already installed" -ForegroundColor Green
}

# Login to Azure if not already logged in
$loginStatus = az account show --query name --output tsv 2>$null
if (-not $loginStatus) {
    Show-Header "Logging in to Azure"
    az login
}
else {
    Write-Host "Already logged in to Azure as: $loginStatus" -ForegroundColor Green
}

# Set subscription context
if ($AzureSubscriptionId) {
    Show-Header "Setting Azure Subscription"
    az account set --subscription $AzureSubscriptionId
    Write-Host "Subscription set to: $AzureSubscriptionId" -ForegroundColor Green
}

# Create resource group if it doesn't exist and if CreateInfrastructure is set
if ($CreateInfrastructure) {
    Show-Header "Creating Azure Resources"
    
    # Create resource group if it doesn't exist
    $rgExists = az group show --name $ResourceGroupName 2>$null
    if (-not $rgExists) {
        Write-Host "Creating resource group: $ResourceGroupName" -ForegroundColor Yellow
        az group create --name $ResourceGroupName --location $Location --tags "Created By=Setup-Script" "Created On=$(Get-Date -Format 'yyyy-MM-dd')" "Customer Name=Internal" "Purpose=Demo" "Region=$Location" "Tower=Migration" "V-ID=vpmamidi"
        Write-Host "Resource group created successfully" -ForegroundColor Green
    }
    else {
        Write-Host "Resource group already exists: $ResourceGroupName" -ForegroundColor Green
    }
    
    # Create App Service Plan if it doesn't exist
    $appServicePlanName = "asp-infra-winmig-emea-vpmamidi-demo"
    $appServicePlanExists = az appservice plan show --name $appServicePlanName --resource-group $ResourceGroupName 2>$null
    if (-not $appServicePlanExists) {
        Write-Host "Creating App Service Plan: $appServicePlanName" -ForegroundColor Yellow
        az appservice plan create --name $appServicePlanName --resource-group $ResourceGroupName --sku F1 --is-linux false
        Write-Host "App Service Plan created successfully" -ForegroundColor Green
    }
    else {
        Write-Host "App Service Plan already exists: $appServicePlanName" -ForegroundColor Green
    }
    
    # Create Web Apps for NetFrameworkWebApp and StoreApp
    $netFxAppName = "contoso-app-netframeworkwebapp-d-eus-01"
    $storeAppName = "contoso-app-storeapp-d-eus-01"
    
    $netFxAppExists = az webapp show --name $netFxAppName --resource-group $ResourceGroupName 2>$null
    if (-not $netFxAppExists) {
        Write-Host "Creating Web App: $netFxAppName" -ForegroundColor Yellow
        az webapp create --name $netFxAppName --resource-group $ResourceGroupName --plan $appServicePlanName --runtime "dotnet:8"
        Write-Host "Web App created successfully: $netFxAppName" -ForegroundColor Green
    }
    else {
        Write-Host "Web App already exists: $netFxAppName" -ForegroundColor Green
    }
    
    $storeAppExists = az webapp show --name $storeAppName --resource-group $ResourceGroupName 2>$null
    if (-not $storeAppExists) {
        Write-Host "Creating Web App: $storeAppName" -ForegroundColor Yellow
        az webapp create --name $storeAppName --resource-group $ResourceGroupName --plan $appServicePlanName --runtime "dotnet:8"
        Write-Host "Web App created successfully: $storeAppName" -ForegroundColor Green
    }
    else {
        Write-Host "Web App already exists: $storeAppName" -ForegroundColor Green
    }
}

# If Azure DevOps organization and project are provided, configure the pipeline
if ($AzureDevOpsOrg -and $AzureDevOpsProject) {
    Show-Header "Configuring Azure DevOps Pipeline"
    
    # Login to Azure DevOps
    Write-Host "Logging in to Azure DevOps organization: $AzureDevOpsOrg" -ForegroundColor Yellow
    az devops configure --defaults organization="https://dev.azure.com/$AzureDevOpsOrg" project="$AzureDevOpsProject"
    
    # Create service connection for Azure
    Write-Host "Creating Azure service connection..." -ForegroundColor Yellow
    $serviceConnectionName = "Azure-Service-Connection"
    az devops service-endpoint azurerm create --name $serviceConnectionName --azure-rm-subscription-id $AzureSubscriptionId --azure-rm-subscription-name $(az account show --query name -o tsv) --azure-rm-tenant-id $(az account show --query tenantId -o tsv)
    
    # Create pipeline
    Write-Host "Creating pipeline..." -ForegroundColor Yellow
    $pipelineName = "Application-Deployment"
    $pipelineYamlPath = "infrastructure/cicd/azure-devops-app-pipeline.yml"
    az pipelines create --name $pipelineName --repository $RepositoryName --branch $BranchName --yaml-path $pipelineYamlPath
    
    Write-Host "Pipeline created successfully: $pipelineName" -ForegroundColor Green
}
else {
    Show-Header "Azure DevOps Pipeline Configuration"
    Write-Host "Azure DevOps organization and project information not provided." -ForegroundColor Yellow
    Write-Host "To set up the pipeline in Azure DevOps, follow these steps:" -ForegroundColor Yellow
    Write-Host "1. Go to your Azure DevOps project" -ForegroundColor White
    Write-Host "2. Navigate to Pipelines > New Pipeline" -ForegroundColor White
    Write-Host "3. Select your repository" -ForegroundColor White
    Write-Host "4. Choose 'Existing Azure Pipelines YAML file'" -ForegroundColor White
    Write-Host "5. Select the file path: 'infrastructure/cicd/azure-devops-app-pipeline.yml'" -ForegroundColor White
    Write-Host "6. Review and run the pipeline" -ForegroundColor White
}

Show-Header "Setup Complete"
Write-Host "Steps to access your applications after deployment:" -ForegroundColor Green
Write-Host "- NetFrameworkWebApp: https://contoso-app-netframeworkwebapp-d-eus-01.azurewebsites.net" -ForegroundColor White
Write-Host "- StoreApp: https://contoso-app-storeapp-d-eus-01.azurewebsites.net" -ForegroundColor White
Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
Write-Host "- If you encounter Azure Policy issues, check tag capitalization" -ForegroundColor White
Write-Host "- If App Service creation fails, verify quota and try the Free tier (F1)" -ForegroundColor White
Write-Host "- For detailed deployment logs, check the Azure DevOps pipeline logs" -ForegroundColor White
