# CI/CD Pipeline for StoreApp

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline set up for the StoreApp application.

## Overview

The CI/CD pipeline automates the process of building, testing, and deploying the StoreApp application to Azure. It is implemented using GitHub Actions and consists of several stages:

1. **Build & Test**: Builds the .NET application and runs any available tests
2. **Validate Infrastructure**: Validates the Terraform configuration for Azure resources
3. **Deploy Infrastructure**: Provisions or updates Azure resources using Terraform
4. **Deploy Application**: Deploys the application to Azure App Service

## Pipeline Triggers

The pipeline can be triggered in the following ways:

- **Automatically** on push to the `main` branch
- **Automatically** when a pull request is opened against the `main` branch (build and validate only)
- **Manually** via the GitHub Actions UI with the ability to select the deployment environment

## Environments

The pipeline supports the following environments:

- **dev** (default): Development environment
- **test**: Testing/QA environment
- **prod**: Production environment

## Security

The pipeline uses GitHub Secrets for storing sensitive information:

- `AZURE_CREDENTIALS`: Azure service principal credentials for authentication

## Prerequisites

To use this pipeline, you need to:

1. Create a service principal in Azure:
   ```powershell
   az ad sp create-for-rbac --name "github-actions-sp" --role contributor --scopes /subscriptions/{subscription-id} --sdk-auth
   ```

2. Add the JSON output as a GitHub secret named `AZURE_CREDENTIALS`

## Workflow File

The workflow is defined in `.github/workflows/azure-pipeline.yml`.

## Pipeline Stages

### 1. Build

- Restores NuGet packages
- Builds the application
- Runs tests (if available)
- Publishes the application
- Uploads the build artifacts

### 2. Validate Terraform

- Initializes Terraform
- Validates the Terraform configuration
- Checks Terraform formatting

### 3. Deploy Infrastructure

- Logs in to Azure
- Initializes Terraform
- Creates a Terraform plan
- Applies the Terraform plan to create/update Azure resources
- Exports resource names as environment variables

### 4. Deploy Application

- Downloads the build artifacts
- Logs in to Azure
- Deploys the application to Azure App Service
- Performs a health check to verify the deployment

## Rollback Procedure

In case of deployment failures:

1. The pipeline will automatically fail and report the issue
2. To rollback, you can either:
   - Fix the issue and redeploy
   - Manually restore from a previous working state using the Azure portal
   - Revert to a previous Terraform state (if infrastructure changes caused the issue)

## Monitoring

After deployment, you can monitor the application using:

- Application Insights in the Azure portal
- Logs available in the Azure App Service portal
- GitHub Actions workflow run history

## Adding Quality Gates

This pipeline can be extended with additional quality gates:

- Code coverage requirements
- Security scanning
- Performance testing
- Compliance checks
