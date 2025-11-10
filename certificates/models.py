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
    
    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.user.name}"

