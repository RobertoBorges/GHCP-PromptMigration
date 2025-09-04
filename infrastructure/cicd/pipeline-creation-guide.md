# Automated Pipeline Creation Guide

This guide explains how to use the automated script to create and run an Azure DevOps pipeline for deploying both infrastructure and application.

## Prerequisites

Before running the script, ensure you have:

1. Azure CLI installed
2. Git installed and configured
3. Access to an Azure DevOps organization and project
4. Access to an Azure subscription with permissions to create resources

## Using the Script

The `create-pipeline.ps1` script automates the following tasks:

1. Installs the Azure DevOps extension for the Azure CLI if needed
2. Logs you into Azure
3. Configures Azure DevOps CLI defaults
4. Creates or verifies a variable group for Terraform backend configuration
5. Creates Azure resources for Terraform state if they don't exist
6. Creates necessary environments in Azure DevOps (Dev, Test, Prod)
7. Guides you through creating a service connection if it doesn't exist
8. Creates the pipeline using the existing YAML file
9. Optionally runs the pipeline

## Running the Script

1. Open PowerShell as Administrator
2. Navigate to the script directory:
   ```powershell
   cd C:\Users\v-pmamidi\source\repos\GHCP-PromptMigration\infrastructure\cicd
   ```
3. Run the script:
   ```powershell
   .\create-pipeline.ps1
   ```
4. Follow the prompts in the script

## Manual Steps

The script may require some manual steps:

1. **Azure Login**: You'll need to authenticate with Azure when prompted
2. **Service Connection**: If a service connection doesn't exist, you'll need to create one manually in the Azure DevOps portal
3. **Pipeline Run**: You can choose whether to run the pipeline immediately after creation

## Troubleshooting

If you encounter issues:

1. **Azure CLI Authentication**: Make sure you're logged into the correct Azure account
2. **Permissions**: Ensure you have sufficient permissions in both Azure and Azure DevOps
3. **YAML File**: Verify that the YAML pipeline file exists at the specified path
4. **Variable Group**: If variable creation fails, you may need to create it manually

## Next Steps

After the pipeline is created:

1. Review the pipeline in the Azure DevOps portal
2. Check the environments and variable groups
3. Run the pipeline if you didn't choose to run it automatically
4. Monitor the pipeline execution and check logs for any errors

For more information, refer to:
- `infrastructure/cicd/azure-devops-setup-guide.md`
- `infrastructure/cicd/azure-devops-quick-reference.md`
- `infrastructure/cicd/azure-devops-customization.md`
