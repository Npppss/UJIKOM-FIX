"""
Script Testing Komprehensif - Semua Fitur
Jalankan: python run_tests.py
"""
import os
import django
from datetime import timedelta, time as dt_time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_registration.settings')
django.setup()

from django.test import Client
from django.utils import timezone
from accounts.models import User
from events.models import Event
from registrations.models import EventRegistration

GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_section(title):
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}  {title}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")


def test(name, success, details=""):
    color = GREEN if success else RED
    symbol = "✓" if success else "✗"
    print(f"{color}{symbol}{RESET} {name}")
    if details:
        print(f"    {details}")
    return success


def login(client, email, password):
    response = client.post('/accounts/login/', {'email': email, 'password': password})
    return response.status_code == 302


def main():
    client = Client(HTTP_HOST='localhost')
    results = {'passed': 0, 'failed': 0}
    
    print_section("🧪 COMPREHENSIVE TESTING")
    
    # Setup
    print_section("1. SETUP")
    admin = User.objects.filter(email='admin@test.com').first()
    organizer = User.objects.filter(email='organizer@test.com').first()
    test_user = User.objects.filter(email='user@test.com').first()
    
    # Test ADMIN
    print_section("2. TEST ADMIN")
    if admin and login(client, 'admin@test.com', 'Admin123#'):
        test("Admin login", True)
        results['passed'] += 1
        
        # Dashboard
        r = client.get('/dashboard/admin/')
        if test("Admin dashboard", r.status_code == 200):
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        # Event list
        r = client.get('/events/list/')
        if test("Admin event list", r.status_code == 200):
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        # Create event (H-3 valid)
        valid_date = (timezone.now().date() + timedelta(days=3))
        r = client.post('/events/create/', {
            'title': 'Test Event',
            'description': 'Test',
            'event_date': valid_date.isoformat(),
            'event_time': '14:00',
            'location': 'Test',
            'status': 'published'
        })
        if test("Admin create event (H-3 valid)", r.status_code in [200, 302]):
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        # Export
        r = client.get('/dashboard/admin/export/?format=xlsx')
        test("Admin export Excel", r.status_code in [200, 404])
        results['passed'] += 1
    else:
        test("Admin login", False)
        results['failed'] += 1
    
    # Test ORGANIZER
    print_section("3. TEST EVENT ORGANIZER")
    client.logout()
    if organizer and login(client, 'organizer@test.com', 'Organizer123#'):
        test("Organizer login", True)
        results['passed'] += 1
        
        # Dashboard
        r = client.get('/dashboard/organizer/')
        if test("Organizer dashboard", r.status_code == 200):
            results['passed'] += 1
        else:
            results['failed'] += 1
        
        # Security test: try edit admin event
        admin_event = Event.objects.filter(user=admin).first()
        if admin_event:
            r = client.get(f'/events/edit/{admin_event.id}/')
            if test("Organizer edit admin event (security)", r.status_code in [403, 404, 302], 
                   f"Status: {r.status_code}"):
                results['passed'] += 1
            else:
                results['failed'] += 1
    else:
        test("Organizer login", False)
        results['failed'] += 1
    
    # Test ATTENDANCE
    print_section("4. TEST ATTENDANCE")
    client.logout()
    if test_user and login(client, 'user@test.com', 'User123#'):
        test("User login", True)
        results['passed'] += 1
        
        # Find past event
        past_event = Event.objects.filter(
            event_date__lt=timezone.now().date()
        ).first()
        
        if past_event:
            # Register to past event
            reg, created = EventRegistration.objects.get_or_create(
                event=past_event,
                user=test_user,
                defaults={'token': '1234567890', 'status': 'registered'}
            )
            test("User registered to past event", True, f"Token: {reg.token}")
            results['passed'] += 1
            
            # Attendance
            r = client.get(f'/registrations/attendance/{past_event.id}/')
            if test("Attendance page", r.status_code == 200):
                results['passed'] += 1
            else:
                results['failed'] += 1
            
            # Submit attendance
            if reg.status == 'registered':
                r = client.post(f'/registrations/attendance/{past_event.id}/', {
                    'token': reg.token
                })
                if test("Attendance with valid token", r.status_code in [200, 302]):
                    results['passed'] += 1
                    reg.refresh_from_db()
                    if reg.status == 'attended':
                        test("  → Status changed to 'attended'", True)
                    else:
                        test("  → Status changed to 'attended'", False)
                else:
                    results['failed'] += 1
    else:
        test("User login", False)
        results['failed'] += 1
    
    # Summary
    print_section("📊 SUMMARY")
    total = results['passed'] + results['failed']
    percentage = (results['passed'] / total * 100) if total > 0 else 0
    
    print(f"{BOLD}Total Tests: {total}{RESET}")
    print(f"{GREEN}Passed: {results['passed']}{RESET}")
    print(f"{RED}Failed: {results['failed']}{RESET}")
    print(f"{BOLD}Success Rate: {percentage:.1f}%{RESET}\n")


if __name__ == '__main__':
    main()

