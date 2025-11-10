from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'event_date', 'event_time', 'status', 'created_at']
    list_filter = ['status', 'event_date', 'created_at']
    search_fields = ['title', 'description', 'location']

