from django.contrib import admin
from .models import User, UserSession


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'role', 'is_verified', 'created_at']
    list_filter = ['role', 'email_verified_at', 'is_active']
    search_fields = ['email', 'name', 'phone']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'address', 'education')}),
        ('Role', {'fields': ('role',)}),
        ('Email Verification', {'fields': ('email_verified_at', 'otp_code', 'otp_expired')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ['email']
        return []


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'last_activity', 'expired_at', 'is_expired']
    list_filter = ['expired_at']
    search_fields = ['user__email', 'session_key']
    
    def is_expired(self, obj):
        from django.utils import timezone
        return timezone.now() > obj.expired_at
    is_expired.boolean = True

