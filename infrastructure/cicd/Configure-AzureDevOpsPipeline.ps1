# Configure-AzureDevOpsPipeline.ps1
# This script configures the application pipeline in Azure DevOps using your current settings

param (
    [Parameter(Mandatory=$true)]
    [string]$AzureDevOpsOrg,
    
    [Parameter(Mandatory=$true)]
    [string]$AzureDevOpsProject,
    
    [Parameter(Mandatory=$false)]
    [string]$AzureSubscriptionId,
    
    [Parameter(Mandatory=$false)]
    [string]$ServiceConnectionName = "Azure-Service-Connection",
    
    [switch]$CreateServiceConnection = $false,
    
    [switch]$RunPipeline = $false
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param ([string]$Message)
    Write-Host "`n>> $Message" -ForegroundColor Cyan
}

# Variables for our project
$repoName = "GHCP-PromptMigration"
$branchName = "pipeline-branch"
$pipelineName = "MigratedApps-Deployment"
$yamlPath = "infrastructure/cicd/azure-devops-app-pipeline.yml"
$resourceGroupName = "rg-infra-winmig-emea-vpmamidi-demo"
$netFxAppName = "contoso-app-netframeworkwebapp-d-eus-01"
$storeAppName = "contoso-app-storeapp-d-eus-01"

Write-Step "Checking prerequisites"

