from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*allowed_roles):
    """Decorator untuk cek role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Silakan login terlebih dahulu.')
                return redirect('accounts:login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'Anda tidak memiliki akses untuk halaman ini.')
                
                if request.user.role == 'admin':
                    return redirect('dashboard:admin')
                elif request.user.role == 'event_organizer':
                    return redirect('dashboard:organizer')
                else:
                    return redirect('dashboard:user')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def email_verification_required(view_func):
    """Decorator untuk cek email verification (hanya untuk user)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'user':
            if not request.user.is_verified():
                messages.warning(request, 'Silakan verifikasi email terlebih dahulu.')
                return redirect('accounts:email_verify')
        return view_func(request, *args, **kwargs)
    return wrapper

