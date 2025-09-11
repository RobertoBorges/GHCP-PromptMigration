# Configure-Pipeline-Trigger.ps1
# This script sets up a pipeline trigger configuration in Azure DevOps

param (
    [Parameter(Mandatory=$true)]
    [string]$AzureDevOpsOrg,
    
    [Parameter(Mandatory=$true)]
    [string]$AzureDevOpsProject,
    
    [Parameter(Mandatory=$true)]
    [string]$PipelineName = "Application-Deployment",
    
    [string]$BranchName = "pipeline-branch",
    
    [string]$YamlPath = "infrastructure/cicd/azure-devops-app-pipeline.yml",
    
    [switch]$ManualTriggerOnly = $false,
    
    [string]$WebhookUrl = ""
)

$ErrorActionPreference = "Stop"

# Function to display section headers
function Show-Header {
    param ([string]$Title)
    Write-Host "`n===== $Title =====" -ForegroundColor Cyan
}

# Check if Azure CLI and Azure DevOps extension are installed
Show-Header "Checking Prerequisites"

try {
    $azVersion = az --version
    Write-Host "✓ Azure CLI is installed: $($azVersion[0])" -ForegroundColor Green
}
catch {
    Write-Host "❌ Azure CLI is not installed. Please install it from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Check if Azure DevOps extension is installed
$azExtensions = az extension list --output json | ConvertFrom-Json
if (-not ($azExtensions | Where-Object { $_.name -eq "azure-devops" })) {
    Write-Host "Installing Azure DevOps extension..." -ForegroundColor Yellow
    az extension add --name azure-devops
    Write-Host "✓ Azure DevOps extension installed successfully" -ForegroundColor Green
}
else {
    Write-Host "✓ Azure DevOps extension is already installed" -ForegroundColor Green
}

# Configure Azure DevOps defaults
Show-Header "Configuring Azure DevOps"
Write-Host "Setting Azure DevOps organization: $AzureDevOpsOrg" -ForegroundColor Yellow
az devops configure --defaults organization="https://dev.azure.com/$AzureDevOpsOrg" project="$AzureDevOpsProject"

# Login to Azure DevOps
Show-Header "Logging in to Azure DevOps"
Write-Host "You may be prompted to login to Azure DevOps..." -ForegroundColor Yellow
az devops login

# Check if pipeline exists
Show-Header "Checking Pipeline"
$pipelines = az pipelines list --query "[?name=='$PipelineName']" --output json | ConvertFrom-Json
if ($pipelines.Count -eq 0) {
    Write-Host "Pipeline '$PipelineName' does not exist. Creating it now..." -ForegroundColor Yellow
    
    # Create pipeline
    az pipelines create --name $PipelineName --yml-path $YamlPath --branch $BranchName
    
    Write-Host "✓ Pipeline '$PipelineName' created successfully" -ForegroundColor Green
    
    # Get the newly created pipeline
    $pipelines = az pipelines list --query "[?name=='$PipelineName']" --output json | ConvertFrom-Json
}
else {
    Write-Host "✓ Pipeline '$PipelineName' already exists" -ForegroundColor Green
}

# Get pipeline ID
$pipelineId = $pipelines[0].id
Write-Host "Pipeline ID: $pipelineId" -ForegroundColor Yellow

# Configure pipeline trigger based on parameters
Show-Header "Configuring Pipeline Trigger"

if ($ManualTriggerOnly) {
    # Configure for manual triggers only
    Write-Host "Configuring pipeline for manual triggers only..." -ForegroundColor Yellow
    
    # Generate YAML content for manual trigger
    $triggerYaml = @"
trigger: none

pool:
  vmImage: 'windows-latest'

"@
    
    # Update the pipeline YAML to disable automatic triggers
    # Note: This is a simplified approach - in a real environment, you would modify the YAML file in the repo
    Write-Host "⚠️ Note: To fully disable automatic triggers, update the YAML file in your repository." -ForegroundColor Yellow
    Write-Host "Add 'trigger: none' at the top of your pipeline YAML file." -ForegroundColor Yellow
}
else {
    # Configure for branch-based trigger
    Write-Host "Configuring pipeline for automatic triggers on branch '$BranchName'..." -ForegroundColor Yellow
    
    # Generate YAML content for branch trigger
    $triggerYaml = @"
trigger:
  branches:
    include:
      - $BranchName

pool:
  vmImage: 'windows-latest'

"@
    
    # Update the pipeline YAML to enable automatic triggers
    # Note: This is a simplified approach - in a real environment, you would modify the YAML file in the repo
    Write-Host "⚠️ Note: To properly configure branch triggers, update the YAML file in your repository." -ForegroundColor Yellow
    Write-Host "Add the trigger configuration at the top of your pipeline YAML file." -ForegroundColor Yellow
}

# Set up webhook trigger if URL provided
if ($WebhookUrl) {
    Show-Header "Setting Up Webhook Trigger"
    Write-Host "Configuring webhook trigger for the pipeline..." -ForegroundColor Yellow
    
    # This is a placeholder - the actual webhook setup would require Azure DevOps REST API calls
    # which are beyond the scope of the Azure CLI tools
    Write-Host "⚠️ Webhook configuration requires Azure DevOps REST API calls." -ForegroundColor Yellow
    Write-Host "Please follow these manual steps:" -ForegroundColor Yellow
    Write-Host "1. Go to Azure DevOps > $AzureDevOpsProject > Pipelines > $PipelineName" -ForegroundColor White
    Write-Host "2. Click Edit > Triggers" -ForegroundColor White
    Write-Host "3. Enable 'Build completion' or 'Repository' webhooks" -ForegroundColor White
    Write-Host "4. Configure your webhook URL: $WebhookUrl" -ForegroundColor White
}

# Run the pipeline manually to verify setup
Show-Header "Triggering Pipeline"
Write-Host "Do you want to trigger the pipeline now? (Y/N)" -ForegroundColor Yellow
$triggerNow = Read-Host

if ($triggerNow -eq "Y" -or $triggerNow -eq "y") {
    Write-Host "Triggering pipeline run..." -ForegroundColor Yellow
    az pipelines run --id $pipelineId
    
    Write-Host "✓ Pipeline triggered successfully. Check the Azure DevOps portal for progress." -ForegroundColor Green
    Write-Host "Pipeline URL: https://dev.azure.com/$AzureDevOpsOrg/$AzureDevOpsProject/_build?definitionId=$pipelineId" -ForegroundColor Cyan
}
else {
    Write-Host "Pipeline not triggered. You can manually trigger it from the Azure DevOps portal." -ForegroundColor Yellow
    Write-Host "Pipeline URL: https://dev.azure.com/$AzureDevOpsOrg/$AzureDevOpsProject/_build?definitionId=$pipelineId" -ForegroundColor Cyan
}

Show-Header "Manual Pipeline Management"
Write-Host "Here are some useful commands for managing your pipeline:" -ForegroundColor Yellow
Write-Host "- Run the pipeline:" -ForegroundColor White
Write-Host "  az pipelines run --id $pipelineId" -ForegroundColor DarkGray
Write-Host "- Get pipeline details:" -ForegroundColor White
Write-Host "  az pipelines show --id $pipelineId" -ForegroundColor DarkGray
Write-Host "- List recent pipeline runs:" -ForegroundColor White
Write-Host "  az pipelines runs list --pipeline-id $pipelineId" -ForegroundColor DarkGray

Show-Header "Setup Complete"
Write-Host "Your pipeline is now configured in Azure DevOps." -ForegroundColor Green
