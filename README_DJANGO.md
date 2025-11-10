# 📚 README - DJANGO IMPLEMENTATION

Dokumentasi lengkap implementasi Sistem Pendaftaran Kegiatan menggunakan Django Framework dengan 3 Role: **USER**, **ADMIN**, dan **EVENT ORGANIZER**.

---

## 📑 DAFTAR DOKUMENTASI

### 🚀 Getting Started
- **[DJANGO_QUICK_START.md](./DJANGO_QUICK_START.md)** - Panduan cepat setup dan instalasi Django

### 📖 Dokumentasi Implementasi
- **[DJANGO_IMPLEMENTATION.md](./DJANGO_IMPLEMENTATION.md)** - Dokumentasi lengkap implementasi Django
  - Struktur folder Django
  - Django Models (User, Event, EventRegistration, Certificate)
  - Middleware (Session Timeout, Role Check)
  - Forms (Registration, Login, Event, Attendance)
  - Views contoh

- **[DJANGO_SETTINGS_AND_URLS.md](./DJANGO_SETTINGS_AND_URLS.md)** - Konfigurasi lengkap
  - Settings.py lengkap
  - URLs configuration untuk semua app
  - Email Service
  - Token Service
  - Export Service (Excel/CSV)
  - Password Validator
  - Views lengkap (Dashboard, Registrations)
  - Admin Configuration

### 🏗️ Logika Sistem
- **[LOGIKA_SISTEM_3_ROLE.md](./LOGIKA_SISTEM_3_ROLE.md)** - Logika bisnis dan aturan sistem
- **[FLOW_DIAGRAM.md](./FLOW_DIAGRAM.md)** - Diagram alur sistem
- **[RINGKASAN_PERBANDINGAN_ROLE.md](./RINGKASAN_PERBANDINGAN_ROLE.md)** - Perbandingan 3 role

### 🗄️ Database
- **[database_schema.sql](./database_schema.sql)** - Schema database SQL (referensi)

---

## 🎯 QUICK OVERVIEW

### Tech Stack
- **Backend**: Django 4.2+
- **Database**: MySQL/MariaDB
- **Frontend**: Django Templates + Bootstrap 5
- **Authentication**: Custom User Model dengan Django Auth
- **Charts**: Chart.js untuk dashboard statistik
- **Export**: openpyxl (Excel), pandas (CSV)

### Struktur Apps
```
event_registration/
├── accounts/          # Authentication & User Management
├── events/            # Event Management
├── dashboard/         # Dashboard untuk semua role
├── registrations/     # Pendaftaran & Attendance
├── certificates/      # Sertifikat Management
└── utils/            # Utility functions (email, token, export)
```

### 3 Role System

| Role | Deskripsi | Fitur Utama |
|------|-----------|-------------|
| **USER** | Peserta kegiatan | Daftar kegiatan, isi daftar hadir, lihat sertifikat |
| **ADMIN** | Administrator | Kelola semua kegiatan, statistik global, ekspor semua data |
| **EVENT ORGANIZER** | Penyelenggara | Kelola kegiatan sendiri, statistik kegiatan sendiri, ekspor data sendiri |

---

