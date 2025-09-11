# Creating an Azure DevOps Pipeline for StoreApp Deployment

This guide provides detailed steps to create a pipeline in Azure DevOps that will build, test, and deploy the StoreApp application and its associated infrastructure to Azure.

## Prerequisites

- Azure DevOps account with access to the project
- Azure subscription with required permissions
- Resource group and storage account for Terraform state (already created)

## Step 1: Access Azure DevOps Pipelines

1. Open a web browser and navigate to: `https://dev.azure.com/learnadoz/ghcpnew/_build`
2. Sign in with your Azure DevOps credentials if prompted

## Step 2: Create a New Pipeline

1. Click the **New pipeline** button in the top right corner
2. On the "Where is your code?" page, select **Azure Repos Git**
3. Select the repository **ghcp** (which contains your migrated application)
4. On the "Configure your pipeline" page, select **Existing Azure Pipelines YAML file**
5. In the path selector, navigate to `/infrastructure/cicd/azure-pipelines.yml`
6. Click **Continue**
7. Review the pipeline YAML content
8. Click **Save and run** to create the pipeline and start the first run

## Step 3: Create Variable Group for Terraform Backend

Before the pipeline can run successfully, you need to create a variable group with Terraform backend configuration:

1. Navigate to **Pipelines > Library** in Azure DevOps
2. Click **+ Variable group**
3. Set the name to `TerraformBackend`
4. Add the following variables:
   - **TF_BACKEND_RG**: `rg-terraform-state` (the resource group name for Terraform state)
   - **TF_BACKEND_STORAGE**: `tfstate53980` (the storage account name for Terraform state)
   - **TF_BACKEND_CONTAINER**: `tfstate` (the container name for Terraform state)
5. Click **Save**

## Step 4: Create Required Environments

The pipeline requires environments to be defined in Azure DevOps:

1. Navigate to **Pipelines > Environments**
2. Click **New environment**
3. Name: `Dev`
4. Resource: `None`
5. Click **Create**
6. Repeat the process to create a `Test` environment (optional)
7. Repeat the process to create a `Prod` environment (optional)

## Step 5: Create Service Connection

The pipeline needs a service connection to access Azure resources:

1. Navigate to **Project Settings > Service connections**
2. Click **New service connection**
3. Select **Azure Resource Manager**
4. Choose **Service principal (automatic)**
5. Select your **Subscription**
6. Resource Group: Leave blank to allow access to all resource groups
7. Service connection name: `Azure Subscription`
8. Check **Grant access permission to all pipelines**
9. Click **Save**

## Step 6: Run the Pipeline

Now that you have set up all the prerequisites, you can run the pipeline:

1. Navigate to **Pipelines > Pipelines**
2. Select your newly created pipeline
3. Click **Run pipeline**
4. Select the **main** branch
5. Click **Run**

## Monitoring the Pipeline

As the pipeline runs, you can monitor its progress:

1. The **Build** stage will compile, test, and publish the application
2. The **Validate Infrastructure** stage will validate the Terraform configuration
3. The **Deploy_Dev** stage will:
   - Deploy the infrastructure using Terraform
   - Deploy the application to the Azure App Service

## Troubleshooting

If the pipeline fails, check the following:

1. **Service Connection**: Ensure the service connection is working correctly and has the necessary permissions
2. **Variable Group**: Verify the TerraformBackend variable group exists with the correct values
3. **Environments**: Confirm that the Dev environment exists
4. **Repository Access**: Make sure the pipeline has access to the repository

## Next Steps

After successful deployment:

1. Access your application at the URL provided in the pipeline output
2. Verify that all resources have been correctly created in Azure
3. Consider setting up approval checks for Test and Prod environments if needed

## Additional Resources

For more information, refer to:
- `infrastructure/cicd/azure-devops-setup-guide.md`
- `infrastructure/cicd/azure-devops-quick-reference.md`
- `infrastructure/cicd/azure-devops-customization.md`
