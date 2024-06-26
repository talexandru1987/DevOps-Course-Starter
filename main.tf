terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
        resource_group_name  = "Cohort28_AleTan_ProjectExercise"
        storage_account_name = "alexstorageex13"
        container_name       = "bacpac1"
        key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-terraformToDo"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image     = "appsvcsample/python-helloworld"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGODB_CONNECTION_STRING"  = var.mongodb_connection_string
    "FLASK_APP"                  = var.flask_app
    "FLASK_ENV"                  = var.flask_env
    "SECRET_KEY"                 = var.secret_key
    "OAUTH_ID"                   = var.oauth_client_id
    "OAUTH_KEY"                  = var.oauth_client_secret
    "OAUTH_URL"                  = var.oauth_url
    "ENV"                        = var.env
    "LOGIN_DISABLED"             = var.login_disabled
  }
}

// Cosmos account
resource "azurerm_cosmosdb_account" "terraCosmos" {
  name                = "${var.prefix}-cosmosdb"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableServerless"
  }
  
  capabilities {
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "terraDatabase" {
  name                = "ToDo-Database"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.terraCosmos.name
}

resource "azurerm_cosmosdb_mongo_collection" "todo_boards" {
  name                = "todo-boards"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.terraCosmos.name
  database_name       = azurerm_cosmosdb_mongo_database.terraDatabase.name

  index {
    keys = ["_id"]
  }
}

resource "azurerm_cosmosdb_mongo_collection" "todo_cards" {
  name                = "todo-cards"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.terraCosmos.name
  database_name       = azurerm_cosmosdb_mongo_database.terraDatabase.name

  index {
    keys = ["_id"]
  }
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
