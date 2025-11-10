# 🚀 DJANGO QUICK START GUIDE

Panduan cepat untuk memulai implementasi sistem pendaftaran kegiatan dengan Django.

---

## 📋 PREREQUISITES

- Python 3.8+
- MySQL/MariaDB
- pip (Python package manager)
- Virtual environment (recommended)

---

## 🛠️ INSTALASI

### 1. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
Django>=4.2.0
Pillow>=10.0.0
django-crispy-forms>=2.0
crispy-bootstrap5>=0.7
openpyxl>=3.1.0
pandas>=2.0.0
mysqlclient>=2.1.0  # atau pymysql
python-decouple>=3.8  # untuk environment variables
```

### 3. Create Django Project

```bash
django-admin startproject event_registration .
python manage.py startapp accounts
python manage.py startapp events
python manage.py startapp dashboard
python manage.py startapp registrations
python manage.py startapp certificates
mkdir utils
```

### 4. Setup Database

Buat database MySQL:
```sql
CREATE DATABASE event_registration CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure Settings

Edit `event_registration/settings.py`:
- Set `AUTH_USER_MODEL = 'accounts.User'`
- Configure database
- Configure email settings
- Add installed apps
- Add middleware

### 6. Migrate Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

---

## 📁 STRUKTUR PROJECT

Setelah setup, struktur folder akan seperti ini:

```
event_registration/
├── manage.py
├── requirements.txt
├── .env                    # Environment variables (jangan commit)
├── event_registration/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── middleware.py
│   └── admin.py
├── events/
├── dashboard/
├── registrations/
├── certificates/
├── utils/
├── templates/
├── static/
└── media/
```

---

## 🔑 KONFIGURASI PENTING

### .env File

Buat file `.env` di root project:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=event_registration
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@eventregistration.com
SITE_URL=http://localhost:8000
```

### Settings.py - Install Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'accounts',
    'events',
    'dashboard',
    'registrations',
    'certificates',
]
```

### Settings.py - Custom User Model

```python
AUTH_USER_MODEL = 'accounts.User'
```

### Settings.py - Middleware

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'accounts.middleware.SessionTimeoutMiddleware',  # Custom
    'accounts.middleware.RoleRequiredMiddleware',    # Custom
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### Settings.py - Session Timeout

```python
SESSION_COOKIE_AGE = 300  # 5 menit
SESSION_SAVE_EVERY_REQUEST = True
```

---

## 🏃 RUN DEVELOPMENT SERVER

```bash
python manage.py runserver
```

Akses:
- Frontend: http://localhost:8000
- Admin: http://localhost:8000/admin

---

## 📝 IMPLEMENTASI BERURUT

### Phase 1: Core System ✅

1. ✅ Buat Models (User, Event, EventRegistration, Certificate)
2. ✅ Setup Custom User Model
3. ✅ Buat Forms (Registration, Login, Event)
4. ✅ Buat Views (Auth, Registration, Email Verification)
5. ✅ Setup Middleware (Session Timeout, Role Check)
6. ✅ Setup Email Service

### Phase 2: Event Management

1. ✅ Buat Event CRUD (Create, Read, Update, Delete)
2. ✅ Validasi H-3 untuk pembuatan event
3. ✅ Katalog event publik dengan sorting
4. ✅ Search event

### Phase 3: Registration & Attendance

1. ✅ Pendaftaran event oleh user
2. ✅ Generate token 10 digit
3. ✅ Email token ke user
4. ✅ Validasi deadline pendaftaran
5. ✅ Daftar hadir dengan token
6. ✅ Validasi waktu daftar hadir (hari H)

### Phase 4: Dashboard & Statistik

1. ✅ Dashboard Admin dengan 3 grafik (Chart.js)
2. ✅ Dashboard Event Organizer dengan 3 grafik
3. ✅ Ekspor data ke xls/csv

### Phase 5: Certificate & Additional

1. ✅ Generate sertifikat
2. ✅ Riwayat kegiatan user
3. ✅ Daftar sertifikat user
4. ✅ Reset password
5. ✅ Mobile responsive / PWA

---

## 🧪 TESTING

### Create Test User

```python
python manage.py shell

from accounts.models import User
user = User.objects.create_user(
    email='user@test.com',
    password='Password123#',
    name='Test User',
    phone='081234567890',
    address='Test Address',
    education='S1',
    role='user'
)
```

### Test Admin

```python
from accounts.models import User
admin = User.objects.create_superuser(
    email='admin@test.com',
    password='Admin123#',
    name='Admin User'
)
```

### Test Event Organizer

```python
from accounts.models import User
organizer = User.objects.create_user(
    email='organizer@test.com',
    password='Organizer123#',
    name='Event Organizer',
    phone='081234567890',
    address='Test Address',
    education='S1',
    role='event_organizer',
    email_verified_at=timezone.now()
)
```

---

## 🐛 TROUBLESHOOTING

### Error: No module named 'mysqlclient'

**Solusi:**
```bash
# Windows
pip install mysqlclient

# Atau gunakan pymysql
pip install pymysql

# Di settings.py, tambahkan di atas:
import pymysql
pymysql.install_as_MySQLdb()
```

### Error: Email tidak terkirim

**Solusi:**
- Cek SMTP settings di settings.py
- Untuk Gmail, gunakan App Password (bukan password biasa)
- Untuk development, gunakan console backend:
  ```python
  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
  ```

### Error: Static files tidak muncul

**Solusi:**
```bash
python manage.py collectstatic
```

### Error: Media files tidak muncul di development

**Pastikan di urls.py:**
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📚 REFERENSI DOKUMENTASI

### File-file Dokumentasi:

1. **DJANGO_IMPLEMENTATION.md** - Dokumentasi lengkap implementasi Django
   - Models
   - Views
   - Forms
   - Middleware
   - Services

2. **DJANGO_SETTINGS_AND_URLS.md** - Konfigurasi Settings & URLs
   - Settings.py lengkap
   - URLs configuration
   - Email service
   - Token service
   - Export service

3. **LOGIKA_SISTEM_3_ROLE.md** - Logika sistem dan business rules
   - Struktur role
   - Alur sistem
   - Validasi

4. **database_schema.sql** - Schema database (referensi)
   - Tabel-tabel
   - Indexes
   - Triggers

5. **FLOW_DIAGRAM.md** - Diagram alur sistem
   - Flow registrasi
   - Flow login
   - Flow pendaftaran
   - Flow daftar hadir

---

## 🎯 NEXT STEPS

1. ✅ Baca `DJANGO_IMPLEMENTATION.md` untuk implementasi lengkap
2. ✅ Ikuti Phase 1-5 untuk implementasi berurutan
3. ✅ Setup email service untuk production
4. ✅ Buat templates HTML dengan Bootstrap 5
5. ✅ Implement Chart.js untuk dashboard statistik
6. ✅ Setup PWA untuk mobile responsive

---

## 💡 TIPS

1. **Development**: Gunakan `DEBUG=True` dan console email backend
2. **Production**: Set `DEBUG=False` dan gunakan SMTP email
3. **Security**: Jangan commit `.env` file
4. **Performance**: Gunakan `select_related()` dan `prefetch_related()` untuk query optimization
5. **Testing**: Buat unit test untuk setiap fitur

---

**Happy Coding! 🚀**

