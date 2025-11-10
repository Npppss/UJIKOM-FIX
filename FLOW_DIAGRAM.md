# DIAGRAM ALUR SISTEM - 3 ROLE

## 1. FLOW REGISTRASI USER

```
[USER] → Buka Halaman Register
    ↓
Isi Form (Nama, Email, Phone, Address, Education, Password)
    ↓
Validasi Password (min 8 karakter, angka, huruf besar/kecil, karakter spesial)
    ↓
[SISTEM]
    - Hash Password (bcrypt)
    - Generate OTP 6 digit atau Link Aktivasi
    - Set Expired: 5 menit dari sekarang
    - Simpan ke database (status: belum verified)
    - Kirim Email Verifikasi
    ↓
[USER] → Cek Email
    ↓
Opsi A: Klik Link Aktivasi
    ↓
[SISTEM] → Validasi Token & Expired Time
    ↓
Jika Valid → Update email_verified_at = NOW()
Jika Invalid/Expired → Tampilkan Error
    ↓
[USER] → Bisa Login

Opsi B: Input OTP
    ↓
[SISTEM] → Validasi OTP & Expired Time (5 menit)
    ↓
Jika Valid → Update email_verified_at = NOW()
Jika Invalid/Expired → Tampilkan Error
    ↓
[USER] → Bisa Login
```

---

## 2. FLOW LOGIN (Semua Role)

```
[USER/ADMIN/EVENT_ORGANIZER] → Buka Halaman Login
    ↓
Input Email & Password
    ↓
[SISTEM] Validasi:
    - Email terdaftar?
    - Password cocok?
    - Role user?
        → Cek email_verified_at != NULL
    ↓
Jika Valid:
    - Create Session Token
    - Set last_activity = NOW()
    - Set expired_at = NOW() + 5 menit
    - Simpan ke tabel sessions
    ↓
Redirect berdasarkan Role:
    - USER → Dashboard User
    - ADMIN → Dashboard Admin  
    - EVENT_ORGANIZER → Dashboard Event Organizer
    ↓
[Middleware] → Setiap Request:
    - Cek session token valid
    - Cek last_activity
    - Jika (NOW() - last_activity) > 5 menit:
        → Destroy session
        → Redirect ke login (Session expired)
    - Jika aktif:
        → Update last_activity = NOW()
        → Update expired_at = NOW() + 5 menit
```

---

## 3. FLOW MEMBUAT KEGIATAN (Admin/Event Organizer)

```
[ADMIN/EVENT_ORGANIZER] → Login
    ↓
Menu: "Tambah Kegiatan"
    ↓
Isi Form:
    - Judul Kegiatan
    - Deskripsi
    - Tanggal Kegiatan
    - Waktu Kegiatan
    - Lokasi
    - Upload Flyer
    - Upload Template Sertifikat (optional)
    ↓
[SISTEM] Validasi:
    - Tanggal Kegiatan >= (TODAY + 3 hari)? → H-3 Rule
    - File flyer valid (ext, size)?
    - Template sertifikat valid (jika ada)?
    ↓
Jika Valid:
    - Upload file flyer → /uploads/flyers/
    - Upload template sertifikat → /uploads/certificates/
    - Set registration_closed_at = event_date + event_time
    - Simpan ke database
    - Status: published (bisa diakses publik)
    ↓
Berhasil → Redirect ke Daftar Kegiatan
```

---

## 4. FLOW PENDAFTARAN KEGIATAN (User)

```
[USER] → Login
    ↓
Menu: "Katalog Kegiatan"
    ↓
[SISTEM] → Tampilkan Kegiatan:
    - Default: Urut berdasarkan (event_date ASC, event_time ASC)
    - Filter: Search berdasarkan keyword (title, description)
    - Filter: Sort (Terbaru, Terlama, Peserta Terbanyak)
    - Hanya tampilkan: status = 'published'
    ↓
[USER] → Pilih Kegiatan
    ↓
Klik "Daftar Kegiatan"
    ↓
[SISTEM] Validasi:
    - Apakah NOW() < registration_closed_at? → Deadline check
    - Apakah user sudah pernah daftar? → UNIQUE(event_id, user_id)
    ↓
Jika Valid:
    - Generate Token 10 digit (random angka, UNIQUE)
    - Simpan ke event_registrations:
        * event_id
        * user_id
        * token
        * status = 'registered'
        * token_sent_at = NOW()
    - Kirim Email ke User dengan Token
    ↓
Berhasil → User terdaftar
```

---

## 5. FLOW DAFTAR HADIR (User)

