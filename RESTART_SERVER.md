# 🔄 CARA RESTART SERVER DENGAN BENAR

## ⚠️ MASALAH
Error 404 karena server masih menggunakan project lama (`event_management`).

## ✅ SOLUSI

### 1. Stop Server yang Berjalan
Tekan `CTRL + C` di terminal yang menjalankan server, atau:
```bash
# Windows PowerShell
Get-Process python | Stop-Process -Force
```

### 2. Clear Cache
```bash
# Hapus pyc files dan __pycache__
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
```

### 3. Restart Server
```bash
python manage.py runserver
```

### 4. Verifikasi
Buka: http://127.0.0.1:8000/accounts/register/

---

## 🔍 VERIFIKASI URL

URL yang seharusnya tersedia:
- ✅ `/accounts/register/` - Register
- ✅ `/accounts/login/` - Login
- ✅ `/accounts/logout/` - Logout
- ✅ `/` - Katalog kegiatan
- ✅ `/events/` - Event management
- ✅ `/dashboard/` - Dashboard

---

## 📝 CATATAN

Pastikan:
1. Server di-stop dulu sebelum restart
2. Tidak ada server lain yang berjalan di port 8000
3. Menggunakan project `event_registration` bukan `event_management`

