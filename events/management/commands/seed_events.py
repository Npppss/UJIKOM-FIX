"""
Django management command untuk generate 100 dummy data Event
Usage: python manage.py seed_events
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, time as dt_time
import random
from decimal import Decimal

from events.models import Event
from accounts.models import User, EventOrganizer
from faker import Faker

fake = Faker('id_ID')  # Indonesian locale


class Command(BaseCommand):
    help = 'Generate 100 dummy data Event (50 Seminar, 50 Konser)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua event yang ada sebelum generate data baru',
        )

    def handle(self, *args, **options):
        # Cek apakah ada EventOrganizer, jika tidak ada, buat otomatis
        organizers = EventOrganizer.objects.all()
        if not organizers.exists():
            self.stdout.write(
                self.style.WARNING('⚠️  Tidak ada EventOrganizer. Membuat EventOrganizer otomatis...')
            )
            
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
                self.stdout.write(self.style.SUCCESS(f'✅ Created user: {organizer_user.email}'))
            
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
                self.stdout.write(self.style.SUCCESS(f'✅ Created EventOrganizer: {organizer.organizer_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'ℹ️  EventOrganizer sudah ada: {organizer.organizer_name}'))
            
            # Refresh organizers
            organizers = EventOrganizer.objects.all()

        # Clear existing events jika diminta
        if options['clear']:
            Event.objects.all().delete()
            self.stdout.write(self.style.WARNING('🗑️  Semua event yang ada telah dihapus.'))

        # Lokasi acak
        locations = ["Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Bali"]
        
        # Bank untuk event berbayar
        banks = ["BCA", "Mandiri", "BRI", "BNI", "CIMB"]
        bank_accounts = ["1234567890", "9876543210", "1122334455", "5544332211", "9988776655"]

        # Generate 50 Seminar
        self.stdout.write(self.style.SUCCESS('📚 Generating 50 Seminar events...'))
        self._generate_events(
            category='seminar',
            count=50,
            organizers=organizers,
            locations=locations,
            banks=banks,
            bank_accounts=bank_accounts,
            price_min=50000,
            price_max=200000
        )

        # Generate 50 Konser
        self.stdout.write(self.style.SUCCESS('🎵 Generating 50 Konser events...'))
        self._generate_events(
            category='concert',
            count=50,
            organizers=organizers,
            locations=locations,
            banks=banks,
            bank_accounts=bank_accounts,
            price_min=100000,
            price_max=500000
        )

        total_events = Event.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Berhasil generate {total_events} dummy data Event!\n'
                f'   - Seminar: {Event.objects.filter(category="seminar").count()}\n'
                f'   - Konser: {Event.objects.filter(category="concert").count()}\n'
                f'   - Status Published: {Event.objects.filter(status="published").count()}\n'
                f'   - Status Completed: {Event.objects.filter(status="completed").count()}\n'
                f'   - Event Berbayar: {Event.objects.exclude(price__isnull=True).count()}\n'
                f'   - Event Gratis: {Event.objects.filter(price__isnull=True).count()}'
            )
        )

    def _generate_events(self, category, count, organizers, locations, banks, bank_accounts, price_min, price_max):
        """Generate events untuk kategori tertentu"""
        # Distribusi status: 20 Upcoming, 15 Ongoing, 15 Selesai
        # Buat list status sesuai distribusi
        status_list = (
            ['published'] * 20 +  # Upcoming (event_date di masa depan)
            ['published_ongoing'] * 15 +  # Ongoing (event_date dekat/sekitar sekarang)
            ['completed'] * 15  # Selesai
        )

        # Randomize list
        random.shuffle(status_list)
        
        # Distribusi berbayar: 40% berbayar, 60% gratis
        paid_list = [True] * 20 + [False] * 30  # 20 berbayar, 30 gratis dari 50
        random.shuffle(paid_list)

        events_created = 0
        for i in range(count):
            # Pilih organizer random
            organizer = random.choice(organizers)
            user = organizer.user

            # Tentukan status dan tanggal
            status = status_list[i]
            
            if status == 'published':
                # Upcoming: event_date 7-90 hari dari sekarang
                event_date = timezone.now().date() + timedelta(days=random.randint(7, 90))
                event_time = dt_time(random.randint(8, 18), random.choice([0, 30]))
                event_status = 'published'
            elif status == 'published_ongoing':
                # Ongoing: event_date -3 sampai +3 hari dari sekarang
                event_date = timezone.now().date() + timedelta(days=random.randint(-3, 3))
                event_time = dt_time(random.randint(8, 18), random.choice([0, 30]))
                event_status = 'published'
            else:  # completed
                # Selesai: event_date 1-30 hari yang lalu
                event_date = timezone.now().date() - timedelta(days=random.randint(1, 30))
                event_time = dt_time(random.randint(8, 18), random.choice([0, 30]))
                event_status = 'completed'

            # Tentukan apakah berbayar (40% berbayar, 60% gratis)
            is_paid = paid_list[i]
            
            # Generate title berdasarkan kategori
            if category == 'seminar':
                title = fake.sentence(nb_words=4).replace('.', '').title()
                # Pastikan judul tidak terlalu panjang
                if len(title) > 100:
                    title = title[:100]
            else:  # concert
                title = fake.sentence(nb_words=3).replace('.', '').title()
                if len(title) > 100:
                    title = title[:100]

            # Generate description (3-4 kalimat)
            description = ' '.join([fake.sentence() for _ in range(random.randint(3, 4))])

            # Tentukan lokasi
            location = random.choice(locations)
            location_type = random.choice(['offline', 'online', 'hybrid'])

            # Buat event
            event = Event.objects.create(
                user=user,
                title=title,
                category=category,
                description=description,
                event_date=event_date,
                event_time=event_time,
                location=location,
                location_type=location_type,
                status=event_status,
                price=Decimal(random.randint(price_min, price_max)).quantize(Decimal('0.01')) if is_paid else None,
                bank_name=random.choice(banks) if is_paid else None,
                bank_account=random.choice(bank_accounts) if is_paid else None,
            )

            events_created += 1

        return events_created

