# LOGIKA SISTEM PENDAFTARAN KEGIATAN/EVENT - 3 ROLE

## STRUKTUR ROLE

### 1. USER (Peserta)
**Tugas dan Akses:**
- Mendaftar akun dengan verifikasi email/OTP
- Login ke sistem
- Melihat katalog kegiatan publik
- Mencari kegiatan berdasarkan kata kunci
- Mendaftar mengikuti kegiatan (mendapat token 10 digit)
- Mengisi daftar hadir dengan token (hanya pada hari H setelah jam kegiatan)
- Melihat sertifikat kegiatan yang diikuti
- Melihat riwayat kegiatan yang pernah diikuti
- Reset password jika lupa

**Pembatasan:**
- Satu email hanya untuk satu akun
- Akun belum terverifikasi tidak bisa login
- Pendaftaran kegiatan maksimal hingga waktu kegiatan dimulai
- Daftar hadir hanya bisa diisi pada hari H setelah jam kegiatan

---

### 2. ADMIN
**Tugas dan Akses:**
- Login ke dashboard admin
- Membuat kegiatan/event (maksimal H-3 dari tanggal kegiatan)
- Mengelola SEMUA kegiatan (edit, hapus, lihat)
- Melihat dashboard dengan statistik:
  - Grafik batang: Jumlah kegiatan per bulan (Jan-Des)
  - Grafik batang: Jumlah peserta per bulan (Jan-Des)
  - Top 10 kegiatan dengan peserta terbanyak
- Ekspor data peserta ke xls/csv (semua kegiatan)
- Mengelola user dan event organizer
- Melihat semua data peserta

**Pembatasan:**
- Membuat kegiatan maksimal H-3 dari tanggal kegiatan

---

### 3. EVENT ORGANIZER
**Tugas dan Akses:**
- Login ke dashboard event organizer
- Membuat kegiatan/event (maksimal H-3 dari tanggal kegiatan)
- Mengelola KEGIATAN SENDIRI (edit, hapus, lihat)
- Melihat dashboard dengan statistik:
  - Grafik batang: Jumlah kegiatan per bulan (HANYA KEGIATAN SENDIRI)
  - Grafik batang: Jumlah peserta per bulan (HANYA KEGIATAN SENDIRI)
  - Top 10 kegiatan dengan peserta terbanyak (HANYA KEGIATAN SENDIRI)
- Ekspor data peserta ke xls/csv (HANYA KEGIATAN SENDIRI)
- Melihat data peserta kegiatan yang dibuatnya
- Mengirimkan sertifikat ke peserta

**Pembatasan:**
- Hanya bisa mengelola kegiatan yang dibuatnya sendiri
- Membuat kegiatan maksimal H-3 dari tanggal kegiatan

---

## PERBEDAAN UTAMA ADMIN vs EVENT ORGANIZER

| Fitur | ADMIN | EVENT ORGANIZER |
|-------|-------|-----------------|
| Mengelola Kegiatan | Semua kegiatan | Hanya kegiatan sendiri |
| Statistik Dashboard | Semua data | Hanya data kegiatan sendiri |
| Ekspor Data | Semua peserta | Hanya peserta kegiatan sendiri |
| Mengelola User | Ya (full access) | Tidak |
| Mengelola Event Organizer | Ya | Tidak |

---

## ALUR PENDAFTARAN KEGIATAN

### 1. ADMIN/EVENT ORGANIZER Membuat Kegiatan
```
1. Login sebagai Admin/Event Organizer
2. Masuk ke menu "Tambah Kegiatan"
3. Isi form:
   - Judul Kegiatan
   - Tanggal Kegiatan (validasi: minimal H-3)
   - Waktu/Jam Kegiatan
   - Lokasi Kegiatan
   - Upload Flyer
   - Upload Template Sertifikat (optional)
   - Deskripsi Kegiatan
4. Sistem validasi: Tanggal kegiatan harus minimal 3 hari dari sekarang
5. Simpan kegiatan (status: PUBLIK/DRAFT)
```

