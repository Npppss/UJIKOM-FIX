from django import forms
from django.core.exceptions import ValidationError
import re
from .models import User, EventOrganizer


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password',
        min_length=8,
        help_text='Minimal 8 karakter, harus mengandung angka, huruf besar, huruf kecil, dan karakter spesial (contoh: @$!%*?&#-_+=)'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Konfirmasi Password'
    )
    
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'address', 'education', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Validasi password - mengizinkan lebih banyak karakter spesial
        # Karakter spesial yang diizinkan: @$!%*?&#-_+=()[]{}|\\:;"'<>,./~
        # Pattern: minimal 1 huruf kecil, 1 huruf besar, 1 angka, 1 karakter spesial
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_number = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[@$!%*?&#\-_+=()\[\]{}|\\:;"\'<>,./~]', password))
        has_min_length = len(password) >= 8
        
        errors = []
        if not has_min_length:
            errors.append('Minimal 8 karakter')
        if not has_lowercase:
            errors.append('Huruf kecil (a-z)')
        if not has_uppercase:
            errors.append('Huruf besar (A-Z)')
        if not has_number:
            errors.append('Angka (0-9)')
        if not has_special:
            errors.append('Karakter spesial (contoh: @$!%*?&#-_+=)')
        
        if errors:
            raise ValidationError(
                'Password harus memenuhi: ' + ', '.join(errors)
            )
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError({'password_confirm': 'Password dan konfirmasi password tidak cocok'})
        
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email sudah terdaftar. Gunakan email lain atau lakukan login.')
        return email


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )


class OTPVerificationForm(forms.Form):
    otp_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan 6 digit OTP'}),
        label='Kode OTP'
    )


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )


class PasswordResetConfirmForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password Baru',
        min_length=8
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Konfirmasi Password Baru'
    )
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        # Validasi password dengan karakter spesial yang lebih luas
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_number = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[@$!%*?&#\-_+=()\[\]{}|\\:;"\'<>,./~]', password))
        has_min_length = len(password) >= 8
        
        errors = []
        if not has_min_length:
            errors.append('Minimal 8 karakter')
        if not has_lowercase:
            errors.append('Huruf kecil (a-z)')
        if not has_uppercase:
            errors.append('Huruf besar (A-Z)')
        if not has_number:
            errors.append('Angka (0-9)')
        if not has_special:
            errors.append('Karakter spesial (contoh: @$!%*?&#-_+=)')
        
        if errors:
            raise ValidationError(
                'Password harus memenuhi: ' + ', '.join(errors)
            )
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError({'password_confirm': 'Password dan konfirmasi password tidak cocok'})
        
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    """Form untuk update data diri user"""
    
    class Meta:
        model = User
        fields = ['name', 'phone', 'address', 'education']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Lengkap'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'No. Handphone (contoh: 081234567890)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Alamat Tempat Tinggal'
            }),
            'education': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pendidikan Terakhir (contoh: S1, S2, SMA)'
            }),
        }
        labels = {
            'name': 'Nama Lengkap',
            'phone': 'No. Handphone',
            'address': 'Alamat Tempat Tinggal',
            'education': 'Pendidikan Terakhir',
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Validasi format nomor telepon
            if not re.match(r'^\+?1?\d{9,15}$', phone):
                raise ValidationError('Format nomor telepon tidak valid. Gunakan format: 081234567890')
        return phone


class EventOrganizerRegistrationForm(forms.Form):
    """Form untuk registrasi Event Organizer"""
    
    # User fields
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
        label='Email',
        help_text='Email untuk login dan verifikasi'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        label='Password',
        min_length=8,
        help_text='Minimal 8 karakter, kombinasi huruf dan angka'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Konfirmasi Password'
        }),
        label='Konfirmasi Password'
    )
    
    # Event Organizer fields
    organizer_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nama Organizer'
        }),
        label='Nama Organizer',
        help_text='Nama resmi organisasi atau perusahaan'
    )
    person_in_charge = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nama Penanggung Jawab'
        }),
        label='Penanggung Jawab',
        help_text='Nama lengkap penanggung jawab'
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '081234567890'
        }),
        label='No. Telepon',
        help_text='Format: 081234567890'
    )
    organizer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Organizer'
        }),
        label='Email Organizer',
        help_text='Email resmi organizer (bisa berbeda dari email user)'
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Alamat lengkap kantor/organisasi'
        }),
        label='Alamat Organizer',
        help_text='Alamat lengkap kantor/organisasi'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Deskripsi singkat tentang organizer dan kegiatan yang biasa dilakukan'
        }),
        label='Deskripsi Organizer',
        help_text='Deskripsi singkat tentang organizer dan kegiatan yang biasa dilakukan'
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com'
        }),
        label='Website',
        help_text='Website organizer (opsional)'
    )
    social_media = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Link Instagram, Facebook, dll'
        }),
        label='Social Media',
        help_text='Link social media (opsional)'
    )
    business_license = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpg,.jpeg,.png'
        }),
        label='Surat Izin Usaha',
        help_text='Upload surat izin usaha atau dokumen legal lainnya (opsional)'
    )
    logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.jpg,.jpeg,.png'
        }),
        label='Logo Organizer',
        help_text='Logo organizer (opsional)'
    )
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Saya menyetujui Syarat & Ketentuan dan Kebijakan Privasi',
        error_messages={'required': 'Anda harus menyetujui Syarat & Ketentuan dan Kebijakan Privasi'}
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email sudah terdaftar. Gunakan email lain atau lakukan login.')
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        # Validasi password minimal 8 karakter, kombinasi huruf & angka
        has_letter = bool(re.search(r'[a-zA-Z]', password1))
        has_number = bool(re.search(r'[0-9]', password1))
        has_min_length = len(password1) >= 8
        
        errors = []
        if not has_min_length:
            errors.append('Minimal 8 karakter')
        if not has_letter:
            errors.append('Harus mengandung huruf')
        if not has_number:
            errors.append('Harus mengandung angka')
        
        if errors:
            raise ValidationError('Password harus memenuhi: ' + ', '.join(errors))
        
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError({'password2': 'Password dan konfirmasi password tidak cocok'})
        
        return cleaned_data
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            if not re.match(r'^\+?1?\d{9,15}$', phone_number):
                raise ValidationError('Format nomor telepon tidak valid. Gunakan format: 081234567890')
        return phone_number

