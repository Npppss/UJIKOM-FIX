# 🎯 PANDUAN TESTING ATTENDANCE & SERTIFIKAT

## ✅ STATUS SAAT INI

### Yang Sudah Berjalan ✅
- ✅ User daftar kegiatan → dapat token via email
- ✅ Email token berhasil dikirim dengan format yang benar
- ✅ Token 10 digit ter-generate dengan benar

### Yang Perlu Di-Test ⏳
- ⏳ User isi daftar hadir dengan token (hari H)
- ⏳ Generate sertifikat otomatis setelah attendance
- ⏳ Download sertifikat

---

## 🧪 TESTING ATTENDANCE

### Prasyarat
1. **Event sudah lewat** (tanggal & waktu sudah terlewati)
2. **User sudah terdaftar** pada event tersebut
3. **User sudah dapat token** via email

### Langkah Testing

#### 1. Cek Event yang Sudah Lewat
```
URL: http://127.0.0.1:8000/registrations/history/
→ Cari event yang tanggal & waktunya sudah lewat
→ Status: "Terdaftar" (belum hadir)
```

#### 2. Isi Daftar Hadir
```
URL: http://127.0.0.1:8000/registrations/attendance/{event_id}/

Test Case 1: Token Valid ✅
- Masukkan token dari email
- Expected: ✅ Berhasil, status berubah menjadi "Hadir"
- Expected: ✅ Sertifikat ter-generate (jika ada template)

Test Case 2: Token Invalid ❌
- Masukkan token yang salah
- Expected: ❌ Error "Token tidak valid"

Test Case 3: Event Belum Mulai ❌
- Coba isi attendance untuk event yang belum mulai
- Expected: ❌ Error "Daftar hadir dapat diisi pada hari H setelah jam kegiatan dimulai"
```

#### 3. Cek Sertifikat
```
URL: http://127.0.0.1:8000/certificates/
→ Cek apakah sertifikat muncul setelah attendance
→ Download sertifikat
```

---

## 📋 CHECKLIST ATTENDANCE

- [ ] Event sudah lewat (tanggal & waktu)
- [ ] User sudah terdaftar
- [ ] User sudah dapat token via email
- [ ] Tombol "Isi Daftar Hadir" muncul di riwayat
- [ ] Form attendance muncul
- [ ] Token valid → berhasil attendance ✅
- [ ] Token invalid → error ❌
- [ ] Event belum mulai → error ❌
- [ ] Status berubah menjadi "Hadir"
- [ ] Sertifikat ter-generate (jika ada template)
- [ ] Sertifikat muncul di halaman certificates
- [ ] Download sertifikat berhasil

---

## 🐛 TROUBLESHOOTING

### Tombol "Isi Daftar Hadir" tidak muncul
- **Cek**: Apakah event sudah lewat? (tanggal & waktu)
- **Cek**: Apakah user sudah terdaftar?
- **Cek**: Apakah sudah mengisi attendance sebelumnya?

### Token tidak valid
- **Cek**: Apakah token yang dimasukkan sesuai dengan email?
- **Cek**: Apakah token sudah digunakan sebelumnya?

### Sertifikat tidak ter-generate
- **Cek**: Apakah event memiliki certificate_template?
- **Cek**: Apakah ada error di console/log?
- **Cek**: Apakah service generate_certificate sudah diimplementasi?

---

## 📝 CATATAN

### Event Test Data
Dari `create_test_data.py`, ada event yang sudah lewat:
- **Event ID 1**: "Webinar Digital Marketing"
  - Tanggal: 1 November 2025 (sudah lewat)
  - Waktu: 10:00
  - User sudah terdaftar dengan token: `3969912781`

### Token dari Email
Token yang dikirim via email adalah token yang harus digunakan untuk attendance.

---

## 🚀 NEXT STEPS

Setelah testing attendance:
1. Test generate sertifikat
2. Test download sertifikat
3. Test fitur admin/organizer yang belum
4. Test fitur umum (search, sort, session timeout)

