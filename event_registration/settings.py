"""
Django settings for event_registration project.
Uses environment-based configuration.
"""
from decouple import config

# Determine environment from environment variable or default to development
ENVIRONMENT = config('ENVIRONMENT', default='development').lower()

# Import environment-specific settings
if ENVIRONMENT == 'production':
    from .settings.production import *
elif ENVIRONMENT == 'staging':
    from .settings.staging import *
else:
    from .settings.development import *

