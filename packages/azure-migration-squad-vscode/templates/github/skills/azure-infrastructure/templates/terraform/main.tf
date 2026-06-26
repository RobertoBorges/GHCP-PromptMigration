# =============================================================================
# Azure Terraform Main Configuration
# =============================================================================
# Infrastructure as Code for Azure Application Deployment
# Mirrors the Bicep template functionality with Terraform equivalents
# =============================================================================

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
    # Configure via backend.tfvars or CLI:
    #   resource_group_name  = "rg-tfstate"
    #   storage_account_name = "sttfstate"
    #   container_name       = "tfstate"
    #   key                  = "app.terraform.tfstate"
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = false
      recover_soft_deleted_key_vaults = true
    }
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
  }
}

# =============================================================================
# Variables
# =============================================================================

variable "workload_name" {
  description = "Name of the workload (used for resource naming)"
  type        = string

  validation {
    condition     = length(var.workload_name) >= 3 && length(var.workload_name) <= 20
    error_message = "Workload name must be between 3 and 20 characters."
  }
}

variable "environment_name" {
  description = "Environment name"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment_name)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastus2"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# =============================================================================
# Locals
# =============================================================================

locals {
  resource_token = lower(substr(md5("${var.workload_name}-${var.environment_name}"), 0, 8))

  default_tags = merge(var.tags, {
    Environment = var.environment_name
    Workload    = var.workload_name
    ManagedBy   = "Terraform"
  })
}

# =============================================================================
# Resource Group
# =============================================================================

resource "azurerm_resource_group" "main" {
  name     = "rg-${var.workload_name}-${var.environment_name}"
  location = var.location
  tags     = local.default_tags
}

# =============================================================================
# Log Analytics Workspace
# =============================================================================

resource "azurerm_log_analytics_workspace" "main" {
  name                = "log-${var.workload_name}-${var.environment_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = var.environment_name == "prod" ? 90 : 30
  tags                = local.default_tags
}

# =============================================================================
# Application Insights
# =============================================================================

resource "azurerm_application_insights" "main" {
  name                = "appi-${var.workload_name}-${var.environment_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"
  tags                = local.default_tags
}

# =============================================================================
# Container Registry
# =============================================================================

resource "azurerm_container_registry" "main" {
  name                = "acr${local.resource_token}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = var.environment_name == "prod" ? "Premium" : "Basic"
  admin_enabled       = false
  tags                = local.default_tags
}

# =============================================================================
# Container Apps Environment
# =============================================================================

resource "azurerm_container_app_environment" "main" {
  name                       = "cae-${var.workload_name}-${var.environment_name}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  zone_redundancy_enabled    = var.environment_name == "prod"
  tags                       = local.default_tags
}

# =============================================================================
# Key Vault
# =============================================================================

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  name                       = "kv-${var.workload_name}-${local.resource_token}"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  enable_rbac_authorization  = true
  purge_protection_enabled   = var.environment_name == "prod"
  soft_delete_retention_days = 7
  tags                       = local.default_tags
}

# =============================================================================
# SQL Server & Database
# =============================================================================

resource "azurerm_mssql_server" "main" {
  name                         = "sql-${var.workload_name}-${var.environment_name}"
  location                     = azurerm_resource_group.main.location
  resource_group_name          = azurerm_resource_group.main.name
  version                      = "12.0"
  minimum_tls_version          = "1.2"
  administrator_login          = "${var.workload_name}admin"
  administrator_login_password = "ChangeMe!InitialSetup123" # Use Key Vault or managed identity in production
  tags                         = local.default_tags

  azuread_administrator {
    login_username = "sqladmin"
    object_id      = data.azurerm_client_config.current.object_id
  }
}

resource "azurerm_mssql_database" "main" {
  name         = "${var.workload_name}db"
  server_id    = azurerm_mssql_server.main.id
  sku_name     = var.environment_name == "prod" ? "S1" : "Basic"
  max_size_gb  = 2
  zone_redundant = var.environment_name == "prod"
  tags         = local.default_tags
}

# =============================================================================
# App Service Plan (for App Service hosting option)
# =============================================================================

resource "azurerm_service_plan" "main" {
  name                = "asp-${var.workload_name}-${var.environment_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = var.environment_name == "prod" ? "P1v3" : "B1"
  zone_balancing_enabled = var.environment_name == "prod"
  tags                = local.default_tags
}

# =============================================================================
# Web App (App Service)
# =============================================================================

resource "azurerm_linux_web_app" "main" {
  name                = "app-${var.workload_name}-${var.environment_name}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id
  https_only          = true
  tags                = local.default_tags

  identity {
    type = "SystemAssigned"
  }

  site_config {
    always_on        = true
    ftps_state       = "Disabled"
    minimum_tls_version = "1.2"
    http2_enabled    = true
    health_check_path = "/health"

    application_stack {
      dotnet_version = "10.0"
    }
  }

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE"            = "1"
    "ASPNETCORE_ENVIRONMENT"              = var.environment_name == "prod" ? "Production" : "Development"
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.main.connection_string
  }
}

# =============================================================================
# Key Vault RBAC - App Service access to secrets
# =============================================================================

resource "azurerm_role_assignment" "app_keyvault_secrets" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_web_app.main.identity[0].principal_id
}

# =============================================================================
# Autoscale (production only)
# =============================================================================

resource "azurerm_monitor_autoscale_setting" "main" {
  count               = var.environment_name == "prod" ? 1 : 0
  name                = "asp-${var.workload_name}-${var.environment_name}-autoscale"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  target_resource_id  = azurerm_service_plan.main.id
  tags                = local.default_tags

  profile {
    name = "Default"

    capacity {
      minimum = 2
      maximum = 10
      default = 2
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_service_plan.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT5M"
        time_aggregation   = "Average"
        operator           = "GreaterThan"
        threshold          = 70
      }

      scale_action {
        direction = "Increase"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT5M"
      }
    }

    rule {
      metric_trigger {
        metric_name        = "CpuPercentage"
        metric_resource_id = azurerm_service_plan.main.id
        time_grain         = "PT1M"
        statistic          = "Average"
        time_window        = "PT10M"
        time_aggregation   = "Average"
        operator           = "LessThan"
        threshold          = 30
      }

      scale_action {
        direction = "Decrease"
        type      = "ChangeCount"
        value     = "1"
        cooldown  = "PT10M"
      }
    }
  }
}

# =============================================================================
# Outputs
# =============================================================================

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "container_registry_name" {
  description = "Name of the container registry"
  value       = azurerm_container_registry.main.name
}

output "container_registry_login_server" {
  description = "Login server for the container registry"
  value       = azurerm_container_registry.main.login_server
}

output "container_apps_environment_id" {
  description = "ID of the Container Apps environment"
  value       = azurerm_container_app_environment.main.id
}

output "key_vault_name" {
  description = "Name of the Key Vault"
  value       = azurerm_key_vault.main.name
}

output "key_vault_uri" {
  description = "URI of the Key Vault"
  value       = azurerm_key_vault.main.vault_uri
}

output "application_insights_connection_string" {
  description = "Application Insights connection string"
  value       = azurerm_application_insights.main.connection_string
  sensitive   = true
}

output "sql_server_fqdn" {
  description = "Fully qualified domain name of the SQL Server"
  value       = azurerm_mssql_server.main.fully_qualified_domain_name
}

output "app_service_default_hostname" {
  description = "Default hostname of the App Service"
  value       = azurerm_linux_web_app.main.default_hostname
}

output "app_service_principal_id" {
  description = "Principal ID of the App Service managed identity"
  value       = azurerm_linux_web_app.main.identity[0].principal_id
}