### 2. USER Mendaftar Kegiatan
```
1. User login
2. Buka katalog kegiatan (diurutkan: terdekat waktu)
3. Pilih kegiatan yang diinginkan
4. Klik "Daftar Kegiatan"
5. Validasi:
   - Apakah waktu pendaftaran masih dibuka? (maksimal hingga jam kegiatan dimulai)
   - Apakah user sudah pernah mendaftar?
6. Sistem generate token 10 digit (random angka)
7. Token dikirim ke email user
8. User terdaftar sebagai peserta kegiatan
9. Status: TERDAFTAR (belum hadir)
```

### 3. USER Isi Daftar Hadir
```
1. User login
2. Buka riwayat kegiatan
3. Pilih kegiatan yang sudah didaftarkan
4. Validasi:
   - Apakah sudah hari H?
   - Apakah sudah mencapai jam kegiatan?
5. Jika valid, tombol "Isi Daftar Hadir" aktif
6. User masukkan token 10 digit
7. Validasi token:
   - Cocokkan dengan token yang dikirim saat pendaftaran
   - Token belum digunakan
8. Jika valid:
   - Update status: HADIR
   - Generate sertifikat (jika ada template)
   - Beri akses untuk download sertifikat
```

---

## ALUR REGISTRASI DAN LOGIN

### Registrasi USER
```
1. User buka halaman register
2. Isi form:
   - Nama Lengkap
   - Email (validasi: belum terdaftar)
   - No. Handphone
   - Alamat Tempat Tinggal
   - Pendidikan Terakhir
   - Password (min 8 karakter: angka, huruf besar, huruf kecil, karakter spesial)
   - Konfirmasi Password
3. Validasi password sesuai kriteria
4. Sistem:
   - Hash password dengan bcrypt
   - Generate OTP atau Link Aktivasi
   - Set expired time: 5 menit
   - Kirim email verifikasi
5. User cek email dan klik link/input OTP
6. Validasi:
   - Cek expired time
   - Cek OTP/link valid
7. Jika valid:
   - Update status user: VERIFIED
   - User bisa login
```

### Login (Semua Role)
```
1. User input email dan password
2. Sistem validasi:
   - Email terdaftar?
   - Password cocok?
   - Status verified? (untuk USER)
3. Jika valid:
   - Create session
   - Set session timeout: 5 menit
   - Redirect berdasarkan role:
     * USER → Dashboard User
     * ADMIN → Dashboard Admin
     * EVENT ORGANIZER → Dashboard Event Organizer
4. Set middleware untuk cek session timeout setiap request
```

---

## STRUKTUR DATABASE

### Table: users
```sql
- id (primary key)
- name (nama lengkap)
- email (unique)
- phone (no handphone)
- address (alamat tempat tinggal)
- education (pendidikan terakhir)
- password (hashed)
- role (ENUM: 'user', 'admin', 'event_organizer')
- email_verified_at (timestamp, NULL jika belum)
- email_verification_token (untuk link aktivasi)
- email_verification_expired (timestamp)
- otp_code (untuk OTP)
- otp_expired (timestamp)
- reset_password_token
- reset_password_expired
- created_at
- updated_at
```

### Table: events (kegiatan)
```sql
- id (primary key)
- user_id (foreign key ke users - pembuat kegiatan, bisa admin atau event_organizer)
- title (judul kegiatan)
- description (deskripsi)
- event_date (tanggal kegiatan)
- event_time (waktu/jam kegiatan)
- location (lokasi)
- flyer_path (path file flyer)
- certificate_template_path (path template sertifikat)
- registration_closed_at (timestamp: event_date + event_time)
- created_at
- updated_at
- deleted_at (soft delete)
```

### Table: event_registrations (pendaftaran peserta)
```sql
- id (primary key)
- event_id (foreign key ke events)
- user_id (foreign key ke users)
- token (10 digit angka acak)
- token_sent_at (timestamp)
- status (ENUM: 'registered', 'attended', 'absent')
- attendance_at (timestamp saat isi daftar hadir)
- created_at
- updated_at
- UNIQUE(event_id, user_id) - satu user hanya bisa daftar sekali per event
```

### Table: sessions (untuk session timeout)
```sql
- id (primary key)
- user_id (foreign key ke users)
- token (session token)
- last_activity (timestamp)
- expired_at (last_activity + 5 menit)
- created_at
- updated_at
```

---

## MIDDLEWARE & VALIDASI

### 1. Authentication Middleware
```
- Cek session token valid
- Cek session expired (5 menit tidak aktif)
- Jika expired: logout dan redirect ke login
```

