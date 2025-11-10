from django import forms
from django.core.exceptions import ValidationError
import re
from .models import User


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

