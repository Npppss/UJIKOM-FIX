variable "repository_url" {
  description = "GitHub repository URL"
  type        = string
}

variable "branch_name" {
  description = "GitHub branch name"
  type        = string
  default     = "main"
}

variable "domain_name" {
  description = "Domain name for Amplify"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "access_token" {
  description = "GitHub access token"
  type        = string
  sensitive   = true
}

