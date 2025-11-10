# IMPLEMENTASI DJANGO - SISTEM PENDAFTARAN KEGIATAN (3 ROLE)

Dokumentasi implementasi lengkap menggunakan Django Framework untuk frontend dan backend.

---

## 📁 STRUKTUR FOLDER DJANGO

```
event_registration/
├── manage.py
├── requirements.txt
├── event_registration/          # Main project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py                  # Root URLs
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                    # App untuk authentication & user management
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── middleware.py           # Session timeout middleware
│   ├── validators.py           # Password validator
│   └── templates/
│       ├── accounts/
│       │   ├── login.html
│       │   ├── register.html
│       │   ├── email_verify.html
│       │   └── password_reset.html
├── events/                     # App untuk event management
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── services.py            # Business logic
│   └── templates/
│       ├── events/
│       │   ├── catalog.html
│       │   ├── detail.html
│       │   ├── create.html
│       │   └── list.html
├── dashboard/                  # App untuk dashboard
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       ├── dashboard/
│       │   ├── admin_dashboard.html
│       │   ├── organizer_dashboard.html
│       │   └── user_dashboard.html
├── registrations/              # App untuk pendaftaran & attendance
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
│       ├── registrations/
│       │   ├── register_event.html
│       │   ├── attendance.html
│       │   └── history.html
├── certificates/              # App untuk sertifikat
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── services.py
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── email_service.py
│   ├── token_service.py
│   └── export_service.py
├── static/                    # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── media/                     # Uploaded files
│   ├── flyers/
│   └── certificates/
└── templates/                 # Base templates
    ├── base.html
    ├── base_user.html
    ├── base_admin.html
    └── base_organizer.html
```

---

## 🔧 INSTALASI & SETUP

### 1. Install Dependencies

```bash
pip install django
pip install django-environ
pip install pillow                    # Untuk image upload
pip install django-crispy-forms       # Untuk form rendering
pip install crispy-bootstrap5         # Bootstrap 5 untuk forms
pip install openpyxl                  # Untuk export Excel
pip install pandas                    # Untuk export CSV
pip install django-session-timeout    # Opsional: untuk session timeout
pip install django-extensions         # Opsional: untuk development tools
```

### 2. requirements.txt

```txt
Django>=4.2.0
django-environ>=0.10.0
Pillow>=10.0.0
django-crispy-forms>=2.0
crispy-bootstrap5>=0.7
openpyxl>=3.1.0
pandas>=2.0.0
```

### 3. Create Project & Apps

```bash
django-admin startproject event_registration .
python manage.py startapp accounts
python manage.py startapp events
python manage.py startapp dashboard
python manage.py startapp registrations
python manage.py startapp certificates
mkdir utils
```

---

## 📊 DJANGO MODELS

### accounts/models.py

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
import secrets

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email harus diisi')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('email_verified_at', models.DateTimeField(auto_now_add=True))
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('event_organizer', 'Event Organizer'),
    ]
    
    name = models.CharField(max_length=255, verbose_name='Nama Lengkap')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(
        max_length=20,
        verbose_name='No. Handphone',
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Format nomor telepon tidak valid")]
    )
    address = models.TextField(verbose_name='Alamat Tempat Tinggal')
    education = models.CharField(max_length=100, verbose_name='Pendidikan Terakhir')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    # Email verification
    email_verified_at = models.DateTimeField(null=True, blank=True)
    email_verification_token = models.CharField(max_length=255, null=True, blank=True)
    email_verification_expired = models.DateTimeField(null=True, blank=True)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_expired = models.DateTimeField(null=True, blank=True)
    
    # Password reset
    reset_password_token = models.CharField(max_length=255, null=True, blank=True)
    reset_password_expired = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def is_verified(self):
        return self.email_verified_at is not None
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_event_organizer(self):
        return self.role == 'event_organizer'
    
    def is_user(self):
        return self.role == 'user'

