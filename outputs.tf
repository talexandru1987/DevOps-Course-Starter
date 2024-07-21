output "webapp_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "cd_webhook" {
  value       = "https://${azurerm_linux_web_app.main.site_credential[0].name}:${azurerm_linux_web_app.main.site_credential[0].password}@${azurerm_linux_web_app.main.name}.scm.azurewebsites.net/docker/hook"
  sensitive   = true
}

output "cosmosdb_account_endpoint" {
  value = azurerm_cosmosdb_account.terraCosmos.endpoint
}

output "cosmosdb_database_id" {
  value = azurerm_cosmosdb_mongo_database.terraDatabase.id
}

output "cosmosdb_todo_boards_collection_id" {
  value = azurerm_cosmosdb_mongo_collection.todo_boards.id
}

output "cosmosdb_todo_cards_collection_id" {
  value = azurerm_cosmosdb_mongo_collection.todo_cards.id
}