# Quick Start: Configuring Application Pipeline in Azure DevOps

This guide provides quick, actionable steps to configure your application deployment pipeline in Azure DevOps.

## Prerequisites

- Azure DevOps organization and project
- Azure subscription for deployment
- PowerShell 5.1 or higher
- Azure CLI installed and configured

## Step 1: Run the Configuration Script

The fastest way to configure your pipeline is using the provided PowerShell script:

```powershell
# Navigate to the script location
cd C:\Users\v-pmamidi\source\repos\GHCP-PromptMigration\infrastructure\cicd

# Run the configuration script (replace with your values)
.\Configure-AzureDevOpsPipeline.ps1 -AzureDevOpsOrg "YourOrgName" -AzureDevOpsProject "YourProjectName" -CreateServiceConnection -AzureSubscriptionId "your-subscription-id" -RunPipeline
```

### Script Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| AzureDevOpsOrg | Your Azure DevOps organization name | Yes |
| AzureDevOpsProject | Your Azure DevOps project name | Yes |
| AzureSubscriptionId | Your Azure subscription ID | No, but required for creating service connection |
| ServiceConnectionName | Name for Azure service connection | No (default: "Azure-Service-Connection") |
| CreateServiceConnection | Switch to create the service connection | No |
| RunPipeline | Switch to run the pipeline after configuration | No |

## Step 2: Monitor Pipeline Creation

The script will:
1. Check prerequisites
2. Configure Azure DevOps CLI
3. Create/update service connection (if requested)
4. Create/update pipeline using YAML definition
5. Configure pipeline variables
6. Run the pipeline (if requested)

## Step 3: Verify Pipeline in Azure DevOps Portal

1. Go to your Azure DevOps project: `https://dev.azure.com/YourOrgName/YourProjectName`
2. Navigate to **Pipelines** > **Pipelines**
3. Find and select the `MigratedApps-Deployment` pipeline
4. Verify the pipeline configuration:
   - Trigger settings
   - Variables
   - Service connection

## Step 4: Test Pipeline Execution

If you didn't run the pipeline during configuration:

1. In the Azure DevOps portal, click **Run pipeline**
2. Select the `pipeline-branch` branch
3. Click **Run**

Or use Azure CLI:

```powershell
az pipelines run --name "MigratedApps-Deployment"
```

## Step 5: Verify Deployment

After the pipeline completes successfully:

1. Access your applications:
   - NetFrameworkWebApp: https://contoso-app-netframeworkwebapp-d-eus-01.azurewebsites.net
   - StoreApp: https://contoso-app-storeapp-d-eus-01.azurewebsites.net
2. Verify functionality and appearance

## Troubleshooting

### Service Connection Issues
- Ensure you have Owner/Contributor rights on the Azure subscription
- Try creating the service connection manually in the Azure DevOps portal

### Pipeline Creation Failures
- Verify the YAML path is correct: `infrastructure/cicd/azure-devops-app-pipeline.yml`
- Check repository permissions

### Deployment Failures
- Verify resource group exists: `rg-infra-winmig-emea-vpmamidi-demo`
- Ensure App Service Plan and Web Apps are created
- Check service connection permissions

## Need More Help?

For detailed configuration options:
- See `AZURE-PORTAL-SETUP-GUIDE.md` for manual portal setup
- See `PIPELINE-TRIGGER-GUIDE.md` for trigger configuration details
- Run `Get-Help .\Configure-AzureDevOpsPipeline.ps1 -Full` for script documentation