# Check Azure CLI
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✓ Azure CLI: v$($azVersion.'azure-cli')" -ForegroundColor Green
}
catch {
    Write-Host "✗ Azure CLI not installed. Please install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Check Azure DevOps extension
$extensions = az extension list --output json | ConvertFrom-Json
if (-not ($extensions | Where-Object { $_.name -eq "azure-devops" })) {
    Write-Host "Installing Azure DevOps extension..." -ForegroundColor Yellow
    az extension add --name azure-devops
    Write-Host "✓ Azure DevOps extension installed" -ForegroundColor Green
}
else {
    Write-Host "✓ Azure DevOps extension installed" -ForegroundColor Green
}

Write-Step "Configuring Azure DevOps"
az devops configure --defaults organization="https://dev.azure.com/$AzureDevOpsOrg" project="$AzureDevOpsProject"

# Login to Azure CLI if needed
if ($AzureSubscriptionId) {
    Write-Step "Logging in to Azure"
    $currentAccount = az account show --output json 2>$null | ConvertFrom-Json
    
    if (-not $currentAccount -or $currentAccount.id -ne $AzureSubscriptionId) {
        Write-Host "Logging in to Azure..." -ForegroundColor Yellow
        az login
        az account set --subscription $AzureSubscriptionId
    }
    else {
        Write-Host "✓ Already logged in to Azure subscription: $($currentAccount.name)" -ForegroundColor Green
    }
}

# Login to Azure DevOps
Write-Step "Logging in to Azure DevOps"
Write-Host "You may be prompted for authentication..." -ForegroundColor Yellow
az devops login

# Create Service Connection if requested and if Azure subscription is provided
if ($CreateServiceConnection -and $AzureSubscriptionId) {
    Write-Step "Creating Azure Service Connection"
    
    # Check if service connection already exists
    $serviceConnections = az devops service-endpoint list --query "[?name=='$ServiceConnectionName']" --output json | ConvertFrom-Json
    
    if ($serviceConnections -and $serviceConnections.Count -gt 0) {
        Write-Host "✓ Service connection '$ServiceConnectionName' already exists" -ForegroundColor Green
    }
    else {
        Write-Host "Creating service connection '$ServiceConnectionName'..." -ForegroundColor Yellow
        az devops service-endpoint azurerm create --name $ServiceConnectionName `
            --azure-rm-subscription-id $AzureSubscriptionId `
            --azure-rm-subscription-name $(az account show --query name -o tsv) `
            --azure-rm-tenant-id $(az account show --query tenantId -o tsv)
        
        Write-Host "✓ Service connection created" -ForegroundColor Green
    }
}

# Create or update the pipeline
Write-Step "Setting up the pipeline"

# Check if pipeline already exists
$pipelines = az pipelines list --query "[?name=='$pipelineName']" --output json | ConvertFrom-Json

if ($pipelines -and $pipelines.Count -gt 0) {
    $pipelineId = $pipelines[0].id
    Write-Host "Updating existing pipeline '$pipelineName' (ID: $pipelineId)..." -ForegroundColor Yellow
    az pipelines update --id $pipelineId --name $pipelineName --yaml-path $yamlPath --branch $branchName
}
else {
    Write-Host "Creating new pipeline '$pipelineName'..." -ForegroundColor Yellow
    $result = az pipelines create --name $pipelineName --repository $repoName --branch $branchName --yml-path $yamlPath --skip-first-run --output json | ConvertFrom-Json
    $pipelineId = $result.id
}

Write-Host "✓ Pipeline configured (ID: $pipelineId)" -ForegroundColor Green

# Configure pipeline variables
Write-Step "Setting pipeline variables"

$variables = @(
    @{ name = "environment"; value = "dev" },
    @{ name = "location"; value = "eastus" },
    @{ name = "offering"; value = "infra" },
    @{ name = "subOffering"; value = "winmig" },
    @{ name = "factoryRegion"; value = "emea" },
    @{ name = "vId"; value = "vpmamidi" },
    @{ name = "purpose"; value = "demo" },
    @{ name = "resourceGroupName"; value = $resourceGroupName },
    @{ name = "netFxAppName"; value = $netFxAppName },
    @{ name = "storeAppName"; value = $storeAppName },
    @{ name = "azureServiceConnection"; value = $ServiceConnectionName }
)

foreach ($var in $variables) {
    Write-Host "Setting variable: $($var.name) = $($var.value)" -ForegroundColor Yellow
    az pipelines variable create --pipeline-id $pipelineId --name $var.name --value $var.value --output none
}

Write-Host "✓ Pipeline variables configured" -ForegroundColor Green

# Enable continuous integration
Write-Step "Configuring trigger settings"
Write-Host "The pipeline is configured to trigger on changes to branches: main, master, pipeline-branch" -ForegroundColor Yellow
Write-Host "These settings are defined in the YAML file" -ForegroundColor Yellow

# Run the pipeline if requested
if ($RunPipeline) {
    Write-Step "Running the pipeline"
    Write-Host "Starting pipeline execution..." -ForegroundColor Yellow
    $run = az pipelines run --id $pipelineId --output json | ConvertFrom-Json
    Write-Host "✓ Pipeline started - Run ID: $($run.id)" -ForegroundColor Green
    Write-Host "Monitor run progress at: $($run._links.web.href)" -ForegroundColor Cyan
}

Write-Step "Configuration complete"
Write-Host "The application pipeline has been configured in Azure DevOps!" -ForegroundColor Green
Write-Host ""
Write-Host "Pipeline information:" -ForegroundColor White
Write-Host "- Name: $pipelineName" -ForegroundColor White
Write-Host "- ID: $pipelineId" -ForegroundColor White
Write-Host "- YAML path: $yamlPath" -ForegroundColor White
Write-Host "- Branch: $branchName" -ForegroundColor White
Write-Host "- Service connection: $ServiceConnectionName" -ForegroundColor White
Write-Host ""
Write-Host "Resource information:" -ForegroundColor White
Write-Host "- Resource group: $resourceGroupName" -ForegroundColor White
Write-Host "- NetFx Web App: $netFxAppName" -ForegroundColor White
Write-Host "- Store App: $storeAppName" -ForegroundColor White
Write-Host ""
Write-Host "To manually run the pipeline:" -ForegroundColor Yellow
Write-Host "az pipelines run --id $pipelineId" -ForegroundColor DarkGray
Write-Host ""
Write-Host "Access your pipeline in the Azure DevOps portal:" -ForegroundColor Yellow
Write-Host "https://dev.azure.com/$AzureDevOpsOrg/$AzureDevOpsProject/_build?definitionId=$pipelineId" -ForegroundColor Cyan
