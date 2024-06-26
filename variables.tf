variable "prefix" {
  description = "The prefix used for all resources in this environment"
  type        = string

  validation {
    condition     = length(var.prefix) <= 43 && length(var.prefix) >= 3 && can(regex("^[a-z0-9-]*$", var.prefix))
    error_message = "The prefix must be between 3 and 43 characters long and can only contain lowercase letters, numbers, and hyphens."
  }
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "Cohort28_AleTan_ProjectExercise"  # Updated to lowercase with hyphens
}

variable "oauth_client_id" {
  description = "OAuth Client ID"
  type        = string
  sensitive   = true
}

variable "oauth_client_secret" {
  description = "OAuth Client Secret"
  type        = string
  sensitive   = true
}

variable "mongodb_connection_string" {
  description = "MongoDB connection string"
  type        = string
  sensitive   = true
}

variable "flask_app" {
  description = "The Flask app entry point"
  type        = string
  default     = "todo_app/app"
}

variable "flask_env" {
  description = "Flask environment"
  type        = string
  default     = "development"
}

variable "secret_key" {
  description = "Secret key for Flask app"
  type        = string
  sensitive   = true
}

variable "oauth_url" {
  description = "OAuth URL"
  type        = string
  default     = "https://anothertodo.azurewebsites.net/.auth/login/github/callback"
}

variable "env" {
  description = "Environment name"
  type        = string
  default     = "local"  # Updated to lowercase
}

variable "login_disabled" {
  description = "Login disabled flag"
  type        = string
  default     = "false"  # Updated to lowercase
}
