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
        from django.utils import timezone
        extra_fields.setdefault('email_verified_at', timezone.now())
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
    
    # Field untuk suspend organizer
    is_suspended = models.BooleanField(default=False, verbose_name='Suspended')
    suspended_at = models.DateTimeField(null=True, blank=True)
    suspended_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='suspended_users')
    suspension_reason = models.TextField(null=True, blank=True, verbose_name='Alasan Suspension')


class Achievement(models.Model):
    """Model untuk achievement yang diberikan ke user"""
    TYPE_CHOICES = [
        ('report_valid', 'Report Valid'),
        ('community_guardian', 'Community Guardian'),
        ('truth_seeker', 'Truth Seeker'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement_type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Jenis Achievement')
    title = models.CharField(max_length=255, verbose_name='Judul Achievement')
    description = models.TextField(verbose_name='Deskripsi')
    icon = models.CharField(max_length=50, default='bi-trophy', verbose_name='Icon')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'achievements'
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.name} - {self.title}"


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
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expired_at


class EventOrganizer(models.Model):
    """Model untuk Event Organizer dengan verifikasi identitas"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='event_organizer',
        verbose_name='User'
    )
    organizer_name = models.CharField(
        max_length=150,
        verbose_name='Nama Organizer',
        help_text='Nama resmi organisasi atau perusahaan'
    )
    person_in_charge = models.CharField(
        max_length=100,
        verbose_name='Penanggung Jawab',
        help_text='Nama lengkap penanggung jawab'
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='No. Telepon',
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Format nomor telepon tidak valid")]
    )
    email = models.EmailField(
        verbose_name='Email Organizer',
        help_text='Email resmi organizer (bisa berbeda dari email user)'
    )
    address = models.TextField(
        verbose_name='Alamat Organizer',
        help_text='Alamat lengkap kantor/organisasi'
    )
    description = models.TextField(
        verbose_name='Deskripsi Organizer',
        help_text='Deskripsi singkat tentang organizer dan kegiatan yang biasa dilakukan'
    )
    website = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Website',
        help_text='Website organizer (opsional)'
    )
    social_media = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Social Media',
        help_text='Link social media (Instagram, Facebook, dll) - opsional'
    )
    business_license = models.FileField(
        upload_to='eo_docs/',
        blank=True,
        null=True,
        verbose_name='Surat Izin Usaha',
        help_text='Upload surat izin usaha atau dokumen legal lainnya (opsional)'
    )
    logo = models.ImageField(
        upload_to='eo_logos/',
        blank=True,
        null=True,
        verbose_name='Logo Organizer',
        help_text='Logo organizer (opsional)'
    )
    verified = models.BooleanField(
        default=False,
        verbose_name='Terverifikasi',
        help_text='Status verifikasi oleh admin'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Dibuat Pada'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Diperbarui Pada'
    )
    
    class Meta:
        db_table = 'event_organizers'
        verbose_name = 'Event Organizer'
        verbose_name_plural = 'Event Organizers'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.organizer_name
    
    def is_verified(self):
        return self.verified

