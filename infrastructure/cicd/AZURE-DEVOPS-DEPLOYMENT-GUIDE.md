# Deploying Your Application to Azure DevOps - Step by Step Guide

This guide will walk you through the process of setting up CI/CD for your migrated applications in Azure DevOps.

## Prerequisites

- Azure DevOps account with permissions to create pipelines
- Azure subscription with necessary permissions
- Git repository with your migrated applications

## Step 1: Set Up an Azure Service Connection

1. Open your Azure DevOps project
2. Go to **Project Settings** (bottom left corner)
3. Select **Service connections** under Pipelines
4. Click **New service connection**
5. Select **Azure Resource Manager**
6. Choose **Service principal (automatic)**
7. Fill in the details:
   - Subscription: Select your Azure subscription
   - Resource Group: Leave empty to grant access to all resource groups
   - Service connection name: `Azure-Service-Connection`
   - Check **Grant access permission to all pipelines**
8. Click **Save**

## Step 2: Import the Azure DevOps Pipeline

1. In Azure DevOps, go to **Pipelines** > **Pipelines**
2. Click **New pipeline**
3. Select your repository location:
   - If using Azure Repos: Choose **Azure Repos Git**
   - If using GitHub: Choose **GitHub**
4. Select your repository containing the migrated applications
5. Select **Existing Azure Pipelines YAML file**
6. Enter the path: `/infrastructure/cicd/azure-devops-app-pipeline.yml`
7. Click **Continue**

## Step 3: Update Pipeline Variables (if needed)

The pipeline includes default variables, but you may need to update them to match your environment:

1. Go to the pipeline editor
2. Click **Variables** in the top-right corner
3. Verify or update the following variables:
   - `environment`: dev (or your target environment)
   - `location`: eastus (or your target region)
   - `offering`: infra
   - `subOffering`: winmig
   - `factoryRegion`: emea
   - `vId`: vpmamidi
   - `purpose`: demo
   - `resourceGroupName`: Should follow pattern rg-$(offering)-$(subOffering)-$(factoryRegion)-$(vId)-$(purpose)
   - `netFxAppName`: contoso-app-netframeworkwebapp-d-eus-01
   - `storeAppName`: contoso-app-storeapp-d-eus-01
4. Click **Save**

## Step 4: Create Azure Development Environment (Optional)

To add approvals for deployment:

1. Go to **Environments** under Pipelines
2. Click **New environment**
3. Name it `Development`
4. Click **Create**
5. Go to the environment's settings
6. Add approvals or checks if desired

## Step 5: Run the Pipeline

1. Navigate to your pipeline
2. Click **Run pipeline**
3. Select the branch to build
4. Click **Run**

## Step 6: Monitor Deployment Progress

1. Watch the pipeline execution in real-time
2. The pipeline will:
   - Build both applications (NetFrameworkWebApp and StoreApp)
   - Publish build artifacts
   - Deploy to Azure App Services

## Step 7: Verify Deployment

After successful deployment:

1. Access your applications at:
   - NetFrameworkWebApp: https://contoso-app-netframeworkwebapp-d-eus-01.azurewebsites.net
   - StoreApp: https://contoso-app-storeapp-d-eus-01.azurewebsites.net
2. Test key functionality in both applications
3. Check Application Insights for telemetry

## Troubleshooting Common Issues

### Build Failures

- Ensure source code is properly structured
- Check that .NET SDK version is compatible (8.0.x)
- Verify all project references and NuGet packages are available

### Deployment Failures

- Verify Azure App Services exist and are properly named
- Check that the resource group exists
- Verify service connection has proper permissions
- Check Azure Policy compliance (tags, naming conventions)

### Policy Restrictions

If facing Azure policy restrictions:

1. Ensure tags in your Terraform configuration follow proper capitalization:
   ```hcl
   common_tags = {
     "Created By"    = var.v_id
     "Created On"    = local.current_date
     "Customer Name" = var.customer_name
     "Purpose"       = var.purpose
     "Region"        = var.factory_region
     "Tower"         = var.tower
     "V-ID"          = var.v_id
   }
   ```

2. Verify resource naming follows convention:
   - Resource Group: `rg-infra-winmig-emea-vpmamidi-demo`
   - App Service: `contoso-app-netframeworkwebapp-d-eus-01`

## Next Steps

After successful deployment:

1. Set up monitoring and alerts
2. Configure automated testing in the pipeline
3. Implement release gates for production deployment
4. Configure blue-green deployment strategy for zero-downtime updates
