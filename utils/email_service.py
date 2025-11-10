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
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_registration_token(user, event, token):
    """Kirim token untuk daftar hadir"""
    subject = f'Token Pendaftaran Kegiatan - {event.title}'
    
    # Format lokasi berdasarkan tipe
    if event.location_type == 'online':
        location_info = f"Online (Zoom Meeting)"
    elif event.location_type == 'hybrid':
        location_info = f"Hybrid: {event.location} + Zoom Meeting"
    else:
        location_info = event.location
    
    # Informasi Zoom Meeting
    zoom_info = ""
    if event.zoom_link:
        zoom_info = f"""
    
    📹 INFORMASI ZOOM MEETING:
    Link Zoom: {event.zoom_link}"""
        if event.zoom_meeting_id:
            zoom_info += f"\n    Meeting ID: {event.zoom_meeting_id}"
        if event.zoom_passcode:
            zoom_info += f"\n    Passcode: {event.zoom_passcode}"
    
    message = f"""
    Halo {user.name},
    
    Anda telah berhasil mendaftar pada kegiatan:
    {event.title}
    
    📅 Tanggal: {event.event_date.strftime('%d %B %Y')}
    ⏰ Waktu: {event.event_time.strftime('%H:%M')} WIB
    📍 Lokasi: {location_info}{zoom_info}
    
    🔑 Token Daftar Hadir Anda: {token}
    
    Simpan token ini dengan baik! Token akan digunakan saat mengisi daftar hadir pada hari H kegiatan.
    
    Daftar hadir dapat diisi setelah jam kegiatan dimulai.
    
    Salam,
    Tim Sistem Pendaftaran Kegiatan
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


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
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

