# Manual Pipeline Creation for Azure DevOps

Since we're encountering permission issues with the Azure CLI, let's create the pipeline manually in the Azure DevOps portal.

## Step 1: Set Up Azure Resources for Terraform State

First, we need to ensure we have Azure resources for the Terraform state management. Open a PowerShell window as Administrator and run:

```powershell
# Login to Azure
az login

# Create resource group (if it doesn't exist)
$terraformStateRG = "terraform-state-rg"
az group create --name $terraformStateRG --location eastus

# Create storage account (if it doesn't exist)
$terraformStateStorage = "tfstate53980"  # This storage account already exists
az storage account create --name $terraformStateStorage --resource-group $terraformStateRG --location eastus --sku Standard_LRS

# Create container (if it doesn't exist)
$terraformStateContainer = "tfstate"
az storage container create --name $terraformStateContainer --account-name $terraformStateStorage --auth-mode login
```

## Step 2: Create Variable Group in Azure DevOps

1. Go to https://dev.azure.com/learnadoz/ghcp/_library?itemType=VariableGroups
2. Click **+ Variable group**
3. Name it: `TerraformBackend`
4. Add the following variables:
   - **TF_BACKEND_RG**: `terraform-state-rg`
   - **TF_BACKEND_STORAGE**: `tfstate53980`
   - **TF_BACKEND_CONTAINER**: `tfstate`
5. Click **Save**

## Step 3: Create Environments in Azure DevOps

1. Go to https://dev.azure.com/learnadoz/ghcp/_environments
2. Click **New environment**
3. Name: `Dev`
4. Resource: `None`
5. Click **Create**
6. Repeat for `Test` and `Prod` environments

## Step 4: Create Service Connection in Azure DevOps

1. Go to https://dev.azure.com/learnadoz/ghcp/_settings/adminservices
2. Click **New service connection**
3. Select **Azure Resource Manager**
4. Choose **Service principal (automatic)**
5. Select your **Subscription**
6. Resource Group: Leave blank to allow access to all resource groups
7. Service connection name: `Azure Subscription`
8. Check **Grant access permission to all pipelines**
9. Click **Save**

## Step 5: Create Pipeline in Azure DevOps

1. Go to https://dev.azure.com/learnadoz/ghcp/_build
2. Click **New pipeline**
3. Select **Azure Repos Git**
4. Select the repository **ghcp**
5. On the "Configure your pipeline" page, select **Existing Azure Pipelines YAML file**
6. Select the branch: `main`
7. Path: `/infrastructure/cicd/azure-pipelines.yml`
8. Click **Continue**
9. Review the pipeline YAML content
10. Click **Save** to save the pipeline
11. Rename the pipeline to `StoreApp-Deployment-Pipeline` (optional)

## Step 6: Run the Pipeline

1. Go to https://dev.azure.com/learnadoz/ghcp/_build
2. Select your newly created pipeline
3. Click **Run pipeline**
4. Select the **main** branch
5. Click **Run**

## Step 7: Monitor the Pipeline Execution

1. Watch the pipeline execution in the Azure DevOps portal
2. Review each stage and job
3. Check logs for any errors

## Step 8: Verify Deployment

After the pipeline completes:
1. Go to the Azure portal
2. Check the created resources in the specified resource group
3. Verify that the application is deployed and running correctly
4. Check the Application Insights for telemetry data
