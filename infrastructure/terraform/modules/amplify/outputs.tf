output "app_id" {
  description = "Amplify App ID"
  value       = aws_amplify_app.main.id
}

output "domain" {
  description = "Amplify domain"
  value       = aws_amplify_domain_association.main.domain_name
}

