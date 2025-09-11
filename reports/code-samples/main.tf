# main.tf - Terraform configuration for Azure infrastructure

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Variables
variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "classicstore"
}

variable "location" {
  description = "Azure region to deploy resources"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Environment (dev, test, prod)"
  type        = string
  default     = "dev"
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.app_name}-${var.environment}"
  location = var.location
  tags = {
    Environment = var.environment
    Application = var.app_name
  }
}

# App Service Plan
resource "azurerm_service_plan" "asp" {
  name                = "asp-${var.app_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Windows"
  sku_name            = "B1" # Basic tier for development

  tags = {
    Environment = var.environment
    Application = var.app_name
  }
}

# App Service
resource "azurerm_windows_web_app" "app" {
  name                = "${var.app_name}-${var.environment}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      current_stack  = "dotnet"
      dotnet_version = "v8.0"
    }
    always_on = true
  }

  app_settings = {
    "ASPNETCORE_ENVIRONMENT" = var.environment
  }

  tags = {
    Environment = var.environment
    Application = var.app_name
  }
}

# Application Insights
resource "azurerm_application_insights" "appinsights" {
  name                = "ai-${var.app_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"

  tags = {
    Environment = var.environment
    Application = var.app_name
  }
}

# Update App Service with Application Insights key
resource "azurerm_app_service_app_settings" "app_insights_settings" {
  app_service_id = azurerm_windows_web_app.app.id
  
  app_settings = {
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.appinsights.instrumentation_key
  }
}

# Outputs
output "website_url" {
  value = "https://${azurerm_windows_web_app.app.default_hostname}"
}

output "app_insights_key" {
  value     = azurerm_application_insights.appinsights.instrumentation_key
  sensitive = true
}
