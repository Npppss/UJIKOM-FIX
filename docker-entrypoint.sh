#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if environment variable is set
if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "Checking/Creating superuser..."
    python manage.py shell << EOF
from accounts.models import User
from django.utils import timezone

email = "${DJANGO_SUPERUSER_EMAIL:-admin@admin.com}"
password = "${DJANGO_SUPERUSER_PASSWORD:-Admin123!}"

if not User.objects.filter(email=email).exists():
    user = User.objects.create_user(
        email=email,
        password=password,
        name='Admin Docker',
        phone='081234567890',
        address='Docker Container',
        education='S1',
        role='admin'
    )
    user.email_verified_at = timezone.now()
    user.save()
    print(f"Superuser created: {email}")
else:
    print(f"Superuser already exists: {email}")
EOF
fi

# Start server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000

