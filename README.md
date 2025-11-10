# Dynamic Experience - Event Registration System

Sistem pendaftaran kegiatan berbasis web yang memungkinkan pengguna untuk mendaftar, mengikuti, dan mendapatkan sertifikat dari berbagai event seperti Seminar dan Konser.

## 🚀 Fitur Utama

### 👥 Multi-Role System
- **User**: Mendaftar event, mengisi daftar hadir, download sertifikat
- **Event Organizer**: Membuat dan mengelola event, validasi pembayaran
- **Admin**: Mengelola semua event, review laporan, statistik lengkap

### 📅 Event Management
- Kategori: Seminar & Conference, Concert & Festival
- Tipe Lokasi: Offline, Online, Hybrid (dengan Zoom Meeting)
- Event berbayar dengan sistem validasi pembayaran
- Upload flyer dan template sertifikat

### 💳 Payment System
- Upload bukti pembayaran
- Validasi pembayaran oleh Event Organizer
- Status pembayaran real-time

### 📰 News/Berita
- Admin & Event Organizer dapat membuat berita
- User dapat membaca dan berkomentar
- Filter berdasarkan kategori

### 🤖 AI Chatbot "Dexy"
- Chatbot AI untuk membantu user
- Terintegrasi dengan OpenAI API

### 📊 Dashboard & Analytics
- Dashboard berbeda untuk setiap role
- Statistik event, peserta, dan pembayaran
- Export data ke Excel/CSV

### 📱 Mobile Responsive
- Desain responsif untuk semua perangkat
- Optimized untuk mobile, tablet, dan desktop

## 🛠️ Teknologi

- **Backend**: Django 4.x
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5, TailwindCSS
- **AI**: OpenAI API (untuk chatbot)
- **Email**: SMTP Gmail
- **PDF Generation**: ReportLab (untuk sertifikat)

## 📦 Instalasi

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. **Clone repository**
```bash
git clone https://github.com/Npppss/UJIKOM-FIX.git
cd UJIKOM-FIX
```

2. **Buat virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
Buat file `.env` di root project:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST_PASSWORD=your-gmail-app-password
OPENAI_API_KEY=your-openai-api-key
SITE_URL=http://localhost:8000
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run server**
```bash
python manage.py runserver
```

8. **Akses aplikasi**
- URL: http://localhost:8000
- Admin: http://localhost:8000/admin

## 👤 Default Credentials

### Admin
- Email: `admin@example.com`
- Password: `Admin123#`

### Event Organizer
- Email: `organizer@example.com`
- Password: `Organizer123#`

### User
- Email: `user@example.com`
- Password: `User123#`

> **Note**: Buat user baru melalui admin panel atau register page

## 📁 Struktur Project

```
UJIKOM-FIX/
├── accounts/          # User management, authentication
├── events/            # Event models, views, forms
├── registrations/     # Event registration, attendance
├── certificates/      # Certificate generation
├── dashboard/         # Dashboard views per role
├── utils/             # Utilities (email, token, export)
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── event_registration/ # Django settings
└── manage.py
```

## 🔑 Environment Variables

Pastikan file `.env` berisi:

```env
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
EMAIL_HOST_PASSWORD=your-gmail-app-password
OPENAI_API_KEY=your-openai-api-key
SITE_URL=http://localhost:8000
```

## 📝 Fitur Detail

### Event Registration
- User dapat mendaftar event
- Mendapat token 10 digit via email
- Upload bukti pembayaran (untuk event berbayar)
- Validasi pembayaran oleh Event Organizer

### Attendance System
- Isi daftar hadir dengan token
- Generate sertifikat otomatis (jika ada template)
- Download sertifikat PDF

### Report System
- User dapat melaporkan event yang tidak sesuai
- Admin review dan approve/reject
- Auto-suspend organizer jika report valid

### Payment Validation
- Event Organizer validasi pembayaran
- Approve atau reject dengan alasan
- Status real-time untuk user

## 🎨 UI/UX Features

- Modern gradient design
- Smooth animations
- Mobile-first responsive design
- Dark mode support (partial)
- Interactive charts dan statistics

## 📊 Dashboard Features

### User Dashboard
- Total event terdaftar
- Event yang akan datang
- Riwayat kegiatan

### Event Organizer Dashboard
- Total event dibuat
- Total peserta
- Event dengan peserta terbanyak
- Charts dan statistics

### Admin Dashboard
- Total event
- Total peserta
- Pending reports count
- Top events
- Charts dan analytics

## 🔒 Security Features

- Password complexity validation
- Email verification (OTP)
- Session timeout
- Role-based access control
- CSRF protection
- SQL injection protection

## 📧 Email Features

- Registration token email
- Email verification (OTP)
- Password reset
- Zoom Meeting details (untuk online/hybrid events)

## 🚀 Deployment

Untuk production, pastikan:
1. Set `DEBUG=False`
2. Gunakan database production (PostgreSQL recommended)
3. Setup static files collection
4. Setup media files storage
5. Configure ALLOWED_HOSTS
6. Setup HTTPS
7. Setup environment variables di server

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Npppss

## 🙏 Acknowledgments

- Django Framework
- Bootstrap 5
- TailwindCSS
- OpenAI API
- ReportLab

---

**Note**: Pastikan untuk tidak commit file `.env` yang berisi sensitive information. Gunakan environment variables untuk production.

