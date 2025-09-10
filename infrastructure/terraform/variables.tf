variable "app_name" {
  description = "The name of the application, used to generate resource names"
  type        = string
  default     = "storeapp"
}

variable "location" {
  description = "The Azure region where resources will be created"
  type        = string
  default     = "eastus"
}

variable "environment" {
  description = "The environment (dev, test, prod)"
  type        = string
  default     = "dev"
}

variable "organization_prefix" {
  description = "The organization prefix for CMF naming convention"
  type        = string
  default     = "contoso"
}

variable "offering" {
  description = "The primary offering category"
  type        = string
  default     = "infra"
}

variable "sub_offering" {
  description = "The sub-offering category"
  type        = string
  default     = "winmig"
}

variable "factory_region" {
  description = "The factory region (e.g., emea, amer)"
  type        = string
  default     = "emea"
}

variable "v_id" {
  description = "The ID of the engineer (e.g., alias)"
  type        = string
  default     = "v-pmamidi"
}

variable "purpose" {
  description = "The purpose of the resources (e.g., demo, poc)"
  type        = string
  default     = "demo"
}

variable "customer_name" {
  description = "The name of the customer"
  type        = string
  default     = "Contoso"
}

variable "tower" {
  description = "The tower name"
  type        = string
  default     = "AppMod"
}

variable "app_service_sku" {
  description = "The SKU for the App Service Plan"
  type        = string
  default     = "B1"
}

variable "enable_vnet_integration" {
  description = "Whether to enable VNet integration for the App Service"
  type        = bool
  default     = false
}

variable "subnet_id" {
  description = "The ID of the subnet to integrate with the App Service"
  type        = string
  default     = ""
}
