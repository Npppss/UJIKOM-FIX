from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import UserSession
from datetime import timedelta


class SessionTimeoutMiddleware(MiddlewareMixin):
    """Middleware untuk session timeout 5 menit"""
    
    def process_request(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            
            if session_key:
                try:
                    user_session = UserSession.objects.get(session_key=session_key)
                    
                    # Cek apakah session expired
                    if user_session.is_expired():
                        # Destroy session
                        user_session.delete()
                        request.session.flush()
                        
                        # Logout user
                        logout(request)
                        
                        messages.error(request, 'Session expired. Tidak ada aktivitas selama 5 menit.')
                        return redirect('accounts:login')
                    
                    # Update last_activity dan expired_at
                    user_session.last_activity = timezone.now()
                    user_session.expired_at = timezone.now() + timedelta(minutes=5)
                    user_session.save()
                    
                except UserSession.DoesNotExist:
                    # Buat session baru jika belum ada
                    UserSession.objects.create(
                        user=request.user,
                        session_key=session_key,
                        last_activity=timezone.now(),
                        expired_at=timezone.now() + timedelta(minutes=5),
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
        
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RoleRequiredMiddleware(MiddlewareMixin):
    """Middleware untuk cek role user"""
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'required_role'):
            required_role = view_func.required_role
            
            if not request.user.is_authenticated:
                messages.error(request, 'Silakan login terlebih dahulu.')
                return redirect('accounts:login')
            
            if request.user.role != required_role:
                messages.error(request, 'Anda tidak memiliki akses untuk halaman ini.')
                
                # Redirect berdasarkan role
                if request.user.role == 'admin':
                    return redirect('dashboard:admin')
                elif request.user.role == 'event_organizer':
                    return redirect('dashboard:organizer')
                else:
                    return redirect('dashboard:user')
        
        return None

