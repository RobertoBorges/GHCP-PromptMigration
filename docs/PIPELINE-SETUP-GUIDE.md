# Azure DevOps Pipeline Setup Guide

## Prerequisites

Before running the pipeline, you need to set up the following components in your Azure DevOps organization:

## 1. Install Required Extensions

Your pipeline is using Terraform tasks that need to be installed from the Azure DevOps Marketplace:

1. Go to the [Azure DevOps Marketplace](https://marketplace.visualstudio.com/azuredevops)
2. Search for "Terraform" by Microsoft DevLabs
3. Install the following extensions:
   - **Terraform by Microsoft DevLabs** - This extension includes the `TerraformInstaller` task
   - **Terraform Tasks for Azure Pipelines** - This extension includes the `TerraformTaskV4` tasks

## 2. Create Required Environments

Your pipeline references environments that don't exist yet. You need to create:

1. **Dev Environment**
   - Go to Azure DevOps project > Pipelines > Environments
   - Click "New environment"
   - Enter "Dev" as the name
   - Select "None" for Resource (unless you want to link to a Kubernetes cluster)
   - Click "Create"

2. **Prod Environment**
   - Go to Azure DevOps project > Pipelines > Environments
   - Click "New environment"
   - Enter "Prod" as the name
   - Select "None" for Resource
   - Click "Create"
   - Optionally: Add approval checks for this environment under "Approvals and checks"

## 3. Configure Variable Groups

Ensure you have created the required variable groups:

1. **AzureServicePrincipal** variable group with:
   - ARM_CLIENT_ID
   - ARM_CLIENT_SECRET
   - ARM_TENANT_ID
   - ARM_SUBSCRIPTION_ID

2. **TerraformConfig** variable group with:
   - TF_STATE_RESOURCE_GROUP_NAME
   - TF_STATE_STORAGE_ACCOUNT_NAME
   - TF_STATE_CONTAINER_NAME
   - TF_STATE_KEY

## 4. Create Service Connection

Ensure you have a service connection named "azure-service-connection":

1. Go to Project Settings > Service connections
2. Create a new service connection of type "Azure Resource Manager"
3. Name it "azure-service-connection"
4. Select the appropriate subscription and resource group

## 5. Running the Pipeline

After completing the above steps:

1. Go to Pipelines > Pipelines
2. Create a new pipeline if you haven't already
3. Select your repository
4. Select "Existing Azure Pipelines YAML file"
5. Browse to `/infrastructure/cicd/cicd-pipeline.yml`
6. Click "Continue"
7. Review the pipeline and click "Run"

## Troubleshooting

If you encounter errors related to Terraform tasks:
- Make sure the extensions are installed at the organization level
- Verify that your Azure DevOps project has access to the extensions
- Try refreshing your pipeline editor page

If you encounter errors related to environments:
- Make sure the environment names match exactly what's in the pipeline
- Check that your user has permission to access these environments

For service connection issues:
- Verify the service principal has appropriate permissions
- Make sure the service connection name matches what's used in the pipeline
