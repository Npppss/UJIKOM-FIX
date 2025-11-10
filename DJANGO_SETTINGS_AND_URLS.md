# DJANGO SETTINGS & URLS CONFIGURATION

## ⚙️ SETTINGS.PY

### event_registration/settings.py

```python
import os
from pathlib import Path
from django.utils import timezone

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    
    # Local apps
    'accounts',
    'events',
    'dashboard',
    'registrations',
    'certificates',
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'accounts.middleware.SessionTimeoutMiddleware',  # Custom session timeout
    'accounts.middleware.RoleRequiredMiddleware',     # Custom role check
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'event_registration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'event_registration.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'event_registration'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'accounts.validators.ComplexPasswordValidator',  # Custom validator
    },
]

# Internationalization
LANGUAGE_CODE = 'id-id'
TIME_ZONE = 'Asia/Jakarta'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:user'

# Session settings
SESSION_COOKIE_AGE = 300  # 5 menit dalam detik
SESSION_SAVE_EVERY_REQUEST = True  # Update session setiap request
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@eventregistration.com')

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Security Settings (untuk production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

---

## 🔗 URLS CONFIGURATION

### event_registration/urls.py (Root)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),  # Katalog publik
    path('accounts/', include('accounts.urls')),
    path('events/', include('events.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('registrations/', include('registrations.urls')),
    path('certificates/', include('certificates.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### accounts/urls.py

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('email/verify/', views.verify_email, name='email_verify'),
    path('email/verify/<str:token>/', views.verify_email_link, name='email_verify_link'),
    path('email/resend/', views.resend_verification, name='resend_otp'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('password/reset/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]
```

### events/urls.py

```python
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Public routes
    path('', views.catalog, name='catalog'),
    path('detail/<int:event_id>/', views.detail, name='detail'),
    
    # Admin & Event Organizer routes
    path('create/', views.create_event, name='create'),
    path('list/', views.event_list, name='list'),
    path('edit/<int:event_id>/', views.edit_event, name='edit'),
    path('delete/<int:event_id>/', views.delete_event, name='delete'),
    path('participants/<int:event_id>/', views.participants, name='participants'),
]
```

### dashboard/urls.py

```python
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('user/', views.user_dashboard, name='user'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('organizer/', views.organizer_dashboard, name='organizer'),
    path('admin/export/', views.admin_export, name='admin_export'),
    path('organizer/export/', views.organizer_export, name='organizer_export'),
]
```

### registrations/urls.py

```python
from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path('attendance/<int:event_id>/', views.attendance, name='attendance'),
    path('history/', views.history, name='history'),
]
```

### certificates/urls.py

```python
from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.certificate_list, name='list'),
    path('download/<int:certificate_id>/', views.download_certificate, name='download'),
]
```

---

## 📧 EMAIL SERVICE

### utils/email_service.py

