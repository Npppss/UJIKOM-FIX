# 🧪 NEXT TESTING STEPS

## ✅ YANG SUDAH DI-TEST (USER)

- [x] Register dengan password valid
- [x] Verifikasi email dengan OTP
- [x] Login
- [x] Dashboard user
- [x] Riwayat kegiatan
- [x] Sertifikat
- [x] Katalog kegiatan
- [x] Reset password

---

## 🎯 YANG PERLU DI-TEST

### 1. TEST ADMIN (Priority: HIGH)

#### Login & Dashboard
- [ ] Login sebagai admin (`admin@test.com` / `Admin123#`)
- [ ] Dashboard admin menampilkan 3 grafik:
  - [ ] Grafik jumlah kegiatan per bulan
  - [ ] Grafik jumlah peserta per bulan
  - [ ] Top 10 kegiatan dengan peserta terbanyak

#### Event Management
- [ ] Buat kegiatan baru (test validasi H-3)
- [ ] Edit kegiatan
- [ ] Hapus kegiatan
- [ ] Lihat peserta semua kegiatan
- [ ] Ekspor data peserta (Excel)
- [ ] Ekspor data peserta (CSV)

#### Validasi
- [ ] Test validasi H-3 (coba buat event kurang dari 3 hari)
- [ ] Test upload flyer
- [ ] Test upload template sertifikat

---

### 2. TEST EVENT ORGANIZER (Priority: HIGH)

#### Login & Dashboard
- [ ] Login sebagai organizer (`organizer@test.com` / `Organizer123#`)
- [ ] Dashboard organizer menampilkan 3 grafik (hanya kegiatan sendiri):
  - [ ] Grafik jumlah kegiatan per bulan
  - [ ] Grafik jumlah peserta per bulan
  - [ ] Top 10 kegiatan dengan peserta terbanyak

#### Event Management
- [ ] Buat kegiatan baru (test validasi H-3)
- [ ] Edit kegiatan sendiri
- [ ] Hapus kegiatan sendiri
- [ ] Coba edit/hapus kegiatan admin (harus ditolak)
- [ ] Lihat peserta kegiatan sendiri
- [ ] Ekspor data peserta (hanya kegiatan sendiri)

---

### 3. TEST USER - FITUR LAINNYA (Priority: MEDIUM)

#### Daftar Kegiatan
- [ ] User login
- [ ] Buka katalog kegiatan
- [ ] Daftar kegiatan yang masih buka
- [ ] Cek email untuk token
- [ ] Cek riwayat kegiatan

#### Attendance (Daftar Hadir)
- [ ] Buka riwayat kegiatan
- [ ] Pilih kegiatan yang sudah lewat (hari H)
- [ ] Isi daftar hadir dengan token
- [ ] Verifikasi token
- [ ] Status berubah menjadi "Hadir"

#### Sertifikat
- [ ] Setelah isi daftar hadir, cek sertifikat
- [ ] Download sertifikat

---

### 4. TEST FITUR UMUM (Priority: MEDIUM)

#### Katalog Kegiatan
- [ ] Search kegiatan berdasarkan keyword
- [ ] Sort kegiatan (Terdekat, Terbaru, Terlama, Peserta Terbanyak)
- [ ] Pagination (jika ada banyak kegiatan)

#### Session Timeout
- [ ] Login sebagai user
- [ ] Tunggu 5 menit tanpa aktivitas
- [ ] Coba akses halaman → harus auto logout

#### Email Service
- [ ] Test email verifikasi (OTP)
- [ ] Test email token pendaftaran
- [ ] Test email reset password

---

## 🚀 QUICK TEST GUIDE

### Test Admin
```bash
1. Login: http://127.0.0.1:8000/accounts/login/
   Email: admin@test.com
   Password: Admin123#

2. Dashboard: http://127.0.0.1:8000/dashboard/admin/
   - Cek 3 grafik muncul

3. Buat Event: http://127.0.0.1:8000/events/create/
   - Test validasi H-3

4. Export: http://127.0.0.1:8000/dashboard/admin/export/?format=excel
```

### Test Event Organizer
```bash
1. Login: http://127.0.0.1:8000/accounts/login/
   Email: organizer@test.com
   Password: Organizer123#

2. Dashboard: http://127.0.0.1:8000/dashboard/organizer/
   - Cek 3 grafik muncul (hanya kegiatan sendiri)

3. Buat Event: http://127.0.0.1:8000/events/create/
   - Test validasi H-3

4. Export: http://127.0.0.1:8000/dashboard/organizer/export/?format=excel
```

### Test User - Daftar Kegiatan
```bash
1. Login sebagai user
2. Katalog: http://127.0.0.1:8000/
3. Pilih kegiatan
4. Klik "Daftar Kegiatan"
5. Cek email untuk token
6. Riwayat: http://127.0.0.1:8000/registrations/history/
```

---

## 📊 TEST DATA YANG SUDAH DIBUAT

Setelah menjalankan `create_test_data.py`:
- ✅ Event 1: Workshop Python (Organizer) - Masih buka pendaftaran
- ✅ Event 2: Seminar Teknologi (Admin) - Masih buka pendaftaran
- ✅ Event 3: Webinar Digital Marketing (Organizer) - Sudah lewat (untuk test attendance)
- ✅ User sudah terdaftar di Event 1 dan Event 3

---

**Silakan test semua fitur di atas!** 🎯

