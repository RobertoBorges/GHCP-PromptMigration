# CI/CD Pipeline User Guide

This guide provides instructions on how to use and maintain the CI/CD pipeline for the StoreApp application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setting Up GitHub Secrets](#setting-up-github-secrets)
3. [Pipeline Workflows](#pipeline-workflows)
4. [Deployment Environments](#deployment-environments)
5. [Manual Triggers](#manual-triggers)
6. [Monitoring Deployments](#monitoring-deployments)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## Prerequisites

Before using the CI/CD pipeline, ensure you have:

- GitHub repository access with proper permissions
- Azure subscription with Contributor access
- Azure CLI installed locally for setup tasks
- PowerShell 7+ for running the setup scripts

## Setting Up GitHub Secrets

The pipeline requires the following secrets to be configured in your GitHub repository:

1. **AZURE_CREDENTIALS**: Azure service principal credentials in JSON format

To set up these secrets:

1. Run the `setup-azure-credentials.ps1` script:
   ```powershell
   ./setup-azure-credentials.ps1 -SubscriptionId "your-subscription-id"
   ```

2. Copy the JSON output and add it as a secret named `AZURE_CREDENTIALS` in your GitHub repository:
   - Go to your GitHub repository
   - Navigate to Settings > Secrets > Actions
   - Click "New repository secret"
   - Name: `AZURE_CREDENTIALS`
   - Value: Paste the JSON output from the script

## Pipeline Workflows

The CI/CD pipeline consists of the following workflows:

### Main Pipeline (`azure-pipeline.yml`)

This is the primary workflow that handles:
- Building and testing the application
- Validating Terraform configurations
- Deploying infrastructure to Azure
- Deploying the application to Azure App Service

## Deployment Environments

The pipeline supports three environments:

1. **dev**: Development environment (default)
   - Used for ongoing development work
   - Automatically deployed on pushes to main

2. **test**: Testing/QA environment
   - Used for more formal testing before production
   - Deployed manually via workflow dispatch

3. **prod**: Production environment
   - The live customer-facing environment
   - Deployed manually via workflow dispatch with approval

Each environment is configured with environment protection rules in GitHub:
- `dev`: No approval required
- `test`: Requires one approver
- `prod`: Requires two approvers

## Manual Triggers

To manually trigger a deployment:

1. Go to the GitHub repository
2. Navigate to Actions > Azure Pipeline
3. Click "Run workflow"
4. Select the branch (usually `main`)
5. Choose the target environment (dev, test, or prod)
6. Click "Run workflow"

## Monitoring Deployments

You can monitor deployments in several ways:

1. **GitHub Actions**: View the workflow run in the Actions tab of your repository
2. **Azure Portal**: 
   - Monitor App Service deployments in the Deployment Center
   - Check Application Insights for application performance
   - Review App Service logs for runtime issues

3. **Application Health**: 
   - The pipeline performs a health check after deployment
   - View the deployed application at the URL provided in the workflow summary

## Troubleshooting

Common issues and their solutions:

1. **Authentication Failures**:
   - Check if the `AZURE_CREDENTIALS` secret is valid and not expired
   - Verify the service principal has the correct permissions

2. **Terraform Errors**:
   - Review the Terraform plan output for validation errors
   - Check for changes made directly in Azure that conflict with Terraform state

3. **Deployment Failures**:
   - Check App Service logs for application startup errors
   - Verify that all required application settings are configured

4. **GitHub Actions Runner Issues**:
   - Check the runner logs for environment-related problems
   - Verify that the runner has the necessary resources

## Best Practices

1. **Code Reviews**:
   - Always perform code reviews before merging to main
   - Use pull requests for all changes

2. **Branch Protection**:
   - Configure branch protection rules for the main branch
   - Require status checks to pass before merging

3. **Semantic Versioning**:
   - Use proper semantic versioning for releases
   - Update the version using the `pipeline-tasks.ps1` script

4. **Testing**:
   - Maintain comprehensive test coverage
   - Add new tests for all new features

5. **Infrastructure as Code**:
   - Never make manual changes to Azure resources
   - Always update the Terraform files for infrastructure changes

6. **Secrets Management**:
   - Regularly rotate service principal credentials
   - Never commit secrets to the repository
