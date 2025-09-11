# Azure DevOps Portal Setup Guide

This document provides step-by-step instructions for setting up your application deployment pipeline directly in the Azure DevOps portal.

## Prerequisites

1. Azure DevOps account
2. Access to your Azure DevOps project
3. Repository with your migrated application code
4. Azure subscription for deploying resources

## Step 1: Create an Azure Service Connection

First, create a service connection to allow Azure DevOps to deploy to your Azure subscription:

1. In Azure DevOps, go to **Project Settings** (gear icon in the bottom left)
2. Select **Service connections** under Pipelines
3. Click **New service connection**
4. Select **Azure Resource Manager**
5. Choose **Service principal (automatic)** and click **Next**
6. Select your **Subscription** from the dropdown
7. Enter `Azure-Service-Connection` as the **Service connection name**
8. Check **Grant access permission to all pipelines**
9. Click **Save**

## Step 2: Create the Pipeline

1. In Azure DevOps, go to **Pipelines** > **Pipelines**
2. Click **New pipeline**
3. Select your repository location:
   - If using Azure Repos: Choose **Azure Repos Git**
   - If using GitHub: Choose **GitHub**
4. Select your repository containing the migrated applications
5. When prompted to configure your pipeline, select **Existing Azure Pipelines YAML file**
6. For the Path, enter: `/infrastructure/cicd/azure-devops-app-pipeline.yml`
7. Click **Continue**
8. Review the pipeline YAML and click **Save**

## Step 3: Configure Pipeline Variables (Optional)

If you need to modify any of the default variables:

1. Navigate to your pipeline
2. Click **Edit**
3. Click the **Variables** button in the top-right corner
4. Click **New Variable** to add a variable or edit existing ones
5. Add the following variables if they don't exist or need modification:
   - `environment`: dev
   - `location`: eastus
   - `offering`: infra
   - `subOffering`: winmig
   - `factoryRegion`: emea
   - `vId`: vpmamidi
   - `purpose`: demo
   - `resourceGroupName`: rg-infra-winmig-emea-vpmamidi-demo
   - `netFxAppName`: contoso-app-netframeworkwebapp-d-eus-01
   - `storeAppName`: contoso-app-storeapp-d-eus-01
6. Click **Save**

## Step 4: Configure Pipeline Triggers

1. Navigate to your pipeline
2. Click **Edit**
3. Click the **More actions** button (three dots) in the top-right corner
4. Select **Triggers**
5. Configure the following:

   ### Continuous Integration
   - Under **YAML**, you'll see the triggers are already defined in the YAML file
   - The pipeline is configured to trigger automatically when changes are pushed to `main`, `master`, or `pipeline-branch`
   
   ### Scheduled Triggers (Optional)
   - To add a scheduled trigger, click **Add** under **Scheduled**
   - Set the schedule using cron syntax (e.g., `0 0 * * *` for midnight every day)
   - Select the branches to build
   - Click **Save**
   
   ### Pull Request Validation (Optional)
   - Under **Pull request validation**, click **Enable pull request validation**
   - Add the branch(es) to monitor for pull requests
   - Click **Save**

6. Click **Save** to apply your changes

## Step 5: Run the Pipeline

1. Navigate to your pipeline
2. Click **Run pipeline**
3. Select the branch to build (e.g., `pipeline-branch`)
4. Click **Run**

## Step 6: Monitor Deployment

1. After triggering the pipeline, you'll be taken to the pipeline run page
2. Monitor the progress of the build and deployment stages
3. Click on any stage to see detailed logs
4. When the pipeline completes, verify the deployment by accessing the application URLs:
   - NetFrameworkWebApp: https://contoso-app-netframeworkwebapp-d-eus-01.azurewebsites.net
   - StoreApp: https://contoso-app-storeapp-d-eus-01.azurewebsites.net

## Troubleshooting

### Service Connection Issues
- Verify the service principal has Contributor access to your subscription
- Try recreating the service connection

### Build Failures
- Check the build logs for specific error messages
- Verify the .NET SDK version is compatible with your projects

### Deployment Failures
- Ensure the resource group and app services exist
- Verify Azure Policy compliance for resource naming and tagging
- Check that service connection has proper permissions

### Trigger Issues
- If automatic triggers aren't working, verify branch names match exactly
- For manual triggers, ensure you have proper permissions to run the pipeline
