# AWS Amplify App
resource "aws_amplify_app" "main" {
  name       = "${var.project_name}-${var.environment}"
  repository = var.repository_url
  branch     = var.branch_name

  # Build specification
  build_spec = <<-EOT
    version: 1
    frontend:
      phases:
        preBuild:
          commands:
            - npm install -g @aws-amplify/cli
        build:
          commands:
            - echo "Building static assets..."
            - python manage.py collectstatic --noinput
      artifacts:
        baseDirectory: staticfiles
        files:
          - '**/*'
  EOT

  # Environment variables
  environment_variables = {
    ENVIRONMENT = var.environment
    PROJECT     = var.project_name
  }

  # Custom domain
  custom_rule {
    source = "/<*>"
    target = "/index.html"
    status = "200"
  }

  tags = {
    Name        = "${var.project_name}-amplify-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
  }
}

# AWS Amplify Branch (main branch)
resource "aws_amplify_branch" "main" {
  app_id      = aws_amplify_app.main.id
  branch_name = var.branch_name

  enable_auto_build = true
  enable_pull_request_preview = true

  environment_variables = {
    ENVIRONMENT = var.environment
  }
}

# AWS Amplify Domain Association
resource "aws_amplify_domain_association" "main" {
  app_id      = aws_amplify_app.main.id
  domain_name = var.domain_name

  # Subdomain for static assets
  sub_domain {
    branch_name = aws_amplify_branch.main.branch_name
    prefix      = "static"
  }

  # Wait for domain verification
  wait_for_verification = true
}

# Outputs
output "app_id" {
  description = "Amplify App ID"
  value       = aws_amplify_app.main.id
}

output "domain" {
  description = "Amplify domain"
  value       = aws_amplify_domain_association.main.domain_name
}