class UserSession(models.Model):
    """Custom session untuk timeout 5 menit"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    last_activity = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sessions'
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['expired_at']),
        ]
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expired_at
```

### events/models.py

```python
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta
from accounts.models import User

class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    title = models.CharField(max_length=255, verbose_name='Judul Kegiatan')
    description = models.TextField(verbose_name='Deskripsi Kegiatan')
    event_date = models.DateField(verbose_name='Tanggal Kegiatan')
    event_time = models.TimeField(verbose_name='Waktu Kegiatan')
    location = models.CharField(max_length=255, verbose_name='Lokasi')
    flyer = models.ImageField(
        upload_to='flyers/',
        null=True,
        blank=True,
        verbose_name='Flyer Kegiatan'
    )
    certificate_template = models.FileField(
        upload_to='certificate_templates/',
        null=True,
        blank=True,
        verbose_name='Template Sertifikat'
    )
    registration_closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['event_date', 'event_time']),
            models.Index(fields=['status']),
            models.Index(fields=['registration_closed_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto set registration_closed_at
        if self.event_date and self.event_time:
            from datetime import datetime
            event_datetime = datetime.combine(self.event_date, self.event_time)
            self.registration_closed_at = event_datetime
        super().save(*args, **kwargs)
    
    def is_registration_open(self):
        return timezone.now() < self.registration_closed_at if self.registration_closed_at else False
    
    def can_be_attended(self):
        """Cek apakah sudah waktunya untuk isi daftar hadir"""
        if not self.event_date or not self.event_time:
            return False
        from datetime import datetime
        event_datetime = datetime.combine(self.event_date, self.event_time)
        event_datetime = timezone.make_aware(event_datetime)
        return timezone.now() >= event_datetime
    
    def get_participant_count(self):
        return self.registrations.filter(status='attended').count()
```

### registrations/models.py

```python
from django.db import models
from accounts.models import User
from events.models import Event

class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('absent', 'Absent'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    token = models.CharField(max_length=10, unique=True, verbose_name='Token 10 Digit')
    token_sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    attendance_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'event_registrations'
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'
        unique_together = ['event', 'user']  # Satu user hanya bisa daftar sekali per event
        indexes = [
            models.Index(fields=['event', 'user']),
            models.Index(fields=['token']),
            models.Index(fields=['status']),
            models.Index(fields=['attendance_at']),
        ]
    
    def __str__(self):
        return f"{self.user.name} - {self.event.title}"
```

### certificates/models.py

```python
from django.db import models
from accounts.models import User
from events.models import Event
from registrations.models import EventRegistration

class Certificate(models.Model):
    event_registration = models.OneToOneField(
        EventRegistration,
        on_delete=models.CASCADE,
        related_name='certificate'
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='certificates')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    certificate_file = models.FileField(
        upload_to='certificates/',
        verbose_name='File Sertifikat'
    )
    certificate_number = models.CharField(max_length=100, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    downloaded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'certificates'
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
        indexes = [
            models.Index(fields=['event']),
            models.Index(fields=['user']),
            models.Index(fields=['certificate_number']),
        ]
    
    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.user.name}"
```

---

## 🔐 DJANGO AUTHENTICATION & MIDDLEWARE

### accounts/middleware.py

```python
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from .models import UserSession
from datetime import timedelta

class SessionTimeoutMiddleware(MiddlewareMixin):
    """Middleware untuk session timeout 5 menit"""
    
    def process_request(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            
            if session_key:
                try:
                    user_session = UserSession.objects.get(session_key=session_key)
                    
                    # Cek apakah session expired
                    if user_session.is_expired():
                        # Destroy session
                        user_session.delete()
                        request.session.flush()
                        
                        # Logout user
                        from django.contrib.auth import logout
                        logout(request)
                        
                        messages.error(request, 'Session expired. Tidak ada aktivitas selama 5 menit.')
                        return redirect('accounts:login')
                    
                    # Update last_activity dan expired_at
                    user_session.last_activity = timezone.now()
                    user_session.expired_at = timezone.now() + timedelta(minutes=5)
                    user_session.save()
                    
                except UserSession.DoesNotExist:
                    # Buat session baru jika belum ada
                    UserSession.objects.create(
                        user=request.user,
                        session_key=session_key,
                        last_activity=timezone.now(),
                        expired_at=timezone.now() + timedelta(minutes=5),
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RoleRequiredMiddleware(MiddlewareMixin):
    """Middleware untuk cek role user"""
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'required_role'):
            required_role = view_func.required_role
            
            if not request.user.is_authenticated:
                messages.error(request, 'Silakan login terlebih dahulu.')
                return redirect('accounts:login')
            
            if request.user.role != required_role:
                messages.error(request, 'Anda tidak memiliki akses untuk halaman ini.')
                
                # Redirect berdasarkan role
                if request.user.role == 'admin':
                    return redirect('dashboard:admin')
                elif request.user.role == 'event_organizer':
                    return redirect('dashboard:organizer')
                else:
                    return redirect('dashboard:user')
        
        return None
```

### Decorator untuk Role Check

### accounts/decorators.py

```python
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(*allowed_roles):
    """Decorator untuk cek role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Silakan login terlebih dahulu.')
                return redirect('accounts:login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'Anda tidak memiliki akses untuk halaman ini.')
                
                if request.user.role == 'admin':
                    return redirect('dashboard:admin')
                elif request.user.role == 'event_organizer':
                    return redirect('dashboard:organizer')
                else:
                    return redirect('dashboard:user')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def email_verification_required(view_func):
    """Decorator untuk cek email verification (hanya untuk user)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'user':
            if not request.user.is_verified():
                messages.warning(request, 'Silakan verifikasi email terlebih dahulu.')
                return redirect('accounts:email_verify')
        return view_func(request, *args, **kwargs)
    return wrapper
```

### Decorator untuk Event Access

### events/decorators.py

```python
from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Event

def event_owner_required(view_func):
    """Decorator untuk cek apakah user adalah owner event (untuk Event Organizer)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        event_id = kwargs.get('event_id') or kwargs.get('id')
        event = get_object_or_404(Event, id=event_id)
        
        # Admin bisa akses semua
        if request.user.is_admin():
            return view_func(request, *args, **kwargs)
        
        # Event Organizer hanya bisa akses event sendiri
        if request.user.is_event_organizer():
            if event.user_id != request.user.id:
                messages.error(request, 'Anda tidak memiliki akses untuk mengelola kegiatan ini.')
                return redirect('dashboard:organizer')
        
        return view_func(request, *args, **kwargs)
    return wrapper
```

---

## 📝 DJANGO FORMS

### accounts/forms.py

```python
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import User
import re

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password',
        min_length=8,
        help_text='Minimal 8 karakter, harus mengandung angka, huruf besar, huruf kecil, dan karakter spesial'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Konfirmasi Password'
    )
    
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'address', 'education', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Validasi password
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
        
        if not re.match(password_pattern, password):
            raise ValidationError(
                'Password minimal 8 karakter dan harus mengandung angka, '
                'huruf besar, huruf kecil, dan karakter spesial (@$!%*?&#)'
            )
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError({'password_confirm': 'Password dan konfirmasi password tidak cocok'})
        
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email sudah terdaftar. Gunakan email lain atau lakukan login.')
        return email

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )

