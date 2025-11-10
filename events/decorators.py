from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Event


def event_owner_required(view_func):
    """Decorator untuk cek apakah user adalah owner event (untuk Event Organizer)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        event_id = kwargs.get('event_id') or kwargs.get('id')
        event = get_object_or_404(Event, id=event_id)
        
        # Admin bisa akses semua
        if request.user.is_admin():
            return view_func(request, *args, **kwargs)
        
        # Event Organizer hanya bisa akses event sendiri
        if request.user.is_event_organizer():
            if event.user_id != request.user.id:
                messages.error(request, 'Anda tidak memiliki akses untuk mengelola kegiatan ini.')
                return redirect('dashboard:organizer')
        
        return view_func(request, *args, **kwargs)
    return wrapper

