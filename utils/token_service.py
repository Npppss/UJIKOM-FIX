import secrets
from registrations.models import EventRegistration


def generate_registration_token():
    """Generate token 10 digit yang unik"""
    max_attempts = 100  # Prevent infinite loop
    
    for _ in range(max_attempts):
        # Generate 10 digit angka
        token = ''.join([str(secrets.randbelow(10)) for _ in range(10)])
        
        # Cek apakah token sudah ada
        if not EventRegistration.objects.filter(token=token).exists():
            return token
    
    # Fallback: gunakan timestamp + random jika masih collision
    import time
    token = str(int(time.time()))[-6:] + ''.join([str(secrets.randbelow(10)) for _ in range(4)])
    return token[:10]

