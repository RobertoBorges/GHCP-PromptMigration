# Azure DevOps Infrastructure Deployment Guide

This guide outlines the process for deploying the infrastructure for the StoreApp using Azure DevOps Pipelines and Terraform. The deployment follows the Cloud Management Framework (CMF) Tenant Naming conventions.

## Prerequisites

1. Azure DevOps project with repository access
2. Azure subscription
3. Service Principal with Contributor rights on the subscription
4. Permission to create resources in Azure

## Step 1: Set Up Terraform Backend Storage

The Terraform backend has been successfully set up with the following configuration:

- **Resource Group**: `rg-infra-app-emea-vpmamidi-demo`
- **Storage Account**: `contosotfdwus01`
- **Container**: `tfstate`
- **State Key**: `storeapp-dev.tfstate`

If you need to set up the backend again, you can use the provided script:

```powershell
# Navigate to the terraform directory
cd infrastructure/terraform

# Run the setup script with the proper parameters
.\setup-terraform-backend.ps1 -Environment dev -Location westus -ProjectName storeapp -OrganizationPrefix contoso -Offering infra -FactoryRegion emea -Purpose demo -CustomerName Contoso -Tower AppMod
```
./setup-terraform-backend.ps1 -Environment dev -Location eastus -ProjectName storeapp -OrganizationPrefix contoso
```

This script will:
- Create a resource group following CMF naming conventions
- Create a storage account for Terraform state
- Create a blob container for state files
- Generate a backend.tfvars file for Terraform initialization
- Output variable values needed for Azure DevOps variable groups

## Step 2: Set Up Azure DevOps Variable Groups

Create two variable groups in Azure DevOps:

### 1. AzureServicePrincipal

This group should contain:
- `ARM_CLIENT_ID`: Service Principal client ID
- `ARM_CLIENT_SECRET`: Service Principal client secret (mark as secret)
- `ARM_TENANT_ID`: Azure tenant ID
- `ARM_SUBSCRIPTION_ID`: Azure subscription ID

### 2. TerraformConfig

This group should contain the following values for the Terraform backend:
- `TF_STATE_RESOURCE_GROUP_NAME`: rg-infra-app-emea-vpmamidi-demo
- `TF_STATE_STORAGE_ACCOUNT_NAME`: contosotfdwus01
- `TF_STATE_CONTAINER_NAME`: tfstate
- `TF_STATE_KEY`: storeapp-dev.tfstate

## Step 3: Create Service Connection

1. In Azure DevOps, go to Project Settings > Service connections
2. Create a new Azure Resource Manager service connection
3. Name it `azure-service-connection`
4. Select your Azure subscription
5. Use Service Principal authentication
6. Allow all pipelines to use this connection

## Step 4: Create Azure DevOps Pipeline

1. Go to Pipelines > Pipelines
2. Create a new pipeline
3. Select your repository
4. Choose "Existing Azure Pipelines YAML file"
5. Select `/infrastructure/cicd/cicd-pipeline.yml`
6. Save and run the pipeline

## Step 5: Deploy Infrastructure

The pipeline will execute the following stages:

1. **CI Stage**: Build and validate code
2. **Validate Infrastructure**: Run Terraform validation
3. **Deploy to Development**: Deploy infrastructure to Dev environment
4. **Deploy to Production**: Deploy infrastructure to Prod environment (with approval)

## Naming Convention

This deployment follows the Cloud Management Framework (CMF) Tenant Naming convention:

- Format: `<org>-<resource-type>-<app/service>-<environment>-<region>-<instance>`
- Example: `contoso-app-storeapp-d-eus-01`

### Resource Type Abbreviations:
- Resource Group: No abbreviation
- App Service Plan: `plan`
- App Service: `app`
- Application Insights: `appi`
- Storage Account: `st` (with restrictions on special characters)

### Environment Abbreviations:
- Development: `d`
- Test: `t`
- QA: `q`
- UAT: `u`
- Production: `p`

### Region Abbreviations:
- East US: `eus`
- West US: `wus`
- North Europe: `neu`
- West Europe: `weu`
- East Asia: `eas`
- Southeast Asia: `seas`

## Terraform Files

- **main.tf**: Main infrastructure configuration
- **variables.tf**: Variable definitions
- **outputs.tf**: Output values from deployment
- **terraform.tfvars**: Variable values
- **setup-terraform-backend.ps1**: Script to set up Terraform backend

## Customization

To customize the deployment:

1. Edit `terraform.tfvars` to change the organization prefix, app name, etc.
2. Update `variables.tf` if new variables are needed
3. Modify `main.tf` to add or change resources

## Troubleshooting

If the deployment fails:

1. Check the pipeline logs for error messages
2. Verify the Service Principal has appropriate permissions
3. Ensure the variable groups contain the correct values
4. Check that the Terraform backend storage is correctly configured
5. Validate Terraform files locally before running the pipeline

For resource-specific errors, refer to the Azure documentation for those resources.
