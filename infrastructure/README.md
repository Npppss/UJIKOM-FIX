# AWS Infrastructure - EPICVIBE ORGANIZER

Infrastructure as Code (IaC) menggunakan Terraform untuk deployment AWS dengan AWS Amplify.

## Arsitektur

Lihat [architecture.md](./architecture.md) untuk diagram arsitektur lengkap.

## Prerequisites

1. **AWS Account** dengan IAM user yang memiliki permissions:
   - EC2, ECS, RDS, S3, VPC, CloudFront, Amplify, ElastiCache
   - IAM untuk role creation
   - CloudWatch untuk monitoring

2. **Terraform** (>= 1.0)
   ```bash
   terraform version
   ```

3. **AWS CLI** configured
   ```bash
   aws configure
   ```

4. **GitHub Access Token** untuk AWS Amplify

## Struktur Folder

```
infrastructure/
├── terraform/
│   ├── main.tf                 # Main configuration
│   ├── variables.tf            # Variable definitions
│   ├── outputs.tf               # Output values
│   ├── terraform.tfvars.example # Example variables file
│   └── modules/
│       ├── vpc/                 # VPC module
│       ├── rds/                 # RDS module
│       ├── s3/                  # S3 module
│       ├── ecs/                 # ECS module
│       ├── alb/                 # ALB module
│       ├── cloudfront/          # CloudFront module
│       ├── amplify/             # AWS Amplify module
│       ├── elasticache/         # ElastiCache module
│       ├── secrets/             # Secrets Manager module
│       └── cloudwatch/          # CloudWatch module
├── architecture.md              # Architecture diagram
└── README.md                    # This file
```

## Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd infrastructure/terraform
```

### 2. Create terraform.tfvars

Copy example file dan isi dengan values:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
aws_region = "ap-southeast-1"
environment = "production"
project_name = "epicvibe"

# Database
db_name = "epicvibe_db"
db_username = "epicvibe_admin"
db_password = "YOUR_SECURE_PASSWORD"

# Domain
domain_name = "epicvibe.com"

# GitHub
github_repository_url = "https://github.com/Npppss/UJIKOM-FIX"
github_branch = "main"
github_access_token = "YOUR_GITHUB_TOKEN"

# Django Secrets
django_secret_key = "YOUR_DJANGO_SECRET_KEY"
openai_api_key = "YOUR_OPENAI_API_KEY"
email_password = "YOUR_EMAIL_PASSWORD"
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Plan Deployment

```bash
terraform plan
```

### 5. Apply Infrastructure

```bash
terraform apply
```

## AWS Amplify Configuration

AWS Amplify akan:
- Connect ke GitHub repository
- Build static assets (CSS, JS, images)
- Deploy ke CDN
- Setup custom domain dengan SSL

### Manual Amplify Setup (Alternative)

Jika ingin setup manual:

1. Go to AWS Amplify Console
2. Connect repository (GitHub)
3. Configure build settings:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - npm install -g @aws-amplify/cli
       build:
         commands:
           - python manage.py collectstatic --noinput
     artifacts:
       baseDirectory: staticfiles
       files:
         - '**/*'
   ```
4. Add custom domain
5. Enable auto deployments

## Modules

### VPC Module
- Creates VPC with public and private subnets
- Internet Gateway and NAT Gateway
- Route tables

### RDS Module
- PostgreSQL database
- Multi-AZ deployment
- Automated backups
- Security groups

### S3 Module
- Media bucket for uploads
- Static files bucket
- Lifecycle policies

### ECS Module
- ECS Cluster
- Fargate tasks
- Auto Scaling
- Task definitions
- Service definitions

### ALB Module
- Application Load Balancer
- Target groups
- Listeners
- Security groups

### CloudFront Module
- CloudFront distribution
- Origin configuration
- SSL certificates

### Amplify Module
- Amplify app
- Branch configuration
- Domain association

### ElastiCache Module
- Redis cluster
- Security groups

### Secrets Module
- AWS Secrets Manager
- Secure storage for credentials

### CloudWatch Module
- Log groups
- Alarms
- Dashboards

## Deployment Workflow

1. **Infrastructure Setup** (Terraform):
   ```bash
   terraform apply
   ```

2. **Build Docker Image**:
   ```bash
   docker build -t epicvibe:latest .
   docker tag epicvibe:latest <ECR_REPO_URL>:latest
   docker push <ECR_REPO_URL>:latest
   ```

3. **Update ECS Service**:
   ```bash
   aws ecs update-service --cluster epicvibe-cluster --service epicvibe-service --force-new-deployment
   ```

4. **Amplify Auto-Deploy**:
   - Push to GitHub triggers automatic build
   - Static assets deployed automatically

## Cost Estimation

- **ECS Fargate**: ~$50-100/month (2 tasks, 0.5 vCPU, 1GB RAM each)
- **RDS PostgreSQL**: ~$100-200/month (db.t3.medium, Multi-AZ)
- **S3**: ~$10-20/month (storage + requests)
- **CloudFront**: ~$5-15/month (data transfer)
- **ALB**: ~$20/month
- **ElastiCache**: ~$30-50/month (cache.t3.micro)
- **Amplify**: Free tier, then ~$15/month
- **Data Transfer**: ~$10-30/month

**Total Estimated**: ~$250-450/month

## Monitoring

- CloudWatch Dashboards
- CloudWatch Alarms
- Application logs in CloudWatch Logs
- X-Ray for distributed tracing (optional)

## Security

- VPC with private subnets
- Security groups
- IAM roles with least privilege
- Secrets Manager for sensitive data
- WAF for web protection
- SSL/TLS encryption

## Backup & Disaster Recovery

- RDS automated backups (7 days retention)
- S3 versioning enabled
- Multi-AZ deployment
- Terraform state in S3

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

**Warning**: This will delete all resources including databases!

## Troubleshooting

### ECS Tasks Not Starting
- Check CloudWatch Logs
- Verify security groups
- Check task definition
- Verify IAM roles

### Amplify Build Failing
- Check build logs in Amplify Console
- Verify build_spec configuration
- Check environment variables

### Database Connection Issues
- Verify security groups allow ECS to RDS
- Check RDS endpoint
- Verify credentials in Secrets Manager

## Support

Untuk pertanyaan atau issues, silakan buat issue di repository.

