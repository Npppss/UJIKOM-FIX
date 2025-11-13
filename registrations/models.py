from django.db import models
from accounts.models import User
from events.models import Event


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('absent', 'Absent'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('not_required', 'Tidak Diperlukan'),
        ('pending', 'Menunggu Validasi'),
        ('approved', 'Disetujui'),
        ('rejected', 'Ditolak'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    token = models.CharField(max_length=10, unique=True, verbose_name='Token 10 Digit')
    token_sent_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    attendance_at = models.DateTimeField(null=True, blank=True)
    
    # Payment fields
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True, verbose_name='Bukti Pembayaran')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='not_required', verbose_name='Status Pembayaran')
    payment_validated_at = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Validasi Pembayaran')
    payment_validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_payments', verbose_name='Divalidasi Oleh')
    payment_rejection_reason = models.TextField(null=True, blank=True, verbose_name='Alasan Penolakan Pembayaran')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'event_registrations'
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'
        unique_together = ['event', 'user']
    
    def __str__(self):
        return f"{self.user.name} - {self.event.title}"


class PaymentRejection(models.Model):
    """Model untuk track history penolakan pembayaran"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='payment_rejections')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_rejections')
    rejection_reason = models.TextField(verbose_name='Alasan Penolakan')
    rejected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_payments', verbose_name='Ditolak Oleh')
    rejected_at = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Penolakan')
    
    class Meta:
        db_table = 'payment_rejections'
        verbose_name = 'Payment Rejection'
        verbose_name_plural = 'Payment Rejections'
        ordering = ['-rejected_at']
    
    def __str__(self):
        return f"Rejection: {self.user.name} - {self.event.title} ({self.rejected_at})"

