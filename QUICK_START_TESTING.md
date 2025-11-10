# 🚀 QUICK START TESTING - ADMIN & EVENT ORGANIZER

## ✅ STATUS SAAT INI
- ✅ **USER Flow**: Lengkap dan berjalan
- ✅ **Test Data**: Sudah dibuat (admin, organizer, events)
- ✅ **Validasi H-3**: Sudah diimplementasi
- ✅ **Dashboard**: Sudah siap dengan 3 grafik

---

## 🎯 LANGKAH SELANJUTNYA

### **STEP 1: Test ADMIN** (10 menit)

#### 1.1 Login Admin
```
URL: http://127.0.0.1:8000/accounts/login/
Email: admin@test.com
Password: Admin123#
```

#### 1.2 Cek Dashboard Admin
```
URL: http://127.0.0.1:8000/dashboard/admin/
✅ Cek: 3 grafik muncul (Events, Participants, Top 10)
```

#### 1.3 Buat Kegiatan Baru
```
URL: http://127.0.0.1:8000/events/create/

Test Case 1: Valid (H-3)
- Tanggal: 3 hari dari sekarang atau lebih
- Expected: ✅ Berhasil dibuat

Test Case 2: Invalid (Kurang dari H-3)
- Tanggal: 2 hari dari sekarang
- Expected: ❌ Error "minimal 3 hari sebelum tanggal penyelenggaraan"
```

#### 1.4 Lihat Daftar Kegiatan
```
URL: http://127.0.0.1:8000/events/list/
✅ Cek: Menampilkan SEMUA kegiatan (admin + organizer)
```

#### 1.5 Export Data
```
Excel: http://127.0.0.1:8000/dashboard/admin/export/?format=xlsx
CSV:   http://127.0.0.1:8000/dashboard/admin/export/?format=csv
✅ Cek: File terdownload dengan data semua peserta
```

---

### **STEP 2: Test EVENT ORGANIZER** (10 menit)

#### 2.1 Login Event Organizer
```
URL: http://127.0.0.1:8000/accounts/login/
Email: organizer@test.com
Password: Organizer123#
```

#### 2.2 Cek Dashboard Organizer
```
URL: http://127.0.0.1:8000/dashboard/organizer/
✅ Cek: 3 grafik muncul (HANYA data kegiatan sendiri)
```

#### 2.3 Buat Kegiatan Baru
```
URL: http://127.0.0.1:8000/events/create/
✅ Test validasi H-3 sama seperti admin
```

#### 2.4 Test Security (PENTING!)
```
1. Coba Edit Kegiatan Admin:
   URL: http://127.0.0.1:8000/events/edit/{admin_event_id}/
   Expected: ❌ DITOLAK (403 atau redirect)

2. Coba Hapus Kegiatan Admin:
   URL: http://127.0.0.1:8000/events/delete/{admin_event_id}/
   Expected: ❌ DITOLAK (403 atau redirect)

3. Lihat Daftar Kegiatan:
   URL: http://127.0.0.1:8000/events/list/
   Expected: ✅ HANYA menampilkan kegiatan sendiri
```

#### 2.5 Export Data (Hanya Kegiatan Sendiri)
```
Excel: http://127.0.0.1:8000/dashboard/organizer/export/?format=xlsx
CSV:   http://127.0.0.1:8000/dashboard/organizer/export/?format=csv
✅ Cek: File hanya berisi data peserta dari kegiatan sendiri
```

---

## 📋 CHECKLIST CEPAT

### Admin
- [ ] Login berhasil
- [ ] Dashboard 3 grafik muncul
- [ ] Buat kegiatan (validasi H-3 ✅)
- [ ] Edit/hapus semua kegiatan
- [ ] Export Excel/CSV berhasil

### Event Organizer
- [ ] Login berhasil
- [ ] Dashboard 3 grafik (hanya sendiri)
- [ ] Buat kegiatan (validasi H-3 ✅)
- [ ] Edit/hapus hanya kegiatan sendiri
- [ ] Tidak bisa edit/hapus kegiatan admin ❌
- [ ] Export Excel/CSV (hanya sendiri)

---

## 🐛 JIKA ADA ERROR

### Grafik tidak muncul
- Cek console browser (F12)
- Cek apakah Chart.js library ter-load
- Cek apakah ada data kegiatan

### Validasi H-3 tidak berfungsi
- Pastikan tanggal minimal 3 hari dari sekarang
- Cek error message di form

### Export tidak berfungsi
- Cek apakah library openpyxl terinstall
- Cek apakah ada data peserta

### Access Denied (403)
- **Expected** untuk organizer yang coba akses kegiatan admin
- **Tidak expected** untuk akses sendiri

---

## 📝 CATAT HASIL TESTING

Setelah testing, catat:
1. ✅ Fitur yang berjalan dengan baik
2. ❌ Fitur yang error
3. 🐛 Bug yang ditemukan
4. 💡 Saran perbaikan

---

## 🎯 SETELAH TESTING INI

1. **Test Fitur User yang Belum**:
   - Daftar kegiatan → dapat token via email
   - Isi daftar hadir dengan token
   - Generate sertifikat

2. **Test Fitur Umum**:
   - Search kegiatan
   - Sort kegiatan
   - Session timeout (5 menit)

3. **Fix Bugs** yang ditemukan

4. **Final Testing** semua flow

---

## 📚 REFERENSI

- **Panduan Lengkap**: `TEST_ADMIN_ORGANIZER.md`
- **Checklist**: `TESTING_CHECKLIST.md`
- **Credentials**: `TEST_CREDENTIALS.md`

