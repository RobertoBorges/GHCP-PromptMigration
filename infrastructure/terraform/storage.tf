# Storage configuration for the App Service

# Mount the file share to the App Service
resource "azurerm_app_service_virtual_network_swift_connection" "storage_mount" {
  count          = var.enable_vnet_integration ? 1 : 0
  app_service_id = azurerm_windows_web_app.app.id
  subnet_id      = var.subnet_id
  depends_on     = [azurerm_windows_web_app.app]
}

# Update the App Service settings for database connection
resource "azurerm_app_service_slot_custom_hostname_binding" "app_settings" {
  app_service_slot_id = azurerm_windows_web_app.app.id
  hostname            = azurerm_windows_web_app.app.default_hostname
  depends_on          = [azurerm_windows_web_app.app]
}
