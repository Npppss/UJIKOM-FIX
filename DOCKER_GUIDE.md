# 🐳 Panduan Docker - Event Registration System

## Quick Start

### 1. Build dan Jalankan dengan Docker Compose

```bash
# Build dan jalankan container
docker-compose up --build

# Atau jalankan di background
docker-compose up --build -d
```

### 2. Akses Aplikasi

Setelah container berjalan, akses:
- **Website**: http://localhost:8000
- **Admin Dashboard**: http://localhost:8000/dashboard/admin/
- **Django Admin**: http://localhost:8000/admin/ (jika tersedia)

### 3. Login Admin Default

```
Email   : admin@admin.com
Password: Admin123!
```

---

## Cara Mengubah Kredensial Admin

Edit `docker-compose.yml` dan ubah environment variables:

```yaml
environment:
  - DJANGO_SUPERUSER_EMAIL=email_baru@domain.com
  - DJANGO_SUPERUSER_PASSWORD=PasswordBaru123!
```

Lalu rebuild:

```bash
docker-compose down
docker-compose up --build
```

---

## Perintah Docker Berguna

### Melihat Log
```bash
docker-compose logs -f
```

### Masuk ke Container
```bash
docker-compose exec web bash
```

### Menjalankan Perintah Django di Container
```bash
# Membuat migrasi
docker-compose exec web python manage.py makemigrations

# Menjalankan migrasi
docker-compose exec web python manage.py migrate

# Membuat superuser manual
docker-compose exec web python manage.py createsuperuser

# Django shell
docker-compose exec web python manage.py shell
```

### Stop dan Hapus Container
```bash
# Stop container
docker-compose down

# Stop dan hapus volume (data akan hilang)
docker-compose down -v
```

---

## Troubleshooting

### Error: Permission denied
Jika di Linux/Mac, pastikan `docker-entrypoint.sh` executable:
```bash
chmod +x docker-entrypoint.sh
```

### Error: Port 8000 already in use
Stop aplikasi lain yang menggunakan port 8000 atau ubah port di `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Akses via http://localhost:8080
```

### Melihat Database di Container
```bash
docker-compose exec web python manage.py dbshell
```

---

## Konfigurasi Production

Untuk production, ubah `docker-compose.yml`:

```yaml
environment:
  - DEBUG=False
  - SECRET_KEY=your-super-secret-key-here
  - DJANGO_SUPERUSER_EMAIL=admin@yoursite.com
  - DJANGO_SUPERUSER_PASSWORD=VeryStrongPassword123!
```

Dan gunakan Gunicorn di `docker-entrypoint.sh`:
```bash
# Ganti baris terakhir dengan:
exec gunicorn event_registration.wsgi:application --bind 0.0.0.0:8000
```

