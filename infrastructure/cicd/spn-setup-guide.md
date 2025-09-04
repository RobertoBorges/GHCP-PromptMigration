# Setting Up Azure DevOps Pipeline with Service Principal Authentication

This guide will help you set up your Azure DevOps pipeline using the Service Principal (SPN) credentials for authentication to Azure.

## Prerequisites

- Azure DevOps project with permissions to create pipelines and variable groups
- The Service Principal information (provided below)

## Service Principal (SPN) Information

We have a Service Principal with the following details:

- **SPN Name**: ghcp
- **Application / Client ID**: [CLIENT_ID] <!-- Replace with the actual Client ID -->
- **Object ID**: [OBJECT_ID] <!-- Replace with the actual Object ID -->
- **Tenant ID**: [TENANT_ID] <!-- Replace with the actual Tenant ID -->
- **Secret Value**: [SECRET_VALUE] <!-- Replace with the actual Secret Value -->
- **Secret ID**: [SECRET_ID] <!-- Replace with the actual Secret ID -->

## Step 1: Create a Variable Group for SPN Credentials

1. Go to **Pipelines** > **Library** in Azure DevOps
2. Click **+ Variable group**
3. Name it: `ServicePrincipalCredentials`
4. Add the following variables:
   - **ARM_CLIENT_ID**: `[CLIENT_ID]` <!-- Replace with the actual Client ID -->
   - **ARM_TENANT_ID**: `[TENANT_ID]` <!-- Replace with the actual Tenant ID -->
   - **ARM_CLIENT_SECRET**: `[SECRET_VALUE]` (Mark as secret) <!-- Replace with the actual Secret Value -->
   - **AZURE_SUBSCRIPTION_ID**: Your Azure subscription ID (need to be provided)
5. Check **Allow access to all pipelines**
6. Click **Save**

## Step 2: Create the Service Connection

1. Go to **Project Settings** > **Service connections**
2. Click **New service connection**
3. Select **Azure Resource Manager**
4. Choose **Service principal (manual)**
5. Fill in the information:
   - **Subscription ID**: Your Azure subscription ID
   - **Subscription Name**: Any descriptive name for your subscription
   - **Service Principal ID**: `[CLIENT_ID]` <!-- Replace with the actual Client ID -->
   - **Service Principal Key**: `[SECRET_VALUE]` <!-- Replace with the actual Secret Value -->
   - **Tenant ID**: `[TENANT_ID]` <!-- Replace with the actual Tenant ID -->
   - **Service connection name**: `Azure Subscription`
6. Check **Grant access permission to all pipelines**
7. Click **Verify and save**

## Step 3: Create the Pipeline

1. Go to **Pipelines** > **Pipelines**
2. Click **New pipeline**
3. Select **Azure Repos Git**
4. Select your repository
5. Choose **Existing Azure Pipelines YAML file**
6. Path: `/infrastructure/cicd/azure-pipelines-spn.yml`
7. Click **Continue**
8. Click **Save** to save the pipeline

## Step 4: Link the Variable Group to the Pipeline

1. Go to **Pipelines** > **Pipelines**
2. Select your pipeline
3. Click **Edit**
4. Click the three dots (...) in the top right corner
5. Select **Variables**
6. In the **Variable groups** tab, click **Link variable group**
7. Select the `ServicePrincipalCredentials` variable group
8. Click **Link**
9. Click **Save**

## Step 5: Run the Pipeline

1. Go back to the pipeline view
2. Click **Run pipeline**
3. Select the branch (main)
4. Click **Run**

## Important Notes:

1. **Security**: The Service Principal secret is sensitive information and should be treated as such. It is automatically marked as a secret in Azure DevOps.

2. **Permission Requirements**: The Service Principal needs the following permissions:
   - Contributor access to the subscription or resource group for deploying resources
   - Storage Blob Data Contributor for accessing Terraform state

3. **Troubleshooting**:
   - If you encounter authentication issues, verify that the Service Principal has the required permissions
   - Check the pipeline logs for detailed error messages
   - Ensure the secret hasn't expired

4. **Rotation**: Periodically rotate the Service Principal secret for security best practices

## For Local Development

If you want to use the same Service Principal for local development, set the following environment variables:

```powershell
$env:ARM_CLIENT_ID = "[CLIENT_ID]" <!-- Replace with the actual Client ID -->
$env:ARM_TENANT_ID = "[TENANT_ID]" <!-- Replace with the actual Tenant ID -->
$env:ARM_CLIENT_SECRET = "[SECRET_VALUE]" <!-- Replace with the actual Secret Value -->
$env:ARM_SUBSCRIPTION_ID = "<your-subscription-id>"
```

Then run your Terraform commands as usual. The authentication will use these environment variables.
