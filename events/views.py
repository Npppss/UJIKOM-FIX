from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from accounts.decorators import role_required, email_verification_required
from events.decorators import event_owner_required
from .models import Event, ReportEvent, News, NewsComment
from .forms import EventForm, ReportEventForm, NewsForm, NewsCommentForm
from accounts.models import Achievement


def index(request):
    """Homepage dengan hero section dan featured events"""
    # Get featured events (latest 6 published events)
    featured_events = Event.objects.filter(
        status='published',
        deleted_at__isnull=True,
        registration_closed_at__gt=timezone.now()
    ).order_by('-event_date', '-event_time')[:6]
    
    # Categories (can be extended to use a Category model)
    categories = [
        {'id': 'seminar', 'name': 'Seminar & Conference'},
        {'id': 'concert', 'name': 'Concert & Festival'},
    ]
    
    return render(request, 'index.html', {
        'featured_events': featured_events,
        'categories': categories,
    })


def catalog(request):
    """Katalog kegiatan publik (tidak perlu login)"""
    # Tampilkan event dengan status published atau completed
    events = Event.objects.filter(
        status__in=['published', 'completed'],
        deleted_at__isnull=True
    )
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Category Filter - menggunakan field category dari model
    category = request.GET.get('category', '')
    if category == 'seminar':
        events = events.filter(category='seminar')
    elif category == 'concert':
        events = events.filter(category='concert')
    
    # Sorting
    sort_by = request.GET.get('sort', 'nearest')
    if sort_by == 'newest':
        events = events.order_by('-event_date', '-event_time')
    elif sort_by == 'oldest':
        events = events.order_by('event_date', 'event_time')
    elif sort_by == 'most_participants':
        events = events.annotate(
            participant_count=Count('registrations')
        ).order_by('-participant_count')
    else:  # nearest (default)
        events = events.order_by('event_date', 'event_time')
    
    # Get featured event (nearest upcoming event)
    featured_event = None
    all_events = Event.objects.filter(
        status__in=['published', 'completed'],
        deleted_at__isnull=True
    ).order_by('event_date', 'event_time').first()
    
    if all_events:
        featured_event = all_events
    
    # Untuk "Semua Kategori", kita perlu semua event tanpa pagination di template
    # Tapi tetap paginate untuk performa
    paginator = Paginator(events, 12)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    
    # Untuk "Semua Kategori", kita perlu semua event (tanpa pagination) untuk ditampilkan di kedua section
    all_events_for_display = None
    if not category:
        # Ambil semua event tanpa pagination untuk ditampilkan di kedua section
        all_events_for_display = Event.objects.filter(
            status__in=['published', 'completed'],
            deleted_at__isnull=True
        )
        if search_query:
            all_events_for_display = all_events_for_display.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        # Apply sorting
        if sort_by == 'newest':
            all_events_for_display = all_events_for_display.order_by('-event_date', '-event_time')
        elif sort_by == 'oldest':
            all_events_for_display = all_events_for_display.order_by('event_date', 'event_time')
        elif sort_by == 'most_participants':
            all_events_for_display = all_events_for_display.annotate(
                participant_count=Count('registrations')
            ).order_by('-participant_count')
        else:  # nearest (default)
            all_events_for_display = all_events_for_display.order_by('event_date', 'event_time')
    
    return render(request, 'events/catalog.html', {
        'events': events,
        'all_events': all_events_for_display,  # Untuk "Semua Kategori"
        'search_query': search_query,
        'sort_by': sort_by,
        'category': category,
        'featured_event': featured_event
    })


def news_list(request):
    """Halaman Berita - Menampilkan berita yang dipublikasikan"""
    news_list = News.objects.filter(is_published=True).select_related('author', 'event').order_by('-created_at')
    
    # Filter by category
    category = request.GET.get('category', '')
    if category:
        news_list = news_list.filter(category=category)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(news_list, 9)
    page = request.GET.get('page')
    news_page = paginator.get_page(page)
    
    return render(request, 'events/news_list.html', {
        'news_list': news_page,
        'search_query': search_query,
        'category': category,
    })


