"""
Script untuk testing semua API endpoints
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_registration.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from events.models import Event
from registrations.models import EventRegistration

User = get_user_model()


def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_response(response, expected_status=200, description=""):
    """Helper untuk test response"""
    status_color = '\033[92m' if response.status_code == expected_status else '\033[91m'
    reset_color = '\033[0m'
    
    if response.status_code == expected_status:
        print(f"{status_color}✓{reset_color} {description}: {response.status_code} OK")
        return True
    else:
        print(f"{status_color}✗{reset_color} {description}: {response.status_code} (Expected: {expected_status})")
        if hasattr(response, 'content'):
            print(f"  Error: {response.content.decode()[:200]}")
        return False


def main():
    client = Client(HTTP_HOST='localhost')
    
    print_section("TESTING ALL API ENDPOINTS")
    
    # 1. Setup test data
    print_section("1. SETUP TEST DATA")
    
    # Create test users
    try:
        admin_user = User.objects.create_user(
            email='admin@test.com',
            password='Admin123#',
            name='Admin User',
            phone='081234567890',
            address='Admin Address',
            education='S1',
            role='admin',
            email_verified_at=timezone.now()
        )
        print("✓ Admin user created")
    except:
        admin_user = User.objects.get(email='admin@test.com')
        print("✓ Admin user exists")
    
    try:
        organizer_user = User.objects.create_user(
            email='organizer@test.com',
            password='Organizer123#',
            name='Organizer User',
            phone='081234567891',
            address='Organizer Address',
            education='S1',
            role='event_organizer',
            email_verified_at=timezone.now()
        )
        print("✓ Organizer user created")
    except:
        organizer_user = User.objects.get(email='organizer@test.com')
        print("✓ Organizer user exists")
    
    try:
        test_user = User.objects.create_user(
            email='user@test.com',
            password='User123#',
            name='Test User',
            phone='081234567892',
            address='User Address',
            education='S1',
            role='user',
            email_verified_at=timezone.now()
        )
        print("✓ User created")
    except:
        test_user = User.objects.get(email='user@test.com')
        print("✓ User exists")
    
    # Create test event
    from datetime import time as dt_time
    try:
        test_event = Event.objects.create(
            user=organizer_user,
            title='Test Event',
            description='Test Event Description',
            event_date=(timezone.now().date() + timedelta(days=5)),
            event_time=dt_time(10, 0),
            location='Test Location',
            status='published'
        )
        print("✓ Test event created")
    except:
        test_event = Event.objects.filter(title='Test Event').first()
        if not test_event:
            test_event = Event.objects.create(
                user=organizer_user,
                title='Test Event',
                description='Test Event Description',
                event_date=(timezone.now().date() + timedelta(days=5)),
                event_time=dt_time(10, 0),
                location='Test Location',
                status='published'
            )
        print("✓ Test event exists")
    
    # 2. Test Public Endpoints
    print_section("2. TEST PUBLIC ENDPOINTS")
    
    # Catalog
    response = client.get('/')
    test_response(response, 200, "GET / - Catalog")
    
    # Event Detail
    response = client.get(f'/events/detail/{test_event.id}/')
    test_response(response, 200, f"GET /events/detail/{test_event.id}/ - Event Detail")
    
    # 3. Test Authentication Endpoints
    print_section("3. TEST AUTHENTICATION ENDPOINTS")
    
    # Register
    response = client.get('/accounts/register/')
    test_response(response, 200, "GET /accounts/register/ - Register Page")
    
    # Login Page
    response = client.get('/accounts/login/')
    test_response(response, 200, "GET /accounts/login/ - Login Page")
    
    # Login (Admin)
    response = client.post('/accounts/login/', {
        'email': 'admin@test.com',
        'password': 'Admin123#'
    })
    test_response(response, 302, "POST /accounts/login/ - Admin Login")
    
    # Login (Organizer)
    client.logout()
    response = client.post('/accounts/login/', {
        'email': 'organizer@test.com',
        'password': 'Organizer123#'
    })
    test_response(response, 302, "POST /accounts/login/ - Organizer Login")
    
    # Login (User)
    client.logout()
    response = client.post('/accounts/login/', {
        'email': 'user@test.com',
        'password': 'User123#'
    })
    test_response(response, 302, "POST /accounts/login/ - User Login")
    
    # 4. Test User Endpoints
    print_section("4. TEST USER ENDPOINTS")
    
    client.login(username='user@test.com', password='User123#')
    
    # User Dashboard
    response = client.get('/dashboard/user/')
    test_response(response, 200, "GET /dashboard/user/ - User Dashboard")
    
    # Register Event
    response = client.post(f'/registrations/register/{test_event.id}/')
    test_response(response, 302, f"POST /registrations/register/{test_event.id}/ - Register Event")
    
    # History
    response = client.get('/registrations/history/')
    test_response(response, 200, "GET /registrations/history/ - History")
    
    # Certificates
    response = client.get('/certificates/')
    test_response(response, 200, "GET /certificates/ - Certificates")
    
    client.logout()
    
    # 5. Test Admin Endpoints
    print_section("5. TEST ADMIN ENDPOINTS")
    
    client.login(username='admin@test.com', password='Admin123#')
    
    # Admin Dashboard
    response = client.get('/dashboard/admin/')
    test_response(response, 200, "GET /dashboard/admin/ - Admin Dashboard")
    
    # Event List
    response = client.get('/events/list/')
    test_response(response, 200, "GET /events/list/ - Event List")
    
    # Create Event Page
    response = client.get('/events/create/')
    test_response(response, 200, "GET /events/create/ - Create Event Page")
    
    # Create Event (POST)
    response = client.post('/events/create/', {
        'title': 'Admin Event',
        'description': 'Admin Event Description',
        'event_date': (timezone.now().date() + timedelta(days=5)).strftime('%Y-%m-%d'),
        'event_time': '14:00',
        'location': 'Admin Location',
    })
    test_response(response, 302, "POST /events/create/ - Create Event")
    
    # Edit Event Page
    admin_event = Event.objects.filter(title='Admin Event').first()
    if admin_event:
        response = client.get(f'/events/edit/{admin_event.id}/')
        test_response(response, 200, f"GET /events/edit/{admin_event.id}/ - Edit Event Page")
    
    # Participants
    response = client.get(f'/events/participants/{test_event.id}/')
    test_response(response, 200, f"GET /events/participants/{test_event.id}/ - Participants")
    
    # Export
    response = client.get('/dashboard/admin/export/?format=excel')
    test_response(response, 200, "GET /dashboard/admin/export/ - Export Excel")
    
    response = client.get('/dashboard/admin/export/?format=csv')
    test_response(response, 200, "GET /dashboard/admin/export/ - Export CSV")
    
    client.logout()
    
    # 6. Test Organizer Endpoints
    print_section("6. TEST ORGANIZER ENDPOINTS")
    
    client.login(username='organizer@test.com', password='Organizer123#')
    
    # Organizer Dashboard
    response = client.get('/dashboard/organizer/')
    test_response(response, 200, "GET /dashboard/organizer/ - Organizer Dashboard")
    
    # Event List (Own Events)
    response = client.get('/events/list/')
    test_response(response, 200, "GET /events/list/ - Event List (Organizer)")
    
    # Create Event
    response = client.get('/events/create/')
    test_response(response, 200, "GET /events/create/ - Create Event Page")
    
    # Edit Own Event
    response = client.get(f'/events/edit/{test_event.id}/')
    test_response(response, 200, f"GET /events/edit/{test_event.id}/ - Edit Own Event")
    
    # Participants
    response = client.get(f'/events/participants/{test_event.id}/')
    test_response(response, 200, f"GET /events/participants/{test_event.id}/ - Participants")
    
    # Export
    response = client.get('/dashboard/organizer/export/?format=excel')
    test_response(response, 200, "GET /dashboard/organizer/export/ - Export Excel")
    
    client.logout()
    
    # 7. Test Email Verification
    print_section("7. TEST EMAIL VERIFICATION")
    
    # Email Verify Page
    response = client.get('/accounts/email/verify/')
    test_response(response, 200, "GET /accounts/email/verify/ - Email Verify Page")
    
    # Resend OTP Page
    response = client.get('/accounts/email/resend/')
    test_response(response, 200, "GET /accounts/email/resend/ - Resend OTP Page")
    
    # Password Reset Page
    response = client.get('/accounts/password/reset/')
    test_response(response, 200, "GET /accounts/password/reset/ - Password Reset Page")
    
    print_section("TESTING COMPLETED")
    print("\n✓ All endpoints have been tested!")
    print("\nNote: Some endpoints may return 302 (redirect) or 200 (OK)")
    print("Check the status codes above to verify each endpoint.\n")


if __name__ == '__main__':
    main()

