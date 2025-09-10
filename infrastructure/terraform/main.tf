terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  # Backend configuration will be provided via backend.tfvars file
  backend "azurerm" {}
}

provider "azurerm" {
  features {}
}

# Use data source for the current client configuration
data "azurerm_client_config" "current" {}

# Local variables for naming consistency following specified naming convention
locals {
  current_date = formatdate("YYYY-MM-DD", timestamp())
  
  # CMF naming convention formatting
  location_short = lookup({
    "eastus"         = "eus",
    "westus"         = "wus",
    "northeurope"    = "neu",
    "westeurope"     = "weu",
    "eastasia"       = "eas",
    "southeastasia"  = "seas"
  }, var.location, substr(var.location, 0, 3))
  
  env_short = lookup({
    "dev"   = "d",
    "test"  = "t",
    "qa"    = "q",
    "uat"   = "u",
    "prod"  = "p"
  }, var.environment, substr(var.environment, 0, 1))
  
  # Resource group: rg-<offering>-<sub offering>-<factoryregion>-<v-id>-<purpose>
  rg_name = "rg-${var.offering}-${var.sub_offering}-${var.factory_region}-${var.v_id}-${var.purpose}"
  
  # Resource naming for other resources
  app_service_plan_name = "${var.organization_prefix}-plan-${var.app_name}-${local.env_short}-${local.location_short}-01"
  app_insights_name = "${var.organization_prefix}-appi-${var.app_name}-${local.env_short}-${local.location_short}-01"
  app_service_name = "${var.organization_prefix}-app-${var.app_name}-${local.env_short}-${local.location_short}-01"
  storage_name = "${replace(var.organization_prefix, "-", "")}st${var.app_name}${local.env_short}${local.location_short}01"
  
  common_tags = {
    "created by"     = var.v_id
    "created on"     = local.current_date
    "customer name"  = var.customer_name
    "purpose"        = var.purpose
    "region"         = var.factory_region
    "tower"          = var.tower
    "v-id"           = var.v_id
    "environment"    = var.environment
    "application"    = var.app_name
    "managed by"     = "Terraform"
    "email-id"       = "${var.v_id}@microsoft.com"
  }
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = local.rg_name
  location = var.location
  tags     = local.common_tags
}

# App Service Plan
resource "azurerm_service_plan" "app_plan" {
  name                = local.app_service_plan_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Windows"
  sku_name            = var.app_service_sku
  tags                = local.common_tags
}

# Application Insights
resource "azurerm_application_insights" "insights" {
  name                = local.app_insights_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  application_type    = "web"
  tags                = local.common_tags
}

# App Service
resource "azurerm_windows_web_app" "app" {
  name                = local.app_service_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.app_plan.id
  
  site_config {
    always_on           = true
    minimum_tls_version = "1.2"
    application_stack {
      current_stack  = "dotnet"
      dotnet_version = "v8.0"
    }
    health_check_path = "/"
  }

  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = azurerm_application_insights.insights.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.insights.connection_string
    "ApplicationInsightsAgent_EXTENSION_VERSION" = "~3"
    "ASPNETCORE_ENVIRONMENT"                = var.environment
    "SCM_DO_BUILD_DURING_DEPLOYMENT"        = "true"
    "ConnectionStrings__DefaultConnection"  = "Data Source=D:\\home\\site\\wwwroot\\App_Data\\storeapp.db"
    "WEBSITE_RUN_FROM_PACKAGE"              = "1"
  }

  logs {
    detailed_error_messages = true
    failed_request_tracing  = true
    
    application_logs {
      file_system_level = "Information"
    }
    
    http_logs {
      file_system {
        retention_in_days = 7
        retention_in_mb   = 35
      }
    }
  }

  identity {
    type = "SystemAssigned"
  }

  tags = local.common_tags
}

# Optional: Storage Account for more persistent SQLite storage
resource "azurerm_storage_account" "storage" {
  name                     = local.storage_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  tags                     = local.common_tags
}

# File Share for SQLite database
resource "azurerm_storage_share" "db_share" {
  name                 = "sqlite-data"
  storage_account_name = azurerm_storage_account.storage.name
  quota                = 5
}

# Mount the File Share to App Service
resource "azurerm_app_service_virtual_network_swift_connection" "vnet_integration_main" {
  count          = var.enable_vnet_integration ? 1 : 0
  app_service_id = azurerm_windows_web_app.app.id
  subnet_id      = var.subnet_id
}

# Mount the File Share to App Service
resource "azurerm_storage_account_network_rules" "storage_rules" {
  count              = var.enable_vnet_integration ? 1 : 0
  storage_account_id = azurerm_storage_account.storage.id
  default_action     = "Deny"
  virtual_network_subnet_ids = [var.subnet_id]
  bypass             = ["AzureServices", "Logging", "Metrics"]
}
