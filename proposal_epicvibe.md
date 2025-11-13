# PROPOSAL PENAWARAN PENGEMBANGAN SISTEM

---

<div style="text-align: center; margin-top: 100px; margin-bottom: 100px;">

# **EPICVIBE ORGANIZER**

## Solusi Digital Terpadu untuk Manajemen Acara Modern

---

**Versi Dokumen:** 1.0  
**Tanggal:** November 2025  
**Status:** Proposal Penawaran

---

<div style="text-align: center; margin: 40px 0;">
    <img src="assets/logo-epicvibe.png" alt="EPICVIBE ORGANIZER Logo" style="max-width: 400px; height: auto;">
</div>

---

**Dikembangkan oleh:**  
Tim Pengembangan Dynamic Experience  
**Email:** novandrae7980@gmail.com  
**Telepon:** +6281931599440

</div>

---

\newpage

---

# DAFTAR ISI

1. [Latar Belakang](#1-latar-belakang)
2. [Tujuan Proyek](#2-tujuan-proyek)
3. [Ruang Lingkup Pekerjaan](#3-ruang-lingkup-pekerjaan)
4. [Tech Stack](#4-tech-stack)
5. [Diagram Arsitektur Sistem](#5-diagram-arsitektur-sistem)
6. [Estimasi Harga Penawaran](#6-estimasi-harga-penawaran)
7. [Jadwal & Timeline Implementasi](#7-jadwal--timeline-implementasi)
8. [Ringkasan dan Nilai Bisnis](#8-ringkasan-dan-nilai-bisnis)
9. [Kesimpulan](#9-kesimpulan)

---

\newpage

---

## 1. LATAR BELAKANG

Dalam era digital yang terus berkembang, industri event management menghadapi tantangan yang semakin kompleks. Banyak Event Organizer (EO) masih mengandalkan metode manual atau sistem yang terpisah-pisah dalam mengelola berbagai aspek acara mereka. Kondisi ini menciptakan beberapa permasalahan kritis:

### 1.1 Permasalahan yang Dihadapi

- **Inefisiensi Operasional**: Proses manual untuk registrasi peserta, pembayaran, dan manajemen acara memakan waktu yang signifikan dan rentan terhadap kesalahan manusia.

- **Fragmentasi Sistem**: Penggunaan berbagai platform terpisah untuk registrasi, pembayaran, komunikasi, dan pelaporan menyebabkan data tersebar dan sulit untuk dianalisis secara terintegrasi.

- **Biaya Operasional Tinggi**: Sistem yang tidak terintegrasi memerlukan lebih banyak sumber daya manusia dan waktu, yang pada akhirnya meningkatkan biaya operasional.

- **Keterbatasan Skalabilitas**: Sistem tradisional sulit untuk menyesuaikan dengan peningkatan volume acara atau jumlah peserta secara dinamis.

- **Keamanan Data**: Metode manual dan sistem yang tidak terpusat meningkatkan risiko keamanan data peserta dan informasi sensitif lainnya.

### 1.2 Kebutuhan Solusi Modern

Berdasarkan analisis mendalam terhadap kebutuhan industri event management, diperlukan solusi berbasis cloud yang dapat:

- Mengintegrasikan seluruh proses manajemen acara dalam satu platform terpadu
- Menyediakan skalabilitas otomatis untuk menangani peningkatan beban kerja
- Memastikan keamanan data dengan standar enterprise-grade
- Memberikan insights berbasis data untuk pengambilan keputusan yang lebih baik
- Mendukung inovasi teknologi masa depan seperti Machine Learning dan AI

**EPICVIBE ORGANIZER** hadir sebagai solusi komprehensif yang dirancang khusus untuk mengatasi semua tantangan tersebut, dengan memanfaatkan teknologi cloud modern dan arsitektur yang scalable.

---

## 2. TUJUAN PROYEK

Proyek pengembangan **EPICVIBE ORGANIZER** memiliki tujuan strategis yang dirancang untuk memberikan nilai maksimal bagi Event Organizer dan seluruh stakeholder. Berikut adalah tujuan utama proyek:

### 2.1 Tujuan Utama

1. **Menyediakan Sistem Manajemen Event yang Efisien dan Modern**
   - Mengembangkan platform terintegrasi yang memungkinkan Event Organizer mengelola seluruh siklus acara dari satu dashboard terpusat
   - Menyediakan antarmuka pengguna yang intuitif dan mudah digunakan, mengurangi kurva pembelajaran bagi pengguna baru
   - Mengotomatisasi proses-proses repetitif untuk meningkatkan efisiensi operasional hingga 70%

2. **Membangun Platform Berbasis Cloud dengan Keamanan Tinggi dan Skalabilitas**
   - Mengimplementasikan infrastruktur cloud menggunakan Amazon Web Services (AWS) dengan arsitektur yang dapat diskalakan secara otomatis
   - Menerapkan keamanan berlapis dengan Virtual Private Cloud (VPC), enkripsi end-to-end, dan compliance dengan standar keamanan internasional
   - Memastikan uptime 99.9% dengan sistem monitoring dan auto-scaling yang canggih

3. **Mendukung Pengembangan Teknologi Masa Depan dengan Stack Modern**
   - Menggunakan teknologi terkini seperti Django, Python, dan framework modern untuk memastikan maintainability jangka panjang
   - Membangun arsitektur yang modular dan extensible, memungkinkan pengembangan fitur baru tanpa mengganggu sistem yang ada
   - Menyediakan API yang robust dan terdokumentasi dengan baik untuk integrasi dengan sistem pihak ketiga

4. **Mengintegrasikan Inovasi Berbasis Machine Learning**
   - Mengimplementasikan model LSTM (Long Short-Term Memory) untuk Next Word Prediction dalam sistem chatbot, meningkatkan pengalaman pengguna
   - Mengembangkan Hybrid Event Recommendation System yang memberikan rekomendasi personal untuk peserta berdasarkan preferensi dan riwayat
   - Menerapkan analitik prediktif untuk membantu Event Organizer dalam perencanaan dan optimasi acara

5. **Menyediakan Solusi Cloud-Native yang Terintegrasi**
   - Mengoptimalkan deployment dengan AWS Amplify untuk frontend dan infrastruktur yang scalable
   - Memanfaatkan managed services seperti Amazon RDS untuk database dan AWS S3 untuk storage, mengurangi overhead maintenance
   - Mengimplementasikan monitoring dan logging komprehensif dengan CloudWatch untuk observability penuh

### 2.2 Tujuan Jangka Panjang

- Menjadi platform terdepan di industri event management Indonesia
- Membangun ekosistem yang menghubungkan Event Organizer, peserta, dan vendor
- Mengembangkan fitur-fitur inovatif berbasis AI/ML untuk memberikan competitive advantage
- Mencapai skalabilitas untuk menangani ribuan acara secara bersamaan

---

## 3. RUANG LINGKUP PEKERJAAN

Ruang lingkup pekerjaan dalam pengembangan **EPICVIBE ORGANIZER** mencakup seluruh aspek pengembangan sistem, mulai dari perencanaan hingga deployment dan maintenance. Berikut adalah detail lengkap ruang lingkup pekerjaan:

### 3.1 Pengembangan Full-Stack

**Backend Development:**
- Pengembangan RESTful API menggunakan Django REST Framework
- Implementasi sistem autentikasi dan otorisasi berbasis JWT (JSON Web Tokens)
- Pengembangan modul-modul inti: manajemen event, registrasi peserta, pembayaran, sertifikat, dan pelaporan
- Integrasi dengan payment gateway untuk proses pembayaran yang aman
- Implementasi sistem notifikasi email dan SMS untuk komunikasi dengan peserta
- Pengembangan sistem manajemen file dan media dengan optimasi storage

**Frontend Development:**
- Pengembangan antarmuka pengguna responsif menggunakan modern web technologies
- Implementasi dashboard untuk Event Organizer dengan visualisasi data real-time
- Pengembangan portal peserta untuk registrasi, pembayaran, dan akses materi
- Optimasi performa dan user experience (UX) untuk berbagai perangkat
- Implementasi Progressive Web App (PWA) untuk akses mobile yang optimal

### 3.2 Infrastruktur Cloud (AWS) - *Fase Production Deployment*

**Setup dan Konfigurasi (Rencana):**
- Konfigurasi Virtual Private Cloud (VPC) dengan subnet public dan private untuk keamanan maksimal
- Setup Amazon EC2 instances dengan Auto Scaling Groups untuk high availability
- Konfigurasi Application Load Balancer (ALB) untuk distribusi beban yang optimal
- Migrasi database dari SQLite3 ke Amazon RDS (PostgreSQL) dengan Multi-AZ deployment untuk redundancy
- Konfigurasi Amazon S3 untuk storage file dan media dengan lifecycle policies
- Setup Amazon CloudFront untuk Content Delivery Network (CDN) global

**Deployment dan DevOps (Rencana):**
- Implementasi CI/CD pipeline menggunakan GitHub Actions
- Containerization dengan Docker dan orchestration menggunakan Amazon ECS
- Infrastructure as Code (IaC) dengan Terraform untuk reproducibility
- Setup monitoring dan alerting dengan Amazon CloudWatch
- Konfigurasi backup otomatis dan disaster recovery plan

**Status Saat Ini:**
- Sistem berjalan di development environment dengan SQLite3 database
- Deployment lokal dengan Django development server
- File storage menggunakan local media directory
- Email service menggunakan SMTP Gmail

### 3.3 Keamanan dan Compliance

- Implementasi enkripsi data at rest dan in transit (TLS/SSL)
- Setup AWS WAF (Web Application Firewall) untuk proteksi terhadap serangan web
- Implementasi rate limiting dan DDoS protection
- Audit keamanan dan penetration testing
- Compliance dengan standar keamanan data (GDPR-ready, data privacy)
- Implementasi role-based access control (RBAC) yang granular

### 3.4 Artificial Intelligence Integration

**Chatbot dengan OpenAI:**
- Integrasi OpenAI API untuk chatbot cerdas "Dexy"
- Implementasi natural language processing untuk memahami konteks pertanyaan pengguna
- Fitur chatbot untuk membantu pengguna dengan pertanyaan tentang event, registrasi, token, sertifikat, dan fitur lainnya
- Response yang kontekstual dan informatif berdasarkan data sistem

**Future Enhancement (Opsional):**
- **LSTM Next Word Prediction**: Pengembangan model LSTM untuk prediksi kata berikutnya dalam chatbot (rencana)
- **Hybrid Event Recommendation System**: Sistem rekomendasi yang menggabungkan collaborative filtering dan content-based filtering (rencana)
- **Analytics Dashboard**: Dashboard analytics untuk tracking efektivitas dan insights (rencana)

### 3.5 Monitoring dan Maintenance

- Setup comprehensive logging dengan AWS CloudWatch Logs
- Implementasi application performance monitoring (APM)
- Setup alerting untuk critical metrics dan errors
- Dokumentasi teknis lengkap untuk maintenance
- Training untuk tim maintenance klien
- Dukungan teknis selama periode garansi

---

## 4. TECH STACK

**EPICVIBE ORGANIZER** dibangun menggunakan teknologi modern dan teruji yang dipilih berdasarkan pertimbangan performa, skalabilitas, dan maintainability. Berikut adalah detail lengkap tech stack yang akan digunakan:

### 4.1 Backend Technology

| Komponen | Teknologi | Versi | Keterangan |
|----------|-----------|-------|------------|
| **Framework** | Django | 4.2+ | Web framework Python yang powerful dan scalable |
| **Language** | Python | 3.8+ | Bahasa pemrograman modern dengan ekosistem yang kaya |
| **Database (Development)** | SQLite3 | - | Database ringan untuk development dan testing |
| **Database (Production)** | PostgreSQL | 15+ | Relational database management system yang robust untuk production |
| **Authentication** | Django Session Auth | - | Sistem autentikasi built-in Django dengan session management |
| **Form Handling** | Django Crispy Forms | 2.0+ | Library untuk form rendering dengan Bootstrap |
| **File Processing** | Pillow | 10.0+ | Library untuk image processing |
| **PDF Generation** | ReportLab | 4.0+ | Library untuk generate sertifikat PDF |
| **Email Service** | Django SMTP | - | Email backend untuk notifikasi dan verifikasi |
| **AI Integration** | OpenAI API | 1.0+ | Integrasi dengan OpenAI untuk chatbot cerdas |

### 4.2 Frontend Technology

| Komponen | Teknologi | Versi | Keterangan |
|----------|-----------|-------|------------|
| **Template Engine** | Django Templates | 4.2+ | Server-side rendering dengan template inheritance |
| **CSS Framework** | Bootstrap | 5.3+ | Responsive CSS framework untuk UI components |
| **Utility CSS** | TailwindCSS | 3.4+ | Utility-first CSS framework untuk rapid UI development |
| **Icons** | Bootstrap Icons | 1.10+ | Icon library yang konsisten dengan Bootstrap |
| **Fonts** | Google Fonts | - | Poppins, Montserrat, Inter untuk typography |
| **JavaScript** | Vanilla JS | - | Native JavaScript untuk interaktivitas |
| **Responsive Design** | Mobile-First | - | Design yang optimal untuk semua perangkat |

### 4.3 Cloud Infrastructure (AWS) - *Rencana Production Deployment*

| Layanan | Keterangan | Penggunaan |
|---------|------------|------------|
| **Amazon EC2** | Elastic Compute Cloud | Server instances untuk aplikasi backend |
| **Amazon RDS** | Relational Database Service | Managed PostgreSQL database dengan Multi-AZ |
| **Amazon S3** | Simple Storage Service | Storage untuk file, media, dan static assets |
| **Amazon CloudFront** | Content Delivery Network | CDN untuk distribusi konten global |
| **Amazon Route 53** | DNS Service | Domain name system management |
| **AWS Certificate Manager (ACM)** | SSL/TLS Certificates | Managed SSL certificates untuk HTTPS |
| **Application Load Balancer (ALB)** | Load Balancing | Distribusi traffic dan health checks |
| **Amazon CloudWatch** | Monitoring & Logging | Monitoring, logging, dan alerting |
| **AWS Auto Scaling** | Auto Scaling | Automatic scaling berdasarkan demand |
| **Amazon VPC** | Virtual Private Cloud | Isolated network environment untuk keamanan |
| **AWS WAF** | Web Application Firewall | Proteksi terhadap serangan web |

**Catatan**: Saat ini sistem masih dalam fase development dengan deployment lokal. Cloud infrastructure akan diimplementasikan pada fase production deployment.

### 4.4 DevOps & Infrastructure as Code - *Rencana Production*

| Tool | Keterangan | Penggunaan |
|------|------------|------------|
| **Docker** | Containerization | Container untuk aplikasi dan dependencies (rencana) |
| **Amazon ECS** | Elastic Container Service | Container orchestration dan management (rencana) |
| **GitHub Actions** | CI/CD Pipeline | Automated testing, building, dan deployment (rencana) |
| **Terraform** | Infrastructure as Code | Provisioning dan management infrastruktur AWS (rencana) |
| **Version Control** | Git | Source code management dan versioning |
| **Environment Config** | python-decouple | Management environment variables dan secrets |

### 4.5 Artificial Intelligence Integration

| Komponen | Teknologi | Keterangan |
|----------|-----------|------------|
| **AI Service** | OpenAI API | Integrasi dengan OpenAI GPT untuk chatbot cerdas |
| **Chatbot** | Custom Django View | Chatbot "Dexy" dengan integrasi OpenAI untuk menjawab pertanyaan pengguna |
| **Natural Language Processing** | OpenAI GPT Models | Pemrosesan bahasa alami untuk memahami konteks pertanyaan |
| **Future Enhancement** | LSTM / Recommendation System | Rencana pengembangan untuk next word prediction dan event recommendation (opsional) |

### 4.6 Development Tools & Libraries

- **Version Control**: Git dengan GitHub
- **Package Management**: pip dengan requirements.txt
- **Data Processing**: pandas, openpyxl untuk export data
- **Image Processing**: Pillow untuk upload dan processing gambar
- **PDF Generation**: ReportLab untuk generate sertifikat
- **Environment Management**: python-decouple untuk environment variables
- **Testing**: Django Test Framework (built-in)
- **Documentation**: Markdown files dan inline comments

---

## 5. DIAGRAM ARSITEKTUR SISTEM

Arsitektur **EPICVIBE ORGANIZER** dirancang dengan prinsip cloud-native, high availability, dan skalabilitas. Berikut adalah diagram arsitektur sistem secara keseluruhan:

<div style="text-align: center; margin: 40px 0;">
    <img src="assets/architecture-diagram.png" alt="Diagram Arsitektur EPICVIBE ORGANIZER" style="max-width: 100%; height: auto;">
</div>

*Gambar 1: Arsitektur Sistem EPICVIBE ORGANIZER*

### 5.1 Komponen Arsitektur

**Layer 1: Client Layer**
- Web Application (Django Templates + Bootstrap + TailwindCSS) - responsive design
- Mobile Web (Mobile-First Design)
- Browser-based interface (tidak perlu install aplikasi)

**Layer 2: Application Layer (Development)**
- Django Development Server - local development
- Django WSGI Application - production ready
- Template Engine - server-side rendering
- Middleware - session management, role-based access control

**Layer 2: Application Layer (Production - Rencana)**
- Application Load Balancer (ALB) - distribusi traffic
- EC2 Auto Scaling Group - backend servers
- ECS Cluster - containerized services (rencana)

**Layer 3: Data Layer (Development)**
- SQLite3 Database - local development database
- Local File Storage (/media/) - untuk upload files

**Layer 3: Data Layer (Production - Rencana)**
- Amazon RDS (PostgreSQL) - primary database dengan Multi-AZ
- Amazon ElastiCache (Redis) - caching layer (rencana)
- Amazon S3 - object storage untuk files dan media

**Layer 4: Security Layer**
- AWS WAF - web application firewall
- VPC dengan private subnets - network isolation
- Security Groups - firewall rules
- IAM Roles - access control

**Layer 5: Monitoring & Management**
- CloudWatch - monitoring dan logging
- CloudWatch Alarms - automated alerting
- AWS Systems Manager - configuration management

### 5.2 User Flow Diagram

Berikut adalah alur lengkap pengguna dalam sistem **EPICVIBE ORGANIZER**:

#### **Flow 1: User Registration & Verification**

```
[PUBLIC] → Buka Halaman Register
    ↓
Pilih Tipe Akun:
    - User (Peserta)
    - Event Organizer
    ↓
Isi Form Registrasi:
    - Nama Lengkap
    - Email (unique validation)
    - No. Handphone
    - Alamat
    - Pendidikan Terakhir
    - Password (min 8 karakter: huruf besar, kecil, angka, karakter spesial)
    ↓
[SISTEM] Validasi:
    - Email belum terdaftar?
    - Password sesuai kriteria?
    ↓
Jika Valid:
    - Hash password (bcrypt)
    - Generate OTP 6 digit / Link Aktivasi
    - Set expired: 5 menit
    - Simpan ke database (status: unverified)
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

#### **Flow 2: Login (Semua Role)**

```
[USER/ADMIN/EVENT_ORGANIZER] → Buka Halaman Login
    ↓
Input Email & Password
    ↓
[SISTEM] Validasi:
    - Email terdaftar?
    - Password cocok?
    - Untuk USER: email_verified_at != NULL?
    ↓
Jika Valid:
    - Create Session
    - Set last_activity = NOW()
    - Set session timeout: 5 menit
    ↓
Redirect berdasarkan Role:
    - USER → Dashboard User
    - ADMIN → Dashboard Admin
    - EVENT_ORGANIZER → Dashboard Event Organizer
    ↓
[Middleware] → Setiap Request:
    - Cek session valid
    - Cek last_activity
    - Jika (NOW() - last_activity) > 5 menit:
        → Destroy session
        → Redirect ke login (Session expired)
    - Jika aktif:
        → Update last_activity = NOW()
```

#### **Flow 3: Event Creation (Admin/Event Organizer)**

```
[ADMIN/EVENT_ORGANIZER] → Login
    ↓
Menu: "Tambah Kegiatan"
    ↓
Isi Form Event:
    - Judul Kegiatan
    - Kategori (Seminar/Konser)
    - Deskripsi
    - Tanggal & Waktu Kegiatan
    - Lokasi (Offline/Online/Hybrid)
    - Zoom Link (jika Online/Hybrid)
    - Harga Tiket (opsional, jika gratis kosongkan)
    - Nomor Rekening & Nama Bank (jika berbayar)
    - Upload Flyer
    - Upload Template Sertifikat (opsional)
    - Upload Materi Seminar (opsional, untuk Seminar)
    ↓
[SISTEM] Validasi:
    - Tanggal Kegiatan >= (TODAY + 3 hari)? → H-3 Rule
    - File flyer valid (ext, size)?
    - Template sertifikat valid (jika ada)?
    ↓
Jika Valid:
    - Upload file flyer → /media/flyers/
    - Upload template sertifikat → /media/certificate_templates/
    - Upload materi → /media/event_materials/
    - Set registration_closed_at = event_date + event_time
    - Status: published (bisa diakses publik)
    - Simpan ke database
    ↓
Berhasil → Redirect ke Daftar Kegiatan
```

#### **Flow 4: Event Registration (User) - Event Gratis**

```
[USER] → Login
    ↓
Menu: "Katalog Kegiatan"
    ↓
[SISTEM] → Tampilkan Kegiatan:
    - Default: Urut berdasarkan (event_date ASC, event_time ASC)
    - Filter: Search (title, description, location)
    - Filter: Sort (Terbaru, Terlama, Peserta Terbanyak)
    - Filter: Kategori (Seminar/Konser)
    - Hanya tampilkan: status = 'published'
    ↓
[USER] → Pilih Kegiatan (Event Gratis)
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
        * event_id, user_id, token
        * status = 'registered'
        * payment_status = 'not_required'
        * token_sent_at = NOW()
    - Kirim Email ke User dengan Token
    ↓
Berhasil → User terdaftar, status: Registered
```

#### **Flow 5: Event Registration (User) - Event Berbayar**

```
[USER] → Login
    ↓
Pilih Kegiatan (Event Berbayar)
    ↓
Klik "Daftar Kegiatan"
    ↓
[SISTEM] Validasi:
    - Apakah NOW() < registration_closed_at?
    - Apakah user sudah pernah daftar?
    - Cek jumlah penolakan pembayaran (max 3x):
        → Jika rejection_count >= 3: TOLAK
    ↓
Jika Valid:
    - Generate Token 10 digit
    - Simpan ke event_registrations:
        * status = 'registered'
        * payment_status = 'pending'
    - Kirim Email dengan Token & Info Pembayaran
    ↓
[USER] → Upload Bukti Pembayaran
    ↓
[SISTEM]:
    - Simpan payment_proof
    - payment_status = 'pending'
    ↓
[EVENT_ORGANIZER] → Review Pembayaran
    ↓
Opsi A: Approve
    ↓
[SISTEM]:
    - payment_status = 'approved'
    - payment_validated_at = NOW()
    - payment_validated_by = organizer
    ↓
[USER] → Terima Notifikasi: Pembayaran Disetujui

Opsi B: Reject
    ↓
[EVENT_ORGANIZER] → Input Alasan Penolakan
    ↓
[SISTEM]:
    - Simpan ke PaymentRejection (history)
    - Hapus registration (user bisa daftar ulang)
    - Kirim Email: Alasan Penolakan
    ↓
[USER] → Terima Notifikasi: Pembayaran Ditolak
    ↓
[USER] → Bisa Daftar Ulang (maksimal 3x rejection)
```

#### **Flow 6: Attendance & Certificate (User)**

```
[USER] → Login
    ↓
Menu: "Riwayat Kegiatan"
    ↓
[USER] → Pilih Kegiatan (status = 'registered')
    ↓
[SISTEM] Cek:
    - Apakah tanggal sekarang >= event_date?
    - Apakah waktu sekarang >= event_time?
    - Apakah payment_status = 'approved' (untuk event berbayar)?
    ↓
Jika SUDAH WAKTU & VALID:
    - Tombol "Isi Daftar Hadir" = AKTIF
Jika BELUM WAKTU:
    - Tombol "Isi Daftar Hadir" = DISABLED
    ↓
[USER] → Klik "Isi Daftar Hadir"
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
    - Generate Sertifikat PDF (jika ada template)
    - Simpan sertifikat ke tabel certificates
    - Kirim Email Sertifikat ke User
    ↓
Berhasil → User bisa download sertifikat
```

#### **Flow 7: Report Event (User)**

```
[USER] → Login
    ↓
Menu: "Laporkan Kegiatan" (di detail event)
    ↓
Isi Form Report:
    - Judul Laporan
    - Deskripsi Masalah
    ↓
[SISTEM]:
    - Simpan ke ReportEvent
    - Status: pending
    - Kirim notifikasi ke Admin
    ↓
[ADMIN] → Review Report
    ↓
Opsi A: Approve
    ↓
[SISTEM]:
    - Status: approved
    - Admin bisa tindak lanjuti
    ↓
[USER] → Terima Notifikasi: Laporan Disetujui

Opsi B: Reject
    ↓
[ADMIN] → Input Alasan Penolakan
    ↓
[SISTEM]:
    - Status: rejected
    - Kirim Email: Alasan Penolakan
    ↓
[USER] → Terima Notifikasi: Laporan Ditolak
```

#### **Flow 8: News System (Public/User)**

```
[PUBLIC/USER] → Buka Halaman Berita
    ↓
[SISTEM] → Tampilkan Berita:
    - Urut berdasarkan: created_at DESC
    - Hanya tampilkan: status = 'published'
    ↓
[USER] → Pilih Berita
    ↓
Baca Berita & Komentar
    ↓
[USER] → Input Komentar (jika login)
    ↓
[SISTEM]:
    - Simpan komentar
    - Tampilkan di halaman berita
```

#### **Flow 9: Chatbot "Dexy" (User)**

```
[USER] → Buka Halaman Chatbot
    ↓
Input Pertanyaan:
    - Tentang event, registrasi, token, sertifikat, dll
    ↓
[SISTEM]:
    - Kirim ke OpenAI API
    - Generate response berdasarkan konteks sistem
    - Tampilkan response ke user
    ↓
[USER] → Terima Jawaban dari Chatbot
```

#### **Flow 10: Material Download (User - Seminar Only)**

```
[USER] → Login
    ↓
Menu: "Riwayat Kegiatan"
    ↓
Pilih Kegiatan (Seminar, status = 'attended')
    ↓
[SISTEM] Cek:
    - Apakah event.category = 'seminar'?
    - Apakah user status = 'attended'?
    - Apakah material_file ada?
    ↓
Jika Valid:
    - Tampilkan tombol "Download Materi"
    ↓
[USER] → Klik "Download Materi"
    ↓
[SISTEM]:
    - Generate download link
    - Track download activity
    ↓
[USER] → Download File Materi
```

### 5.3 Data Flow (Technical)

1. **User Request Flow:**
   - User mengakses aplikasi melalui browser
   - Request diarahkan ke Django server
   - Backend memproses request dan berkomunikasi dengan database (SQLite3/PostgreSQL)
   - Response dikembalikan ke user melalui template rendering

2. **File Upload Flow:**
   - File diupload melalui form
   - File disimpan ke /media/ directory (development)
   - Metadata file disimpan di database
   - Untuk production: File akan disimpan ke S3 dengan presigned URLs

3. **Email Processing:**
   - Email dikirim melalui Django SMTP backend
   - Gmail SMTP untuk development
   - Async email sending (future enhancement dengan Celery)

---

## 6. ESTIMASI HARGA PENAWARAN

Berikut adalah breakdown estimasi harga untuk pengembangan **EPICVIBE ORGANIZER**. Harga dapat dinegosiasikan berdasarkan scope dan kebutuhan spesifik klien.

### 6.1 Breakdown Harga per Modul

| No | Modul/Komponen | Deskripsi | Status | Estimasi Harga (IDR) |
|----|----------------|-----------|--------|---------------------|
| 1 | **Backend Development** | Pengembangan sistem Django, business logic, database design, authentication system, semua modul inti | ✅ **Selesai** | Rp 150.000.000 |
| 2 | **Frontend Development** | Pengembangan UI/UX, dashboard 3 role, responsive design, mobile optimization | ✅ **Selesai** | Rp 120.000.000 |
| 3 | **AI Integration** | Integrasi OpenAI API untuk chatbot "Dexy" | ✅ **Selesai** | Rp 30.000.000 |
| 4 | **Testing & Quality Assurance** | Unit testing, integration testing, security testing, performance testing | ✅ **Selesai** | Rp 40.000.000 |
| 5 | **Documentation** | Technical documentation, user manual | ✅ **Selesai** | Rp 20.000.000 |
| 6 | **Cloud Infrastructure Setup** | AWS setup, VPC configuration, security setup, monitoring, migrasi database | 🔄 **Rencana** | Rp 80.000.000 |
| 7 | **DevOps & CI/CD** | Docker containerization, CI/CD pipeline, IaC dengan Terraform | 🔄 **Rencana** | Rp 50.000.000 |
| 8 | **Production Deployment** | Deployment ke AWS, domain setup, SSL, monitoring production | 🔄 **Rencana** | Rp 40.000.000 |
| 9 | **Maintenance (6 Bulan)** | Bug fixes, security updates, technical support, monitoring | 🔄 **Rencana** | Rp 60.000.000 |
| 10 | **ML Enhancement (Opsional)** | LSTM model development, recommendation system | ⏸️ **Opsional** | Rp 100.000.000 |

### 6.2 Ringkasan Total

**Fase Development (Sudah Selesai):**
| Kategori | Jumlah |
|----------|--------|
| **Subtotal Development** | Rp 360.000.000 |
| **PPN (11%)** | Rp 39.600.000 |
| **TOTAL FASE DEVELOPMENT** | **Rp 399.600.000** |

**Fase Production Deployment (Rencana):**
| Kategori | Jumlah |
|----------|--------|
| **Subtotal Production** | Rp 170.000.000 |
| **PPN (11%)** | Rp 18.700.000 |
| **TOTAL FASE PRODUCTION** | **Rp 188.700.000** |

**TOTAL KESELURUHAN:**
| Kategori | Jumlah |
|----------|--------|
| **Total Development + Production** | **Rp 588.300.000** |
| **Maintenance 6 Bulan** | Rp 60.000.000 |
| **GRAND TOTAL** | **Rp 648.300.000** |

### 6.3 Catatan Penting

- **Fase Development sudah selesai** dan sistem sudah berjalan dengan fitur lengkap
- Harga untuk **Fase Production Deployment** belum termasuk biaya AWS infrastructure (EC2, RDS, S3, dll) yang akan ditagihkan secara terpisah oleh AWS
- Estimasi biaya AWS infrastructure: **Rp 5.000.000 - Rp 15.000.000 per bulan** (tergantung usage)
- Harga dapat dinegosiasikan untuk paket dengan scope yang disesuaikan
- Pembayaran untuk Fase Production dapat dilakukan dengan skema: 40% di awal, 40% milestone, 20% setelah completion
- Maintenance setelah 6 bulan dapat diperpanjang dengan biaya tambahan
- **ML Enhancement** bersifat opsional dan dapat ditambahkan di kemudian hari

### 6.4 Opsi Paket

**Paket Development (Sudah Selesai):**
- Backend + Frontend + AI Integration + Testing + Documentation
- **Harga: Rp 399.600.000** (sudah termasuk PPN)
- ✅ **Status: Selesai dan Berjalan**

**Paket Production Deployment:**
- Cloud Infrastructure Setup + DevOps + CI/CD + Production Deployment
- **Harga: Rp 188.700.000** (sudah termasuk PPN)
- 🔄 **Status: Rencana Implementasi**

**Paket Enterprise (Full Features + Extended Support):**
- Semua fitur Paket Production + Extended maintenance 12 bulan + Priority support + ML Enhancement
- **Harga: Rp 808.300.000** (sudah termasuk PPN)
- ⏸️ **Status: Opsional**

---

## 7. JADWAL & TIMELINE IMPLEMENTASI

Proyek **EPICVIBE ORGANIZER** direncanakan untuk diselesaikan dalam **12 minggu (3 bulan)** dengan tahapan yang terstruktur. Berikut adalah timeline detail implementasi:

### 7.1 Timeline Overview - Fase Development (Selesai)

| Fase | Durasi | Status | Deskripsi |
|------|--------|--------|-----------|
| **Phase 1: Planning & Design** | Minggu 1-2 | ✅ **Selesai** | Requirement analysis, system design, database design, UI/UX design |
| **Phase 2: Backend Development** | Minggu 3-6 | ✅ **Selesai** | Django development, database implementation, authentication, semua modul inti |
| **Phase 3: Frontend Development** | Minggu 4-7 | ✅ **Selesai** | UI development dengan Bootstrap & TailwindCSS, integration dengan backend, responsive design |
| **Phase 4: AI Integration** | Minggu 7-8 | ✅ **Selesai** | Integrasi OpenAI API untuk chatbot "Dexy" |
| **Phase 5: Testing & QA** | Minggu 9-10 | ✅ **Selesai** | Comprehensive testing, bug fixes, performance optimization |
| **Phase 6: Documentation & Handover** | Minggu 11-12 | ✅ **Selesai** | Technical documentation, user manual, system handover |

### 7.1.1 Timeline Overview - Fase Production Deployment (Rencana)

| Fase | Durasi | Status | Deskripsi |
|------|--------|--------|-----------|
| **Phase 1: Database Migration** | Minggu 1-2 | 🔄 **Rencana** | Migrasi dari SQLite3 ke PostgreSQL, data migration |
| **Phase 2: Cloud Infrastructure** | Minggu 2-4 | 🔄 **Rencana** | AWS setup, VPC configuration, RDS setup, S3 configuration |
| **Phase 3: DevOps Setup** | Minggu 4-6 | 🔄 **Rencana** | Docker containerization, CI/CD pipeline, Terraform IaC |
| **Phase 4: Production Deployment** | Minggu 6-7 | 🔄 **Rencana** | Production deployment, domain setup, SSL, monitoring |
| **Phase 5: Testing & Go-Live** | Minggu 8 | 🔄 **Rencana** | Production testing, performance optimization, go-live |

### 7.2 Detail Timeline per Minggu - Fase Development (Selesai)

#### **Minggu 1-2: Planning & Design**
- **Minggu 1:**
  - Kick-off meeting dengan stakeholder
  - Requirement gathering dan analysis
  - System architecture design
  - Database schema design
  - API specification design

- **Minggu 2:**
  - UI/UX design dan mockup
  - Technical specification document
  - Project setup dan development environment
  - Review dan approval design documents

**Deliverables:**
- System Design Document
- Database Schema
- API Specification
- UI/UX Mockups
- Project Plan

#### **Minggu 3-6: Backend Development**
- **Minggu 3:**
  - Setup Django project structure
  - Database models implementation
  - Authentication system (JWT)
  - User management module

- **Minggu 4:**
  - Event management module
  - Registration module
  - Payment integration
  - File upload system

- **Minggu 5:**
  - Certificate generation module
  - Reporting module
  - Notification system (email/SMS)
  - Admin dashboard API

- **Minggu 6:**
  - API documentation (Swagger)
  - Unit testing
  - Code review dan refactoring
  - Backend milestone review

**Deliverables:**
- Backend API (v1.0)
- API Documentation
- Unit Tests
- Database Migration Scripts

#### **Minggu 4-7: Frontend Development** (Parallel dengan Backend)
- **Minggu 4:**
  - Next.js project setup
  - Component library setup
  - Authentication UI
  - Dashboard layout

- **Minggu 5:**
  - Event management UI
  - Registration flow
  - Payment UI
  - User profile pages

- **Minggu 6:**
  - Admin dashboard
  - Reporting and analytics UI
  - Certificate download UI
  - Responsive design implementation

- **Minggu 7:**
  - Integration dengan backend API
  - Error handling dan validation
  - Performance optimization
  - Frontend milestone review

**Deliverables:**
- Frontend Application (v1.0)
- Responsive Design
- Component Library
- Integration Tests

#### **Minggu 5-8: Cloud Infrastructure** (Parallel)
- **Minggu 5:**
  - AWS account setup
  - VPC configuration
  - Security groups setup
  - RDS database setup

- **Minggu 6:**
  - EC2 instances setup
  - S3 bucket configuration
  - CloudFront CDN setup
  - Load balancer configuration

- **Minggu 7:**
  - Docker containerization
  - ECS cluster setup
  - CI/CD pipeline (GitHub Actions)
  - Infrastructure as Code (Terraform)

- **Minggu 8:**
  - Monitoring setup (CloudWatch)
  - Auto-scaling configuration
  - Backup and disaster recovery
  - Security hardening

**Deliverables:**
- AWS Infrastructure
- CI/CD Pipeline
- Terraform Scripts
- Monitoring Dashboard

#### **Minggu 8-10: Machine Learning Integration** (Opsional)
- **Minggu 8:**
  - Data collection dan preprocessing
  - LSTM model architecture design
  - Training environment setup

- **Minggu 9:**
  - LSTM model training
  - Model evaluation dan optimization
  - Recommendation system development
  - API integration untuk ML services

- **Minggu 10:**
  - ML model deployment (SageMaker)
  - A/B testing setup
  - Performance monitoring
  - ML module review

**Deliverables:**
- Trained ML Models
- Recommendation API
- ML Documentation
- Performance Metrics

#### **Minggu 10-11: Testing & Quality Assurance**
- **Minggu 10:**
  - Integration testing
  - End-to-end testing
  - Security testing
  - Performance testing

- **Minggu 11:**
  - Bug fixes dan optimization
  - User acceptance testing (UAT)
  - Load testing
  - Security audit

**Deliverables:**
- Test Reports
- Bug Fixes
- Performance Report
- Security Audit Report

#### **Minggu 12: Deployment & Handover**
- **Minggu 12:**
  - Production deployment
  - Final testing di production
  - Documentation finalization
  - Training untuk tim klien
  - Go-live dan support

**Deliverables:**
- Production System
- Technical Documentation
- User Manual
- Training Materials
- Support Plan

### 7.3 Milestone dan Pembayaran

**Fase Development (Sudah Selesai):**
| Milestone | Deliverable | Status | % Progress |
|-----------|-------------|--------|------------|
| **Milestone 1** | Design Documents Approval | ✅ **Selesai** | 10% |
| **Milestone 2** | Backend Development Complete | ✅ **Selesai** | 40% |
| **Milestone 3** | Frontend Development Complete | ✅ **Selesai** | 60% |
| **Milestone 4** | AI Integration Complete | ✅ **Selesai** | 75% |
| **Milestone 5** | Testing & QA Complete | ✅ **Selesai** | 90% |
| **Milestone 6** | Documentation & Handover | ✅ **Selesai** | 100% |

**Fase Production Deployment (Rencana):**
| Milestone | Deliverable | Status | % Progress | Pembayaran |
|-----------|-------------|--------|------------|------------|
| **Milestone 1** | Database Migration Complete | 🔄 **Rencana** | 25% | 40% (Down Payment) |
| **Milestone 2** | Cloud Infrastructure Ready | 🔄 **Rencana** | 50% | 30% |
| **Milestone 3** | DevOps & CI/CD Complete | 🔄 **Rencana** | 75% | 20% |
| **Milestone 4** | Production Deployment & Go-Live | 🔄 **Rencana** | 100% | 10% (Final) |

---

## 8. RINGKASAN DAN NILAI BISNIS

**EPICVIBE ORGANIZER** bukan sekadar sistem manajemen event biasa, melainkan solusi transformasi digital yang dirancang untuk memberikan competitive advantage yang signifikan bagi Event Organizer. Berikut adalah ringkasan nilai bisnis dan keunggulan yang ditawarkan:

### 8.1 Efisiensi Waktu dan Biaya

**Penghematan Waktu:**
- **Otomatisasi Proses**: Sistem mengotomatisasi 80% proses manual, mengurangi waktu administrasi hingga 70%
- **Single Dashboard**: Semua fungsi manajemen event terpusat dalam satu dashboard, menghilangkan kebutuhan untuk beralih antar platform
- **Template dan Workflow**: Template event yang dapat digunakan kembali dan workflow yang terdefinisi mempercepat setup acara baru hingga 60%

**Penghematan Biaya:**
- **Reduksi Biaya Operasional**: Mengurangi kebutuhan staf administrasi hingga 40% melalui otomatisasi
- **Eliminasi Biaya Platform Terpisah**: Menggantikan multiple subscription dengan satu platform terintegrasi
- **Optimasi Resource**: Auto-scaling AWS memastikan Anda hanya membayar untuk resource yang digunakan

**ROI (Return on Investment):**
- Estimasi penghematan biaya operasional: **Rp 50.000.000 - Rp 100.000.000 per tahun**
- Payback period: **6-12 bulan** setelah implementasi
- Peningkatan revenue melalui efisiensi dan kemampuan menangani lebih banyak acara

### 8.2 Keamanan Tinggi dengan AWS + VPC

**Enterprise-Grade Security:**
- **Network Isolation**: VPC dengan private subnets memastikan database dan sensitive data tidak terpapar ke internet publik
- **Enkripsi End-to-End**: Semua data dienkripsi baik saat transit (TLS/SSL) maupun saat rest (AES-256)
- **Web Application Firewall**: AWS WAF melindungi dari serangan DDoS, SQL injection, dan serangan web lainnya
- **Compliance Ready**: Arsitektur dirancang untuk compliance dengan standar keamanan internasional (GDPR-ready)

**Data Protection:**
- **Automated Backups**: Backup otomatis harian dengan retention policy yang dapat dikonfigurasi
- **Disaster Recovery**: Multi-AZ deployment memastikan high availability dan quick recovery
- **Access Control**: Role-based access control (RBAC) yang granular untuk mengelola akses data
- **Audit Trail**: Logging komprehensif untuk audit dan compliance

**Kepercayaan Stakeholder:**
- Keamanan data yang tinggi meningkatkan kepercayaan peserta dan partner
- Compliance dengan standar keamanan membantu dalam tender dan partnership dengan organisasi besar

### 8.3 Skalabilitas Tanpa Batas

**Elastic Scaling:**
- **Auto-Scaling**: Sistem secara otomatis menambah atau mengurangi resource berdasarkan demand
- **Handle Traffic Spikes**: Dapat menangani peningkatan traffic hingga 10x tanpa degradasi performa
- **Global CDN**: CloudFront memastikan akses cepat dari mana saja di dunia

**Growth Ready:**
- **Horizontal Scaling**: Arsitektur memungkinkan penambahan server dengan mudah tanpa downtime
- **Database Scaling**: RDS dengan read replicas untuk menangani beban query yang tinggi
- **Microservices Ready**: Arsitektur modular memungkinkan pengembangan fitur baru tanpa mengganggu sistem yang ada

**Cost Efficiency:**
- Bayar hanya untuk resource yang digunakan (pay-as-you-go)
- Tidak perlu investasi besar di awal untuk hardware
- Skalabilitas otomatis menghindari over-provisioning

### 8.4 Inovasi Machine Learning

**Next Word Prediction (LSTM):**
- **Enhanced User Experience**: Chatbot dengan prediksi kata yang akurat meningkatkan interaksi pengguna
- **Time Saving**: Mengurangi waktu input hingga 40% dengan autocomplete yang cerdas
- **Learning System**: Model terus belajar dan membaik dari interaksi pengguna

**Hybrid Event Recommendation System:**
- **Personalized Recommendations**: Peserta mendapatkan rekomendasi acara yang relevan berdasarkan preferensi
- **Increased Engagement**: Rekomendasi personal meningkatkan conversion rate registrasi hingga 30%
- **Data-Driven Insights**: Analytics dari recommendation system memberikan insights tentang preferensi pasar

**Competitive Advantage:**
- Fitur AI/ML memberikan diferensiasi dari kompetitor
- Positioning sebagai platform teknologi terdepan
- Foundation untuk pengembangan fitur AI lebih lanjut di masa depan

### 8.5 Cloud-Native Architecture

**Modern Technology Stack:**
- Teknologi terkini memastikan sistem tetap relevan dan maintainable untuk jangka panjang
- Community support yang kuat untuk semua teknologi yang digunakan
- Regular updates dan security patches dari vendor

**DevOps Best Practices:**
- CI/CD pipeline memastikan deployment yang cepat dan reliable
- Infrastructure as Code memungkinkan reproducibility dan version control
- Automated testing mengurangi risiko bug di production

**Operational Excellence:**
- Monitoring dan alerting proaktif memungkinkan deteksi masalah sebelum berdampak pada user
- Centralized logging memudahkan troubleshooting dan debugging
- Documentation lengkap memudahkan onboarding dan maintenance

### 8.6 Manfaat Jangka Panjang

**Strategic Benefits:**
- **Data Analytics**: Kumpulan data yang terpusat memungkinkan analitik mendalam untuk pengambilan keputusan strategis
- **Market Intelligence**: Insights dari data acara membantu memahami tren pasar dan preferensi peserta
- **Business Growth**: Platform yang scalable mendukung pertumbuhan bisnis tanpa batasan teknis

**Innovation Platform:**
- Arsitektur yang extensible memungkinkan pengembangan fitur baru dengan cepat
- API yang robust memungkinkan integrasi dengan sistem pihak ketiga
- Foundation untuk pengembangan produk digital lainnya

**Competitive Positioning:**
- Teknologi modern memberikan competitive advantage
- Brand positioning sebagai inovator di industri event management
- Attractiveness untuk partnership dan investment

---

## 9. KESIMPULAN

**EPICVIBE ORGANIZER** adalah solusi komprehensif yang dirancang untuk mengubah cara Event Organizer mengelola acara mereka. Dengan kombinasi teknologi cloud modern, keamanan enterprise-grade, dan inovasi machine learning, platform ini tidak hanya menyelesaikan masalah operasional saat ini, tetapi juga memposisikan organisasi untuk sukses jangka panjang.

### 9.1 Komitmen Kami

Kami berkomitmen untuk memberikan:
- **Kualitas Terbaik**: Code quality, security, dan performance yang sesuai standar enterprise
- **Timeline yang Tepat**: Delivery sesuai jadwal yang telah disepakati
- **Support Berkelanjutan**: Dukungan teknis dan maintenance yang responsif
- **Partnership Jangka Panjang**: Komitmen untuk pertumbuhan dan evolusi sistem bersama

### 9.2 Next Steps

Untuk melanjutkan diskusi dan negosiasi lebih lanjut, kami mengundang Anda untuk:

1. **Review Meeting**: Diskusi detail tentang requirement dan scope
2. **Technical Deep Dive**: Presentasi arsitektur dan teknologi secara detail
3. **Proposal Refinement**: Penyesuaian proposal berdasarkan feedback
4. **Contract Discussion**: Pembahasan kontrak dan terms of engagement

### 9.3 Kontak

Untuk pertanyaan, klarifikasi, atau diskusi lebih lanjut, silakan hubungi:

**Tim Pengembangan EPICVIBE ORGANIZER**  
**Email:** novandrae7980@gmail.com  
**Telepon:** +6281931599440  
**Alamat:** Jakarta, Indonesia

---

<div style="text-align: center; margin-top: 50px;">

**Terima kasih atas perhatian dan kepercayaan Anda.**

**Kami berharap dapat bermitra dengan Anda dalam mewujudkan visi transformasi digital untuk industri event management.**

---

**EPICVIBE ORGANIZER**  
*Solusi Digital Terpadu untuk Manajemen Acara Modern*

</div>

---

\newpage

---

## LAMPIRAN

### A. Glosarium

- **API**: Application Programming Interface
- **AWS**: Amazon Web Services
- **CDN**: Content Delivery Network
- **CI/CD**: Continuous Integration / Continuous Deployment
- **ECS**: Elastic Container Service
- **IaC**: Infrastructure as Code
- **JWT**: JSON Web Token
- **LSTM**: Long Short-Term Memory
- **ML**: Machine Learning
- **PWA**: Progressive Web App
- **RDS**: Relational Database Service
- **RBAC**: Role-Based Access Control
- **S3**: Simple Storage Service
- **VPC**: Virtual Private Cloud
- **WAF**: Web Application Firewall

### B. Referensi Teknis

- Django Documentation: https://docs.djangoproject.com/
- AWS Architecture Center: https://aws.amazon.com/architecture/
- Next.js Documentation: https://nextjs.org/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs/

### C. Legal Disclaimer

Proposal ini bersifat rahasia dan hanya untuk tujuan evaluasi. Semua informasi teknis dan komersial dalam dokumen ini adalah milik EPICVIBE ORGANIZER dan tidak boleh didistribusikan tanpa izin tertulis.

---

**Dokumen ini dibuat dengan penuh dedikasi untuk memberikan solusi terbaik bagi kebutuhan Anda.**

---

*End of Document*

