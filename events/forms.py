from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Event, ReportEvent, News, NewsComment


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'description', 'event_date', 'event_time', 'location_type', 'location', 'zoom_link', 'zoom_meeting_id', 'zoom_passcode', 'price', 'bank_name', 'bank_account', 'flyer', 'certificate_template']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location_type': forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleLocationFields()'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'zoom_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://zoom.us/j/...'}),
            'zoom_meeting_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 123 456 7890'}),
            'zoom_passcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 123456'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: BCA, Mandiri, BRI'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor rekening untuk pembayaran'}),
            'flyer': forms.FileInput(attrs={'class': 'form-control'}),
            'certificate_template': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Judul Kegiatan',
            'category': 'Kategori Event',
            'description': 'Deskripsi Kegiatan',
            'event_date': 'Tanggal Kegiatan',
            'event_time': 'Waktu Kegiatan',
            'location_type': 'Tipe Lokasi',
            'location': 'Lokasi',
            'zoom_link': 'Link Zoom Meeting',
            'zoom_meeting_id': 'Meeting ID',
            'zoom_passcode': 'Passcode',
            'price': 'Harga Tiket',
            'bank_name': 'Nama Bank',
            'bank_account': 'Nomor Rekening',
            'flyer': 'Flyer Kegiatan',
            'certificate_template': 'Template Sertifikat',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        location_type = cleaned_data.get('location_type')
        location = cleaned_data.get('location')
        zoom_link = cleaned_data.get('zoom_link')
        
        # Validasi untuk online/hybrid event
        if location_type in ['online', 'hybrid']:
            if not zoom_link:
                raise ValidationError('Link Zoom Meeting wajib diisi untuk event online atau hybrid.')
        
        # Validasi untuk offline event
        if location_type == 'offline':
            if not location or not location.strip():
                raise ValidationError('Lokasi wajib diisi untuk event offline.')
        
        return cleaned_data
    
    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        
        if event_date:
            # Validasi H-3: minimal 3 hari dari sekarang
            min_date = (timezone.now().date() + timedelta(days=3))
            
            if event_date < min_date:
                raise ValidationError(
                    f'Kegiatan harus dibuat minimal 3 hari sebelum tanggal penyelenggaraan (H-3). '
                    f'Tanggal terdekat yang bisa dipilih: {min_date.strftime("%d %B %Y")}'
                )
        
        return event_date
    
    def clean_flyer(self):
        flyer = self.cleaned_data.get('flyer')
        
        if flyer:
            # Validasi ukuran file (max 5MB)
            if flyer.size > 5 * 1024 * 1024:
                raise ValidationError('Ukuran file flyer maksimal 5MB')
            
            # Validasi jenis file
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if flyer.content_type not in allowed_types:
                raise ValidationError('File flyer harus berupa gambar (JPG, PNG)')
        
        return flyer
    
    def clean_certificate_template(self):
        template = self.cleaned_data.get('certificate_template')
        
        if template:
            # Validasi ukuran file (max 10MB)
            if template.size > 10 * 1024 * 1024:
                raise ValidationError('Ukuran file template sertifikat maksimal 10MB')
        
        return template


class ReportEventForm(forms.ModelForm):
    """Form untuk melaporkan event"""
    
    reason = forms.ChoiceField(
        choices=[('', '-- Pilih Alasan Laporan --')] + list(ReportEvent.REASON_CHOICES),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        label='Alasan Laporan',
        required=True
    )
    
    class Meta:
        model = ReportEvent
        fields = ['reason', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Jelaskan secara detail mengapa event ini perlu dilaporkan...',
                'required': True
            }),
        }
        labels = {
            'description': 'Deskripsi Laporan',
        }
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description.strip()) < 20:
            raise ValidationError('Deskripsi laporan minimal 20 karakter. Mohon jelaskan secara detail.')
        return description


class NewsForm(forms.ModelForm):
    """Form untuk membuat/update berita"""
    
    class Meta:
        model = News
        fields = ['event', 'title', 'category', 'content', 'payment_info', 'payment_deadline', 'seminar_materials', 'concert_lineup', 'featured_image', 'is_published']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'payment_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Informasi tentang pembayaran event (jika berbayar)'}),
            'payment_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'seminar_materials': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Daftar materi yang akan dibahas dalam seminar'}),
            'concert_lineup': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Daftar grup musik atau artis yang akan tampil'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'event': 'Event Terkait (Opsional)',
            'title': 'Judul Berita',
            'category': 'Kategori',
            'content': 'Konten Berita',
            'payment_info': 'Informasi Pembayaran',
            'payment_deadline': 'Batas Waktu Pembayaran',
            'seminar_materials': 'Materi Seminar',
            'concert_lineup': 'Lineup Konser',
            'featured_image': 'Gambar Utama',
            'is_published': 'Publikasikan',
        }
    
    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Ukuran gambar maksimal 5MB')
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if image.content_type not in allowed_types:
                raise ValidationError('File gambar harus berupa JPG atau PNG')
        return image


class NewsCommentForm(forms.ModelForm):
    """Form untuk komentar berita"""
    
    class Meta:
        model = NewsComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tulis komentar Anda...',
                'required': True
            }),
        }
        labels = {
            'content': 'Komentar',
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 5:
            raise ValidationError('Komentar minimal 5 karakter.')
        return content

