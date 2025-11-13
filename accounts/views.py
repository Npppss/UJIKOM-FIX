from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import secrets
from .models import User, UserSession, EventOrganizer
from .forms import (
    UserRegistrationForm, LoginForm, OTPVerificationForm,
    PasswordResetForm, PasswordResetConfirmForm, ProfileUpdateForm,
    EventOrganizerRegistrationForm
)
from utils.email_service import send_verification_email, send_password_reset_email


def register(request):
    if request.method == 'POST':
        # Validasi checkbox Terms & Conditions
        terms_accepted = request.POST.get('terms_accepted')
        if not terms_accepted:
            messages.error(request, 'Anda harus menyetujui Syarat & Ketentuan dan Kebijakan Privasi untuk melanjutkan.')
            form = UserRegistrationForm(request.POST)
            return render(request, 'accounts/register.html', {'form': form})
        
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
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
                email_sent = send_verification_email(user, otp_code, verification_token)
                
                if email_sent:
                    messages.success(request, f'Registrasi berhasil! OTP telah dikirim ke {user.email}. Silakan cek email untuk verifikasi.')
                else:
                    messages.warning(request, f'Registrasi berhasil, tapi email gagal dikirim. OTP Anda: {otp_code}. Silakan verifikasi dengan OTP ini.')
                
                # Simpan OTP di session untuk fallback
                request.session['registration_otp'] = otp_code
                request.session['registration_email'] = user.email
                
                return redirect('accounts:email_verify')
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan saat registrasi: {str(e)}')
                print(f"Registration error: {e}")
        else:
            # Form tidak valid, tampilkan error
            messages.error(request, 'Mohon perbaiki error di form sebelum submit.')
            print(f"Form errors: {form.errors}")
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


def user_logout(request):
    if request.user.is_authenticated:
        session_key = request.session.session_key
        if session_key:
            UserSession.objects.filter(session_key=session_key).delete()
    logout(request)
    messages.success(request, 'Anda telah logout.')
    return redirect('accounts:login')


def verify_email(request):
    # Cek apakah ada OTP di session (fallback jika email gagal)
    session_otp = request.session.get('registration_otp')
    session_email = request.session.get('registration_email')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            
            try:
                # Coba cari user dengan OTP
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
                
                # Hapus session OTP
                if 'registration_otp' in request.session:
                    del request.session['registration_otp']
                if 'registration_email' in request.session:
                    del request.session['registration_email']
                
                messages.success(request, 'Email berhasil diverifikasi! Silakan login.')
                return redirect('accounts:login')
                
            except User.DoesNotExist:
                # Fallback: cek session OTP
                if session_otp and otp_code == session_otp:
                    try:
                        user = User.objects.get(email=session_email)
                        user.email_verified_at = timezone.now()
                        user.otp_code = None
                        user.otp_expired = None
                        user.email_verification_token = None
                        user.email_verification_expired = None
                        user.save()
                        
                        # Hapus session
                        del request.session['registration_otp']
                        del request.session['registration_email']
                        
                        messages.success(request, 'Email berhasil diverifikasi! Silakan login.')
                        return redirect('accounts:login')
                    except User.DoesNotExist:
                        messages.error(request, 'Kode OTP tidak valid.')
                else:
                    messages.error(request, 'Kode OTP tidak valid.')
    else:
        form = OTPVerificationForm()
        # Tampilkan OTP dari session jika ada (untuk debugging)
        if session_otp:
            messages.info(request, f'Jika email tidak diterima, gunakan OTP: {session_otp}')
    
    return render(request, 'accounts/email_verify.html', {'form': form, 'session_otp': session_otp})


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


def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            if user.is_verified():
                messages.info(request, 'Email sudah terverifikasi.')
                return redirect('accounts:login')
            
            # Generate OTP dan token baru
            otp_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
            verification_token = secrets.token_urlsafe(32)
            
            user.otp_code = otp_code
            user.otp_expired = timezone.now() + timedelta(minutes=5)
            user.email_verification_token = verification_token
            user.email_verification_expired = timezone.now() + timedelta(minutes=5)
            user.save()
            
            # Kirim email verifikasi
            send_verification_email(user, otp_code, verification_token)
            
            messages.success(request, 'Email verifikasi telah dikirim ulang. Silakan cek email.')
            return redirect('accounts:email_verify')
            
        except User.DoesNotExist:
            messages.error(request, 'Email tidak terdaftar.')
    
    return render(request, 'accounts/resend_otp.html')


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                # Generate reset token
                reset_token = secrets.token_urlsafe(32)
                user.reset_password_token = reset_token
                user.reset_password_expired = timezone.now() + timedelta(hours=1)
                user.save()
                
                # Kirim email reset password
                send_password_reset_email(user, reset_token)
                
                messages.success(request, 'Link reset password telah dikirim ke email Anda.')
                return redirect('accounts:login')
                
            except User.DoesNotExist:
                messages.error(request, 'Email tidak terdaftar.')
    else:
        form = PasswordResetForm()
    
    return render(request, 'accounts/password_reset.html', {'form': form})


