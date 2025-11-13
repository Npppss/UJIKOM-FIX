terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "epicvibe-terraform-state"
    key    = "epicvibe/terraform.tfstate"
    region = "ap-southeast-1"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "EPICVIBE-ORGANIZER"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

# VPC Module
module "vpc" {
  source = "./modules/vpc"
  
  vpc_name             = "${var.project_name}-vpc"
  vpc_cidr             = var.vpc_cidr
  availability_zones   = slice(data.aws_availability_zones.available.names, 0, 2)
  environment          = var.environment
  project_name         = var.project_name
}

# RDS Module
module "rds" {
  source = "./modules/rds"
  
  vpc_id               = module.vpc.vpc_id
  private_subnet_ids   = module.vpc.private_subnet_ids
  db_name              = var.db_name
  db_username          = var.db_username
  db_password          = var.db_password
  environment          = var.environment
  project_name         = var.project_name
}

# S3 Module
module "s3" {
  source = "./modules/s3"
  
  environment  = var.environment
  project_name = var.project_name
}

# ElastiCache Module
module "elasticache" {
  source = "./modules/elasticache"
  
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  environment        = var.environment
  project_name       = var.project_name
}

# ECS Module
module "ecs" {
  source = "./modules/ecs"
  
  vpc_id              = module.vpc.vpc_id
  public_subnet_ids   = module.vpc.public_subnet_ids
  private_subnet_ids  = module.vpc.private_subnet_ids
  alb_security_group  = module.alb.security_group_id
  db_endpoint         = module.rds.db_endpoint
  db_name             = var.db_name
  db_username         = var.db_username
  db_password         = var.db_password
  redis_endpoint      = module.elasticache.redis_endpoint
  s3_bucket_media     = module.s3.media_bucket_name
  environment         = var.environment
  project_name        = var.project_name
  aws_region          = var.aws_region
}

# ALB Module
module "alb" {
  source = "./modules/alb"
  
  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
  environment       = var.environment
  project_name      = var.project_name
  domain_name       = var.domain_name
}

# CloudFront Module
module "cloudfront" {
  source = "./modules/cloudfront"
  
  alb_dns_name      = module.alb.dns_name
  alb_zone_id       = module.alb.zone_id
  domain_name       = var.domain_name
  environment       = var.environment
  project_name      = var.project_name
}

# AWS Amplify Module
module "amplify" {
  source = "./modules/amplify"
  
  repository_url    = var.github_repository_url
  branch_name      = var.github_branch
  domain_name      = var.domain_name
  environment       = var.environment
  project_name      = var.project_name
  access_token      = var.github_access_token
}

# Secrets Manager
module "secrets" {
  source = "./modules/secrets"
  
  db_password       = var.db_password
  django_secret_key = var.django_secret_key
  openai_api_key    = var.openai_api_key
  email_password    = var.email_password
  environment       = var.environment
  project_name       = var.project_name
}

# CloudWatch
module "cloudwatch" {
  source = "./modules/cloudwatch"
  
  environment  = var.environment
  project_name = var.project_name
}