```
[USER] → Login
    ↓
Menu: "Riwayat Kegiatan"
    ↓
[USER] → Pilih Kegiatan yang sudah didaftarkan (status = 'registered')
    ↓
[SISTEM] Cek:
    - Apakah tanggal sekarang >= event_date?
    - Apakah waktu sekarang >= event_time?
    ↓
Jika SUDAH WAKTU:
    - Tombol "Isi Daftar Hadir" = AKTIF
Jika BELUM WAKTU:
    - Tombol "Isi Daftar Hadir" = DISABLED
    - Tampilkan pesan: "Daftar hadir dapat diisi pada hari H setelah jam kegiatan"
    ↓
[USER] → Klik "Isi Daftar Hadir" (jika aktif)
    ↓
Input Token 10 digit
    ↓
[SISTEM] Validasi:
    - Token cocok dengan token di event_registrations?
    - Token belum digunakan? (status masih 'registered'?)
    ↓
Jika Valid:
    - Update event_registrations:
        * status = 'attended'
        * attendance_at = NOW()
    - Generate Sertifikat (jika ada template)
    - Simpan sertifikat ke tabel certificates
    - Kirim Email Sertifikat ke User (optional)
    ↓
Berhasil → User bisa download sertifikat
```

---

## 6. FLOW DASHBOARD ADMIN

```
[ADMIN] → Login
    ↓
Dashboard Admin
    ↓
[SISTEM] Query Data:

1. Grafik: Jumlah Kegiatan per Bulan
   SELECT 
     MONTH(created_at) as bulan,
     COUNT(*) as jumlah
   FROM events
   WHERE YEAR(created_at) = YEAR(NOW())
   GROUP BY MONTH(created_at)
   
2. Grafik: Jumlah Peserta per Bulan
   SELECT 
     MONTH(attendance_at) as bulan,
     COUNT(*) as jumlah
   FROM event_registrations
   WHERE status = 'attended' 
   AND YEAR(attendance_at) = YEAR(NOW())
   GROUP BY MONTH(attendance_at)
   
3. Top 10 Kegiatan dengan Peserta Terbanyak
   CALL sp_get_top_10_events_by_participants(user_id, 'admin')
    ↓
Tampilkan Grafik (Chart.js / ApexCharts)
    ↓
Menu Lain:
    - Kelola Kegiatan (Semua)
    - Kelola User
    - Kelola Event Organizer
    - Ekspor Data (Semua peserta)
```

---

## 7. FLOW DASHBOARD EVENT ORGANIZER

```
[EVENT_ORGANIZER] → Login
    ↓
Dashboard Event Organizer
    ↓
[SISTEM] Query Data (FILTER: user_id = current_user.id):

1. Grafik: Jumlah Kegiatan per Bulan (HANYA KEGIATAN SENDIRI)
   SELECT 
     MONTH(created_at) as bulan,
     COUNT(*) as jumlah
   FROM events
   WHERE user_id = current_user.id
   AND YEAR(created_at) = YEAR(NOW())
   GROUP BY MONTH(created_at)
   
2. Grafik: Jumlah Peserta per Bulan (HANYA KEGIATAN SENDIRI)
   SELECT 
     MONTH(er.attendance_at) as bulan,
     COUNT(*) as jumlah
   FROM event_registrations er
   JOIN events e ON er.event_id = e.id
   WHERE e.user_id = current_user.id
   AND er.status = 'attended'
   AND YEAR(er.attendance_at) = YEAR(NOW())
   GROUP BY MONTH(er.attendance_at)
   
3. Top 10 Kegiatan dengan Peserta Terbanyak (HANYA KEGIATAN SENDIRI)
   CALL sp_get_top_10_events_by_participants(current_user.id, 'event_organizer')
    ↓
Tampilkan Grafik (Chart.js / ApexCharts)
    ↓
Menu Lain:
    - Kelola Kegiatan (Hanya Kegiatan Sendiri)
    - Ekspor Data (Hanya Peserta Kegiatan Sendiri)
```

---

## 8. FLOW RESET PASSWORD

```
[USER] → Klik "Lupa Password"
    ↓
Input Email
    ↓
[SISTEM] Validasi:
    - Email terdaftar?
    ↓
Jika Valid:
    - Generate Reset Token (random string)
    - Set expired: 1 jam dari sekarang
    - Simpan ke users.reset_password_token
    - Simpan ke users.reset_password_expired
    - Kirim Email dengan Link Reset Password
    ↓
[USER] → Cek Email & Klik Link
    ↓
[SISTEM] Validasi:
    - Token valid?
    - Token belum expired?
    ↓
Jika Valid → Tampilkan Form Input Password Baru
    ↓
[USER] → Input Password Baru & Konfirmasi
    ↓
[SISTEM] Validasi:
    - Password sesuai kriteria? (min 8 karakter, angka, huruf besar/kecil, spesial)
    - Password = Konfirmasi Password?
    ↓
Jika Valid:
    - Hash Password Baru (bcrypt)
    - Update users.password
    - Hapus reset_password_token dan reset_password_expired
    ↓
Berhasil → Redirect ke Login
```

---

## 9. FLOW EKSPOR DATA

### Admin Ekspor:
```
[ADMIN] → Dashboard
    ↓
Menu: "Ekspor Data"
    ↓
Pilih Format: XLS atau CSV
    ↓
[SISTEM] Query:
   SELECT 
     e.title as 'Nama Kegiatan',
     e.event_date as 'Tanggal Kegiatan',
     e.event_time as 'Waktu Kegiatan',
     e.location as 'Lokasi',
     u.name as 'Nama Peserta',
     u.email as 'Email',
     u.phone as 'No HP',
     u.address as 'Alamat',
     er.status as 'Status',
     er.created_at as 'Tanggal Daftar',
     er.attendance_at as 'Tanggal Hadir'
   FROM event_registrations er
   JOIN events e ON er.event_id = e.id
   JOIN users u ON er.user_id = u.id
   ORDER BY e.event_date DESC, u.name ASC
    ↓
Generate File (XLS/CSV)
    ↓
Download File
```

