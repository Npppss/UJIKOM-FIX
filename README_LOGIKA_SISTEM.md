# 📚 DOKUMENTASI LOGIKA SISTEM PENDAFTARAN KEGIATAN - 3 ROLE

Sistem pendaftaran kegiatan/event dengan 3 role: **USER**, **ADMIN**, dan **EVENT ORGANIZER**.

---

## 📋 DAFTAR DOKUMENTASI

### 1. **[LOGIKA_SISTEM_3_ROLE.md](./LOGIKA_SISTEM_3_ROLE.md)**
Dokumentasi utama yang berisi:
- Struktur dan tugas masing-masing role
- Alur pendaftaran kegiatan
- Alur registrasi dan login
- Struktur database
- Middleware & validasi
- Dashboard statistik
- Fitur ekspor data
- Pengurutan katalog kegiatan
- Session timeout
- Keamanan password
- Reset password
- Mobile responsive / PWA
- Rekomendasi struktur folder
- Prioritas implementasi

### 2. **[database_schema.sql](./database_schema.sql)**
Schema database lengkap dengan:
- Tabel `users` (3 role)
- Tabel `events` (kegiatan)
- Tabel `event_registrations` (pendaftaran peserta)
- Tabel `sessions` (session timeout)
- Tabel `certificates` (sertifikat)
- Tabel `activity_logs` (opsional)
- Trigger untuk auto-set `registration_closed_at`
- View untuk statistik
- Stored procedure untuk top 10 events
- Index untuk performa query
- Seed data admin default

### 3. **[FLOW_DIAGRAM.md](./FLOW_DIAGRAM.md)**
Diagram alur untuk:
- Flow registrasi user
- Flow login (semua role)
- Flow membuat kegiatan (Admin/Event Organizer)
- Flow pendaftaran kegiatan (User)
- Flow daftar hadir (User)
- Flow dashboard Admin
- Flow dashboard Event Organizer
- Flow reset password
- Flow ekspor data
- Flow session timeout
- Flow akses kegiatan (role check)
- Flow melihat katalog (public/user)

### 4. **[IMPLEMENTASI_MIDDLEWARE.md](./IMPLEMENTASI_MIDDLEWARE.md)**
Contoh implementasi:
- Authentication Middleware
- Session Timeout Middleware
- Role Middleware
- Event Access Middleware
- Email Verification Middleware
- Registration Deadline Validation
- Event Creation Validation (H-3)
- Attendance Validation (Hari H)
- Password Validation
- Email Service
- Token Generation Service
- Dashboard Statistics Service
- Contoh Route Definition

### 5. **[RINGKASAN_PERBANDINGAN_ROLE.md](./RINGKASAN_PERBANDINGAN_ROLE.md)**
Perbandingan detail 3 role:
- Tabel perbandingan fitur
- Perbedaan utama dalam implementasi
- Contoh kasus penggunaan
- Struktur menu berdasarkan role
- Catatan penting untuk developer
- Testing scenarios
- Kesimpulan

---

## 🚀 QUICK START

### Langkah Implementasi:

1. **Setup Database**
   ```bash
   # Import schema
   mysql -u username -p database_name < database_schema.sql
   ```

2. **Baca Dokumentasi Utama**
   - Baca `LOGIKA_SISTEM_3_ROLE.md` untuk memahami struktur sistem
   - Baca `RINGKASAN_PERBANDINGAN_ROLE.md` untuk memahami perbedaan role

3. **Implementasi Phase 1: Core System**
   - Database schema ✅
   - User registration & login (3 role)
   - Email verification (OTP/Link)
   - Password validation & hashing
   - Session management dengan timeout

4. **Implementasi Phase 2: Event Management**
   - CRUD Event (Admin & Event Organizer)
   - Validasi H-3 untuk pembuatan event
   - Katalog event publik dengan sorting
   - Search event

5. **Implementasi Phase 3: Registration & Attendance**
   - Pendaftaran event oleh user
   - Generate token 10 digit
   - Email token ke user
   - Validasi deadline pendaftaran
   - Daftar hadir dengan token
   - Validasi waktu daftar hadir (hari H)

6. **Implementasi Phase 4: Dashboard & Statistik**
   - Dashboard Admin dengan 3 grafik
   - Dashboard Event Organizer dengan 3 grafik
   - Ekspor data ke xls/csv

