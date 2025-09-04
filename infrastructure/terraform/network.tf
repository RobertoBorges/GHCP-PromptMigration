# This file contains optional networking resources for more secure deployments
# These resources are created only if enable_vnet_integration is set to true

# Virtual Network
resource "azurerm_virtual_network" "vnet" {
  count               = var.enable_vnet_integration && var.subnet_id == "" ? 1 : 0
  name                = "${local.name_prefix}-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
  tags                = local.common_tags
}

# Subnet for App Service integration
resource "azurerm_subnet" "app_service_subnet" {
  count                = var.enable_vnet_integration && var.subnet_id == "" ? 1 : 0
  name                 = "app-service-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet[0].name
  address_prefixes     = ["10.0.1.0/24"]
  delegation {
    name = "app-service-delegation"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

# Network Security Group
resource "azurerm_network_security_group" "nsg" {
  count               = var.enable_vnet_integration && var.subnet_id == "" ? 1 : 0
  name                = "${local.name_prefix}-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.common_tags
}

# NSG Rules
resource "azurerm_network_security_rule" "outbound" {
  count                       = var.enable_vnet_integration && var.subnet_id == "" ? 1 : 0
  name                        = "AllowOutbound"
  priority                    = 100
  direction                   = "Outbound"
  access                      = "Allow"
  protocol                    = "*"
  source_port_range           = "*"
  destination_port_range      = "*"
  source_address_prefix       = "*"
  destination_address_prefix  = "*"
  resource_group_name         = azurerm_resource_group.rg.name
  network_security_group_name = azurerm_network_security_group.nsg[0].name
}

# Associate NSG with Subnet
resource "azurerm_subnet_network_security_group_association" "nsg_association" {
  count                     = var.enable_vnet_integration && var.subnet_id == "" ? 1 : 0
  subnet_id                 = azurerm_subnet.app_service_subnet[0].id
  network_security_group_id = azurerm_network_security_group.nsg[0].id
}

# Use the newly created subnet or the provided subnet_id
locals {
  effective_subnet_id = var.enable_vnet_integration ? (
    var.subnet_id != "" ? var.subnet_id : (
      length(azurerm_subnet.app_service_subnet) > 0 ? azurerm_subnet.app_service_subnet[0].id : ""
    )
  ) : ""
}

# Update the App Service VNet integration resource to use the effective subnet ID
resource "azurerm_app_service_virtual_network_swift_connection" "vnet_integration_custom" {
  count          = var.enable_vnet_integration && local.effective_subnet_id != "" ? 1 : 0
  app_service_id = azurerm_windows_web_app.app.id
  subnet_id      = local.effective_subnet_id
}
