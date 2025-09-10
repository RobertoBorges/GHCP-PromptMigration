# Azure Infrastructure for Store Application

This directory contains Terraform configurations to deploy the Store Application to Azure App Service.

## Resources Created

- Azure Resource Group
- App Service Plan
- App Service (Windows Web App)
- Application Insights
- Storage Account with File Share for SQLite data persistence
- Optional VNet integration

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) (version 1.0.0 or later)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) (version 2.30.0 or later)
- Azure subscription

## Getting Started

1. **Login to Azure**

   ```bash
   az login
   ```

2. **Select Your Subscription**

   ```bash
   az account set --subscription "Your Subscription Name or ID"
   ```

3. **Initialize Terraform**

   ```bash
   terraform init
   ```

4. **Customize Variables (Optional)**

   Edit `terraform.tfvars` to customize the deployment settings:

   ```hcl
   app_name         = "your-app-name"
   location         = "your-preferred-region"
   environment      = "dev|test|prod"
   app_service_sku  = "B1|B2|S1|etc"
   ```

5. **Preview the Changes**

   ```bash
   terraform plan
   ```

6. **Apply the Configuration**

   ```bash
   terraform apply
   ```

7. **Access Your Application**

   After the deployment is complete, Terraform will output the URL of your App Service.

## Configuration Details

### App Service

- .NET 8 runtime
- Always On enabled
- TLS 1.2 enforced
- Application Insights integration
- System-assigned managed identity

### SQLite Database

The application uses SQLite as its database. The database file is stored in a mounted Azure File Share for persistence across app restarts and deployments.

### Networking

By default, the App Service is accessible over the public internet. For enhanced security, you can enable VNet integration by setting `enable_vnet_integration = true` and providing a `subnet_id` in the variables.

## Clean Up

To remove all resources created by this Terraform configuration:

```bash
terraform destroy
```

## Production Considerations

For production deployments, consider:

1. Enabling VNet integration
2. Using a higher tier App Service Plan (at least S1)
3. Setting up custom domains and TLS certificates
4. Configuring backup policies
5. Implementing a CI/CD pipeline
6. Using a state backend (Azure Storage or Terraform Cloud)