def news_detail(request, news_id):
    """Detail berita dengan komentar"""
    news = get_object_or_404(News, id=news_id, is_published=True)
    comments = news.comments.select_related('user').all()
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated and request.user.role == 'user':
        comment_form = NewsCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = news
            comment.user = request.user
            comment.save()
            messages.success(request, 'Komentar Anda berhasil ditambahkan!')
            return redirect('events:news_detail', news_id=news_id)
    else:
        comment_form = NewsCommentForm()
    
    return render(request, 'events/news_detail.html', {
        'news': news,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
@role_required('admin', 'event_organizer')
def news_create(request):
    """Admin/Organizer membuat berita baru"""
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Berita berhasil dibuat!')
            return redirect('events:news_list')
    else:
        form = NewsForm()
        # Filter events berdasarkan user role
        if request.user.role == 'event_organizer':
            form.fields['event'].queryset = Event.objects.filter(user=request.user, deleted_at__isnull=True)
        else:
            form.fields['event'].queryset = Event.objects.filter(deleted_at__isnull=True)
    
    return render(request, 'events/news_create.html', {'form': form})


@login_required
@role_required('admin', 'event_organizer')
def news_edit(request, news_id):
    """Admin/Organizer edit berita"""
    news = get_object_or_404(News, id=news_id)
    
    # Check permission
    if request.user.role == 'event_organizer' and news.author != request.user:
        messages.error(request, 'Anda tidak memiliki izin untuk mengedit berita ini.')
        return redirect('events:news_list')
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Berita berhasil diperbarui!')
            return redirect('events:news_detail', news_id=news_id)
    else:
        form = NewsForm(instance=news)
        # Filter events berdasarkan user role
        if request.user.role == 'event_organizer':
            form.fields['event'].queryset = Event.objects.filter(user=request.user, deleted_at__isnull=True)
        else:
            form.fields['event'].queryset = Event.objects.filter(deleted_at__isnull=True)
    
    return render(request, 'events/news_edit.html', {'form': form, 'news': news})


@login_required
@role_required('admin', 'event_organizer')
def news_delete(request, news_id):
    """Admin/Organizer hapus berita"""
    news = get_object_or_404(News, id=news_id)
    
    # Check permission
    if request.user.role == 'event_organizer' and news.author != request.user:
        messages.error(request, 'Anda tidak memiliki izin untuk menghapus berita ini.')
        return redirect('events:news_list')
    
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Berita berhasil dihapus!')
        return redirect('events:news_list')
    
    return render(request, 'events/news_delete.html', {'news': news})


def detail(request, event_id):
    """Detail kegiatan"""
    from registrations.models import EventRegistration
    from registrations.forms import PaymentProofForm
    
    # Allow viewing published and completed events (completed untuk akses materi)
    event = get_object_or_404(Event, id=event_id, status__in=['published', 'completed'], deleted_at__isnull=True)
    
    # Cek apakah user sudah terdaftar
    is_registered = False
    has_reported = False
    registration = None
    payment_form = None
    
    if request.user.is_authenticated:
        registration = EventRegistration.objects.filter(event=event, user=request.user).first()
        is_registered = registration is not None
        has_reported = ReportEvent.objects.filter(event=event, reporter=request.user).exists()
        
        # Jika event berbayar dan belum upload bukti pembayaran, tampilkan form
        if event.price and event.price > 0 and is_registered and not registration.payment_proof:
            payment_form = PaymentProofForm()
    
    # Cek apakah user bisa akses materi seminar
    can_access_material = False
    if request.user.is_authenticated:
        can_access_material = event.can_access_material(request.user)
    
    # Cek jumlah penolakan pembayaran (untuk event berbayar)
    rejection_count = 0
    can_register_again = True
    if request.user.is_authenticated and event.price and event.price > 0:
        from registrations.models import PaymentRejection
        rejection_count = PaymentRejection.objects.filter(event=event, user=request.user).count()
        can_register_again = rejection_count < 3
    
    return render(request, 'events/detail.html', {
        'event': event,
        'is_registered': is_registered,
        'has_reported': has_reported,
        'registration': registration,
        'payment_form': payment_form,
        'can_access_material': can_access_material,
        'rejection_count': rejection_count,
        'can_register_again': can_register_again
    })


@login_required
def download_material(request, event_id):
    """Download materi seminar untuk user yang terdaftar"""
    from django.http import FileResponse, Http404
    from registrations.models import EventRegistration
    
    event = get_object_or_404(Event, id=event_id, deleted_at__isnull=True)
    
    # Cek permission menggunakan method can_access_material
    if not event.can_access_material(request.user):
        messages.error(request, 'Anda tidak memiliki akses untuk mengunduh materi ini.')
        return redirect('events:detail', event_id=event_id)
    
    # Pastikan file ada
    if not event.material_file:
        messages.error(request, 'Materi seminar belum tersedia.')
        return redirect('events:detail', event_id=event_id)
    
    try:
        # Return file response untuk download
        response = FileResponse(
            event.material_file.open('rb'),
            as_attachment=True,
            filename=event.material_file.name.split('/')[-1]
        )
        return response
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan saat mengunduh file: {str(e)}')
        return redirect('events:detail', event_id=event_id)


@login_required
@role_required('admin', 'event_organizer')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.status = 'published'
            event.save()
            
            messages.success(request, 'Kegiatan berhasil dibuat!')
            return redirect('events:list')
    else:
        form = EventForm()
    
    return render(request, 'events/create.html', {'form': form})


@login_required
@role_required('admin', 'event_organizer')
def event_list(request):
    """List semua kegiatan untuk admin/organizer"""
    if request.user.is_admin():
        events = Event.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    else:
        events = Event.objects.filter(user=request.user, deleted_at__isnull=True).order_by('-created_at')
    
    return render(request, 'events/list.html', {'events': events})


@login_required
@role_required('admin', 'event_organizer')
@event_owner_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kegiatan berhasil diupdate!')
            return redirect('events:list')
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/edit.html', {'form': form, 'event': event})


@login_required
@role_required('admin', 'event_organizer')
@event_owner_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.deleted_at = timezone.now()
    event.save()
    
    messages.success(request, 'Kegiatan berhasil dihapus!')
    return redirect('events:list')


@login_required
@role_required('admin', 'event_organizer')
@event_owner_required
def participants(request, event_id):
    """Lihat peserta kegiatan"""
    event = get_object_or_404(Event, id=event_id)
    registrations = event.registrations.select_related('user').all()
    
    return render(request, 'events/participants.html', {
        'event': event,
        'registrations': registrations
    })


@login_required
@role_required('admin', 'event_organizer')
def validate_payment(request, registration_id):
    """Event Organizer memvalidasi pembayaran"""
    from registrations.models import EventRegistration
    
    registration = get_object_or_404(EventRegistration, id=registration_id)
    
    # Pastikan registration adalah untuk event milik organizer
    if request.user.role == 'event_organizer' and registration.event.user != request.user:
        messages.error(request, 'Anda tidak memiliki izin untuk memvalidasi pembayaran ini.')
        return redirect('events:participants', event_id=registration.event.id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            registration.payment_status = 'approved'
            registration.payment_validated_at = timezone.now()
            registration.payment_validated_by = request.user
            registration.payment_rejection_reason = None
            registration.save()
            messages.success(request, f'Pembayaran dari {registration.user.name} telah disetujui.')
            return redirect('events:participants', event_id=registration.event.id)
        elif action == 'reject':
            from registrations.models import PaymentRejection
            
            rejection_reason = request.POST.get('rejection_reason', '')
            if not rejection_reason:
                messages.error(request, 'Alasan penolakan harus diisi.')
                return render(request, 'events/reject_payment.html', {
                    'registration': registration
                })
            
            # Simpan history penolakan
            PaymentRejection.objects.create(
                event=registration.event,
                user=registration.user,
                rejection_reason=rejection_reason,
                rejected_by=request.user
            )
            
            # Hapus registration (user tidak terdaftar lagi dan bisa daftar ulang)
            user_name = registration.user.name
            event_id = registration.event.id
            registration.delete()
            
            messages.success(request, f'Pembayaran dari {user_name} telah ditolak. User dapat mendaftar ulang.')
            return redirect('events:participants', event_id=event_id)
    
    # Jika action reject tapi belum ada alasan, tampilkan form reject
    if request.GET.get('action') == 'reject':
        return render(request, 'events/reject_payment.html', {
            'registration': registration
        })
    
    return render(request, 'events/validate_payment.html', {
        'registration': registration
    })


@login_required
@role_required('user')
def my_reports(request):
    """Riwayat report event yang dibuat oleh user"""
    reports = ReportEvent.objects.filter(reporter=request.user).select_related('event').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        reports = reports.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(reports, 10)
    page = request.GET.get('page')
    reports_page = paginator.get_page(page)
    
    return render(request, 'events/my_reports.html', {
        'reports': reports_page,
        'status_filter': status_filter,
    })


@login_required
@role_required('user')
def report_event(request, event_id):
    """User melaporkan event"""
    event = get_object_or_404(Event, id=event_id, status='published', deleted_at__isnull=True)
    
    # Cek apakah sudah pernah report
    existing_report = ReportEvent.objects.filter(event=event, reporter=request.user).first()
    if existing_report:
        messages.info(request, 'Anda sudah melaporkan event ini sebelumnya.')
        return redirect('events:detail', event_id=event_id)
    
    if request.method == 'POST':
        form = ReportEventForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.event = event
            report.reporter = request.user
            report.status = 'pending'
            report.save()
            
            messages.success(request, 'Laporan Anda telah dikirim. Admin akan meninjau laporan ini.')
            return redirect('events:detail', event_id=event_id)
    else:
        form = ReportEventForm()
    
    return render(request, 'events/report.html', {
        'event': event,
        'form': form
    })


@login_required
@role_required('admin')
def review_reports(request):
    """Admin review semua laporan event"""
    reports = ReportEvent.objects.filter(status='pending').order_by('-created_at')
    
    return render(request, 'events/review_reports.html', {
        'reports': reports
    })


@login_required
@role_required('admin')
def approve_report(request, report_id):
    """Admin approve report dan suspend organizer"""
    report = get_object_or_404(ReportEvent, id=report_id, status='pending')
    
    if request.method == 'POST':
        # Suspend organizer
        organizer = report.event.user
        if organizer.role == 'event_organizer' and not organizer.is_suspended:
            organizer.is_suspended = True
            organizer.suspended_at = timezone.now()
            organizer.suspended_by = request.user
            organizer.suspension_reason = f"Laporan valid dari user: {report.reason} - {report.description}"
            organizer.save()
            
            # Berikan achievement ke reporter
            achievement, created = Achievement.objects.get_or_create(
                user=report.reporter,
                achievement_type='report_valid',
                defaults={
                    'title': 'Community Guardian',
                    'description': 'Anda telah membantu menjaga kualitas komunitas dengan melaporkan event yang tidak sesuai.',
                    'icon': 'bi-shield-check'
                }
            )
            
            # Update report status
            report.status = 'approved'
            report.reviewed_by = request.user
            report.reviewed_at = timezone.now()
            report.admin_feedback = 'Laporan disetujui. Event organizer telah di-suspend.'
            report.save()
            
            messages.success(request, f'Laporan disetujui. Event organizer {organizer.name} telah di-suspend dan user {report.reporter.name} mendapat achievement.')
        else:
            messages.warning(request, 'Event organizer sudah di-suspend sebelumnya atau bukan organizer.')
        
        return redirect('events:review_reports')
    
    return render(request, 'events/approve_report.html', {
        'report': report
    })


@login_required
@role_required('admin')
def reject_report(request, report_id):
    """Admin reject report dan berikan feedback"""
    report = get_object_or_404(ReportEvent, id=report_id, status='pending')
    
    if request.method == 'POST':
        feedback = request.POST.get('feedback', '')
        if not feedback.strip():
            messages.error(request, 'Feedback harus diisi.')
            return render(request, 'events/reject_report.html', {'report': report})
        
        report.status = 'rejected'
        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()
        report.admin_feedback = feedback
        report.save()
        
        messages.success(request, 'Laporan ditolak dan feedback telah dikirim ke user.')
        return redirect('events:review_reports')
    
    return render(request, 'events/reject_report.html', {
        'report': report
    })


def faq(request):
    """Halaman FAQ untuk user yang belum login"""
    return render(request, 'events/faq.html')


@login_required
def chatbot(request):
    """Halaman chatbot Dexy - Hanya untuk user yang sudah login"""
    return render(request, 'events/chatbot.html')


@login_required
def chatbot_api(request):
    """API endpoint untuk chatbot"""
    if request.method != 'POST':
        from django.http import JsonResponse
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        from django.http import JsonResponse
        from django.conf import settings
        from openai import OpenAI
        
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Initialize OpenAI client
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # System prompt untuk Dexy
        system_prompt = """Anda adalah Dexy, asisten AI yang ramah dan membantu untuk platform Dynamic Experience. 
Platform ini adalah sistem pendaftaran kegiatan yang menyediakan berbagai event seperti Seminar, Konser, dan Berita.

Tugas Anda:
1. Menjawab pertanyaan tentang platform Dynamic Experience
2. Membantu user memahami cara menggunakan fitur-fitur platform
3. Menjelaskan tentang event, pendaftaran, token, sertifikat, dll
4. Memberikan informasi tentang cara menghubungi Event Organizer jika diperlukan
5. Bersikap ramah, profesional, dan membantu

Jawablah dalam bahasa Indonesia yang mudah dipahami."""
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        bot_response = response.choices[0].message.content
        
        return JsonResponse({
            'response': bot_response,
            'status': 'success'
        })
        
    except Exception as e:
        from django.http import JsonResponse
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)

