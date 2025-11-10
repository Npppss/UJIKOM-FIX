from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.certificate_list, name='list'),
    path('download/<int:certificate_id>/', views.download_certificate, name='download'),
]

