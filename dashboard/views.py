from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from django.utils import timezone
import json
from accounts.decorators import role_required
from events.models import Event, ReportEvent
from registrations.models import EventRegistration
from utils.export_service import export_participants_to_excel, export_participants_to_csv


@login_required
@role_required('user')
def user_dashboard(request):
    """Dashboard untuk user/peserta"""
    # Statistik user
    total_registered = EventRegistration.objects.filter(user=request.user).count()
    total_attended = EventRegistration.objects.filter(
        user=request.user,
        status='attended'
    ).count()
    total_certificates = request.user.certificates.count()
    
    # Kegiatan terdekat
    upcoming_registrations = EventRegistration.objects.filter(
        user=request.user,
        status='registered',
        event__event_date__gte=timezone.now().date()
    ).select_related('event').order_by('event__event_date')[:5]
    
    return render(request, 'dashboard/user_dashboard.html', {
        'total_registered': total_registered,
        'total_attended': total_attended,
        'total_certificates': total_certificates,
        'upcoming_registrations': upcoming_registrations,
    })


@login_required
@role_required('admin')
def admin_dashboard(request):
    """Dashboard untuk admin"""
    current_year = timezone.now().year
    
    # Statistik: Jumlah kegiatan per bulan
    monthly_events = Event.objects.filter(
        created_at__year=current_year
    ).annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Statistik: Jumlah peserta per bulan
    monthly_participants = EventRegistration.objects.filter(
        status='attended',
        attendance_at__year=current_year
    ).annotate(
        month=ExtractMonth('attendance_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Top 10 kegiatan dengan peserta terbanyak
    top_events = Event.objects.annotate(
        participant_count=Count('registrations', filter=Q(registrations__status='attended'))
    ).order_by('-participant_count')[:10]
    
    # Data untuk chart (format JSON)
    events_chart_data = {
        'labels': [f'Bulan {item["month"]}' for item in monthly_events],
        'data': [item['count'] for item in monthly_events]
    }
    
    participants_chart_data = {
        'labels': [f'Bulan {item["month"]}' for item in monthly_participants],
        'data': [item['count'] for item in monthly_participants]
    }
    
    top_events_chart_data = {
        'labels': [event.title[:30] + '...' if len(event.title) > 30 else event.title for event in top_events],
        'data': [event.participant_count for event in top_events]
    }
    
    # Count pending reports
    pending_reports_count = ReportEvent.objects.filter(status='pending').count()
    
    return render(request, 'dashboard/admin_dashboard.html', {
        'events_chart_data': json.dumps(events_chart_data),
        'participants_chart_data': json.dumps(participants_chart_data),
        'top_events_chart_data': json.dumps(top_events_chart_data),
        'top_events': top_events,
        'pending_reports_count': pending_reports_count,
    })


@login_required
@role_required('event_organizer')
def organizer_dashboard(request):
    """Dashboard untuk event organizer"""
    current_year = timezone.now().year
    user_id = request.user.id
    
    # Statistik: Jumlah kegiatan per bulan (HANYA KEGIATAN SENDIRI)
    monthly_events = Event.objects.filter(
        user_id=user_id,
        created_at__year=current_year
    ).annotate(
        month=ExtractMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Statistik: Jumlah peserta per bulan (HANYA KEGIATAN SENDIRI)
    monthly_participants = EventRegistration.objects.filter(
        event__user_id=user_id,
        status='attended',
        attendance_at__year=current_year
    ).annotate(
        month=ExtractMonth('attendance_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Top 10 kegiatan dengan peserta terbanyak (HANYA KEGIATAN SENDIRI)
    top_events = Event.objects.filter(
        user_id=user_id
    ).annotate(
        participant_count=Count('registrations', filter=Q(registrations__status='attended'))
    ).order_by('-participant_count')[:10]
    
    # Data untuk chart (format JSON)
    events_chart_data = {
        'labels': [f'Bulan {item["month"]}' for item in monthly_events],
        'data': [item['count'] for item in monthly_events]
    }
    
    participants_chart_data = {
        'labels': [f'Bulan {item["month"]}' for item in monthly_participants],
        'data': [item['count'] for item in monthly_participants]
    }
    
    top_events_chart_data = {
        'labels': [event.title[:30] + '...' if len(event.title) > 30 else event.title for event in top_events],
        'data': [event.participant_count for event in top_events]
    }
    
    return render(request, 'dashboard/organizer_dashboard.html', {
        'events_chart_data': json.dumps(events_chart_data),
        'participants_chart_data': json.dumps(participants_chart_data),
        'top_events_chart_data': json.dumps(top_events_chart_data),
        'top_events': top_events,
    })


@login_required
@role_required('admin')
def admin_export(request):
    """Export data peserta untuk admin (semua peserta)"""
    format_type = request.GET.get('format', 'excel')
    
    if format_type == 'csv':
        return export_participants_to_csv(role='admin')
    else:
        return export_participants_to_excel(role='admin')


@login_required
@role_required('event_organizer')
def organizer_export(request):
    """Export data peserta untuk event organizer (hanya peserta kegiatan sendiri)"""
    format_type = request.GET.get('format', 'excel')
    
    if format_type == 'csv':
        return export_participants_to_csv(user_id=request.user.id, role='event_organizer')
    else:
        return export_participants_to_excel(user_id=request.user.id, role='event_organizer')