```python
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_verification_email(user, otp_code, verification_token):
    """Kirim email verifikasi dengan OTP dan link"""
    verification_link = f"{settings.SITE_URL}/accounts/email/verify/{verification_token}/"
    
    subject = 'Verifikasi Email - Sistem Pendaftaran Kegiatan'
    
    message = f"""
    Halo {user.name},
    
    Terima kasih telah mendaftar di Sistem Pendaftaran Kegiatan.
    
    Untuk verifikasi email Anda, silakan gunakan salah satu metode berikut:
    
    1. Klik link berikut: {verification_link}
    2. Atau masukkan kode OTP berikut: {otp_code}
    
    Kode OTP dan link berlaku selama 5 menit.
    
    Jika Anda tidak melakukan registrasi, abaikan email ini.
    
    Salam,
    Tim Sistem Pendaftaran Kegiatan
    """
    
    html_message = render_to_string('emails/verification.html', {
        'user': user,
        'otp_code': otp_code,
        'verification_link': verification_link,
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_registration_token(user, event, token):
    """Kirim token untuk daftar hadir"""
    subject = f'Token Pendaftaran Kegiatan - {event.title}'
    
    message = f"""
    Halo {user.name},
    
    Anda telah berhasil mendaftar pada kegiatan:
    {event.title}
    
    Tanggal: {event.event_date.strftime('%d %B %Y')}
    Waktu: {event.event_time.strftime('%H:%M')}
    Lokasi: {event.location}
    
    Token Daftar Hadir Anda: {token}
    
    Simpan token ini dengan baik! Token akan digunakan saat mengisi daftar hadir pada hari H kegiatan.
    
    Daftar hadir dapat diisi setelah jam kegiatan dimulai.
    
    Salam,
    Tim Sistem Pendaftaran Kegiatan
    """
    
    html_message = render_to_string('emails/registration_token.html', {
        'user': user,
        'event': event,
        'token': token,
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_password_reset_email(user, reset_token):
    """Kirim email reset password"""
    reset_link = f"{settings.SITE_URL}/accounts/password/reset/{reset_token}/"
    
    subject = 'Reset Password - Sistem Pendaftaran Kegiatan'
    
    message = f"""
    Halo {user.name},
    
    Anda telah meminta reset password.
    
    Klik link berikut untuk reset password: {reset_link}
    
    Link berlaku selama 1 jam.
    
    Jika Anda tidak meminta reset password, abaikan email ini.
    
    Salam,
    Tim Sistem Pendaftaran Kegiatan
    """
    
    html_message = render_to_string('emails/password_reset.html', {
        'user': user,
        'reset_link': reset_link,
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
```

---

## 🎫 TOKEN SERVICE

### utils/token_service.py

```python
import secrets
from registrations.models import EventRegistration

def generate_registration_token():
    """Generate token 10 digit yang unik"""
    max_attempts = 100  # Prevent infinite loop
    
    for _ in range(max_attempts):
        # Generate 10 digit angka
        token = ''.join([str(secrets.randbelow(10)) for _ in range(10)])
        
        # Cek apakah token sudah ada
        if not EventRegistration.objects.filter(token=token).exists():
            return token
    
    # Fallback: gunakan timestamp + random jika masih collision
    import time
    token = str(int(time.time()))[-6:] + ''.join([str(secrets.randbelow(10)) for _ in range(4)])
    return token[:10]
```

---

## 📊 EXPORT SERVICE

### utils/export_service.py

