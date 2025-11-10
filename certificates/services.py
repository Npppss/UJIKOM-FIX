import os
from django.conf import settings
from django.utils import timezone
from .models import Certificate
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io


def generate_certificate(registration):
    """
    Generate sertifikat untuk user yang sudah mengisi daftar hadir
    """
    # Cek apakah sertifikat sudah ada
    if hasattr(registration, 'certificate'):
        return registration.certificate
    
    event = registration.event
    user = registration.user
    
    # Cek apakah event punya template sertifikat
    if not event.certificate_template:
        return None
    
    # Generate certificate number
    certificate_number = f"CERT-{event.id:04d}-{registration.id:05d}-{timezone.now().strftime('%Y%m%d')}"
    
    # Create PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Background (optional - bisa menggunakan template image jika ada)
    # Jika event punya template, kita bisa load dan use sebagai background
    # Untuk sekarang, kita buat sederhana dulu
    
    # Title
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height - 100, "SERTIFIKAT")
    
    # Subtitle
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 140, "Diberikan kepada:")
    
    # User name
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 180, user.name)
    
    # Event title
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 220, f"Atas partisipasinya dalam kegiatan:")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 250, event.title)
    
    # Event date
    c.setFont("Helvetica", 12)
    event_date_str = event.event_date.strftime('%d %B %Y')
    c.drawCentredString(width/2, height - 280, f"Tanggal: {event_date_str}")
    
    # Certificate number
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, 50, f"Nomor Sertifikat: {certificate_number}")
    
    # Save PDF
    c.save()
    buffer.seek(0)
    
    # Save to file
    from django.core.files.base import ContentFile
    filename = f"certificate_{certificate_number}.pdf"
    file_content = ContentFile(buffer.read())
    
    # Create certificate object
    certificate = Certificate.objects.create(
        event_registration=registration,
        event=event,
        user=user,
        certificate_number=certificate_number,
        certificate_file=file_content
    )
    certificate.certificate_file.save(filename, file_content, save=True)
    
    return certificate

