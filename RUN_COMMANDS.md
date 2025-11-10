# 🚀 COMMAND UNTUK MENJALANKAN PROJECT

## 📦 INSTALASI DEPENDENCIES (Pertama Kali)

```bash
pip install -r requirements.txt
```

---

## 🗄️ SETUP DATABASE

### 1. Buat Migrations
```bash
python manage.py makemigrations
```

### 2. Apply Migrations
```bash
python manage.py migrate
```

---

## 👤 CREATE SUPERUSER (Admin)

```bash
python manage.py createsuperuser
```

Masukkan:
- Email: (contoh: admin@admin.com)
- Password: (minimal 8 karakter, harus ada angka, huruf besar, huruf kecil, karakter spesial)
- Name: (contoh: Admin User)

**Contoh password valid**: `Admin123#`

---

## ▶️ JALANKAN SERVER

```bash
python manage.py runserver
```

Server akan berjalan di: **http://127.0.0.1:8000/**

---

## 🌐 AKSES URL PENTING

Setelah server running, akses:

- **Katalog Kegiatan**: http://127.0.0.1:8000/
- **Register**: http://127.0.0.1:8000/accounts/register/
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 🧪 TESTING API (Optional)

```bash
python test_api.py
```

---

## 📧 TEST EMAIL OTP

1. Jalankan server: `python manage.py runserver`
2. Buka: http://127.0.0.1:8000/accounts/register/
3. Isi form registrasi dengan email valid
4. Submit form
5. Cek email inbox untuk OTP atau link verifikasi

Email akan dikirim dari: **novankecebadai@gmail.com**

---

## 🔧 TROUBLESHOOTING

### Jika ada error "No module named..."
```bash
pip install -r requirements.txt
```

### Jika database error, reset database:
```bash
# Hapus db.sqlite3
del db.sqlite3

# Buat ulang migrations
python manage.py makemigrations
python manage.py migrate
```

### Jika port 8000 sudah digunakan:
```bash
python manage.py runserver 8080
```

---

## 📋 QUICK START (All-in-One)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python manage.py makemigrations
python manage.py migrate

# 3. Create superuser (opsional)
python manage.py createsuperuser

# 4. Run server
python manage.py runserver
```

---

## ✅ CHECKLIST SEBELUM JALAN

- [ ] Dependencies sudah diinstall (`pip install -r requirements.txt`)
- [ ] Database sudah di-migrate (`python manage.py migrate`)
- [ ] Email sudah dikonfigurasi di `settings.py` (sudah ✅)
- [ ] Server berjalan di http://127.0.0.1:8000/

---

**Selamat menjalankan project! 🎉**

