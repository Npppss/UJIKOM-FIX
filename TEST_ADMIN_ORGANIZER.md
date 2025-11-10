# 🧪 PANDUAN TESTING ADMIN & EVENT ORGANIZER

## 📋 STATUS
- ✅ **USER Flow**: Sudah lengkap dan berjalan
- ⏳ **ADMIN**: Siap untuk di-test
- ⏳ **EVENT ORGANIZER**: Siap untuk di-test

---

## 🔐 CREDENTIALS

### 👨‍💼 ADMIN
```
Email: admin@test.com
Password: Admin123#
URL Login: http://127.0.0.1:8000/accounts/login/
```

### 🎯 EVENT ORGANIZER
```
Email: organizer@test.com
Password: Organizer123#
URL Login: http://127.0.0.1:8000/accounts/login/
```

---

## 🧪 TESTING ADMIN

### 1. Login Admin
1. Buka: `http://127.0.0.1:8000/accounts/login/`
2. Masukkan:
   - Email: `admin@test.com`
   - Password: `Admin123#`
3. Klik "Login"
4. **Expected**: Redirect ke `/dashboard/admin/`

### 2. Dashboard Admin - Grafik Statistik
**URL**: `http://127.0.0.1:8000/dashboard/admin/`

**Cek 3 Grafik:**
- ✅ **Grafik 1**: Jumlah Kegiatan per Bulan (Bar Chart)
- ✅ **Grafik 2**: Jumlah Peserta per Bulan (Bar Chart)
- ✅ **Grafik 3**: Top 10 Kegiatan dengan Peserta Terbanyak (Bar Chart)

**Expected**: 
- Semua grafik muncul dengan data
- Jika belum ada data, grafik kosong (normal)

### 3. Buat Kegiatan (Test Validasi H-3)
**URL**: `http://127.0.0.1:8000/events/create/`

**Test Case 1: Valid (H-3 atau lebih)**
- Tanggal kegiatan: **3 hari dari sekarang** atau lebih
- **Expected**: ✅ Berhasil dibuat

**Test Case 2: Invalid (Kurang dari H-3)**
- Tanggal kegiatan: **2 hari dari sekarang**
- **Expected**: ❌ Error: "Admin hanya dapat membuat kegiatan maksimal H-3"

**Test Case 3: Invalid (Hari ini)**
- Tanggal kegiatan: **Hari ini**
- **Expected**: ❌ Error: "Admin hanya dapat membuat kegiatan maksimal H-3"

**Form Fields:**
- Judul Kegiatan
- Deskripsi
- Tanggal Kegiatan
- Waktu Kegiatan
- Lokasi
- Flyer (optional)
- Template Sertifikat (optional)
- Status (draft/published)

### 4. Edit Kegiatan
**URL**: `http://127.0.0.1:8000/events/edit/{event_id}/`

**Test:**
- Edit kegiatan yang dibuat admin
- Edit kegiatan yang dibuat organizer
- **Expected**: Admin bisa edit semua kegiatan

### 5. Hapus Kegiatan
**URL**: `http://127.0.0.1:8000/events/delete/{event_id}/`

**Test:**
- Hapus kegiatan sendiri
- Hapus kegiatan organizer
- **Expected**: Admin bisa hapus semua kegiatan

### 6. Daftar Kegiatan
**URL**: `http://127.0.0.1:8000/events/list/`

**Expected:**
- Menampilkan **SEMUA** kegiatan (admin + organizer)
- Bisa filter, search, sort

### 7. Lihat Peserta
**URL**: `http://127.0.0.1:8000/events/participants/{event_id}/`

**Expected:**
- Menampilkan semua peserta yang terdaftar
- Bisa lihat detail peserta
- Bisa export data peserta

### 8. Export Data (Excel)
**URL**: `http://127.0.0.1:8000/dashboard/admin/export/?format=xlsx`

**Expected:**
- Download file Excel
- Berisi data semua peserta dari semua kegiatan

### 9. Export Data (CSV)
**URL**: `http://127.0.0.1:8000/dashboard/admin/export/?format=csv`

**Expected:**
- Download file CSV
- Berisi data semua peserta dari semua kegiatan

---

## 🧪 TESTING EVENT ORGANIZER

### 1. Login Event Organizer
1. Buka: `http://127.0.0.1:8000/accounts/login/`
2. Masukkan:
   - Email: `organizer@test.com`
   - Password: `Organizer123#`
3. Klik "Login"
4. **Expected**: Redirect ke `/dashboard/organizer/`

### 2. Dashboard Organizer - Grafik Statistik
**URL**: `http://127.0.0.1:8000/dashboard/organizer/`

**Cek 3 Grafik:**
- ✅ **Grafik 1**: Jumlah Kegiatan per Bulan (HANYA KEGIATAN SENDIRI)
- ✅ **Grafik 2**: Jumlah Peserta per Bulan (HANYA KEGIATAN SENDIRI)
- ✅ **Grafik 3**: Top 10 Kegiatan (HANYA KEGIATAN SENDIRI)

**Expected**: 
- Grafik hanya menampilkan data kegiatan yang dibuat oleh organizer ini
- Tidak menampilkan data kegiatan admin atau organizer lain

### 3. Buat Kegiatan (Test Validasi H-3)
**URL**: `http://127.0.0.1:8000/events/create/`

