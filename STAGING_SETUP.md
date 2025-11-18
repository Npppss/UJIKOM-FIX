# 🚀 STAGING ENVIRONMENT SETUP

Dokumentasi untuk setup dan deployment ke staging environment.

## 📋 Prerequisites

1. **AWS Account** dengan akses ke:
   - RDS (PostgreSQL)
   - ElastiCache (Redis)
   - S3
   - ECS (untuk deployment)

2. **Database**: PostgreSQL instance di AWS RDS
3. **Cache**: Redis instance di AWS ElastiCache
4. **Storage**: S3 bucket untuk media files

## 🔧 Setup Lokal

### 1. Switch ke Branch Staging

```bash
git checkout staging
```

### 2. Install Dependencies Tambahan

```bash
pip install django-redis boto3 django-storages
```

Tambahkan ke `requirements.txt`:
```
django-redis>=5.2.0
boto3>=1.28.0
django-storages>=1.14.0
```

### 3. Setup Environment Variables

Copy file `.env.staging.example` ke `.env.staging`:

```bash
cp .env.staging.example .env.staging
```

Edit `.env.staging` dengan nilai yang sesuai:

```env
ENVIRONMENT=staging
SECRET_KEY=your-staging-secret-key
DEBUG=False
ALLOWED_HOSTS=staging.epicvibe.com,*.staging.epicvibe.com

# Database
DB_NAME=epicvibe_staging
DB_USER=epicvibe_staging
DB_PASSWORD=your-password
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=5432

# Redis
REDIS_URL=redis://your-redis-endpoint:6379/1

# AWS S3
USE_S3=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=epicvibe-staging-media
AWS_S3_REGION_NAME=ap-southeast-1

# Email
EMAIL_HOST_USER=novandrae7980@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SITE_URL=https://staging.epicvibe.com

# OpenAI
OPENAI_API_KEY=your-key
```

### 4. Load Environment Variables

Untuk development lokal dengan staging config:

**Windows (PowerShell):**
```powershell
Get-Content .env.staging | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}
$env:ENVIRONMENT="staging"
python manage.py runserver
```

**Linux/Mac:**
```bash
export $(cat .env.staging | grep -v '^#' | xargs)
export ENVIRONMENT=staging
python manage.py runserver
```

## 🗄️ Database Setup

### 1. Create Database

Connect ke PostgreSQL staging:

```bash
psql -h your-rds-endpoint.rds.amazonaws.com -U epicvibe_staging -d postgres
```

```sql
CREATE DATABASE epicvibe_staging;
GRANT ALL PRIVILEGES ON DATABASE epicvibe_staging TO epicvibe_staging;
\q
```

### 2. Run Migrations

```bash
export ENVIRONMENT=staging
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

## 🧪 Testing Staging Locally

1. Set environment variable:
   ```bash
   export ENVIRONMENT=staging
   ```

2. Run server:
   ```bash
   python manage.py runserver
   ```

3. Test dengan staging database dan Redis

## 🚀 Deployment ke AWS Staging

### 1. Build Docker Image

```bash
docker build -t epicvibe-staging:latest .
```

### 2. Tag Image untuk ECR

```bash
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com

docker tag epicvibe-staging:latest <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/epicvibe-staging:latest
```

### 3. Push ke ECR

```bash
docker push <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/epicvibe-staging:latest
```

### 4. Update ECS Service

```bash
aws ecs update-service \
  --cluster epicvibe-staging-cluster \
  --service epicvibe-staging-service \
  --force-new-deployment \
  --region ap-southeast-1
```

## 🔄 Terraform untuk Staging

### 1. Setup Terraform Variables

Edit `infrastructure/terraform/terraform.tfvars.staging`:

```hcl
environment = "staging"
project_name = "epicvibe"
aws_region = "ap-southeast-1"

# Database
db_name = "epicvibe_staging"
db_username = "epicvibe_staging"
db_password = "your-secure-password"

# Domain
domain_name = "staging.epicvibe.com"

# GitHub
github_branch = "staging"
```

### 2. Deploy Infrastructure

```bash
cd infrastructure/terraform
terraform init
terraform workspace select staging
terraform plan -var-file=terraform.tfvars.staging
terraform apply -var-file=terraform.tfvars.staging
```

## 📝 Checklist Staging

- [ ] Branch `staging` dibuat
- [ ] Environment variables di-setup
- [ ] Database PostgreSQL dibuat
- [ ] Redis cache di-setup
- [ ] S3 bucket dibuat
- [ ] Migrations dijalankan
- [ ] Superuser dibuat
- [ ] Static files di-collect
- [ ] Docker image di-build
- [ ] ECS service di-deploy
- [ ] Domain staging di-configure
- [ ] SSL certificate di-setup
- [ ] Monitoring di-configure

## 🔍 Monitoring

- **CloudWatch Logs**: Application logs
- **CloudWatch Metrics**: Performance metrics
- **RDS Monitoring**: Database performance
- **ECS Service**: Container health

## 🐛 Troubleshooting

### Database Connection Error
- Check security groups allow ECS to RDS
- Verify database credentials
- Check RDS endpoint

### Redis Connection Error
- Check ElastiCache security groups
- Verify Redis endpoint
- Check network connectivity

### S3 Upload Error
- Verify IAM roles have S3 permissions
- Check bucket policy
- Verify AWS credentials

## 📚 Resources

- [Django Settings Documentation](https://docs.djangoproject.com/en/4.2/topics/settings/)
- [AWS ECS Deployment](https://docs.aws.amazon.com/ecs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

