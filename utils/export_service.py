import pandas as pd
from django.http import HttpResponse
from registrations.models import EventRegistration


def export_participants_to_excel(event_ids=None, user_id=None, role=None):
    """
    Export data peserta ke Excel
    """
    # Query registrations
    registrations = EventRegistration.objects.select_related('event', 'user').all()
    
    # Filter berdasarkan event_ids
    if event_ids:
        registrations = registrations.filter(event_id__in=event_ids)
    
    # Filter untuk Event Organizer (hanya event sendiri)
    if role == 'event_organizer' and user_id:
        registrations = registrations.filter(event__user_id=user_id)
    
    # Prepare data
    data = []
    for reg in registrations:
        data.append({
            'Nama Kegiatan': reg.event.title,
            'Tanggal Kegiatan': reg.event.event_date.strftime('%d %B %Y'),
            'Waktu Kegiatan': reg.event.event_time.strftime('%H:%M'),
            'Lokasi': reg.event.location,
            'Nama Peserta': reg.user.name,
            'Email': reg.user.email,
            'No HP': reg.user.phone,
            'Alamat': reg.user.address,
            'Pendidikan': reg.user.education,
            'Status': reg.get_status_display(),
            'Tanggal Daftar': reg.created_at.strftime('%d %B %Y %H:%M'),
            'Tanggal Hadir': reg.attendance_at.strftime('%d %B %Y %H:%M') if reg.attendance_at else '-',
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = 'peserta_kegiatan.xlsx'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Write to Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Peserta', index=False)
    
    return response


def export_participants_to_csv(event_ids=None, user_id=None, role=None):
    """
    Export data peserta ke CSV
    """
    # Query registrations (sama seperti Excel)
    registrations = EventRegistration.objects.select_related('event', 'user').all()
    
    if event_ids:
        registrations = registrations.filter(event_id__in=event_ids)
    
    if role == 'event_organizer' and user_id:
        registrations = registrations.filter(event__user_id=user_id)
    
    # Prepare data
    data = []
    for reg in registrations:
        data.append({
            'Nama Kegiatan': reg.event.title,
            'Tanggal Kegiatan': reg.event.event_date.strftime('%d %B %Y'),
            'Waktu Kegiatan': reg.event.event_time.strftime('%H:%M'),
            'Lokasi': reg.event.location,
            'Nama Peserta': reg.user.name,
            'Email': reg.user.email,
            'No HP': reg.user.phone,
            'Alamat': reg.user.address,
            'Pendidikan': reg.user.education,
            'Status': reg.get_status_display(),
            'Tanggal Daftar': reg.created_at.strftime('%d %B %Y %H:%M'),
            'Tanggal Hadir': reg.attendance_at.strftime('%d %B %Y %H:%M') if reg.attendance_at else '-',
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    filename = 'peserta_kegiatan.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Write to CSV
    df.to_csv(response, index=False, encoding='utf-8-sig')
    
    return response