class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan 6 digit OTP'}),
        label='Kode OTP'
    )

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )

class PasswordResetConfirmForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password Baru',
        min_length=8
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Konfirmasi Password Baru'
    )
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
        
        if not re.match(password_pattern, password):
            raise ValidationError(
                'Password minimal 8 karakter dan harus mengandung angka, '
                'huruf besar, huruf kecil, dan karakter spesial (@$!%*?&#)'
            )
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError({'password_confirm': 'Password dan konfirmasi password tidak cocok'})
        
        return cleaned_data
```

### events/forms.py

```python
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'event_time', 'location', 'flyer', 'certificate_template']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'flyer': forms.FileInput(attrs={'class': 'form-control'}),
            'certificate_template': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        
        if event_date:
            # Validasi H-3: minimal 3 hari dari sekarang
            min_date = (timezone.now().date() + timedelta(days=3))
            
            if event_date < min_date:
                raise ValidationError(
                    f'Kegiatan harus dibuat minimal 3 hari sebelum tanggal penyelenggaraan (H-3). '
                    f'Tanggal terdekat yang bisa dipilih: {min_date.strftime("%d %B %Y")}'
                )
        
        return event_date
    
    def clean_flyer(self):
        flyer = self.cleaned_data.get('flyer')
        
        if flyer:
            # Validasi ukuran file (max 5MB)
            if flyer.size > 5 * 1024 * 1024:
                raise ValidationError('Ukuran file flyer maksimal 5MB')
            
            # Validasi jenis file
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if flyer.content_type not in allowed_types:
                raise ValidationError('File flyer harus berupa gambar (JPG, PNG)')
        
        return flyer
    
    def clean_certificate_template(self):
        template = self.cleaned_data.get('certificate_template')
        
        if template:
            # Validasi ukuran file (max 10MB)
            if template.size > 10 * 1024 * 1024:
                raise ValidationError('Ukuran file template sertifikat maksimal 10MB')
            
            # Validasi jenis file
            allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
            if template.content_type not in allowed_types:
                raise ValidationError('File template sertifikat harus berupa PDF atau gambar')
        
        return template
```

### registrations/forms.py

```python
from django import forms

class AttendanceForm(forms.Form):
    token = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan token 10 digit',
            'maxlength': '10'
        }),
        label='Token Daftar Hadir',
        help_text='Masukkan token 10 digit yang dikirim ke email Anda'
    )
    
    def clean_token(self):
        token = self.cleaned_data.get('token')
        
        # Validasi format: hanya angka, 10 digit
        if not token.isdigit() or len(token) != 10:
            raise forms.ValidationError('Token harus berupa 10 digit angka')
        
        return token
