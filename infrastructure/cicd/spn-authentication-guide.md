# Service Principal Authentication Guide for Azure DevOps

This guide explains how to set up Service Principal authentication for your Azure DevOps pipeline to deploy resources to Azure.

## What is a Service Principal?

A Service Principal is an identity created for use with applications, hosted services, and automated tools to access Azure resources. This identity is used by the pipeline to authenticate to Azure and deploy resources.

## Prerequisites

To set up Service Principal authentication, you need:

- Azure subscription with contributor access
- Azure DevOps project with permissions to create pipelines and variable groups

## Step 1: Create a Variable Group

1. Navigate to **Pipelines** > **Library** in Azure DevOps
2. Click **+ Variable group**
3. Set the name to `ServicePrincipalCredentials`
4. Add the following variables:
   - **ARM_CLIENT_ID**: The Service Principal Client ID
   - **ARM_TENANT_ID**: The Azure AD Tenant ID
   - **ARM_CLIENT_SECRET**: The Service Principal Secret (mark as secret)
   - **ARM_SUBSCRIPTION_ID**: Your Azure Subscription ID
5. Check **Allow access to all pipelines**
6. Click **Save**

## Step 2: Create Service Connection Manually

1. Go to **Project Settings** > **Service connections**
2. Click **New service connection**
3. Select **Azure Resource Manager**
4. Choose **Service principal (manual)**
5. Fill in the Service Principal details:
   - **Subscription ID**: Your Azure subscription ID
   - **Subscription Name**: A descriptive name
   - **Service Principal ID**: The Client ID
   - **Service Principal Key**: The Secret Value
   - **Tenant ID**: The Tenant ID
6. Set the connection name to `Azure Subscription`
7. Check **Grant access permission to all pipelines**
8. Click **Verify and save**

## Step 3: Create Pipeline Using YAML File

1. Navigate to **Pipelines** > **Pipelines**
2. Click **New pipeline**
3. Select **Azure Repos Git**
4. Select your repository
5. Choose **Existing Azure Pipelines YAML file**
6. Path: `/infrastructure/cicd/deployment-pipeline.yml`
7. Click **Continue**
8. Click **Save**

## Step 4: Link Variable Group to Pipeline

1. Edit your pipeline
2. Click the three dots (...) > **Variables**
3. Go to the **Variable groups** tab
4. Click **Link variable group**
5. Select your `ServicePrincipalCredentials` variable group
6. Click **Link**
7. Click **Save**

## Step 5: Run the Pipeline

1. Navigate to the pipeline in Azure DevOps
2. Click **Run pipeline**
3. Select the branch (main)
4. Click **Run**

## Best Practices for Service Principal Security

1. **Least Privilege**: Assign only the permissions needed to the Service Principal
2. **Secret Rotation**: Regularly rotate the Service Principal secret
3. **Monitoring**: Enable audit logging for the Service Principal
4. **Secret Storage**: Always store secrets in variable groups or key vaults, never in code

## Troubleshooting

If you encounter authentication issues:

1. Verify the Service Principal has the required permissions
2. Check that the variable values are correct
3. Ensure the Service Principal is active and not expired
4. Verify that the pipeline has access to the variable group

## Additional Resources

- [Azure DevOps Documentation](https://docs.microsoft.com/en-us/azure/devops/)
- [Azure Service Principal Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)
- [Terraform Azure Provider Authentication](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_client_secret)
