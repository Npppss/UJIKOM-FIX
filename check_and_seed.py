"""
Script untuk cek EventOrganizer dan jalankan seed_events
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_registration.settings')
django.setup()

from accounts.models import User, EventOrganizer
from django.utils import timezone

# Cek EventOrganizer
organizers = EventOrganizer.objects.all()
if not organizers.exists():
    print("⚠️  Tidak ada EventOrganizer. Membuat EventOrganizer...")
    
    # Cek apakah ada user dengan role event_organizer
    organizer_user = User.objects.filter(role='event_organizer').first()
    
    if not organizer_user:
        # Buat user event_organizer
        organizer_user = User.objects.create_user(
            email='organizer@test.com',
            password='Organizer123#',
            name='Test Organizer',
            phone='081234567890',
            address='Test Address',
            education='S1',
            role='event_organizer',
            email_verified_at=timezone.now()
        )
        print(f"✅ Created user: {organizer_user.email}")
    
    # Buat EventOrganizer
    organizer, created = EventOrganizer.objects.get_or_create(
        user=organizer_user,
        defaults={
            'organizer_name': 'Test Event Organizer',
            'person_in_charge': organizer_user.name,
            'phone_number': organizer_user.phone,
            'email': organizer_user.email,
            'address': organizer_user.address,
            'description': 'Test Event Organizer untuk dummy data',
            'verified': True
        }
    )
    
    if created:
        print(f"✅ Created EventOrganizer: {organizer.organizer_name}")
    else:
        print(f"ℹ️  EventOrganizer sudah ada: {organizer.organizer_name}")
else:
    print(f"✅ Found {organizers.count()} EventOrganizer(s)")
    for org in organizers:
        print(f"   - {org.organizer_name} ({org.user.email})")

print("\n✅ EventOrganizer siap. Silakan jalankan: python manage.py seed_events")

