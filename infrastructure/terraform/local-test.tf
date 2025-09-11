terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  # Using local state for initial testing
  # The Azure DevOps pipeline will use the remote backend
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "example" {
  name     = "rg-terraform-test-${var.environment}"
  location = var.location
  
  tags = {
    Environment = var.environment
    CreatedBy   = "Terraform"
    Project     = var.app_name
  }
}

# Variables
variable "environment" {
  description = "The environment (dev, test, prod)"
  type        = string
  default     = "dev"
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
  default     = "westus"
}

variable "app_name" {
  description = "The name of the application, used to generate resource names"
  type        = string
  default     = "storeapp"
}

# Outputs
output "resource_group_name" {
  value = azurerm_resource_group.example.name
}

output "resource_group_location" {
  value = azurerm_resource_group.example.location
}
