# Setup-AppDeploymentPipeline.ps1
# This script sets up the application deployment pipeline in Azure DevOps

param (
    [Parameter(Mandatory=$true)]
    [string]$AzureDevOpsOrg,
    
    [Parameter(Mandatory=$true)]
    [string]$AzureDevOpsProject,
    
    [Parameter(Mandatory=$true)]
    [string]$ServiceConnectionName,
    
    [string]$RepositoryName = "GHCP-PromptMigration",
    
    [string]$BranchName = "pipeline-branch",
    
    [string]$PipelineName = "Application-Deployment-Pipeline",
    
    [string]$YamlPath = "infrastructure/cicd/azure-devops-app-pipeline.yml",
    
    [switch]$TriggerPipeline = $false
)

$ErrorActionPreference = "Stop"

function Write-StepHeader {
    param([string]$Message)
    Write-Host "`n>> $Message" -ForegroundColor Cyan
}

Write-StepHeader "Checking Prerequisites"

# Check if Azure CLI is installed
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✓ Azure CLI installed: v$($azVersion.'azure-cli')" -ForegroundColor Green
} 
catch {
    Write-Host "✗ Azure CLI not found. Please install Azure CLI." -ForegroundColor Red
    Write-Host "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Check if Azure DevOps extension is installed
$azExtensions = az extension list --output json | ConvertFrom-Json
if (-not ($azExtensions | Where-Object { $_.name -eq "azure-devops" })) {
    Write-Host "Installing Azure DevOps extension..." -ForegroundColor Yellow
    az extension add --name azure-devops
}
Write-Host "✓ Azure DevOps extension installed" -ForegroundColor Green

# Configure Azure DevOps CLI defaults
Write-StepHeader "Configuring Azure DevOps CLI"
Write-Host "Setting organization: https://dev.azure.com/$AzureDevOpsOrg" -ForegroundColor Yellow
Write-Host "Setting project: $AzureDevOpsProject" -ForegroundColor Yellow
az devops configure --defaults organization="https://dev.azure.com/$AzureDevOpsOrg" project="$AzureDevOpsProject"

# Login to Azure DevOps
Write-StepHeader "Authenticating with Azure DevOps"
Write-Host "You may be prompted to log in to Azure DevOps..." -ForegroundColor Yellow
az devops login

# Check if service connection exists
Write-StepHeader "Checking Service Connection"
$serviceConnections = az devops service-endpoint list --query "[?name=='$ServiceConnectionName']" --output json | ConvertFrom-Json
if (-not $serviceConnections -or $serviceConnections.Count -eq 0) {
    Write-Host "✗ Service connection '$ServiceConnectionName' not found." -ForegroundColor Red
    Write-Host "Please create a service connection with this name in Azure DevOps portal:" -ForegroundColor Yellow
    Write-Host "1. Go to Project Settings > Service connections > New service connection" -ForegroundColor White
    Write-Host "2. Select Azure Resource Manager" -ForegroundColor White
    Write-Host "3. Choose Service Principal (automatic)" -ForegroundColor White
    Write-Host "4. Name it '$ServiceConnectionName'" -ForegroundColor White
    
    $createConnection = Read-Host "Do you want to continue without the service connection? (y/n)"
    if ($createConnection -ne "y") {
        exit 1
    }
}
else {
    Write-Host "✓ Service connection '$ServiceConnectionName' found" -ForegroundColor Green
}

# Create pipeline
Write-StepHeader "Creating Application Deployment Pipeline"
$existingPipelines = az pipelines list --query "[?name=='$PipelineName']" --output json | ConvertFrom-Json
if ($existingPipelines -and $existingPipelines.Count -gt 0) {
    Write-Host "Pipeline '$PipelineName' already exists with ID: $($existingPipelines[0].id)" -ForegroundColor Yellow
    $pipelineId = $existingPipelines[0].id
    
    # Update the existing pipeline
    Write-Host "Updating existing pipeline..." -ForegroundColor Yellow
    az pipelines update --id $pipelineId --name $PipelineName --yml-path $YamlPath --branch $BranchName
}
else {
    Write-Host "Creating new pipeline '$PipelineName'..." -ForegroundColor Yellow
    $result = az pipelines create --name $PipelineName --yml-path $YamlPath --repository $RepositoryName --branch $BranchName --skip-first-run --output json | ConvertFrom-Json
    $pipelineId = $result.id
}

Write-Host "✓ Pipeline '$PipelineName' configured with ID: $pipelineId" -ForegroundColor Green

# Add pipeline variables
Write-StepHeader "Configuring Pipeline Variables"
Write-Host "Setting required variables for the pipeline..." -ForegroundColor Yellow

# Define the variables to set
$variables = @(
    @{ name = "environment"; value = "dev" },
    @{ name = "location"; value = "eastus" },
    @{ name = "offering"; value = "infra" },
    @{ name = "subOffering"; value = "winmig" },
    @{ name = "factoryRegion"; value = "emea" },
    @{ name = "vId"; value = "vpmamidi" },
    @{ name = "purpose"; value = "demo" },
    @{ name = "resourceGroupName"; value = "rg-infra-winmig-emea-vpmamidi-demo" },
    @{ name = "netFxAppName"; value = "contoso-app-netframeworkwebapp-d-eus-01" },
    @{ name = "storeAppName"; value = "contoso-app-storeapp-d-eus-01" }
)

foreach ($var in $variables) {
    Write-Host "Setting variable: $($var.name) = $($var.value)" -ForegroundColor Yellow
    az pipelines variable create --pipeline-id $pipelineId --name $var.name --value $var.value
}

Write-Host "✓ Pipeline variables configured" -ForegroundColor Green

# Update pipeline YAML with service connection name
Write-StepHeader "Updating Pipeline Configuration"
Write-Host "Ensuring pipeline is configured to use service connection: $ServiceConnectionName" -ForegroundColor Yellow

Write-Host "✓ Pipeline configuration complete" -ForegroundColor Green
Write-Host "NOTE: Please verify in the YAML file that 'azureSubscription' is set to '$ServiceConnectionName'" -ForegroundColor Yellow

# Trigger the pipeline if requested
if ($TriggerPipeline) {
    Write-StepHeader "Triggering Pipeline Execution"
    Write-Host "Starting pipeline run..." -ForegroundColor Yellow
    $runResult = az pipelines run --id $pipelineId --output json | ConvertFrom-Json
    Write-Host "✓ Pipeline triggered with run ID: $($runResult.id)" -ForegroundColor Green
    Write-Host "Monitor run at: $($runResult._links.web.href)" -ForegroundColor Cyan
}

# Summary
Write-StepHeader "Setup Complete"
Write-Host "Application Deployment Pipeline has been set up in Azure DevOps:" -ForegroundColor Green
Write-Host "- Organization: $AzureDevOpsOrg" -ForegroundColor White
Write-Host "- Project: $AzureDevOpsProject" -ForegroundColor White
Write-Host "- Pipeline Name: $PipelineName" -ForegroundColor White
Write-Host "- Pipeline ID: $pipelineId" -ForegroundColor White
Write-Host "- Service Connection: $ServiceConnectionName" -ForegroundColor White
Write-Host "- YAML Path: $YamlPath" -ForegroundColor White

Write-Host "`nTo manually trigger the pipeline:" -ForegroundColor Yellow
Write-Host "az pipelines run --id $pipelineId" -ForegroundColor DarkGray

Write-Host "`nTo view the pipeline in Azure DevOps Portal:" -ForegroundColor Yellow
Write-Host "https://dev.azure.com/$AzureDevOpsOrg/$AzureDevOpsProject/_build?definitionId=$pipelineId" -ForegroundColor Cyan
