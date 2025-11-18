# 🧪 TESTING STAGING ENVIRONMENT

Panduan untuk testing staging environment secara lokal.

## ✅ Status Testing

### Dependencies Installation
- [x] django-redis installed
- [x] boto3 installed
- [x] django-storages installed
- [x] requirements.txt updated

### Configuration
- [x] .env.staging created (for local testing)
- [x] Staging settings updated with fallbacks
- [x] System check passed

### Database
- [x] Migrations ready
- [ ] Run migrations (next step)

### Static Files
- [x] Collectstatic ready
- [ ] Run collectstatic (next step)

## 🚀 Quick Test Commands

### 1. Test Staging Configuration

**Windows PowerShell:**
```powershell
$env:ENVIRONMENT="staging"
python manage.py check
```

**Linux/Mac:**
```bash
export ENVIRONMENT=staging
python manage.py check
```

### 2. Run Migrations

**Windows PowerShell:**
```powershell
$env:ENVIRONMENT="staging"
python manage.py migrate
```

**Linux/Mac:**
```bash
export ENVIRONMENT=staging
python manage.py migrate
```

### 3. Collect Static Files

**Windows PowerShell:**
```powershell
$env:ENVIRONMENT="staging"
python manage.py collectstatic --noinput
```

**Linux/Mac:**
```bash
export ENVIRONMENT=staging
python manage.py collectstatic --noinput
```

### 4. Create Superuser (Optional)

**Windows PowerShell:**
```powershell
$env:ENVIRONMENT="staging"
python manage.py createsuperuser
```

**Linux/Mac:**
```bash
export ENVIRONMENT=staging
python manage.py createsuperuser
```

### 5. Run Development Server

**Windows PowerShell:**
```powershell
$env:ENVIRONMENT="staging"
python manage.py runserver
```

**Linux/Mac:**
```bash
export ENVIRONMENT=staging
python manage.py runserver
```

## 📝 Test Checklist

### Basic Functionality
- [ ] Server starts without errors
- [ ] Homepage loads correctly
- [ ] Login page works
- [ ] Registration works
- [ ] Event listing works
- [ ] Event detail works
- [ ] Event registration works
- [ ] Dashboard loads

### Database
- [ ] Migrations run successfully
- [ ] Database file created (db_staging.sqlite3)
- [ ] Can create users
- [ ] Can create events
- [ ] Can register for events

### Static Files
- [ ] Static files collected
- [ ] CSS loads correctly
- [ ] JavaScript loads correctly
- [ ] Images load correctly

### Cache (if Redis available)
- [ ] Cache works (if REDIS_URL set)
- [ ] Session works with cache

### File Uploads
- [ ] Can upload files (if S3 disabled, uses local)
- [ ] Files saved correctly

## 🔧 Configuration Notes

### Current Setup (Local Testing)
- **Database**: SQLite3 (db_staging.sqlite3)
- **Cache**: Local memory cache (fallback)
- **Storage**: Local file storage
- **Debug**: True (for testing)

### For AWS Staging
- **Database**: PostgreSQL (RDS)
- **Cache**: Redis (ElastiCache)
- **Storage**: S3
- **Debug**: False

## 🐛 Troubleshooting

### Issue: Import Error
**Solution**: Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database Error
**Solution**: Check if database file exists or PostgreSQL is running:
```bash
# For SQLite
ls db_staging.sqlite3

# For PostgreSQL
psql -h localhost -U epicvibe_staging -d epicvibe_staging
```

### Issue: Static Files Not Loading
**Solution**: Run collectstatic:
```bash
python manage.py collectstatic --noinput
```

### Issue: Environment Variable Not Set
**Solution**: Make sure ENVIRONMENT is set:
```powershell
# Windows
$env:ENVIRONMENT="staging"

# Linux/Mac
export ENVIRONMENT=staging
```

## 📊 Next Steps

1. ✅ Dependencies installed
2. ✅ Configuration tested
3. ⏭️ Run migrations
4. ⏭️ Test server
5. ⏭️ Test functionality
6. ⏭️ Prepare for AWS deployment

