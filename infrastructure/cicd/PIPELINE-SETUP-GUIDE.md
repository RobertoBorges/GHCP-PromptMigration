# Azure DevOps Pipeline Setup Guide
# Use this guide to set up your Azure DevOps pipeline for infrastructure deployment

## Prerequisites

1. **Azure DevOps Project** - You need an Azure DevOps project where you'll set up the pipeline.
2. **Azure Service Connection** - A service connection named `azure-service-connection` that allows Azure DevOps to deploy resources to your Azure subscription.
3. **Variable Groups** - Two variable groups need to be set up in Azure DevOps Library:

## Step 1: Set up Variable Groups in Azure DevOps

### Variable Group 1: AzureServicePrincipal
Create a variable group named "AzureServicePrincipal" with the following variables (make sure to mark them as secret):
- ARM_CLIENT_ID: Your service principal client ID
- ARM_CLIENT_SECRET: Your service principal client secret
- ARM_TENANT_ID: Your Azure tenant ID
- ARM_SUBSCRIPTION_ID: Your Azure subscription ID

### Variable Group 2: TerraformConfig
Create a variable group named "TerraformConfig" with the following variables:
- TF_STATE_RESOURCE_GROUP_NAME: rg-infra-app-emea-vpmamidi-demo
- TF_STATE_STORAGE_ACCOUNT_NAME: contosotfdwus01
- TF_STATE_CONTAINER_NAME: tfstate
- TF_STATE_KEY: storeapp-dev.tfstate

## Step 2: Create Azure Service Connection
1. In Azure DevOps project settings, go to "Service connections"
2. Create a new Azure Resource Manager service connection
3. Name it "azure-service-connection"
4. Use service principal authentication
5. Enter your subscription ID, tenant ID, service principal ID and secret
6. Ensure the service principal has proper permissions on the subscription
7. Grant access permission to all pipelines

## Pipeline Options

There are two pipeline options available:

1. **Standard Pipeline (`cicd-pipeline.yml`)** - Uses Terraform extension tasks, which requires installing extensions from the Azure DevOps Marketplace.
2. **Simplified Pipeline (`cicd-pipeline-simplified.yml`)** - Uses Azure CLI tasks to run Terraform commands, which doesn't require additional extensions.

## Step 3: Import Pipeline

### Option 1: Using the Simplified Pipeline (Recommended)

1. **Create a new pipeline in Azure DevOps**:
   - Go to Pipelines > Pipelines
   - Click "Create Pipeline" or "New Pipeline"
   - Select your repository source (Azure Repos Git, GitHub, etc.)
   - Select your repository
   - Choose "Existing Azure Pipelines YAML file"
   - Browse to `/infrastructure/cicd/cicd-pipeline-simplified.yml`
   - Review the pipeline and click "Run"

### Option 2: Using the Standard Pipeline with Extensions

1. **Install the required extensions**:
   - Go to the Azure DevOps Marketplace: https://marketplace.visualstudio.com
   - Search for and install the following extensions:
     - "Terraform" by Microsoft DevLabs (provides TerraformInstaller and TerraformTaskV4 tasks)

2. **Create environments**:
   - Go to Pipelines > Environments
   - Create "Dev" and "Prod" environments
   - Configure approval checks if needed

3. **Import the pipeline**:
   - Follow the same steps as Option 1, but select `/infrastructure/cicd/cicd-pipeline.yml` as the YAML file

## Step 4: Monitor Pipeline Execution
1. The pipeline will run with the following stages:
   - CI: Build and test the application
   - Validate Infrastructure: Check Terraform configurations
   - Deploy to Development: Deploy infrastructure and application to dev environment
   - Deploy to Production: Deploy to production (with approval)
2. Monitor each stage and review logs for any issues

## Step 5: Verify Deployment
1. After successful deployment, check the Azure Portal to verify:
   - Resource group is created with proper naming convention
   - App Service and other resources are created correctly
   - Application is deployed and running

## Troubleshooting

If you encounter errors:

1. **Missing tasks** - Install the required extensions from the Azure DevOps Marketplace or use the simplified pipeline
2. **Missing environments** - Create the required environments or use the simplified pipeline
3. **Authentication errors** - Verify the service connection is configured correctly and has the necessary permissions
4. **Variable errors** - Ensure all required variables are defined in the variable groups
5. **Terraform backend issues** - Verify storage account access and container existence
6. **Deployment failures** - Check Terraform logs for specific error messages
