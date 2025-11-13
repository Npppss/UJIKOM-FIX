output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = module.alb.dns_name
}

output "alb_zone_id" {
  description = "ALB hosted zone ID"
  value       = module.alb.zone_id
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_endpoint
  sensitive   = true
}

output "s3_media_bucket" {
  description = "S3 media bucket name"
  value       = module.s3.media_bucket_name
}

output "redis_endpoint" {
  description = "ElastiCache Redis endpoint"
  value       = module.elasticache.redis_endpoint
  sensitive   = true
}

output "amplify_app_id" {
  description = "AWS Amplify App ID"
  value       = module.amplify.app_id
}

output "amplify_domain" {
  description = "AWS Amplify domain"
  value       = module.amplify.domain
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = module.cloudfront.distribution_id
}

output "cloudfront_domain" {
  description = "CloudFront domain name"
  value       = module.cloudfront.domain_name
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = module.ecs.cluster_name
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = module.ecs.service_name
}

