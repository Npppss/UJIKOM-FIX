"""
Script untuk membuat data testing (kegiatan, registrasi, dll)
"""
import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_registration.settings')
django.setup()

from django.utils import timezone
from datetime import time as dt_time
from accounts.models import User
from events.models import Event
from registrations.models import EventRegistration
from utils.token_service import generate_registration_token

print("="*60)
print("CREATING TEST DATA")
print("="*60)

# Get users
admin = User.objects.filter(role='admin').first()
organizer = User.objects.filter(role='event_organizer').first()
user = User.objects.filter(role='user', email_verified_at__isnull=False).first()

if not admin:
    print("❌ Admin tidak ditemukan!")
    exit(1)

if not organizer:
    print("❌ Organizer tidak ditemukan!")
    exit(1)

if not user:
    print("❌ User tidak ditemukan!")
    exit(1)

print(f"\n✅ Admin: {admin.email}")
print(f"✅ Organizer: {organizer.email}")
print(f"✅ User: {user.email}")

# Create events
print("\n" + "="*60)
print("CREATING EVENTS")
print("="*60)

# Event 1: Organizer event (masih buka pendaftaran)
event1_date = timezone.now().date() + timedelta(days=7)
event1, created = Event.objects.get_or_create(
    title='Workshop Python untuk Pemula',
    defaults={
        'user': organizer,
        'description': 'Workshop Python untuk pemula yang ingin belajar programming',
        'event_date': event1_date,
        'event_time': dt_time(10, 0),
        'location': 'Gedung A, Ruang 101',
        'status': 'published'
    }
)
if created:
    print(f"✅ Created: {event1.title} - {event1.event_date}")
else:
    print(f"ℹ️  Exists: {event1.title} - {event1.event_date}")

# Event 2: Admin event (masih buka pendaftaran)
event2_date = timezone.now().date() + timedelta(days=10)
event2, created = Event.objects.get_or_create(
    title='Seminar Teknologi Terkini',
    defaults={
        'user': admin,
        'description': 'Seminar tentang teknologi terkini dalam dunia IT',
        'event_date': event2_date,
        'event_time': dt_time(14, 0),
        'location': 'Auditorium Utama',
        'status': 'published'
    }
)
if created:
    print(f"✅ Created: {event2.title} - {event2.event_date}")
else:
    print(f"ℹ️  Exists: {event2.title} - {event2.event_date}")

# Event 3: Organizer event (sudah lewat - untuk test attendance)
event3_date = timezone.now().date() - timedelta(days=1)
event3, created = Event.objects.get_or_create(
    title='Webinar Digital Marketing',
    defaults={
        'user': organizer,
        'description': 'Webinar tentang digital marketing untuk bisnis',
        'event_date': event3_date,
        'event_time': dt_time(9, 0),
        'location': 'Online via Zoom',
        'status': 'published'
    }
)
if created:
    print(f"✅ Created: {event3.title} - {event3.event_date} (Past event)")
else:
    print(f"ℹ️  Exists: {event3.title} - {event3.event_date}")

# Register user to events
print("\n" + "="*60)
print("REGISTERING USER TO EVENTS")
print("="*60)

# Register to event1
reg1, created = EventRegistration.objects.get_or_create(
    event=event1,
    user=user,
    defaults={
        'token': generate_registration_token(),
        'token_sent_at': timezone.now(),
        'status': 'registered'
    }
)
if created:
    print(f"✅ User registered to: {event1.title} - Token: {reg1.token}")
else:
    print(f"ℹ️  User already registered to: {event1.title}")

# Register to event3 (past event - untuk test attendance)
reg3, created = EventRegistration.objects.get_or_create(
    event=event3,
    user=user,
    defaults={
        'token': generate_registration_token(),
        'token_sent_at': timezone.now(),
        'status': 'registered'
    }
)
if created:
    print(f"✅ User registered to: {event3.title} - Token: {reg3.token}")
else:
    print(f"ℹ️  User already registered to: {event3.title}")

print("\n" + "="*60)
print("TEST DATA CREATED SUCCESSFULLY!")
print("="*60)
print("\n📋 Summary:")
print(f"  - Events: {Event.objects.count()}")
print(f"  - Registrations: {EventRegistration.objects.count()}")
print(f"\n🎯 Next Steps:")
print("  1. Login sebagai admin/organizer")
print("  2. Test dashboard dengan grafik")
print("  3. Test create/edit event")
print("  4. Test export data")
print("  5. Test user daftar kegiatan")
print("  6. Test attendance dengan token")

