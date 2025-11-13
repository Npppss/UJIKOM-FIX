variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "ap-southeast-1" # Singapore
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "epicvibe"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# Database variables
variable "db_name" {
  description = "Database name"
  type        = string
  default     = "epicvibe_db"
  sensitive   = true
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "epicvibe_admin"
  sensitive   = true
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

# Domain
variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = "epicvibe.com"
}

# GitHub
variable "github_repository_url" {
  description = "GitHub repository URL"
  type        = string
  default     = "https://github.com/Npppss/UJIKOM-FIX"
}

variable "github_branch" {
  description = "GitHub branch for deployment"
  type        = string
  default     = "main"
}

variable "github_access_token" {
  description = "GitHub access token for Amplify"
  type        = string
  sensitive   = true
}

# Django Secrets
variable "django_secret_key" {
  description = "Django SECRET_KEY"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
}

variable "email_password" {
  description = "Email SMTP password"
  type        = string
  sensitive   = true
}