```python
import pandas as pd
from django.http import HttpResponse
from registrations.models import EventRegistration
from events.models import Event

def export_participants_to_excel(event_ids=None, user_id=None, role=None):
    """
    Export data peserta ke Excel
    
    Args:
        event_ids: List event IDs (None = semua event)
        user_id: User ID untuk filter (untuk Event Organizer)
        role: Role user ('admin' atau 'event_organizer')
    """
    # Query registrations
    registrations = EventRegistration.objects.select_related('event', 'user').all()
    
    # Filter berdasarkan event_ids
    if event_ids:
        registrations = registrations.filter(event_id__in=event_ids)
    
    # Filter untuk Event Organizer (hanya event sendiri)
    if role == 'event_organizer' and user_id:
        registrations = registrations.filter(event__user_id=user_id)
    
    # Prepare data
    data = []
    for reg in registrations:
        data.append({
            'Nama Kegiatan': reg.event.title,
            'Tanggal Kegiatan': reg.event.event_date.strftime('%d %B %Y'),
            'Waktu Kegiatan': reg.event.event_time.strftime('%H:%M'),
            'Lokasi': reg.event.location,
            'Nama Peserta': reg.user.name,
            'Email': reg.user.email,
            'No HP': reg.user.phone,
            'Alamat': reg.user.address,
            'Pendidikan': reg.user.education,
            'Status': reg.get_status_display(),
            'Tanggal Daftar': reg.created_at.strftime('%d %B %Y %H:%M'),
            'Tanggal Hadir': reg.attendance_at.strftime('%d %B %Y %H:%M') if reg.attendance_at else '-',
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = 'peserta_kegiatan.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Write to Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Peserta', index=False)
    
    return response

def export_participants_to_csv(event_ids=None, user_id=None, role=None):
    """
    Export data peserta ke CSV
    
    Args:
        event_ids: List event IDs (None = semua event)
        user_id: User ID untuk filter (untuk Event Organizer)
        role: Role user ('admin' atau 'event_organizer')
    """
    # Query registrations (sama seperti Excel)
    registrations = EventRegistration.objects.select_related('event', 'user').all()
    
    if event_ids:
        registrations = registrations.filter(event_id__in=event_ids)
    
    if role == 'event_organizer' and user_id:
        registrations = registrations.filter(event__user_id=user_id)
    
    # Prepare data
    data = []
    for reg in registrations:
        data.append({
            'Nama Kegiatan': reg.event.title,
            'Tanggal Kegiatan': reg.event.event_date.strftime('%d %B %Y'),
            'Waktu Kegiatan': reg.event.event_time.strftime('%H:%M'),
            'Lokasi': reg.event.location,
            'Nama Peserta': reg.user.name,
            'Email': reg.user.email,
            'No HP': reg.user.phone,
            'Alamat': reg.user.address,
            'Pendidikan': reg.user.education,
            'Status': reg.get_status_display(),
            'Tanggal Daftar': reg.created_at.strftime('%d %B %Y %H:%M'),
            'Tanggal Hadir': reg.attendance_at.strftime('%d %B %Y %H:%M') if reg.attendance_at else '-',
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    filename = 'peserta_kegiatan.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Write to CSV
    df.to_csv(response, index=False, encoding='utf-8-sig')  # utf-8-sig untuk Excel
    
    return response
```

---

## ✅ PASSWORD VALIDATOR

### accounts/validators.py

```python
from django.core.exceptions import ValidationError
import re

class ComplexPasswordValidator:
    """
    Validator untuk password yang kompleks:
    - Minimal 8 karakter
    - Harus ada huruf kecil
    - Harus ada huruf besar
    - Harus ada angka
    - Harus ada karakter spesial (@$!%*?&#)
    """
    
    def validate(self, password, user=None):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
        
        if not re.match(pattern, password):
            raise ValidationError(
                'Password minimal 8 karakter dan harus mengandung angka, '
                'huruf besar, huruf kecil, dan karakter spesial (@$!%*?&#)',
                code='password_too_simple',
            )
    
    def get_help_text(self):
        return (
            'Password harus minimal 8 karakter dan mengandung: '
            'angka, huruf besar, huruf kecil, dan karakter spesial (@$!%*?&#)'
        )
```

---

## 📋 VIEWS LENGKAP

### registrations/views.py

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from accounts.decorators import email_verification_required
from events.models import Event
from .models import EventRegistration
from .forms import AttendanceForm
from utils.token_service import generate_registration_token
from utils.email_service import send_registration_token

@login_required
@email_verification_required
def register_event(request, event_id):
    """User mendaftar kegiatan"""
    event = get_object_or_404(Event, id=event_id, status='published', deleted_at__isnull=True)
    
    # Cek apakah sudah terdaftar
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, 'Anda sudah terdaftar pada kegiatan ini.')
        return redirect('events:detail', event_id=event_id)
    
    # Cek deadline pendaftaran
    if not event.is_registration_open():
        messages.error(request, 'Pendaftaran sudah ditutup. Kegiatan sudah dimulai atau sudah lewat.')
        return redirect('events:detail', event_id=event_id)
    
    # Buat registrasi
    token = generate_registration_token()
    registration = EventRegistration.objects.create(
        event=event,
        user=request.user,
        token=token,
        token_sent_at=timezone.now(),
        status='registered'
    )
    
    # Kirim email token
    send_registration_token(request.user, event, token)
    
    messages.success(request, 'Pendaftaran berhasil! Token telah dikirim ke email Anda.')
    return redirect('registrations:history')

