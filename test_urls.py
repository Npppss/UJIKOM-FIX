"""
Test script untuk cek URL patterns
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_registration.settings')
django.setup()

from django.urls import get_resolver
from django.conf import settings

print("="*60)
print("URL CONFIGURATION CHECK")
print("="*60)
print(f"ROOT_URLCONF: {settings.ROOT_URLCONF}")
print(f"Settings Module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print()

resolver = get_resolver()
print("URL Patterns:")
for pattern in resolver.url_patterns:
    print(f"  - {pattern.pattern}")
    if hasattr(pattern, 'url_patterns'):
        for sub_pattern in pattern.url_patterns:
            print(f"    - {sub_pattern.pattern}")

print()
print("Checking accounts URLs...")
try:
    from accounts.urls import urlpatterns as accounts_urls
    print("Accounts URLs found:")
    for url in accounts_urls:
        print(f"  - {url.pattern} -> {url.name}")
except Exception as e:
    print(f"Error: {e}")

