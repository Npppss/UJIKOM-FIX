# 🔍 DEBUG REGISTRATION ISSUE

## Masalah
Setelah submit form register, status code 200 tapi tidak redirect ke halaman verifikasi OTP.

## Kemungkinan Penyebab

### 1. Form Tidak Valid
- Password tidak memenuhi kriteria
- Email sudah terdaftar
- Field lain tidak valid

### 2. Error Tidak Terlihat
- Error tersembunyi di form
- Messages tidak muncul

### 3. Email Service Error
- Email gagal dikirim tapi tidak ada error message

## Solusi yang Sudah Diterapkan

### ✅ 1. Improved Error Display
- Semua form errors ditampilkan dengan jelas
- Error per field ditampilkan
- Non-field errors ditampilkan

### ✅ 2. Better Logging
- Print form errors ke console
- Print exception jika ada
- Session OTP sebagai fallback

### ✅ 3. Fallback OTP
- OTP disimpan di session
- Tampilkan OTP di halaman verify jika email gagal
- Bisa verifikasi dengan OTP dari session

## Cara Test

1. **Submit form dengan password valid:**
   - Password: `Password123#`
   - Semua field diisi
   - Submit form

2. **Cek console/log:**
   - Lihat apakah ada "Form errors" atau "Registration error"
   - Cek apakah user terbuat di database

3. **Cek halaman verify:**
   - Harus redirect ke `/accounts/email/verify/`
   - OTP harus muncul di halaman (jika email gagal)

## Debug Steps

```bash
# 1. Cek user yang terbuat
python manage.py shell
>>> from accounts.models import User
>>> User.objects.filter(role='user').order_by('-created_at')[:5]

# 2. Cek OTP
>>> User.objects.filter(otp_code__isnull=False)[:5]

# 3. Test form validation
python test_registration.py
```

## Expected Behavior

1. User submit form → Form valid
2. User dibuat di database → OTP generated
3. Email dikirim → (atau OTP ditampilkan jika gagal)
4. Redirect ke `/accounts/email/verify/`
5. User input OTP → Email verified
6. Redirect ke login

---

**Silakan coba register lagi dan cek:**
1. Apakah ada error message yang muncul?
2. Apakah redirect ke halaman verify?
3. Apakah OTP muncul di halaman verify?