### 2. Role Middleware
```
- Cek role user sesuai akses halaman
- ADMIN: bisa akses semua
- EVENT ORGANIZER: bisa akses halaman sendiri + kegiatan sendiri
- USER: hanya akses halaman user
```

### 3. Event Access Middleware (untuk Event Organizer)
```
- Saat akses/edit/delete kegiatan:
  - Jika ADMIN: bisa akses semua
  - Jika EVENT ORGANIZER: cek apakah event.user_id = current_user.id
```

### 4. Registration Deadline Middleware
```
- Saat user mendaftar kegiatan:
  - Cek: sekarang < event.registration_closed_at
  - Jika sudah lewat: tolak pendaftaran
```

### 5. Event Creation Validation (H-3)
```
- Saat admin/event organizer membuat kegiatan:
  - Cek: event_date >= today + 3 days
  - Jika kurang dari 3 hari: tolak dengan pesan error
```

### 6. Attendance Validation
```
- Saat user isi daftar hadir:
  - Cek: tanggal sekarang >= event.event_date
  - Cek: waktu sekarang >= event.event_time
  - Cek: token valid dan belum digunakan
```

---

## DASHBOARD STATISTIK

### Admin Dashboard
```
1. Grafik Batang: Jumlah Kegiatan per Bulan
   Query: SELECT MONTH(created_at) as bulan, COUNT(*) as jumlah 
   FROM events WHERE YEAR(created_at) = YEAR(NOW())
   GROUP BY MONTH(created_at)
   (Data: Semua kegiatan)

2. Grafik Batang: Jumlah Peserta per Bulan
   Query: SELECT MONTH(attendance_at) as bulan, COUNT(*) as jumlah
   FROM event_registrations 
   WHERE status = 'attended' AND YEAR(attendance_at) = YEAR(NOW())
   GROUP BY MONTH(attendance_at)
   (Data: Semua peserta yang hadir)

3. Top 10 Kegiatan dengan Peserta Terbanyak
   Query: SELECT e.title, COUNT(er.id) as jumlah_peserta
   FROM events e
   LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'attended'
   GROUP BY e.id
   ORDER BY jumlah_peserta DESC
   LIMIT 10
```

### Event Organizer Dashboard
```
1. Grafik Batang: Jumlah Kegiatan per Bulan (HANYA KEGIATAN SENDIRI)
   Query: SELECT MONTH(created_at) as bulan, COUNT(*) as jumlah 
   FROM events 
   WHERE user_id = current_user.id AND YEAR(created_at) = YEAR(NOW())
   GROUP BY MONTH(created_at)

2. Grafik Batang: Jumlah Peserta per Bulan (HANYA KEGIATAN SENDIRI)
   Query: SELECT MONTH(er.attendance_at) as bulan, COUNT(*) as jumlah
   FROM event_registrations er
   JOIN events e ON er.event_id = e.id
   WHERE e.user_id = current_user.id 
   AND er.status = 'attended' 
   AND YEAR(er.attendance_at) = YEAR(NOW())
   GROUP BY MONTH(er.attendance_at)

3. Top 10 Kegiatan dengan Peserta Terbanyak (HANYA KEGIATAN SENDIRI)
   Query: SELECT e.title, COUNT(er.id) as jumlah_peserta
   FROM events e
   LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'attended'
   WHERE e.user_id = current_user.id
   GROUP BY e.id
   ORDER BY jumlah_peserta DESC
   LIMIT 10
```

---

## FITUR EKSPOR DATA

### Admin Ekspor
```
- File: semua_event_peserta.xls/csv
- Data: Semua peserta dari semua kegiatan
- Kolom: 
  - Nama Kegiatan
  - Tanggal Kegiatan
  - Nama Peserta
  - Email
  - No HP
  - Status (Registered/Attended/Absent)
  - Tanggal Daftar
  - Tanggal Hadir
```

### Event Organizer Ekspor
```
- File: peserta_kegiatan_saya.xls/csv
- Data: Hanya peserta dari kegiatan yang dibuatnya
- Kolom: sama seperti admin
```

---

## PENGURUTAN KATALOG KEGIATAN

### Default Sorting
```
- Urutkan berdasarkan: event_date ASC, event_time ASC
- Kegiatan terdekat waktu ditampilkan pertama
```