### Event Organizer Ekspor:
```
[EVENT_ORGANIZER] → Dashboard
    ↓
Menu: "Ekspor Data"
    ↓
Pilih Format: XLS atau CSV
    ↓
[SISTEM] Query (FILTER: e.user_id = current_user.id):
   SELECT ... (sama seperti admin)
   WHERE e.user_id = current_user.id
    ↓
Generate File (XLS/CSV)
    ↓
Download File
```

---

## 10. FLOW SESSION TIMEOUT (5 MENIT)

```
[USER/ADMIN/EVENT_ORGANIZER] → Login
    ↓
Session Created:
    - last_activity = NOW()
    - expired_at = NOW() + 5 menit
    ↓
Setiap Request ke Server:
    ↓
[Middleware: SessionTimeoutMiddleware]
    ↓
Cek:
    - Session token valid?
    - last_activity ada?
    - (NOW() - last_activity) > 5 menit?
    ↓
Jika YA (Expired):
    - Destroy session dari database
    - Clear session cookie
    - Redirect ke Login
    - Tampilkan pesan: "Session expired. Silakan login kembali."
    ↓
Jika TIDAK (Masih Aktif):
    - Update last_activity = NOW()
    - Update expired_at = NOW() + 5 menit
    - Lanjutkan request
    ↓
[Response] → User mendapatkan response
```

---

## 11. FLOW AKSES KEGIATAN (Role Check)

### Event Organizer Mengakses/Edit Kegiatan:
```
[EVENT_ORGANIZER] → Login
    ↓
Mengakses/Mengedit Kegiatan (misal: /events/123/edit)
    ↓
[Middleware: EventAccessMiddleware]
    ↓
Cek:
    - User role = 'event_organizer'?
    - event.user_id = current_user.id?
    ↓
Jika YA (Punya Akses):
    - Lanjutkan request
    ↓
Jika TIDAK (Bukan Kegiatan Sendiri):
    - Redirect ke Dashboard
    - Tampilkan Error: "Anda tidak memiliki akses untuk mengelola kegiatan ini"
```

### Admin Mengakses Kegiatan:
```
[ADMIN] → Login
    ↓
Mengakses/Mengedit Kegiatan
    ↓
[Middleware: EventAccessMiddleware]
    ↓
Cek:
    - User role = 'admin'?
    ↓
Jika YA:
    - Bisa akses SEMUA kegiatan
    - Lanjutkan request
```

---

## 12. FLOW MELIHAT KATALOG (Public/User)

```
[PUBLIC/USER] → Buka Katalog Kegiatan
    ↓
[SISTEM] Query:
   SELECT *
   FROM events
   WHERE status = 'published'
   AND deleted_at IS NULL
   AND registration_closed_at > NOW()  -- Hanya kegiatan yang masih buka pendaftaran
    ↓
Default Sorting:
   ORDER BY event_date ASC, event_time ASC
   -- Kegiatan terdekat waktu di atas
    ↓
Opsi Sorting:
   - Terbaru: ORDER BY event_date DESC
   - Terlama: ORDER BY event_date ASC
   - Peserta Terbanyak: ORDER BY (SELECT COUNT(*) FROM event_registrations WHERE event_id = events.id) DESC
    ↓
Search/Filter:
   - Keyword search: WHERE title LIKE '%keyword%' OR description LIKE '%keyword%'
    ↓
Tampilkan List Kegiatan
    ↓
[USER] (jika sudah login):
    - Tombol "Daftar" (jika belum terdaftar)
    - Status "Sudah Terdaftar" (jika sudah terdaftar)
[PUBLIC]:
    - Tombol "Login untuk Daftar"
```

---

## RINGKASAN PERBEDAAN ROLE

### USER:
- ✅ Register & Login
- ✅ Daftar Kegiatan
- ✅ Isi Daftar Hadir
- ✅ Lihat Sertifikat
- ✅ Riwayat Kegiatan
- ❌ Tidak bisa membuat/edit kegiatan

### ADMIN:
- ✅ Login
- ✅ Buat/Edit/Hapus SEMUA Kegiatan
- ✅ Dashboard Statistik (Semua Data)
- ✅ Ekspor Data (Semua Peserta)
- ✅ Kelola User & Event Organizer
- ❌ Tidak bisa daftar sebagai peserta

### EVENT ORGANIZER:
- ✅ Login
- ✅ Buat/Edit/Hapus KEGIATAN SENDIRI
- ✅ Dashboard Statistik (Data Kegiatan Sendiri)
- ✅ Ekspor Data (Peserta Kegiatan Sendiri)
- ❌ Tidak bisa akses kegiatan orang lain
- ❌ Tidak bisa kelola user

