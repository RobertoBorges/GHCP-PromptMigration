---
mode: agent
---
Deploy application to Azure

# Azure Deployment Guide

Deploy the modernized application to the selected Azure platform. Follow these steps:
- Use `azure_development-get_deployment_best_practices` to get high-level instructions to follow.
- Use `azure_check_predeploy` to check the infrastructure files and fix issues accordingly.
- Use `azure_check_quota` and `azure_check_region` to ensure the Azure resources can be deployed to the target region.
- Use `azure_azd-up_deploy` to deploy the Azure resources from the infrastructure files.

## Deployment Approach

This project uses Azure Developer CLI (azd) for deployment. The azd tool streamlines the deployment process by handling infrastructure provisioning, application building, and deployment in a single command.

## Pre-Deployment Checklist

Before deploying, ensure:
- You have the latest Azure CLI and Azure Developer CLI installed
- You are logged in to Azure (`az login`)
- You have selected the correct subscription (`az account set --subscription <subscription-id>`)
- Your infrastructure files in the `infra/` folder are correctly set up and validated
- Your application code is ready for deployment
- If containerization is required, ensure Docker is installed and running

## Deployment Process Based on Target Platform

### For Azure App Service Deployments:
- Configure deployment settings in azure.yaml
- Set up application settings and connection strings
- Configure continuous deployment if needed
- Set up custom domains and SSL certificates if applicable
- Configure scaling rules
- Set up monitoring with Application Insights

### For Azure Kubernetes Service (AKS) Deployments:
- Ensure container images are built and pushed to a container registry
- Configure Kubernetes manifests or Helm charts
- Set up ingress controllers if needed
- Configure horizontal pod autoscalers
- Set up monitoring with Azure Monitor for Containers
- Configure network policies and security settings

### For Azure Container Apps Deployments:
- Ensure container images are built and pushed to a container registry
- Configure container app settings in the infrastructure files
- Set up scaling rules and triggers
- Configure ingress settings if needed
- Set up monitoring with Application Insights
- Configure environment variables and secrets

## Deployment Steps

1. **Environment Setup**
   ```bash
   # Initialize azd environment
   azd init

   # or use an existing environment
   azd env select <environment-name>
   ```

2. **Deploy the Application**
   ```bash
   # Deploy with azd
   azd up
   
   # Or provision infrastructure separately
   azd provision
   
   # Then deploy code
   azd deploy
   ```

3. **Verify Deployment**
   Check the deployment status and application health:
   - Verify all resources were created successfully
   - Check application logs for any errors
   - Test application functionality
   - Verify monitoring is working properly
   - Check that authentication is working correctly

## Post-Deployment Tasks

- Configure any additional settings in the Azure portal
- Set up CI/CD pipelines for future deployments
- Configure monitoring alerts
- Set up backup and disaster recovery policies
- Document the deployment process and configuration

At the end, generate a deployment summary report in the reports folder.
Also, update the status report file with the status of the deployment step.
