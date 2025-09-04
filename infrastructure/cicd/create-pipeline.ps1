# PowerShell script for creating an Azure DevOps pipeline for infrastructure and application deployment

Write-Host "Creating Azure DevOps pipeline for infrastructure and application deployment..." -ForegroundColor Green

# Variables for the pipeline
$pipelineName = "StoreApp-Deployment-Pipeline"
$yamlFilePath = "infrastructure/cicd/azure-pipelines.yml"
$projectName = "ghcp"
$organization = "learnadoz"
$repositoryName = "ghcp"

# Function to check if command is available
function Test-CommandExists {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $command) { return $true }
    }
    catch { return $false }
    finally { $ErrorActionPreference = $oldPreference }
}

# Check if Azure CLI and Azure DevOps extension are installed
if (-not (Test-CommandExists az)) {
    Write-Host "Azure CLI is not installed. Please install it from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Check if Azure DevOps extension is installed
$extensions = az extension list --query "[?name=='azure-devops'].name" -o tsv
if (-not $extensions -or -not $extensions.Contains("azure-devops")) {
    Write-Host "Installing Azure DevOps extension..." -ForegroundColor Yellow
    az extension add --name azure-devops --force
}

# Login to Azure
Write-Host "Logging into Azure..." -ForegroundColor Yellow
az login

# Configure Azure DevOps CLI defaults
Write-Host "Configuring Azure DevOps CLI defaults..." -ForegroundColor Yellow
az devops configure --defaults organization="https://dev.azure.com/$organization" project="$projectName"

# Create variable group for Terraform backend
$variableGroupName = "TerraformBackend"
$variableGroupExists = az pipelines variable-group list --query "[?name=='$variableGroupName'].name" -o tsv

if (-not $variableGroupExists) {
    Write-Host "Creating TerraformBackend variable group..." -ForegroundColor Yellow
    
    # Get the resource group name for Terraform state
    Write-Host "Checking for Terraform state resource group..." -ForegroundColor Yellow
    $terraformStateRG = az group list --query "[?contains(name, 'terraform-state')].name" -o tsv
    
    if (-not $terraformStateRG) {
        Write-Host "Terraform state resource group not found. Creating..." -ForegroundColor Yellow
        $terraformStateRG = "terraform-state-rg"
        az group create --name $terraformStateRG --location eastus
    }
    
    # Get the storage account for Terraform state
    Write-Host "Checking for Terraform state storage account..." -ForegroundColor Yellow
    $terraformStateStorage = az storage account list --resource-group $terraformStateRG --query "[0].name" -o tsv
    
    if (-not $terraformStateStorage) {
        Write-Host "Terraform state storage account not found. Creating..." -ForegroundColor Yellow
        $terraformStateStorage = "tfstate$(Get-Random -Minimum 10000 -Maximum 99999)"
        az storage account create --name $terraformStateStorage --resource-group $terraformStateRG --location eastus --sku Standard_LRS
    }
    
    # Get the container for Terraform state
    Write-Host "Checking for Terraform state container..." -ForegroundColor Yellow
    $terraformStateContainer = "tfstate"
    $containerExists = az storage container exists --account-name $terraformStateStorage --name $terraformStateContainer --query "exists" -o tsv
    
    if ($containerExists -ne "true") {
        Write-Host "Terraform state container not found. Creating..." -ForegroundColor Yellow
        az storage container create --name $terraformStateContainer --account-name $terraformStateStorage
    }
    
    # Create the variable group
    az pipelines variable-group create --name $variableGroupName --variables TF_BACKEND_RG=$terraformStateRG TF_BACKEND_STORAGE=$terraformStateStorage TF_BACKEND_CONTAINER=$terraformStateContainer
}

# Create environments if they don't exist
$environments = @("Dev", "Test", "Prod")
foreach ($env in $environments) {
    $envExists = az pipelines environments list --query "[?name=='$env'].name" -o tsv
    
    if (-not $envExists) {
        Write-Host "Creating $env environment..." -ForegroundColor Yellow
        az pipelines environments create --name $env
    }
}

# Create service connection if it doesn't exist
$serviceConnectionName = "Azure Subscription"
$serviceConnectionExists = az devops service-endpoint list --query "[?name=='$serviceConnectionName'].name" -o tsv

if (-not $serviceConnectionExists) {
    Write-Host "Service connection '$serviceConnectionName' not found." -ForegroundColor Yellow
    Write-Host "Please create a service connection in the Azure DevOps portal:" -ForegroundColor Yellow
    Write-Host "1. Go to Project Settings > Service connections" -ForegroundColor Yellow
    Write-Host "2. Click New service connection" -ForegroundColor Yellow
    Write-Host "3. Select Azure Resource Manager" -ForegroundColor Yellow
    Write-Host "4. Choose Service principal (automatic)" -ForegroundColor Yellow
    Write-Host "5. Name it 'Azure Subscription'" -ForegroundColor Yellow
    Write-Host "6. Check 'Grant access permission to all pipelines'" -ForegroundColor Yellow
    Write-Host "7. Click Save" -ForegroundColor Yellow
    
    # Wait for user to create the service connection
    Read-Host "Press Enter once you've created the service connection..."
}

# Create the pipeline
$pipelineExists = az pipelines list --query "[?name=='$pipelineName'].name" -o tsv

if (-not $pipelineExists) {
    Write-Host "Creating pipeline '$pipelineName'..." -ForegroundColor Yellow
    
    # Check if the YAML file exists in the repository
    $yamlFileExists = git ls-files $yamlFilePath

    if (-not $yamlFileExists) {
        Write-Host "YAML file '$yamlFilePath' not found in the repository. Please make sure the file exists." -ForegroundColor Red
        exit 1
    }
    
    # Create the pipeline
    az pipelines create --name $pipelineName --repository $repositoryName --repository-type tfsgit --yaml-path $yamlFilePath
}

# Run the pipeline
Write-Host "Pipeline setup complete. Would you like to run the pipeline now? (Y/N)" -ForegroundColor Green
$runPipeline = Read-Host

if ($runPipeline -eq "Y" -or $runPipeline -eq "y") {
    Write-Host "Running pipeline '$pipelineName'..." -ForegroundColor Yellow
    az pipelines run --name $pipelineName
}

Write-Host "Pipeline creation completed!" -ForegroundColor Green
Write-Host "You can view your pipeline at: https://dev.azure.com/$organization/$projectName/_build" -ForegroundColor Cyan
