from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path('upload-payment/<int:event_id>/', views.upload_payment, name='upload_payment'),
    path('attendance/<int:event_id>/', views.attendance, name='attendance'),
    path('history/', views.history, name='history'),
]

