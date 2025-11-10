"""
Test script untuk cek proses registrasi
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_registration.settings')
django.setup()

from accounts.models import User
from accounts.forms import UserRegistrationForm

# Test form validation
print("="*60)
print("TEST REGISTRATION FORM")
print("="*60)

# Test 1: Valid password
print("\n1. Test Valid Password:")
form_data = {
    'name': 'Test User',
    'email': 'test@example.com',
    'phone': '081234567890',
    'address': 'Test Address',
    'education': 'S1',
    'password': 'Password123#',
    'password_confirm': 'Password123#'
}
form = UserRegistrationForm(data=form_data)
print(f"   Valid: {form.is_valid()}")
if not form.is_valid():
    print(f"   Errors: {form.errors}")

# Test 2: Invalid password (kurang karakter spesial)
print("\n2. Test Invalid Password (no special char):")
form_data['password'] = 'Password123'
form_data['password_confirm'] = 'Password123'
form = UserRegistrationForm(data=form_data)
print(f"   Valid: {form.is_valid()}")
if not form.is_valid():
    print(f"   Errors: {form.errors}")

# Test 3: Password tidak cocok
print("\n3. Test Password Mismatch:")
form_data['password'] = 'Password123#'
form_data['password_confirm'] = 'Password123!'
form = UserRegistrationForm(data=form_data)
print(f"   Valid: {form.is_valid()}")
if not form.is_valid():
    print(f"   Errors: {form.errors}")

# Test 4: Cek user yang belum verified
print("\n4. Check Unverified Users:")
unverified = User.objects.filter(email_verified_at__isnull=True, role='user')
print(f"   Total unverified: {unverified.count()}")
for u in unverified[:3]:
    print(f"   - {u.email}: OTP={u.otp_code}, Expired={u.otp_expired}")

print("\n" + "="*60)

