# Azure DevOps Pipeline Setup Guide

This guide provides step-by-step instructions for setting up the CI/CD pipeline in Azure DevOps for the StoreApp application.

## Prerequisites

Before beginning, ensure you have:

- Access to an Azure DevOps organization and project
- Access to an Azure subscription with permissions to create resources
- The application code pushed to Azure Repos (completed)

## Step 1: Create Resource Group and Storage for Terraform State

Run the following commands to create resources for Terraform state management:

```powershell
# Login to Azure
az login

# Create resource group
az group create --name terraform-state-rg --location eastus

# Create storage account (name must be globally unique)
az storage account create --name storeappterraformstate --resource-group terraform-state-rg --location eastus --sku Standard_LRS

# Create container
az storage container create --name tfstate --account-name storeappterraformstate
```

## Step 2: Create a Service Connection in Azure DevOps

1. Go to your Azure DevOps project
2. Navigate to **Project Settings** > **Service connections**
3. Click **New service connection**
4. Select **Azure Resource Manager**
5. Choose **Service principal (automatic)**
6. Select your **Subscription**
7. Name it: **Azure Subscription**
8. Check **Grant access permission to all pipelines**
9. Click **Save**

## Step 3: Create Variable Group for Terraform Backend

1. Go to **Pipelines** > **Library**
2. Click **+ Variable group**
3. Name it: **TerraformBackend**
4. Add the following variables:
   - **TF_BACKEND_RG**: `terraform-state-rg`
   - **TF_BACKEND_STORAGE**: `storeappterraformstate`
   - **TF_BACKEND_CONTAINER**: `tfstate`
5. Click **Save**

## Step 4: Create Environments

1. Go to **Pipelines** > **Environments**
2. Click **New environment**
3. Name: **Dev**
4. Resource: **None**
5. Click **Create**
6. Repeat for **Test** and **Prod** environments

### Add Approval Requirements (Optional)

For Test and Prod environments:

1. Select the environment
2. Click **Approvals and checks**
3. Click **Approvals**
4. Add required approvers
5. Set minimum number of approvers
6. Click **Create**

## Step 5: Create the Pipeline

1. Go to **Pipelines** > **Pipelines**
2. Click **New pipeline**
3. Select **Azure Repos Git** as your code location
4. Select your repository
5. Choose **Existing Azure Pipelines YAML file**
6. Path: **/infrastructure/cicd/azure-pipelines.yml**
7. Click **Continue**
8. Review the pipeline and click **Save**

## Step 6: Run the Pipeline

1. Go to **Pipelines** > **Pipelines**
2. Select your pipeline
3. Click **Run pipeline**
4. Select the branch (main)
5. Click **Run**

## Step 7: Monitor the Pipeline Execution

1. Watch the pipeline execution
2. Review each stage and job
3. Check logs for any errors

## Step 8: Verify Deployment

After the pipeline completes:

1. Go to the Azure portal
2. Check the created resources
3. Verify that the application is running correctly
4. Check Application Insights for telemetry

## Troubleshooting

If you encounter issues, refer to:

- **Pipeline Logs**: Check detailed logs for each job
- **Azure DevOps Quick Reference**: See `infrastructure/cicd/azure-devops-quick-reference.md`
- **Customization Guide**: See `infrastructure/cicd/azure-devops-customization.md`

## Additional Resources

- [Azure DevOps Documentation](https://docs.microsoft.com/en-us/azure/devops/)
- [Azure Pipelines Tasks](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
