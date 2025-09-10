# Deploying Store App to Azure

This document provides instructions for deploying the ASP.NET Core Store App to Azure using Terraform.

## Prerequisites

Before deploying, ensure you have the following:

1. **Azure CLI** installed and configured
2. **Terraform** installed (version 1.0.0 or later)
3. **PowerShell** version 7.0 or later
4. **.NET 8 SDK** installed
5. Access to an Azure subscription

## Deployment Steps

### 1. Authenticate to Azure

```powershell
az login
az account set --subscription "Your Subscription Name or ID"
```

### 2. Initialize Terraform

Navigate to the terraform directory and initialize:

```powershell
cd infrastructure\terraform
terraform init
```

### 3. Customize Deployment (Optional)

Edit the `terraform.tfvars` file to customize your deployment:

```hcl
app_name = "storeapp"          # Change to your preferred name
location = "eastus"            # Change to your preferred region
environment = "dev"            # Change to dev, test, or prod
app_service_sku = "B1"         # Change to preferred SKU
```

### 4. Preview the Changes

```powershell
terraform plan
```

Review the plan to ensure it will create the expected resources.

### 5. Apply the Terraform Configuration

```powershell
terraform apply
```

Type "yes" when prompted to confirm the deployment.

### 6. Deploy the Application

You can deploy the application using the provided PowerShell script:

```powershell
.\deploy.ps1
```

Or manually:

```powershell
# Build and publish the application
cd src\StoreApp
dotnet publish -c Release

# Get the App Service name from Terraform output
$appServiceName = terraform output -raw app_service_name

# Deploy using ZIP deployment
Compress-Archive -Path .\bin\Release\net8.0\publish\* -DestinationPath .\publish.zip -Force
az webapp deployment source config-zip -g "${appServiceName}-rg" -n $appServiceName --src .\publish.zip
```

### 7. Verify Deployment

After deployment completes, access your application at the URL provided in the Terraform output:

```powershell
terraform output app_service_url
```

## Database Configuration

The application uses SQLite which is deployed with the application code. The database file is stored in an Azure File Share for persistence.

## Troubleshooting

If you encounter issues:

1. **Check App Service Logs**: Navigate to the Azure Portal > App Service > Monitoring > Log Stream
2. **Application Insights**: View telemetry in Azure Portal > Application Insights
3. **Check Deployment Status**: Azure Portal > App Service > Deployment Center

## Cleanup

To remove all Azure resources created by Terraform:

```powershell
terraform destroy
```

Type "yes" when prompted to confirm the deletion of resources.

## Next Steps

- Set up CI/CD pipelines for automated deployments
- Configure custom domains and SSL certificates
- Set up monitoring alerts based on Application Insights
- Implement backup and disaster recovery procedures