**Test Case 1: Valid (H-3 atau lebih)**
- Tanggal kegiatan: **3 hari dari sekarang** atau lebih
- **Expected**: ✅ Berhasil dibuat

**Test Case 2: Invalid (Kurang dari H-3)**
- Tanggal kegiatan: **2 hari dari sekarang**
- **Expected**: ❌ Error: "Event Organizer hanya dapat membuat kegiatan maksimal H-3"

### 4. Edit Kegiatan Sendiri
**URL**: `http://127.0.0.1:8000/events/edit/{event_id}/`

**Test:**
- Edit kegiatan yang dibuat oleh organizer ini
- **Expected**: ✅ Bisa edit

### 5. Edit Kegiatan Admin (Security Test)
**URL**: `http://127.0.0.1:8000/events/edit/{admin_event_id}/`

**Test:**
- Coba edit kegiatan yang dibuat admin
- **Expected**: ❌ **DITOLAK** - Error 403 atau redirect

### 6. Hapus Kegiatan Sendiri
**URL**: `http://127.0.0.1:8000/events/delete/{event_id}/`

**Test:**
- Hapus kegiatan yang dibuat oleh organizer ini
- **Expected**: ✅ Bisa hapus

### 7. Hapus Kegiatan Admin (Security Test)
**URL**: `http://127.0.0.1:8000/events/delete/{admin_event_id}/`

**Test:**
- Coba hapus kegiatan yang dibuat admin
- **Expected**: ❌ **DITOLAK** - Error 403 atau redirect

### 8. Daftar Kegiatan
**URL**: `http://127.0.0.1:8000/events/list/`

**Expected:**
- Menampilkan **HANYA** kegiatan yang dibuat oleh organizer ini
- Tidak menampilkan kegiatan admin atau organizer lain

### 9. Lihat Peserta
**URL**: `http://127.0.0.1:8000/events/participants/{event_id}/`

**Test:**
- Lihat peserta kegiatan sendiri
- **Expected**: ✅ Bisa lihat

**Test Security:**
- Coba akses peserta kegiatan admin
- **Expected**: ❌ **DITOLAK** - Error 403 atau redirect

### 10. Export Data (Excel) - Hanya Kegiatan Sendiri
**URL**: `http://127.0.0.1:8000/dashboard/organizer/export/?format=xlsx`

**Expected:**
- Download file Excel
- Berisi data peserta **HANYA** dari kegiatan organizer ini
- Tidak ada data peserta dari kegiatan admin

### 11. Export Data (CSV) - Hanya Kegiatan Sendiri
**URL**: `http://127.0.0.1:8000/dashboard/organizer/export/?format=csv`

**Expected:**
- Download file CSV
- Berisi data peserta **HANYA** dari kegiatan organizer ini

---

## 🔍 CHECKLIST TESTING

### Admin Checklist
- [ ] Login berhasil
- [ ] Dashboard menampilkan 3 grafik
- [ ] Buat kegiatan (validasi H-3 berfungsi)
- [ ] Edit semua kegiatan
- [ ] Hapus semua kegiatan
- [ ] Lihat daftar semua kegiatan
- [ ] Lihat peserta semua kegiatan
- [ ] Export Excel berhasil
- [ ] Export CSV berhasil

### Event Organizer Checklist
- [ ] Login berhasil
- [ ] Dashboard menampilkan 3 grafik (hanya kegiatan sendiri)
- [ ] Buat kegiatan (validasi H-3 berfungsi)
- [ ] Edit kegiatan sendiri ✅
- [ ] Edit kegiatan admin ❌ (ditolak)
- [ ] Hapus kegiatan sendiri ✅
- [ ] Hapus kegiatan admin ❌ (ditolak)
- [ ] Lihat daftar kegiatan sendiri
- [ ] Lihat peserta kegiatan sendiri ✅
- [ ] Lihat peserta kegiatan admin ❌ (ditolak)
- [ ] Export Excel (hanya kegiatan sendiri)
- [ ] Export CSV (hanya kegiatan sendiri)

---

## 🐛 TROUBLESHOOTING

### Grafik tidak muncul
- **Cek**: Apakah ada data kegiatan?
- **Cek**: Apakah Chart.js library ter-load?
- **Cek**: Console browser untuk error JavaScript

### Validasi H-3 tidak berfungsi
- **Cek**: Apakah tanggal dihitung dengan benar?
- **Cek**: Apakah timezone sudah benar?

### Export tidak berfungsi
- **Cek**: Apakah library openpyxl/csv terinstall?
- **Cek**: Apakah ada data peserta?

### Access Denied (403)
- **Expected**: Organizer tidak bisa akses kegiatan admin
- **Jika terjadi pada akses sendiri**: Cek middleware dan decorator

---

## 📝 CATATAN TESTING

Setelah testing, catat:
1. Fitur yang berjalan dengan baik ✅
2. Fitur yang error ❌
3. Bug yang ditemukan 🐛
4. Saran perbaikan 💡

---

## 🚀 NEXT STEPS SETELAH TESTING

1. Test fitur User yang belum:
   - Daftar kegiatan → dapat token via email
   - Isi daftar hadir dengan token
   - Generate sertifikat otomatis
   - Download sertifikat

2. Test fitur umum:
   - Search kegiatan
   - Sort kegiatan
   - Session timeout (5 menit)

3. Fix bugs yang ditemukan

4. Final testing semua flow

