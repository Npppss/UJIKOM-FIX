# 🔐 TEST CREDENTIALS

## User Accounts untuk Testing

### 👤 USER (Peserta)
- **Email**: (gunakan email yang sudah diregister)
- **Password**: (password yang sudah dibuat)
- **Status**: ✅ Sudah di-test

### 👨‍💼 ADMIN
- **Email**: `admin@test.com`
- **Password**: `Admin123#`
- **Role**: Admin
- **Status**: ⏳ Perlu di-test

### 🎯 EVENT ORGANIZER
- **Email**: `organizer@test.com`
- **Password**: `Organizer123#`
- **Role**: Event Organizer
- **Status**: ⏳ Perlu di-test

---

## Test Scenarios

### 1. Test Admin
1. Login sebagai admin
2. Buat kegiatan (test validasi H-3)
3. Lihat dashboard dengan grafik
4. Ekspor data peserta
5. Kelola semua kegiatan

### 2. Test Event Organizer
1. Login sebagai organizer
2. Buat kegiatan (test validasi H-3)
3. Lihat dashboard dengan grafik (hanya kegiatan sendiri)
4. Ekspor data peserta (hanya kegiatan sendiri)
5. Kelola kegiatan sendiri

### 3. Test User - Daftar Kegiatan
1. Login sebagai user
2. Buka katalog kegiatan
3. Daftar kegiatan
4. Cek email untuk token
5. Isi daftar hadir (jika sudah hari H)

---

## Quick Test Commands

```bash
# Cek semua user
python manage.py shell
>>> from accounts.models import User
>>> User.objects.all().values('email', 'role', 'email_verified_at')

# Cek kegiatan
>>> from events.models import Event
>>> Event.objects.all().values('title', 'user__email', 'event_date')
```

