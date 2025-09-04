# Azure DevOps Pipeline Quick Reference

## Pipeline Overview

This Azure DevOps pipeline automates the build, test, and deployment of the StoreApp application to Azure. It uses Terraform for infrastructure provisioning and Azure App Service for hosting.

## Prerequisites

- Azure DevOps Project
- Azure Subscription
- Service Principal with Contributor access to Azure Subscription
- Storage Account for Terraform State

## Service Connections

| Name | Type | Purpose |
|------|------|---------|
| Azure Subscription | Azure Resource Manager | Used for Azure deployments and Terraform |

## Pipeline Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| vmImageName | Agent VM image | windows-latest |
| buildConfiguration | Build configuration | Release |
| dotnetSdkVersion | .NET SDK version | 8.0.x |
| projectPath | Path to project file | src/StoreApp/StoreApp.csproj |
| publishPath | Path for published artifacts | $(Build.ArtifactStagingDirectory)/app |
| infraPath | Path to Terraform files | infrastructure/terraform |

## Variable Groups

| Group | Variables | Purpose |
|-------|-----------|---------|
| TerraformBackend | TF_BACKEND_RG, TF_BACKEND_STORAGE, TF_BACKEND_CONTAINER | Terraform state storage |

## Environments

| Name | Purpose | Approvals |
|------|---------|-----------|
| Dev | Development environment | None |
| Test | Testing environment | Optional |
| Prod | Production environment | Required |

## Pipeline Stages

1. **Build**: Builds and tests the .NET application
2. **Validate Infrastructure**: Validates Terraform configuration
3. **Deploy_Dev**: Deploys to Development environment
   - DeployInfrastructure: Creates/updates Azure resources
   - DeployApplication: Deploys the application to App Service

## Common Tasks

### Manually Running the Pipeline

1. Go to Pipelines > Pipelines
2. Select the pipeline
3. Click "Run pipeline"
4. Select branch and click "Run"

### Viewing Pipeline Results

1. Go to Pipelines > Pipelines
2. Select the pipeline run
3. View the stages and jobs
4. Click on a job to see detailed logs

### Approving Deployments

1. When a deployment needs approval, approvers receive an email
2. Go to Pipelines > Environments
3. Select the environment
4. Click "Review" on the pending approval
5. Approve or reject with comments

### Checking Deployment Status

1. Go to Pipelines > Environments
2. Select the environment
3. View the deployment history and status

## Troubleshooting

### Common Issues

1. **Service Connection Issues**:
   - Verify the service connection is valid
   - Check if the service principal has the correct permissions

2. **Terraform Backend Issues**:
   - Verify storage account exists and is accessible
   - Check if container exists in the storage account

3. **Build Failures**:
   - Check build logs for compilation errors
   - Verify package references and NuGet sources

4. **Deployment Failures**:
   - Check App Service logs in Azure Portal
   - Verify App Service configuration

### Getting Help

For assistance with this pipeline, contact:
- Your DevOps team
- Azure DevOps administrator

## Documentation Links

- [Azure DevOps Documentation](https://docs.microsoft.com/en-us/azure/devops/)
- [Azure Pipelines Tasks](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/)
- [Terraform Documentation](https://www.terraform.io/docs/)
