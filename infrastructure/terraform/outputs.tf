# Output values for the deployment

output "resource_group_name" {
  description = "The name of the resource group"
  value       = azurerm_resource_group.rg.name
}

output "app_service_plan_name" {
  description = "The name of the App Service Plan"
  value       = azurerm_service_plan.app_plan.name
}

output "app_service_name" {
  description = "The name of the App Service"
  value       = azurerm_windows_web_app.app.name
}

output "app_service_url" {
  description = "The URL of the App Service"
  value       = "https://${azurerm_windows_web_app.app.default_hostname}"
}

output "app_service_id" {
  description = "The ID of the App Service"
  value       = azurerm_windows_web_app.app.id
}

output "application_insights_name" {
  description = "The name of Application Insights"
  value       = azurerm_application_insights.insights.name
}

output "instrumentation_key" {
  description = "The instrumentation key of Application Insights"
  value       = azurerm_application_insights.insights.instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "The connection string of Application Insights"
  value       = azurerm_application_insights.insights.connection_string
  sensitive   = true
}

output "storage_account_name" {
  description = "The name of the storage account"
  value       = azurerm_storage_account.storage.name
}

output "file_share_name" {
  description = "The name of the file share for SQLite data"
  value       = azurerm_storage_share.db_share.name
}