```

---

## 🎯 DJANGO VIEWS (Contoh)

### accounts/views.py (Partial)

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
import secrets
from .models import User, UserSession
from .forms import UserRegistrationForm, LoginForm, OTPVerificationForm
from utils.email_service import send_verification_email, send_registration_token

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.set_password(form.cleaned_data['password'])
            
            # Generate OTP dan token
            otp_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
            verification_token = secrets.token_urlsafe(32)
            
            user.otp_code = otp_code
            user.otp_expired = timezone.now() + timedelta(minutes=5)
            user.email_verification_token = verification_token
            user.email_verification_expired = timezone.now() + timedelta(minutes=5)
            
            user.save()
            
            # Kirim email verifikasi
            send_verification_email(user, otp_code, verification_token)
            
            messages.success(request, 'Registrasi berhasil! Silakan cek email untuk verifikasi.')
            return redirect('accounts:email_verify')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Cek email verification untuk user biasa
                if user.role == 'user' and not user.is_verified():
                    messages.error(request, 'Silakan verifikasi email terlebih dahulu.')
                    return redirect('accounts:email_verify')
                
                # Login user
                login(request, user)
                
                # Buat/update session untuk timeout
                session_key = request.session.session_key
                UserSession.objects.update_or_create(
                    session_key=session_key,
                    defaults={
                        'user': user,
                        'last_activity': timezone.now(),
                        'expired_at': timezone.now() + timedelta(minutes=5),
                        'ip_address': request.META.get('REMOTE_ADDR'),
                        'user_agent': request.META.get('HTTP_USER_AGENT', '')
                    }
                )
                
                # Redirect berdasarkan role
                if user.role == 'admin':
                    return redirect('dashboard:admin')
                elif user.role == 'event_organizer':
                    return redirect('dashboard:organizer')
                else:
                    return redirect('dashboard:user')
            else:
                messages.error(request, 'Email atau password salah.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def verify_email(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            
            try:
                user = User.objects.get(otp_code=otp_code)
                
                # Cek expired
                if timezone.now() > user.otp_expired:
                    messages.error(request, 'Kode OTP sudah expired. Silakan request OTP baru.')
                    return redirect('accounts:resend_otp')
                
                # Verifikasi email
                user.email_verified_at = timezone.now()
                user.otp_code = None
                user.otp_expired = None
                user.email_verification_token = None
                user.email_verification_expired = None
                user.save()
                
                messages.success(request, 'Email berhasil diverifikasi! Silakan login.')
                return redirect('accounts:login')
                
            except User.DoesNotExist:
                messages.error(request, 'Kode OTP tidak valid.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'accounts/email_verify.html', {'form': form})

def verify_email_link(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
        
        # Cek expired
        if timezone.now() > user.email_verification_expired:
            messages.error(request, 'Link verifikasi sudah expired. Silakan request link baru.')
            return redirect('accounts:resend_otp')
        
        # Verifikasi email
        user.email_verified_at = timezone.now()
        user.email_verification_token = None
        user.email_verification_expired = None
        user.otp_code = None
        user.otp_expired = None
        user.save()
        
        messages.success(request, 'Email berhasil diverifikasi! Silakan login.')
        return redirect('accounts:login')
        
    except User.DoesNotExist:
        messages.error(request, 'Link verifikasi tidak valid.')
        return redirect('accounts:login')
```

### events/views.py (Partial)

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from accounts.decorators import role_required, email_verification_required
from events.decorators import event_owner_required
from .models import Event
from .forms import EventForm
from .services import validate_h3_rule

@login_required
@role_required('admin', 'event_organizer')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.status = 'published'
            event.save()
            
            messages.success(request, 'Kegiatan berhasil dibuat!')
            return redirect('events:list')
    else:
        form = EventForm()
    
    return render(request, 'events/create.html', {'form': form})

@login_required
@role_required('admin', 'event_organizer')
@event_owner_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kegiatan berhasil diupdate!')
            return redirect('events:list')
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/edit.html', {'form': form, 'event': event})

def catalog(request):
    """Katalog kegiatan publik (tidak perlu login)"""
    events = Event.objects.filter(
        status='published',
        deleted_at__isnull=True,
        registration_closed_at__gt=timezone.now()
    )
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', 'nearest')
    if sort_by == 'newest':
        events = events.order_by('-event_date', '-event_time')
    elif sort_by == 'oldest':
        events = events.order_by('event_date', 'event_time')
    elif sort_by == 'most_participants':
        events = events.annotate(
            participant_count=Count('registrations')
        ).order_by('-participant_count')
    else:  # nearest (default)
        events = events.order_by('event_date', 'event_time')
    
    # Pagination
    paginator = Paginator(events, 12)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    
    return render(request, 'events/catalog.html', {
        'events': events,
        'search_query': search_query,
        'sort_by': sort_by
    })
```

---

Lanjutkan dengan bagian Views untuk registrations, dashboard, dan utilities... (masih ada banyak)

Apakah saya lanjutkan membuat file-file Django lengkap?