@login_required
@email_verification_required
def attendance(request, event_id):
    """User isi daftar hadir dengan token"""
    event = get_object_or_404(Event, id=event_id)
    registration = get_object_or_404(
        EventRegistration,
        event=event,
        user=request.user
    )
    
    # Cek apakah sudah hadir
    if registration.status == 'attended':
        messages.info(request, 'Anda sudah mengisi daftar hadir.')
        return redirect('registrations:history')
    
    # Cek apakah sudah waktunya
    if not event.can_be_attended():
        messages.error(request, 'Daftar hadir dapat diisi pada hari H setelah jam kegiatan dimulai.')
        return redirect('registrations:history')
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            
            # Validasi token
            if registration.token != token:
                messages.error(request, 'Token tidak valid.')
                return render(request, 'registrations/attendance.html', {
                    'form': form,
                    'event': event,
                    'registration': registration
                })
            
            # Update status
            registration.status = 'attended'
            registration.attendance_at = timezone.now()
            registration.save()
            
            # Generate sertifikat (jika ada template)
            if event.certificate_template:
                from certificates.services import generate_certificate
                generate_certificate(registration)
            
            messages.success(request, 'Daftar hadir berhasil!')
            return redirect('registrations:history')
    else:
        form = AttendanceForm()
    
    return render(request, 'registrations/attendance.html', {
        'form': form,
        'event': event,
        'registration': registration
    })

@login_required
@email_verification_required
def history(request):
    """Riwayat kegiatan user"""
    registrations = EventRegistration.objects.filter(
        user=request.user
    ).select_related('event').order_by('-created_at')
    
    return render(request, 'registrations/history.html', {
        'registrations': registrations
    })