7. **Implementasi Phase 5: Certificate & Additional**
   - Generate sertifikat
   - Riwayat kegiatan user
   - Daftar sertifikat user
   - Reset password
   - Mobile responsive / PWA

---

## 🔑 POIN PENTING

### Perbedaan 3 Role:

| Aspek | USER | ADMIN | EVENT ORGANIZER |
|-------|------|-------|-----------------|
| **Membuat Kegiatan** | ❌ | ✅ Semua | ✅ Sendiri |
| **Mengelola Kegiatan** | ❌ | ✅ Semua | ✅ Sendiri |
| **Statistik Dashboard** | ❌ | ✅ Semua Data | ✅ Data Sendiri |
| **Ekspor Data** | ❌ | ✅ Semua Peserta | ✅ Peserta Sendiri |
| **Daftar Kegiatan** | ✅ | ❌ | ❌ |

### Validasi Penting:

1. **H-3 Rule**: Admin & Event Organizer hanya bisa buat kegiatan maksimal H-3
2. **Registration Deadline**: Pendaftaran tutup saat jam kegiatan dimulai
3. **Attendance**: Daftar hadir hanya bisa diisi pada hari H setelah jam kegiatan
4. **Session Timeout**: 5 menit tidak aktif = auto logout
5. **Email Verification**: User wajib verifikasi email sebelum bisa login
6. **Password**: Min 8 karakter, angka, huruf besar/kecil, karakter spesial

### Middleware Wajib:

1. `AuthMiddleware` - Cek login
2. `SessionTimeoutMiddleware` - Update last_activity setiap request
3. `RoleMiddleware` - Filter akses berdasarkan role
4. `EventAccessMiddleware` - Event Organizer hanya akses event sendiri
5. `EmailVerificationMiddleware` - User wajib verifikasi email

---

## 📊 STRUKTUR DATABASE UTAMA

```
users
  ├── id
  ├── email (unique)
  ├── password (hashed)
  ├── role (user/admin/event_organizer)
  └── email_verified_at

events
  ├── id
  ├── user_id (pembuat: admin atau event_organizer)
  ├── title
  ├── event_date
  ├── event_time
  ├── registration_closed_at (auto set)
  └── deleted_at (soft delete)

event_registrations
  ├── id
  ├── event_id
  ├── user_id
  ├── token (10 digit, unique)
  ├── status (registered/attended/absent)
  └── attendance_at

sessions
  ├── id
  ├── user_id
  ├── token
  ├── last_activity
  └── expired_at (last_activity + 5 menit)

certificates
  ├── id
  ├── event_registration_id
  ├── event_id
  ├── user_id
  └── certificate_path
```

---

## 🔒 KEAMANAN

### Password:
- Hash dengan bcrypt (cost: 10)
- Validasi: `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/`

### Email Verification:
- OTP atau Link Aktivasi
- Expired: 5 menit dari request pertama
- Tidak bisa login sebelum verified

### Session:
- Session token disimpan di database
- Auto logout jika tidak aktif 5 menit
- Update `last_activity` setiap request

### Access Control:
- Role-based access control (RBAC)
- Event Organizer hanya akses data sendiri
- Admin akses semua data

---

## 📱 MOBILE RESPONSIVE / PWA

- Framework CSS: Bootstrap 5 atau Tailwind CSS
- PWA: Service Worker, Manifest.json
- Viewport: meta tag responsive
- Mobile-first design approach

---

## 📞 KONTAK & SUPPORT

Jika ada pertanyaan tentang logika sistem, silakan baca dokumentasi lengkap di:
1. `LOGIKA_SISTEM_3_ROLE.md` - Dokumentasi utama
2. `FLOW_DIAGRAM.md` - Alur sistem
3. `IMPLEMENTASI_MIDDLEWARE.md` - Contoh kode
4. `RINGKASAN_PERBANDINGAN_ROLE.md` - Perbandingan role

---

## 📝 CHANGELOG

### v1.0.0
- ✅ Struktur 3 role (USER, ADMIN, EVENT ORGANIZER)
- ✅ Database schema lengkap
- ✅ Flow diagram semua fitur
- ✅ Middleware & validasi
- ✅ Dokumentasi lengkap

---

**Happy Coding! 🚀**

