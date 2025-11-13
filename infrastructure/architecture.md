# AWS ARCHITECTURE - EPICVIBE ORGANIZER

## Arsitektur Deployment dengan AWS Amplify

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET / USERS                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AWS CLOUDFRONT CDN                            │
│  - Global Content Delivery                                      │
│  - SSL/TLS Termination                                          │
│  - DDoS Protection                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   AWS AMPLIFY            │  │   APPLICATION LOAD      │
│   (Static Assets)        │  │   BALANCER (ALB)        │
│                          │  │                          │
│  - Static Files (CSS/JS) │  │  - Health Checks         │
│  - Images & Assets       │  │  - SSL Termination       │
│  - Custom Domain         │  │  - Request Routing       │
│  - CI/CD Pipeline        │  │                          │
└──────────────────────────┘  └────────────┬─────────────┘
                                            │
                            ┌───────────────┴───────────────┐
                            │                               │
                            ▼                               ▼
                ┌───────────────────────┐      ┌───────────────────────┐
                │   AWS ECS CLUSTER     │      │   AWS ECS CLUSTER     │
                │   (Production)        │      │   (Staging)            │
                │                       │      │                       │
                │  - Django App         │      │  - Django App         │
                │  - Auto Scaling       │      │  - Auto Scaling       │
                │  - Containerized      │      │  - Containerized      │
                └───────────┬───────────┘      └───────────┬───────────┘
                            │                               │
                            └───────────────┬───────────────┘
                                            │
                            ┌───────────────┴───────────────┐
                            │                               │
                            ▼                               ▼
                ┌───────────────────────┐      ┌───────────────────────┐
                │   AMAZON RDS          │      │   AMAZON S3           │
                │   (PostgreSQL)        │      │   (Media Storage)     │
                │                       │      │                       │
                │  - Multi-AZ           │      │  - Flyers              │
                │  - Automated Backups  │      │  - Certificates        │
                │  - Read Replicas      │      │  - Payment Proofs      │
                └───────────────────────┘      │  - Event Materials     │
                                                └───────────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   AMAZON ELASTICACHE   │
                │   (Redis)             │
                │                       │
                │  - Session Cache       │
                │  - Task Queue          │
                └───────────────────────┘
```

## Komponen Arsitektur Detail

### 1. AWS Amplify (Frontend & Static Assets)
- **Purpose**: Hosting static files, CI/CD untuk frontend assets
- **Features**:
  - Automatic deployments dari Git repository
  - Custom domain dengan SSL certificate
  - CDN integration dengan CloudFront
  - Build pipeline untuk static assets
  - Environment variables management

### 2. Application Load Balancer (ALB)
- **Purpose**: Distribusi traffic ke ECS tasks
- **Features**:
  - Health checks untuk ECS tasks
  - SSL/TLS termination
  - Path-based routing
  - Integration dengan AWS WAF

### 3. Amazon ECS (Elastic Container Service)
- **Purpose**: Menjalankan Django application dalam container
- **Configuration**:
  - Fargate launch type (serverless)
  - Auto Scaling berdasarkan CPU/Memory
  - Task definitions dengan Docker images
  - Service discovery
  - Logging ke CloudWatch

### 4. Amazon RDS (PostgreSQL)
- **Purpose**: Primary database
- **Configuration**:
  - Multi-AZ deployment untuk high availability
  - Automated backups (daily)
  - Read replicas untuk scaling
  - Encryption at rest
  - VPC security groups

### 5. Amazon S3
- **Purpose**: Object storage untuk media files
- **Buckets**:
  - `epicvibe-media` - Flyers, certificates, payment proofs
  - `epicvibe-static` - Static files backup
- **Features**:
  - Lifecycle policies
  - Versioning
  - Cross-region replication (optional)

### 6. Amazon ElastiCache (Redis)
- **Purpose**: Caching dan session storage
- **Configuration**:
  - Redis cluster mode
  - Automatic failover
  - Encryption in transit

### 7. AWS CloudFront
- **Purpose**: Global CDN
- **Features**:
  - Edge locations worldwide
  - SSL/TLS certificates
  - DDoS protection
  - Custom error pages

### 8. VPC (Virtual Private Cloud)
- **Purpose**: Network isolation
- **Configuration**:
  - Public subnets (ALB, NAT Gateway)
  - Private subnets (ECS, RDS, ElastiCache)
  - Internet Gateway
  - NAT Gateway untuk outbound traffic

### 9. Security Components
- **AWS WAF**: Web Application Firewall
- **Security Groups**: Firewall rules
- **IAM Roles**: Access control
- **Secrets Manager**: API keys, database credentials

### 10. Monitoring & Logging
- **CloudWatch**: Metrics, logs, alarms
- **CloudWatch Logs**: Application logging
- **CloudWatch Alarms**: Automated alerting
- **X-Ray**: Distributed tracing (optional)

## Data Flow

### Request Flow:
1. User → CloudFront CDN
2. CloudFront → AWS Amplify (static assets) atau ALB (dynamic content)
3. ALB → ECS Tasks (Django application)
4. Django → RDS (database queries)
5. Django → S3 (media files)
6. Django → ElastiCache (caching)

### Deployment Flow:
1. Developer push code ke GitHub
2. GitHub Actions trigger Terraform (infrastructure)
3. AWS Amplify build static assets
4. ECS service update dengan new Docker image
5. ALB health checks verify new tasks
6. Old tasks drained and terminated

## High Availability

- **Multi-AZ Deployment**: RDS, ECS tasks across multiple AZs
- **Auto Scaling**: ECS tasks scale based on demand
- **Load Balancing**: ALB distributes traffic
- **Database Replicas**: Read replicas for scaling
- **Backup Strategy**: Automated daily backups

## Security

- **Network Isolation**: VPC with private subnets
- **Encryption**: Data at rest (RDS, S3) and in transit (TLS)
- **Access Control**: IAM roles and policies
- **WAF**: Protection against common attacks
- **Secrets Management**: AWS Secrets Manager

## Cost Optimization

- **ECS Fargate**: Pay only for running tasks
- **Auto Scaling**: Scale down during low traffic
- **S3 Lifecycle**: Move old files to Glacier
- **Reserved Instances**: For RDS (optional)
- **CloudFront**: Reduce origin requests

