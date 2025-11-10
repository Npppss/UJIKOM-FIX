from django import forms
from .models import EventRegistration


class AttendanceForm(forms.Form):
    token = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan token 10 digit',
            'maxlength': '10'
        }),
        label='Token Daftar Hadir',
        help_text='Masukkan token 10 digit yang dikirim ke email Anda'
    )
    
    def clean_token(self):
        token = self.cleaned_data.get('token')
        
        # Validasi format: hanya angka, 10 digit
        if not token.isdigit() or len(token) != 10:
            raise forms.ValidationError('Token harus berupa 10 digit angka')
        
        return token


class PaymentProofForm(forms.ModelForm):
    """Form untuk upload bukti pembayaran"""
    
    class Meta:
        model = EventRegistration
        fields = ['payment_proof']
        widgets = {
            'payment_proof': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf',
            }),
        }
        labels = {
            'payment_proof': 'Upload Bukti Pembayaran',
        }
    
    def clean_payment_proof(self):
        payment_proof = self.cleaned_data.get('payment_proof')
        if payment_proof:
            # Validasi ukuran file (max 5MB)
            if payment_proof.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Ukuran file bukti pembayaran maksimal 5MB')
            
            # Validasi jenis file
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
            # Cek content_type atau ekstensi file
            if hasattr(payment_proof, 'content_type'):
                if payment_proof.content_type not in allowed_types:
                    raise forms.ValidationError('File bukti pembayaran harus berupa gambar (JPG, PNG) atau PDF')
            else:
                # Fallback: cek ekstensi
                file_name = payment_proof.name.lower()
                if not (file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png') or file_name.endswith('.pdf')):
                    raise forms.ValidationError('File bukti pembayaran harus berupa gambar (JPG, PNG) atau PDF')
        
        return payment_proof