def password_reset_confirm(request, token):
    try:
        user = User.objects.get(reset_password_token=token)
        
        # Cek expired
        if timezone.now() > user.reset_password_expired:
            messages.error(request, 'Link reset password sudah expired.')
            return redirect('accounts:password_reset')
        
        if request.method == 'POST':
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                # Update password
                user.set_password(form.cleaned_data['password'])
                user.reset_password_token = None
                user.reset_password_expired = None
                user.save()
                
                messages.success(request, 'Password berhasil diubah! Silakan login.')
                return redirect('accounts:login')
        else:
            form = PasswordResetConfirmForm()
        
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
        
    except User.DoesNotExist:
        messages.error(request, 'Link reset password tidak valid.')
        return redirect('accounts:password_reset')


@login_required
def profile_update(request):
    """Update data diri user"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data diri berhasil diperbarui!')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'user': request.user
    })


def terms(request):
    """Halaman Syarat & Ketentuan"""
    return render(request, 'accounts/terms.html')


def privacy(request):
    """Halaman Kebijakan Privasi"""
    return render(request, 'accounts/privacy.html')


def register_choice(request):
    """Halaman pilihan registrasi: User atau Event Organizer"""
    return render(request, 'accounts/register_choice.html')


def register_event_organizer(request):
    """Registrasi khusus untuk Event Organizer"""
    if request.method == 'POST':
        # Validasi checkbox Terms & Conditions
        terms_accepted = request.POST.get('terms_accepted')
        if not terms_accepted:
            messages.error(request, 'Anda harus menyetujui Syarat & Ketentuan dan Kebijakan Privasi untuk melanjutkan.')
            form = EventOrganizerRegistrationForm(request.POST, request.FILES)
            return render(request, 'accounts/register_organizer.html', {'form': form})
        
        form = EventOrganizerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Buat User baru dengan role event_organizer
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                
                # Gunakan email sebagai username juga (karena User model menggunakan email sebagai USERNAME_FIELD)
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    name=form.cleaned_data['person_in_charge'],  # Gunakan person_in_charge sebagai name
                    phone=form.cleaned_data['phone_number'],
                    address=form.cleaned_data['address'],
                    education='Event Organizer',  # Default education
                    role='event_organizer'
                )
                
                # Generate OTP dan token untuk email verification
                otp_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
                verification_token = secrets.token_urlsafe(32)
                
                user.otp_code = otp_code
                user.otp_expired = timezone.now() + timedelta(minutes=5)
                user.email_verification_token = verification_token
                user.email_verification_expired = timezone.now() + timedelta(minutes=5)
                user.save()
                
                # Buat EventOrganizer dengan verified=False (perlu verifikasi admin)
                event_organizer = EventOrganizer.objects.create(
                    user=user,
                    organizer_name=form.cleaned_data['organizer_name'],
                    person_in_charge=form.cleaned_data['person_in_charge'],
                    phone_number=form.cleaned_data['phone_number'],
                    email=form.cleaned_data['organizer_email'],
                    address=form.cleaned_data['address'],
                    description=form.cleaned_data['description'],
                    website=form.cleaned_data.get('website') or None,
                    social_media=form.cleaned_data.get('social_media') or None,
                    business_license=form.cleaned_data.get('business_license') or None,
                    logo=form.cleaned_data.get('logo') or None,
                    verified=False  # Default False, perlu verifikasi admin
                )
                
                # Kirim email verifikasi
                email_sent = send_verification_email(user, otp_code, verification_token)
                
                if email_sent:
                    messages.success(request, f'Registrasi Event Organizer berhasil! OTP telah dikirim ke {user.email}. Silakan cek email untuk verifikasi.')
                else:
                    messages.warning(request, f'Registrasi berhasil, tapi email gagal dikirim. OTP Anda: {otp_code}. Silakan verifikasi dengan OTP ini.')
                
                # Simpan OTP di session untuk fallback
                request.session['registration_otp'] = otp_code
                request.session['registration_email'] = user.email
                
                # Redirect ke halaman login dengan pesan sukses
                messages.info(request, 'Akun Event Organizer Anda telah diajukan untuk verifikasi. Admin akan meninjau dan memverifikasi akun Anda. Anda akan mendapat notifikasi setelah akun diverifikasi.')
                return redirect('accounts:login')
                
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan saat registrasi: {str(e)}')
                print(f"Event Organizer Registration error: {e}")
        else:
            # Form tidak valid, tampilkan error
            messages.error(request, 'Mohon perbaiki error di form sebelum submit.')
            print(f"Form errors: {form.errors}")
    else:
        form = EventOrganizerRegistrationForm()
    
    return render(request, 'accounts/register_organizer.html', {'form': form})

