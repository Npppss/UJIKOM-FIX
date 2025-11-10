from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from accounts.decorators import email_verification_required
from .models import Certificate


@login_required
@email_verification_required
def certificate_list(request):
    """Daftar sertifikat user"""
    certificates = Certificate.objects.filter(
        user=request.user
    ).select_related('event', 'event_registration').order_by('-generated_at')
    
    return render(request, 'certificates/list.html', {
        'certificates': certificates
    })


@login_required
@email_verification_required
def download_certificate(request, certificate_id):
    """Download sertifikat"""
    certificate = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    
    # Update downloaded_at
    from django.utils import timezone
    certificate.downloaded_at = timezone.now()
    certificate.save()
    
    # Return file response
    return FileResponse(
        certificate.certificate_file.open(),
        as_attachment=True,
        filename=f"certificate_{certificate.certificate_number}.pdf"
    )

