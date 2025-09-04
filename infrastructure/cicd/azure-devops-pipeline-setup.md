# Azure DevOps Pipeline Setup Guide

The pipeline has been created in Azure DevOps, but there are a few additional steps needed to complete the setup:

## 1. Configure Service Principal Variables

Go to the **Library** section in Azure DevOps and update the **AzureServicePrincipal** variable group with your Service Principal credentials:

- `ARM_CLIENT_ID`: Your Service Principal Client ID
- `ARM_CLIENT_SECRET`: Your Service Principal Client Secret (mark as secret)
- `ARM_SUBSCRIPTION_ID`: Your Azure Subscription ID
- `ARM_TENANT_ID`: Your Azure Tenant ID

## 2. Configure Terraform State Storage Variables

Update the **TerraformConfig** variable group with your Terraform state storage configuration:

- `TF_STATE_RESOURCE_GROUP_NAME`: The resource group name for Terraform state
- `TF_STATE_STORAGE_ACCOUNT_NAME`: The storage account name for Terraform state
- `TF_STATE_CONTAINER_NAME`: The container name for Terraform state
- `TF_STATE_KEY`: The key for the Terraform state file (e.g., "asp-net-core.tfstate")

## 3. Create an Azure Resource Manager Service Connection

1. Go to **Project Settings > Service connections**
2. Click **New service connection**
3. Select **Azure Resource Manager**
4. Choose **Service Principal (automatic)** or **Service Principal (manual)** based on your preference
5. Fill in the required information
6. Name the connection `azure-service-connection` (this name is referenced in the pipeline)
7. Check **Grant access permission to all pipelines**
8. Click **Save**

## 4. Run the Pipeline

Once you've completed the above steps:

1. Go to **Pipelines**
2. Select your **Deployment Pipeline**
3. Click **Run pipeline**
4. Select the **pipeline-branch** branch
5. Click **Run**

## Troubleshooting

If you encounter any issues:

1. Check the pipeline logs for specific error messages
2. Verify that your Service Principal has the necessary permissions on your Azure subscription
3. Ensure that the Terraform state storage account exists and is accessible
4. Check that your pipeline YAML is correctly referencing the variable groups and service connection

## Next Steps

After a successful deployment:

1. Verify the resources in your Azure Portal
2. Validate that your application is running correctly
3. Set up branch policies to control when the pipeline runs
4. Consider implementing additional environments (Dev, Test, Prod)
