from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('user/', views.user_dashboard, name='user'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('organizer/', views.organizer_dashboard, name='organizer'),
    path('admin/export/', views.admin_export, name='admin_export'),
    path('organizer/export/', views.organizer_export, name='organizer_export'),
]

