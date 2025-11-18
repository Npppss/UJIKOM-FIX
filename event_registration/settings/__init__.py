"""
Django settings module with environment-based configuration.
"""
import os
from decouple import config

# Determine environment from environment variable or default to development
ENVIRONMENT = config('ENVIRONMENT', default='development').lower()

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'staging':
    from .staging import *
else:
    from .development import *

