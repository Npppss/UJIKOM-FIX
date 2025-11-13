from django.db import models
from django.utils import timezone
from accounts.models import User
from datetime import datetime


class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    CATEGORY_CHOICES = [
        ('seminar', 'Seminar & Conference'),
        ('concert', 'Concert & Festival'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    title = models.CharField(max_length=255, verbose_name='Judul Kegiatan')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='seminar', verbose_name='Kategori Event')
    description = models.TextField(verbose_name='Deskripsi Kegiatan')
    event_date = models.DateField(verbose_name='Tanggal Kegiatan')
    event_time = models.TimeField(verbose_name='Waktu Kegiatan')
    location = models.CharField(max_length=255, verbose_name='Lokasi')
    location_type = models.CharField(max_length=20, choices=[('offline', 'Offline'), ('online', 'Online'), ('hybrid', 'Hybrid')], default='offline', verbose_name='Tipe Lokasi')
    zoom_link = models.URLField(max_length=500, null=True, blank=True, verbose_name='Link Zoom Meeting', help_text='Link Zoom Meeting (jika event online/hybrid)')
    zoom_meeting_id = models.CharField(max_length=50, null=True, blank=True, verbose_name='Meeting ID', help_text='Zoom Meeting ID (opsional)')
    zoom_passcode = models.CharField(max_length=50, null=True, blank=True, verbose_name='Passcode', help_text='Zoom Passcode (opsional)')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Harga Tiket', help_text='Kosongkan jika event gratis')
    bank_account = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nomor Rekening', help_text='Nomor rekening untuk pembayaran (jika event berbayar)')
    bank_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nama Bank', help_text='Nama bank (contoh: BCA, Mandiri, BRI)')
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
    material_file = models.FileField(
        upload_to='event_materials/',
        null=True,
        blank=True,
        verbose_name='Materi Seminar',
        help_text='Upload materi seminar (PDF, PPT, DOCX, ZIP). Hanya untuk event kategori Seminar.'
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
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto set registration_closed_at
        if self.event_date and self.event_time:
            # Convert event_time to time object if it's a string
            if isinstance(self.event_time, str):
                from datetime import time as dt_time
                time_parts = self.event_time.split(':')
                self.event_time = dt_time(int(time_parts[0]), int(time_parts[1]))
            
            event_datetime = datetime.combine(self.event_date, self.event_time)
            self.registration_closed_at = timezone.make_aware(event_datetime)
        super().save(*args, **kwargs)
    
    def is_registration_open(self):
        return timezone.now() < self.registration_closed_at if self.registration_closed_at else False
    
    def can_be_attended(self):
        """Cek apakah sudah waktunya untuk isi daftar hadir
        User bisa mengisi daftar hadir setelah event dimulai, meskipun telat,
        selama event belum selesai atau dibatalkan
        """
        if not self.event_date or not self.event_time:
            return False
        
        # Jika event sudah selesai atau dibatalkan, tidak bisa lagi
        if self.status in ['completed', 'cancelled']:
            return False
        
        # Cek apakah event sudah dimulai (bisa telat, tidak masalah)
        # Pastikan menggunakan timezone yang sama untuk perbandingan
        from django.conf import settings
        import pytz
        
        event_datetime = datetime.combine(self.event_date, self.event_time)
        # Buat aware datetime dengan timezone Asia/Jakarta
        jakarta_tz = pytz.timezone(settings.TIME_ZONE)
        event_datetime = jakarta_tz.localize(event_datetime)
        
        # Ambil waktu sekarang dan konversi ke timezone Jakarta
        now = timezone.localtime()  # Otomatis menggunakan TIME_ZONE dari settings
        
        return now >= event_datetime
    
    def can_access_material(self, user):
        """
        Cek apakah user bisa mengakses materi seminar
        Kondisi:
        1. User harus login
        2. Event kategori = 'seminar'
        3. Event status = 'completed' (Selesai)
        4. User harus terdaftar di event tersebut
        5. Material file harus ada
        """
        if not user or not user.is_authenticated:
            return False
        
        if self.category != 'seminar':
            return False
        
        if self.status != 'completed':
            return False
        
        if not self.material_file:
            return False
        
        # Cek apakah user terdaftar
        from registrations.models import EventRegistration
        is_registered = EventRegistration.objects.filter(
            event=self,
            user=user
        ).exists()
        
        return is_registered


class ReportEvent(models.Model):
    """Model untuk laporan event dari user"""
    REASON_CHOICES = [
        ('spam', 'Spam atau Konten Menyesatkan'),
        ('inappropriate', 'Konten Tidak Pantas'),
        ('fraud', 'Penipuan atau Scam'),
        ('duplicate', 'Event Duplikat'),
        ('other', 'Lainnya'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Menunggu Review'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_events')
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, verbose_name='Alasan Laporan')
    description = models.TextField(verbose_name='Deskripsi Laporan')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_feedback = models.TextField(null=True, blank=True, verbose_name='Feedback Admin')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_reports')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'report_events'
        verbose_name = 'Report Event'
        verbose_name_plural = 'Report Events'
        unique_together = ['event', 'reporter']  # Satu user hanya bisa report satu event sekali
    
    def __str__(self):
        return f"Report: {self.event.title} by {self.reporter.name}"


class News(models.Model):
    """Model untuk berita/artikel tentang event"""
    CATEGORY_CHOICES = [
        ('seminar', 'Seminar & Conference'),
        ('concert', 'Concert & Festival'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='news', null=True, blank=True, verbose_name='Event Terkait')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_news', verbose_name='Penulis')
    title = models.CharField(max_length=255, verbose_name='Judul Berita')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Kategori')
    content = models.TextField(verbose_name='Konten Berita')
    payment_info = models.TextField(null=True, blank=True, verbose_name='Informasi Pembayaran')
    payment_deadline = models.DateField(null=True, blank=True, verbose_name='Batas Waktu Pembayaran')
    seminar_materials = models.TextField(null=True, blank=True, verbose_name='Materi Seminar')
    concert_lineup = models.TextField(null=True, blank=True, verbose_name='Lineup Konser')
    featured_image = models.ImageField(upload_to='news/', null=True, blank=True, verbose_name='Gambar Utama')
    is_published = models.BooleanField(default=False, verbose_name='Dipublikasikan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'news'
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class NewsComment(models.Model):
    """Model untuk komentar pada berita"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', verbose_name='Berita')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_comments', verbose_name='User')
    content = models.TextField(verbose_name='Komentar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'news_comments'
        verbose_name = 'News Comment'
        verbose_name_plural = 'News Comments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.name} on {self.news.title}"