### Filter/Sorting Options
```
- Terbaru (event_date DESC)
- Terlama (event_date ASC)
- Peserta Terbanyak (COUNT registrations DESC)
```

---

## SESSION TIMEOUT (5 MENIT)

### Implementasi
```
1. Set session saat login:
   - last_activity = now()
   - expired_at = now() + 5 minutes

2. Middleware check setiap request:
   - Cek last_activity
   - Jika (now() - last_activity) > 5 menit:
     * Destroy session
     * Redirect ke login dengan pesan "Session expired"
   - Jika masih aktif:
     * Update last_activity = now()
     * Update expired_at = now() + 5 minutes
```

---

## KEAMANAN PASSWORD

### Validasi Password
```
Regex: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/

- Minimal 8 karakter
- Harus ada huruf kecil (a-z)
- Harus ada huruf besar (A-Z)
- Harus ada angka (0-9)
- Harus ada karakter spesial (@$!%*?&#)
```

### Hashing Password
```
- Gunakan bcrypt dengan salt rounds minimal 10
- Contoh: bcrypt.hash(password, 10)
```

---

## RESET PASSWORD

### Flow
```
1. User klik "Lupa Password"
2. Input email
3. Sistem:
   - Generate reset token (random string)
   - Set expired: 1 jam
   - Kirim email dengan link reset
4. User klik link di email
5. Sistem validasi token dan expired
6. User input password baru dan konfirmasi
7. Validasi password sesuai kriteria
8. Update password (hash baru)
9. Invalid token (hapus)
```

---

## MOBILE RESPONSIVE / PWA

### Teknologi
```
- Framework: Bootstrap 5 atau Tailwind CSS
- PWA: Service Worker, Manifest.json
- Viewport: meta tag responsive
- Mobile-first design approach
```

---

## REKOMENDASI STRUKTUR FOLDER

```
/project
  /app
    /models
      - User.php
      - Event.php
      - EventRegistration.php
      - Session.php
    /controllers
      /user
        - AuthController.php
        - DashboardController.php
        - EventController.php
        - CertificateController.php
      /admin
        - DashboardController.php
        - EventController.php
        - UserController.php
        - ExportController.php
      /event_organizer
        - DashboardController.php
        - EventController.php
        - ExportController.php
    /middleware
      - AuthMiddleware.php
      - RoleMiddleware.php
      - SessionTimeoutMiddleware.php
    /services
      - EmailService.php
      - TokenService.php
      - CertificateService.php
  /config
    - database.php
    - email.php
  /public
    /assets
    /uploads
      /flyers
      /certificates
  /views
    /user
    /admin
    /event_organizer
```

---

## PRIORITAS IMPLEMENTASI

### Phase 1: Core System
1. Database schema
2. User registration & login (3 role)
3. Email verification (OTP/Link)
4. Password validation & hashing
5. Session management dengan timeout

### Phase 2: Event Management
1. CRUD Event (Admin & Event Organizer)
2. Validasi H-3 untuk pembuatan event
3. Katalog event publik dengan sorting
4. Search event

### Phase 3: Registration & Attendance
1. Pendaftaran event oleh user
2. Generate token 10 digit
3. Email token ke user
4. Validasi deadline pendaftaran
5. Daftar hadir dengan token
6. Validasi waktu daftar hadir (hari H)

### Phase 4: Dashboard & Statistik
1. Dashboard Admin dengan 3 grafik
2. Dashboard Event Organizer dengan 3 grafik
3. Ekspor data ke xls/csv

### Phase 5: Certificate & Additional
1. Generate sertifikat
2. Riwayat kegiatan user
3. Daftar sertifikat user
4. Reset password
5. Mobile responsive / PWA

---

## CATATAN PENTING

1. **Pemisahan Data Event Organizer**: Selalu filter berdasarkan `user_id` saat Event Organizer mengakses data
2. **Validasi Role**: Setiap controller harus cek role sebelum akses
3. **Session Timeout**: Update `last_activity` setiap request yang ter-authenticate
4. **Email Service**: Setup SMTP untuk email verifikasi, token, dan reset password
5. **File Upload**: Validasi jenis file dan ukuran untuk flyer dan sertifikat
6. **Token Unik**: Pastikan token 10 digit unik per pendaftaran
7. **Timezone**: Set timezone sesuai lokasi untuk validasi tanggal/waktu

