from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import email_verification_required
from events.models import Event
from .models import EventRegistration
from .forms import AttendanceForm, PaymentProofForm
from utils.token_service import generate_registration_token
from utils.email_service import send_registration_token


@login_required
@email_verification_required
def register_event(request, event_id):
    """User mendaftar kegiatan"""
    event = get_object_or_404(Event, id=event_id, status='published', deleted_at__isnull=True)
    
    # Cek apakah sudah terdaftar
    existing_registration = EventRegistration.objects.filter(event=event, user=request.user).first()
    if existing_registration:
        # Jika sudah terdaftar tapi belum upload bukti pembayaran (untuk event berbayar)
        if event.price and event.price > 0 and not existing_registration.payment_proof:
            messages.info(request, 'Anda sudah terdaftar. Silakan upload bukti pembayaran.')
            return redirect('events:detail', event_id=event_id)
        messages.warning(request, 'Anda sudah terdaftar pada kegiatan ini.')
        return redirect('events:detail', event_id=event_id)
    
    # Cek deadline pendaftaran
    if not event.is_registration_open():
        messages.error(request, 'Pendaftaran sudah ditutup. Kegiatan sudah dimulai atau sudah lewat.')
        return redirect('events:detail', event_id=event_id)
    
    if request.method == 'POST':
        # Jika event berbayar, handle upload bukti pembayaran
        if event.price and event.price > 0:
            payment_proof = request.FILES.get('payment_proof')
            if not payment_proof:
                messages.error(request, 'Bukti pembayaran harus diupload untuk event berbayar.')
                return redirect('events:detail', event_id=event_id)
            
            # Validasi file
            form = PaymentProofForm({'payment_proof': payment_proof}, {'payment_proof': payment_proof})
            if form.is_valid():
                payment_proof = form.cleaned_data['payment_proof']
                
                # Buat registrasi dengan bukti pembayaran
                token = generate_registration_token()
                registration = EventRegistration.objects.create(
                    event=event,
                    user=request.user,
                    token=token,
                    token_sent_at=timezone.now(),
                    status='registered',
                    payment_proof=payment_proof,
                    payment_status='pending'
                )
                
                # Kirim email token
                send_registration_token(request.user, event, token)
                
                messages.success(request, 'Pendaftaran berhasil! Bukti pembayaran telah diupload. Silakan tunggu validasi dari Event Organizer. Token telah dikirim ke email Anda.')
                return redirect('registrations:history')
            else:
                # Form tidak valid, redirect kembali dengan error
                for error in form.errors.values():
                    messages.error(request, error[0])
                return redirect('events:detail', event_id=event_id)
        else:
            # Event gratis, langsung daftar
            token = generate_registration_token()
            registration = EventRegistration.objects.create(
                event=event,
                user=request.user,
                token=token,
                token_sent_at=timezone.now(),
                status='registered',
                payment_status='not_required'
            )
            
            # Kirim email token
            send_registration_token(request.user, event, token)
            
            messages.success(request, 'Pendaftaran berhasil! Token telah dikirim ke email Anda.')
            return redirect('registrations:history')
    else:
        # GET request - redirect ke detail event untuk form upload
        return redirect('events:detail', event_id=event_id)


@login_required
@email_verification_required
def upload_payment(request, event_id):
    """User upload bukti pembayaran setelah terdaftar"""
    event = get_object_or_404(Event, id=event_id, status='published', deleted_at__isnull=True)
    registration = get_object_or_404(EventRegistration, event=event, user=request.user)
    
    # Cek apakah event berbayar
    if not event.price or event.price <= 0:
        messages.error(request, 'Event ini tidak memerlukan pembayaran.')
        return redirect('events:detail', event_id=event_id)
    
    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES, instance=registration)
        if form.is_valid():
            registration.payment_status = 'pending'
            registration.payment_rejection_reason = None  # Reset alasan penolakan
            form.save()
            messages.success(request, 'Bukti pembayaran berhasil diupload. Silakan tunggu validasi dari Event Organizer.')
            return redirect('events:detail', event_id=event_id)
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = PaymentProofForm(instance=registration)
    
    return render(request, 'registrations/upload_payment.html', {
        'form': form,
        'event': event,
        'registration': registration
    })


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
    
    # Untuk event berbayar, cek apakah pembayaran sudah disetujui
    if event.price and event.price > 0:
        if registration.payment_status != 'approved':
            if registration.payment_status == 'pending':
                messages.warning(request, 'Pembayaran Anda masih menunggu validasi dari Event Organizer. Anda belum dapat mengisi daftar hadir.')
            elif registration.payment_status == 'rejected':
                messages.error(request, 'Pembayaran Anda ditolak. Silakan upload bukti pembayaran baru atau hubungi Event Organizer.')
            else:
                messages.error(request, 'Pembayaran belum disetujui. Anda belum dapat mengisi daftar hadir.')
            return redirect('registrations:history')
    
    # Cek apakah sudah waktunya (bisa telat, tidak masalah selama event belum selesai)
    if not event.can_be_attended():
        if event.status in ['completed', 'cancelled']:
            messages.error(request, 'Event ini sudah selesai atau dibatalkan. Daftar hadir tidak dapat diisi lagi.')
        else:
            messages.error(request, 'Daftar hadir dapat diisi setelah jam kegiatan dimulai.')
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
                try:
                    from certificates.services import generate_certificate
                    certificate = generate_certificate(registration)
                    if certificate:
                        messages.success(request, 'Daftar hadir berhasil! Sertifikat telah dibuat. Anda dapat mengunduhnya di halaman Sertifikat.')
                    else:
                        messages.success(request, 'Daftar hadir berhasil!')
                except Exception as e:
                    # Jika ada error generate sertifikat, tetap sukses untuk attendance
                    messages.success(request, 'Daftar hadir berhasil!')
            else:
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
        user=request.user,
        event__deleted_at__isnull=True  # Hanya event yang tidak dihapus
    ).select_related('event').order_by('-created_at')
    
    return render(request, 'registrations/history.html', {
        'registrations': registrations
    })

