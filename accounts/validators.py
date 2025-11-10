from django.core.exceptions import ValidationError
import re


class ComplexPasswordValidator:
    """
    Validator untuk password yang kompleks:
    - Minimal 8 karakter
    - Harus ada huruf kecil
    - Harus ada huruf besar
    - Harus ada angka
    - Harus ada karakter spesial
    """
    
    def validate(self, password, user=None):
        # Mengizinkan lebih banyak karakter spesial
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#\-_+=()\[\]{}|\\:;"\'<>,./~])[A-Za-z\d@$!%*?&#\-_+=()\[\]{}|\\:;"\'<>,./~]{8,}$'
        
        if not re.match(pattern, password):
            raise ValidationError(
                'Password minimal 8 karakter dan harus mengandung angka, '
                'huruf besar, huruf kecil, dan karakter spesial (contoh: @$!%*?&#-_+=)',
                code='password_too_simple',
            )
    
    def get_help_text(self):
        return (
            'Password harus minimal 8 karakter dan mengandung: '
            'angka, huruf besar, huruf kecil, dan karakter spesial (contoh: @$!%*?&#-_+=)'
        )

