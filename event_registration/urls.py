"""
URL configuration for event_registration project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('events.urls', 'events'), namespace='public')),  # Root untuk katalog
    path('events/', include('events.urls')),  # /events/ untuk event management
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('registrations/', include('registrations.urls')),
    path('certificates/', include('certificates.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