```

### dashboard/views.py

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from datetime import datetime
from accounts.decorators import role_required
from events.models import Event
from registrations.models import EventRegistration
from utils.export_service import export_participants_to_excel, export_participants_to_csv

@login_required
@role_required('user')
def user_dashboard(request):
    """Dashboard untuk user/peserta"""
    # Statistik user
    total_registered = EventRegistration.objects.filter(user=request.user).count()
    total_attended = EventRegistration.objects.filter(
        user=request.user,
        status='attended'
    ).count()
    total_certificates = request.user.certificates.count()
    
    # Kegiatan terdekat
    upcoming_registrations = EventRegistration.objects.filter(
        user=request.user,
        status='registered',
        event__event_date__gte=timezone.now().date()
    ).select_related('event').order_by('event__event_date')[:5]
    
    return render(request, 'dashboard/user_dashboard.html', {
        'total_registered': total_registered,
        'total_attended': total_attended,
        'total_certificates': total_certificates,
        'upcoming_registrations': upcoming_registrations,
    })

@login_required
@role_required('admin')
def admin_dashboard(request):
    """Dashboard untuk admin"""
    current_year = timezone.now().year
    
    # Statistik: Jumlah kegiatan per bulan
    monthly_events = Event.objects.filter(
        created_at__year=current_year
    ).annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Statistik: Jumlah peserta per bulan
    monthly_participants = EventRegistration.objects.filter(
        status='attended',
        attendance_at__year=current_year
    ).annotate(
        month=ExtractMonth('attendance_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Top 10 kegiatan dengan peserta terbanyak
    top_events = Event.objects.annotate(
        participant_count=Count('registrations', filter=Q(registrations__status='attended'))
    ).order_by('-participant_count')[:10]
    
    # Data untuk chart (format untuk Chart.js)
    events_chart_data = {
        'labels': [f'Bulan {item["month"]}' for item in monthly_events],
        'data': [item['count'] for item in monthly_events]
    }
    
    participants_chart_data = {
        'labels': [f'Bulan {item["month"]}' for item in monthly_participants],
        'data': [item['count'] for item in monthly_participants]
    }
    
    top_events_chart_data = {
        'labels': [event.title[:30] + '...' if len(event.title) > 30 else event.title for event in top_events],
        'data': [event.participant_count for event in top_events]
    }
    
    return render(request, 'dashboard/admin_dashboard.html', {
        'events_chart_data': events_chart_data,
        'participants_chart_data': participants_chart_data,
        'top_events_chart_data': top_events_chart_data,
        'top_events': top_events,
    })

@login_required
@role_required('event_organizer')
def organizer_dashboard(request):
    """Dashboard untuk event organizer"""
    current_year = timezone.now().year
    user_id = request.user.id
    
    # Statistik: Jumlah kegiatan per bulan (HANYA KEGIATAN SENDIRI)
    monthly_events = Event.objects.filter(
        user_id=user_id,
        created_at__year=current_year
    ).annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Statistik: Jumlah peserta per bulan (HANYA KEGIATAN SENDIRI)
    monthly_participants = EventRegistration.objects.filter(
        event__user_id=user_id,
        status='attended',
        attendance_at__year=current_year
    ).annotate(
        month=ExtractMonth('attendance_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Top 10 kegiatan dengan peserta terbanyak (HANYA KEGIATAN SENDIRI)
    top_events = Event.objects.filter(
        user_id=user_id
    ).annotate(
        participant_count=Count('registrations', filter=Q(registrations__status='attended'))
    ).order_by('-participant_count')[:10]
    
    # Data untuk chart
    events_chart_data = {
        'labels': [f'Bulan {item["month"]}' for item in monthly_events],
        'data': [item['count'] for item in monthly_events]
    }
    
    participants_chart_data = {
        'labels': [f'Bulan {item["month"]}' for item in monthly_participants],
        'data': [item['count'] for item in monthly_participants]
    }
    
    top_events_chart_data = {
        'labels': [event.title[:30] + '...' if len(event.title) > 30 else event.title for event in top_events],
        'data': [event.participant_count for event in top_events]
    }
    
    return render(request, 'dashboard/organizer_dashboard.html', {
        'events_chart_data': events_chart_data,
        'participants_chart_data': participants_chart_data,
        'top_events_chart_data': top_events_chart_data,
        'top_events': top_events,
    })

@login_required
@role_required('admin')
def admin_export(request):
    """Export data peserta untuk admin (semua peserta)"""
    format_type = request.GET.get('format', 'excel')
    
    if format_type == 'csv':
        return export_participants_to_csv(role='admin')
    else:
        return export_participants_to_excel(role='admin')

@login_required
@role_required('event_organizer')
def organizer_export(request):
    """Export data peserta untuk event organizer (hanya peserta kegiatan sendiri)"""
    format_type = request.GET.get('format', 'excel')
    
    if format_type == 'csv':
        return export_participants_to_csv(user_id=request.user.id, role='event_organizer')
    else:
        return export_participants_to_excel(user_id=request.user.id, role='event_organizer')
```

---

## 📝 ADMIN CONFIGURATION

### accounts/admin.py

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserSession

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'role', 'is_verified', 'created_at']
    list_filter = ['role', 'email_verified_at', 'is_active']
    search_fields = ['email', 'name', 'phone']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'address', 'education')}),
        ('Role', {'fields': ('role',)}),
        ('Email Verification', {'fields': ('email_verified_at', 'otp_code', 'otp_expired')}),
        ('Permissions', {'fields': ('is_active',)}),
    )

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'last_activity', 'expired_at', 'is_expired']
    list_filter = ['expired_at']
    search_fields = ['user__email', 'session_key']
    
    def is_expired(self, obj):
        from django.utils import timezone
        return timezone.now() > obj.expired_at
    is_expired.boolean = True
```

### events/admin.py

```python
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'event_date', 'event_time', 'status', 'created_at']
    list_filter = ['status', 'event_date', 'created_at']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['registration_closed_at', 'created_at', 'updated_at']
```

---

Lanjutkan dengan membuat template examples dan management commands?