## 🚀 QUICK START

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```sql
CREATE DATABASE event_registration CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure Settings
- Edit `event_registration/settings.py`
- Setup database credentials
- Setup email SMTP

### 4. Migrate
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run Server
```bash
python manage.py runserver
```

**Detail lengkap:** Baca [DJANGO_QUICK_START.md](./DJANGO_QUICK_START.md)

---

## 📋 FITUR UTAMA

### ✅ Authentication & User Management
- [x] Custom User Model dengan 3 role
- [x] Registrasi dengan verifikasi email (OTP/Link)
- [x] Login dengan session timeout 5 menit
- [x] Reset password dengan email
- [x] Password validation (min 8 karakter, kompleks)

### ✅ Event Management
- [x] CRUD Event (Admin & Event Organizer)
- [x] Validasi H-3 untuk pembuatan event
- [x] Katalog event publik dengan sorting
- [x] Search event berdasarkan keyword
- [x] Upload flyer dan template sertifikat

### ✅ Registration & Attendance
- [x] Pendaftaran event oleh user
- [x] Generate token 10 digit unik
- [x] Email token ke user
- [x] Validasi deadline pendaftaran
- [x] Daftar hadir dengan token (hari H)
- [x] Auto-generate sertifikat

### ✅ Dashboard & Statistik
- [x] Dashboard Admin (3 grafik)
- [x] Dashboard Event Organizer (3 grafik)
- [x] Dashboard User (ringkasan)
- [x] Grafik: Jumlah kegiatan per bulan
- [x] Grafik: Jumlah peserta per bulan
- [x] Top 10 kegiatan dengan peserta terbanyak

### ✅ Export Data
- [x] Ekspor ke Excel (xlsx)
- [x] Ekspor ke CSV
- [x] Admin: export semua peserta
- [x] Event Organizer: export peserta kegiatan sendiri

### ✅ Certificate Management
- [x] Generate sertifikat otomatis
- [x] Download sertifikat
- [x] Riwayat sertifikat user

---

## 🔐 KEAMANAN

### Password Policy
- Minimal 8 karakter
- Harus ada huruf kecil (a-z)
- Harus ada huruf besar (A-Z)
- Harus ada angka (0-9)
- Harus ada karakter spesial (@$!%*?&#)

### Session Security
- Session timeout: 5 menit tidak aktif
- Update last_activity setiap request
- Auto logout jika expired

### Email Verification
- OTP atau Link aktivasi
- Expired: 5 menit
- Tidak bisa login sebelum verified (untuk user)

### Access Control
- Role-based access control (RBAC)
- Event Organizer hanya bisa akses event sendiri
- Admin bisa akses semua

---

## 📊 DASHBOARD STATISTIK

### Admin Dashboard
- **Grafik 1**: Jumlah kegiatan per bulan (Jan-Des) - **Semua data**
- **Grafik 2**: Jumlah peserta per bulan (Jan-Des) - **Semua data**
- **Grafik 3**: Top 10 kegiatan dengan peserta terbanyak - **Semua data**

### Event Organizer Dashboard
- **Grafik 1**: Jumlah kegiatan per bulan (Jan-Des) - **Kegiatan sendiri**
- **Grafik 2**: Jumlah peserta per bulan (Jan-Des) - **Kegiatan sendiri**
- **Grafik 3**: Top 10 kegiatan dengan peserta terbanyak - **Kegiatan sendiri**

### User Dashboard
- Total kegiatan terdaftar
- Total kehadiran
- Total sertifikat
- Kegiatan terdekat

---

## 🔄 WORKFLOW

### User Registration Flow
```
1. User register → Validasi password
2. Generate OTP & Link → Kirim email
3. User verifikasi (OTP atau Link)
4. Email verified → Bisa login
```

### Event Registration Flow
```
1. User login → Pilih event
2. Validasi deadline → Generate token 10 digit
3. Kirim token ke email → Status: Registered
4. Hari H → User isi daftar hadir dengan token
5. Validasi token → Status: Attended → Generate sertifikat
```

### Event Creation Flow (Admin/Organizer)
```
1. Login → Buat event
2. Validasi H-3 → Upload flyer
3. Set event_date + event_time → Auto set registration_closed_at
4. Status: Published → Tampil di katalog publik
```

---

## 📁 STRUKTUR FILE DOKUMENTASI

```
📚 Dokumentasi Django
│
├── 📄 README_DJANGO.md (File ini)
│   └── Index dan overview
│
├── 🚀 DJANGO_QUICK_START.md
│   └── Panduan setup cepat
│
├── 📖 DJANGO_IMPLEMENTATION.md
│   ├── Struktur folder
│   ├── Models
│   ├── Middleware
│   ├── Forms
│   └── Views contoh
│
├── ⚙️ DJANGO_SETTINGS_AND_URLS.md
│   ├── Settings.py lengkap
│   ├── URLs configuration
│   ├── Email Service
│   ├── Token Service
│   ├── Export Service
│   └── Views lengkap
│
├── 🏗️ LOGIKA_SISTEM_3_ROLE.md
│   └── Business logic & rules
│
├── 📊 FLOW_DIAGRAM.md
│   └── Diagram alur sistem
│
├── 🔄 RINGKASAN_PERBANDINGAN_ROLE.md
│   └── Perbandingan 3 role
│
└── 🗄️ database_schema.sql
    └── Schema database (referensi)
```

---

## 💻 CONTOH CODE SNIPPETS

### Custom User Model
```python
class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('event_organizer', 'Event Organizer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    # ... fields lainnya
```

### Role Decorator
```python
@login_required
@role_required('admin', 'event_organizer')
def create_event(request):
    # ...
```

### Event Owner Check
```python
@event_owner_required
def edit_event(request, event_id):
    # ...
```

### Session Timeout
```python
SESSION_COOKIE_AGE = 300  # 5 menit
```

---

## 🧪 TESTING

### Create Test Users
```python
# User
user = User.objects.create_user(
    email='user@test.com',
    password='Password123#',
    role='user'
)

# Admin
admin = User.objects.create_superuser(
    email='admin@test.com',
    password='Admin123#'
)

# Event Organizer
organizer = User.objects.create_user(
    email='organizer@test.com',
    password='Organizer123#',
    role='event_organizer'
)
```

---

## 🐛 TROUBLESHOOTING

Lihat section **TROUBLESHOOTING** di [DJANGO_QUICK_START.md](./DJANGO_QUICK_START.md)

---

## 📞 SUPPORT

Untuk pertanyaan atau bantuan:
1. Baca dokumentasi lengkap di file-file di atas
2. Cek `DJANGO_QUICK_START.md` untuk setup
3. Cek `DJANGO_IMPLEMENTATION.md` untuk implementasi detail

---

## 📝 NEXT STEPS

Setelah membaca dokumentasi:
1. ✅ Setup project Django
2. ✅ Implement Models
3. ✅ Implement Views & Forms
4. ✅ Setup Middleware
5. ✅ Buat Templates dengan Bootstrap 5
6. ✅ Implement Dashboard dengan Chart.js
7. ✅ Setup Email Service
8. ✅ Testing
9. ✅ Deploy

---

**Selamat mengembangkan! 🚀**

