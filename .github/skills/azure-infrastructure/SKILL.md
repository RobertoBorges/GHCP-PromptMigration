---
name: azure-infrastructure
description: |
  Azure Infrastructure as Code patterns using Bicep and Terraform.
  **Use when:** Generating IaC for App Service, Container Apps, or AKS deployments.
  **Triggers on:** Phase 3 infrastructure generation, azd init, Bicep/Terraform file creation.
  **Covers:** Azure Verified Modules, managed identities, Key Vault with RBAC, Application Insights, networking.
---

# Azure Infrastructure Skill

Use this skill when generating Infrastructure as Code (IaC) for Azure deployments.

## When to Use This Skill

- Creating Bicep or Terraform templates for Azure
- Setting up App Service, Container Apps, or AKS infrastructure
- Configuring managed identities and RBAC
- Setting up Application Insights and Log Analytics
- Creating azd-compatible project structure
- Implementing Azure security best practices

## Hosting Platform Selection

| Platform | Best For | Complexity |
|----------|----------|------------|
| **Azure App Service** | Web apps, APIs, quick deployment | Low |
| **Azure Container Apps** | Microservices, event-driven, serverless containers | Medium |
| **Azure Kubernetes Service** | Complex orchestration, full K8s control | High |

## Bicep Project Structure

```
infra/
├── main.bicep                    # Entry point
├── main.parameters.json          # Environment parameters
├── abbreviations.json            # Naming conventions
└── modules/
    ├── appService.bicep          # App Service resources
    ├── containerApp.bicep        # Container Apps resources
    ├── aks.bicep                 # AKS cluster resources
    ├── database.bicep            # Database resources
    ├── monitoring.bicep          # App Insights + Log Analytics
    ├── keyvault.bicep            # Key Vault with RBAC
    ├── identity.bicep            # Managed identities
    └── networking.bicep          # VNet, NSG, Private Endpoints
```

## Terraform Project Structure

```
infra/
├── main.tf                       # Main configuration
├── variables.tf                  # Variable definitions
├── outputs.tf                    # Output values
├── providers.tf                  # Provider configuration
├── terraform.tfvars              # Variable values (gitignored)
└── modules/
    ├── app_service/
    ├── container_app/
    ├── aks/
    ├── database/
    ├── monitoring/
    ├── keyvault/
    ├── identity/
    └── networking/
```

## Azure Developer CLI (azd) Integration

### azure.yaml Template

```yaml
name: my-application
metadata:
  template: my-application@0.0.1
services:
  web:
    project: ./src/Web
    host: appservice  # or containerapp
    language: dotnet  # or java, python, node
hooks:
  preprovision:
    shell: pwsh
    run: ./scripts/pre-provision.ps1
  postprovision:
    shell: pwsh
    run: ./scripts/post-provision.ps1
```

## Bicep Best Practices

### 1. Use Azure Verified Modules (AVM)

```bicep
// Use AVM modules from bicep registry
module appService 'br/public:avm/res/web/site:0.3.0' = {
  name: 'appServiceDeployment'
  params: {
    name: appServiceName
    location: location
    kind: 'app,linux'
    serverFarmResourceId: appServicePlan.outputs.resourceId
    managedIdentities: {
      systemAssigned: true
    }
  }
}
```

### 2. Managed Identity Pattern

```bicep
// Create user-assigned managed identity
resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${prefix}-identity'
  location: location
}

// Assign RBAC role
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, managedIdentity.id, 'contributor')
  properties: {
    principalId: managedIdentity.properties.principalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'b24988ac-6180-42a0-ab88-20f7382dd24c')
  }
}
```

### 3. Key Vault with RBAC (No Access Policies)

```bicep
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: '${prefix}-kv'
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true  // RBAC only, no access policies
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
  }
}
```

### 4. Monitoring Setup

```bicep
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: '${prefix}-logs'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${prefix}-insights'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}
```

## Terraform Best Practices

### 1. Provider Configuration

```hcl
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.45"
    }
  }
  
  backend "azurerm" {
    # Configure in backend.tfvars
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
}
```

### 2. Managed Identity Pattern

```hcl
resource "azurerm_user_assigned_identity" "main" {
  name                = "${var.prefix}-identity"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_role_assignment" "app_to_keyvault" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.main.principal_id
}
```

## Security Best Practices

1. **Use Managed Identities** - Never store credentials in code
2. **Enable RBAC for Key Vault** - No access policies
3. **Private Endpoints** - For databases and storage
4. **Network Security Groups** - Restrict traffic
5. **TLS 1.2 minimum** - For all services
6. **Diagnostic settings** - Log to Log Analytics
7. **Resource locks** - Prevent accidental deletion

## Template Files

- [main.bicep](./templates/bicep/main.bicep) - Bicep entry point
- [appService.bicep](./templates/bicep/modules/appService.bicep) - App Service module
- [main.tf](./templates/terraform/main.tf) - Terraform entry point
- [azure.yaml](./templates/azure.yaml) - azd configuration

## Naming Conventions

Use consistent naming with resource abbreviations:

| Resource Type | Abbreviation | Example |
|---------------|--------------|---------|
| Resource Group | rg | rg-myapp-prod |
| App Service | app | app-myapp-prod |
| App Service Plan | asp | asp-myapp-prod |
| Container App | ca | ca-myapp-prod |
| Container Registry | cr | crmyappprod |
| Key Vault | kv | kv-myapp-prod |
| Storage Account | st | stmyappprod |
| SQL Database | sqldb | sqldb-myapp-prod |
| Application Insights | appi | appi-myapp-prod |
| Log Analytics | log | log-myapp-prod |
