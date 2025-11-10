from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_update, name='profile'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('email/verify/', views.verify_email, name='email_verify'),
    path('email/verify/<str:token>/', views.verify_email_link, name='email_verify_link'),
    path('email/resend/', views.resend_verification, name='resend_otp'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('password/reset/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]

