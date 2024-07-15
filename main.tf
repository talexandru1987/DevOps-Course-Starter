locals {
  oauth_url = "https://${var.prefix}-terraformToDo.azurewebsites.net/.auth/login/github/callback"
}

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
      docker_image_name     = "talexandru87/todo-app:prod"
      docker_registry_url = "https://index.docker.io"
    }
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "FLASK_APP"                  = var.flask_app
    "FLASK_ENV"                  = var.flask_env
    "SECRET_KEY"                 = var.secret_key
    "OAUTH_ID"                   = var.oauth_client_id
    "OAUTH_KEY"                  = var.oauth_client_secret
    "OAUTH_URL"                  = local.oauth_url
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


