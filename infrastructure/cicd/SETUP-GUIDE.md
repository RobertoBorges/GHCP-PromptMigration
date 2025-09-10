# CI/CD Pipeline Setup Guide

This guide provides step-by-step instructions for setting up the CI/CD pipeline for the modernized StoreApp in Azure DevOps.

## Prerequisites

1. Azure DevOps project with the repository containing the modernized StoreApp
2. Azure subscription
3. Permissions to create service connections and variable groups in Azure DevOps
4. Permissions to create resources in Azure

## Step 1: Create Azure Service Connection

1. In Azure DevOps, go to **Project Settings** > **Service connections**
2. Click **New service connection** and select **Azure Resource Manager**
3. Choose **Service principal (automatic)** authentication
4. Select your subscription and resource group scope
5. Name the service connection `azure-service-connection`
6. Check **Allow all pipelines to use this connection** and click **Save**

## Step 2: Create Variable Groups

### Service Principal Variable Group

1. In Azure DevOps, go to **Pipelines** > **Library**
2. Click **+ Variable group**
3. Name the group `AzureServicePrincipal`
4. Add the following variables:
   - `ARM_CLIENT_ID`: The service principal client ID
   - `ARM_CLIENT_SECRET`: The service principal client secret (mark as secret)
   - `ARM_TENANT_ID`: Your Azure tenant ID
   - `ARM_SUBSCRIPTION_ID`: Your Azure subscription ID
5. Click **Save**

### Terraform Configuration Variable Group

1. In Azure DevOps, go to **Pipelines** > **Library**
2. Click **+ Variable group**
3. Name the group `TerraformConfig`
4. Add the following variables:
   - `TF_STATE_RESOURCE_GROUP_NAME`: Resource group for Terraform state
   - `TF_STATE_STORAGE_ACCOUNT_NAME`: Storage account for Terraform state
   - `TF_STATE_CONTAINER_NAME`: Container for Terraform state
   - `TF_STATE_KEY`: Key for the Terraform state file (e.g., `storeapp.tfstate`)
5. Click **Save**

## Step 3: Create Deployment Environments

1. In Azure DevOps, go to **Pipelines** > **Environments**
2. Click **New environment**
3. Name the environment `Dev` and select **None** for resources
4. Click **Create**
5. Repeat steps 2-4 to create a `Prod` environment
6. For the `Prod` environment, add approval gates:
   - Go to the environment and click on the three dots (...) > **Approvals and checks**
   - Click **+ Approval** and add approvers for the production deployment

## Step 4: Set Up Terraform State Backend

Before running the pipeline, you need to create a storage account for the Terraform state:

```powershell
# Set variables
$RESOURCE_GROUP_NAME="terraform-state-rg"
$STORAGE_ACCOUNT_NAME="tfstate$((Get-Random -Minimum 100000 -Maximum 999999))"
$CONTAINER_NAME="tfstate"
$LOCATION="eastus"

# Create resource group
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# Create storage account
az storage account create --resource-group $RESOURCE_GROUP_NAME --name $STORAGE_ACCOUNT_NAME --sku Standard_LRS --encryption-services blob

# Get storage account key
$ACCOUNT_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP_NAME --account-name $STORAGE_ACCOUNT_NAME --query [0].value -o tsv)

# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME --account-key $ACCOUNT_KEY

# Output the storage account name and container name
Write-Host "Storage Account Name: $STORAGE_ACCOUNT_NAME"
Write-Host "Container Name: $CONTAINER_NAME"
Write-Host "Resource Group Name: $RESOURCE_GROUP_NAME"
```

Update the `TerraformConfig` variable group with these values.

## Step 5: Create the Pipeline

1. In Azure DevOps, go to **Pipelines** > **Pipelines**
2. Click **New pipeline**
3. Select **Azure Repos Git** as the source
4. Select your repository
5. Select **Existing Azure Pipelines YAML file**
6. Select `/infrastructure/cicd/cicd-pipeline.yml` from the dropdown
7. Click **Continue**
8. Click **Run** to create and run the pipeline

## Pipeline Structure

The pipeline is structured in stages:

1. **CI Stage**:
   - Builds and tests the application
   - Publishes artifacts for deployment
   - Runs security scans

2. **Infrastructure Validation**:
   - Validates Terraform configuration

3. **Development Deployment**:
   - Deploys infrastructure to the Dev environment
   - Deploys the application to Azure App Service in Dev

4. **Production Deployment**:
   - Deploys infrastructure to the Prod environment
   - Deploys the application to Azure App Service in Prod

## Troubleshooting

- **Terraform Backend Issues**: Ensure the storage account exists and the variable group has the correct values
- **Service Connection Issues**: Verify the service connection has permissions to the Azure subscription
- **Build Failures**: Check the build logs for specific errors related to the application
- **Deployment Failures**: Check the deployment logs for specific errors related to infrastructure or application deployment

## Additional Resources

- [Azure DevOps Documentation](https://docs.microsoft.com/en-us/azure/devops/?view=azure-devops)
- [Terraform Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
