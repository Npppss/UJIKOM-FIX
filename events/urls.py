from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Public routes
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('detail/<int:event_id>/', views.detail, name='detail'),
    
    # Admin & Event Organizer routes
    path('create/', views.create_event, name='create'),
    path('list/', views.event_list, name='list'),
    path('edit/<int:event_id>/', views.edit_event, name='edit'),
    path('delete/<int:event_id>/', views.delete_event, name='delete'),
    path('participants/<int:event_id>/', views.participants, name='participants'),
    path('validate-payment/<int:registration_id>/', views.validate_payment, name='validate_payment'),
    
    # News routes (Admin & Event Organizer)
    path('news/create/', views.news_create, name='news_create'),
    path('news/<int:news_id>/edit/', views.news_edit, name='news_edit'),
    path('news/<int:news_id>/delete/', views.news_delete, name='news_delete'),
    
    # Report Event
    path('report/<int:event_id>/', views.report_event, name='report'),
    path('reports/my/', views.my_reports, name='my_reports'),
    path('reports/review/', views.review_reports, name='review_reports'),
    path('reports/<int:report_id>/approve/', views.approve_report, name='approve_report'),
    path('reports/<int:report_id>/reject/', views.reject_report, name='reject_report'),
    
    # FAQ & Chatbot
    path('faq/', views.faq, name='faq'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
]

