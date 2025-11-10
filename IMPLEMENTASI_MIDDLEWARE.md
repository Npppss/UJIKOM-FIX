# IMPLEMENTASI MIDDLEWARE & VALIDASI

## 1. AUTHENTICATION MIDDLEWARE

```php
// middleware/AuthMiddleware.php

class AuthMiddleware {
    public function handle($request, $next) {
        // Cek apakah user sudah login
        $sessionToken = $request->cookie('session_token') ?? $request->header('Authorization');
        
        if (!$sessionToken) {
            return redirect('/login')->with('error', 'Silakan login terlebih dahulu');
        }
        
        // Cek session di database
        $session = Session::where('token', $sessionToken)
            ->where('expired_at', '>', now())
            ->first();
        
        if (!$session) {
            return redirect('/login')->with('error', 'Session expired. Silakan login kembali');
        }
        
        // Update last_activity untuk session timeout
        $session->update([
            'last_activity' => now(),
            'expired_at' => now()->addMinutes(5)
        ]);
        
        // Attach user ke request
        $user = User::find($session->user_id);
        $request->setUser($user);
        
        return $next($request);
    }
}
```

---

## 2. SESSION TIMEOUT MIDDLEWARE

```php
// middleware/SessionTimeoutMiddleware.php

class SessionTimeoutMiddleware {
    public function handle($request, $next) {
        $user = $request->getUser(); // Dari AuthMiddleware
        
        if ($user) {
            $session = Session::where('user_id', $user->id)
                ->where('token', $request->cookie('session_token'))
                ->first();
            
            if ($session) {
                $lastActivity = Carbon::parse($session->last_activity);
                $now = Carbon::now();
                
                // Cek apakah sudah lebih dari 5 menit tidak aktif
                if ($now->diffInMinutes($lastActivity) > 5) {
                    // Destroy session
                    $session->delete();
                    
                    return redirect('/login')
                        ->withCookie(cookie()->forget('session_token'))
                        ->with('error', 'Session expired. Tidak ada aktivitas selama 5 menit.');
                }
                
                // Update last_activity setiap request
                $session->update([
                    'last_activity' => now(),
                    'expired_at' => now()->addMinutes(5)
                ]);
            }
        }
        
        return $next($request);
    }
}
```

---

## 3. ROLE MIDDLEWARE

```php
// middleware/RoleMiddleware.php

class RoleMiddleware {
    private $allowedRoles;
    
    public function __construct(...$roles) {
        $this->allowedRoles = $roles;
    }
    
    public function handle($request, $next) {
        $user = $request->getUser();
        
        if (!$user) {
            return redirect('/login')->with('error', 'Silakan login terlebih dahulu');
        }
        
        // Cek apakah role user ada di allowed roles
        if (!in_array($user->role, $this->allowedRoles)) {
            return redirect('/dashboard')
                ->with('error', 'Anda tidak memiliki akses untuk halaman ini');
        }
        
        return $next($request);
    }
}

// Penggunaan:
// Route::middleware([RoleMiddleware::class . ':admin,event_organizer'])
```

---

## 4. EVENT ACCESS MIDDLEWARE (Untuk Event Organizer)

```php
// middleware/EventAccessMiddleware.php

class EventAccessMiddleware {
    public function handle($request, $next) {
        $user = $request->getUser();
        $eventId = $request->route('eventId') ?? $request->input('event_id');
        
        if (!$eventId) {
            return response()->json(['error' => 'Event ID tidak ditemukan'], 400);
        }
        
        $event = Event::find($eventId);
        
        if (!$event) {
            return response()->json(['error' => 'Event tidak ditemukan'], 404);
        }
        
        // Admin bisa akses semua event
        if ($user->role === 'admin') {
            return $next($request);
        }
        
        // Event Organizer hanya bisa akses event sendiri
        if ($user->role === 'event_organizer') {
            if ($event->user_id !== $user->id) {
                return redirect('/dashboard/organizer')
                    ->with('error', 'Anda tidak memiliki akses untuk mengelola kegiatan ini');
            }
        }
        
        // User biasa tidak bisa akses
        if ($user->role === 'user') {
            return redirect('/dashboard/user')
                ->with('error', 'Akses ditolak');
        }
        
        return $next($request);
    }
}
```

---

## 5. EMAIL VERIFICATION MIDDLEWARE (Untuk User)

```php
// middleware/EmailVerificationMiddleware.php

class EmailVerificationMiddleware {
    public function handle($request, $next) {
        $user = $request->getUser();
        
        // Hanya untuk role 'user', admin dan event_organizer tidak perlu verifikasi
        if ($user->role === 'user' && !$user->email_verified_at) {
            return redirect('/email/verify')
                ->with('warning', 'Silakan verifikasi email terlebih dahulu');
        }
        
        return $next($request);
    }
}
```

---

## 6. REGISTRATION DEADLINE VALIDATION

```php
// services/EventRegistrationService.php

class EventRegistrationService {
    public function canRegister($userId, $eventId) {
        $event = Event::find($eventId);
        
        if (!$event) {
            return ['success' => false, 'message' => 'Event tidak ditemukan'];
        }
        
        // Cek apakah waktu pendaftaran masih dibuka
        if (now() >= $event->registration_closed_at) {
            return [
                'success' => false,
                'message' => 'Pendaftaran sudah ditutup. Kegiatan sudah dimulai atau sudah lewat.'
            ];
        }
        
        // Cek apakah user sudah terdaftar
        $existingRegistration = EventRegistration::where('event_id', $eventId)
            ->where('user_id', $userId)
            ->first();
        
        if ($existingRegistration) {
            return [
                'success' => false,
                'message' => 'Anda sudah terdaftar pada kegiatan ini'
            ];
        }
        
        return ['success' => true];
    }
}
```

---

## 7. EVENT CREATION VALIDATION (H-3 Rule)

```php
// services/EventService.php

class EventService {
    public function canCreateEvent($eventDate) {
        $today = now()->startOfDay();
        $minDate = $today->copy()->addDays(3); // H-3
        $eventDateCarbon = Carbon::parse($eventDate);
        
        if ($eventDateCarbon->lt($minDate)) {
            return [
                'success' => false,
                'message' => 'Kegiatan harus dibuat minimal 3 hari sebelum tanggal penyelenggaraan (H-3)'
            ];
        }
        
        return ['success' => true];
    }
    
    public function createEvent($data, $userId) {
        // Validasi H-3
        $validation = $this->canCreateEvent($data['event_date']);
        if (!$validation['success']) {
            throw new ValidationException($validation['message']);
        }
        
        // Set registration_closed_at
        $data['registration_closed_at'] = Carbon::parse($data['event_date'])
            ->setTimeFromTimeString($data['event_time']);
        
        $data['user_id'] = $userId;
        
        return Event::create($data);
    }
}
```

---

## 8. ATTENDANCE VALIDATION (Hari H)

```php
// services/AttendanceService.php

class AttendanceService {
    public function canFillAttendance($userId, $eventId) {
        $event = Event::find($eventId);
        $registration = EventRegistration::where('event_id', $eventId)
            ->where('user_id', $userId)
            ->first();
        
        if (!$registration) {
            return ['success' => false, 'message' => 'Anda belum terdaftar pada kegiatan ini'];
        }
        
        if ($registration->status === 'attended') {
            return ['success' => false, 'message' => 'Anda sudah mengisi daftar hadir'];
        }
        
        // Cek apakah sudah hari H dan sudah jam kegiatan
        $eventDateTime = Carbon::parse($event->event_date)
            ->setTimeFromTimeString($event->event_time);
        $now = Carbon::now();
        
        if ($now->lt($eventDateTime)) {
            return [
                'success' => false,
                'message' => 'Daftar hadir dapat diisi pada hari H setelah jam kegiatan dimulai'
            ];
        }
        
        return ['success' => true];
    }
    
    public function verifyToken($userId, $eventId, $token) {
        $registration = EventRegistration::where('event_id', $eventId)
            ->where('user_id', $userId)
            ->where('token', $token)
            ->first();
        
        if (!$registration) {
            return ['success' => false, 'message' => 'Token tidak valid'];
        }
        
        if ($registration->status === 'attended') {
            return ['success' => false, 'message' => 'Token sudah digunakan'];
        }
        
        // Update status
        $registration->update([
            'status' => 'attended',
            'attendance_at' => now()
        ]);
        
        // Generate sertifikat jika ada template
        if ($registration->event->certificate_template_path) {
            $this->generateCertificate($registration);
        }
        
        return ['success' => true, 'registration' => $registration];
    }
}
```

---

## 9. PASSWORD VALIDATION

```php
// services/PasswordService.php

class PasswordService {
    public function validatePassword($password) {
        // Minimal 8 karakter, angka, huruf besar, huruf kecil, karakter spesial
        $pattern = '/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$/';
        
        if (!preg_match($pattern, $password)) {
            return [
                'success' => false,
                'message' => 'Password minimal 8 karakter dan harus mengandung angka, huruf besar, huruf kecil, dan karakter spesial (@$!%*?&#)'
            ];
        }
        
        return ['success' => true];
    }
    
    public function hashPassword($password) {
        return bcrypt($password); // atau password_hash($password, PASSWORD_BCRYPT, ['cost' => 10])
    }
    
    public function verifyPassword($password, $hashedPassword) {
        return password_verify($password, $hashedPassword);
    }
}
```

---

## 10. EMAIL SERVICE

```php
// services/EmailService.php

class EmailService {
    public function sendVerificationEmail($user) {
        // Generate token atau OTP
        $token = Str::random(60);
        $otp = str_pad(rand(0, 999999), 6, '0', STR_PAD_LEFT);
        
        // Simpan ke database
        $user->update([
            'email_verification_token' => $token,
            'email_verification_expired' => now()->addMinutes(5),
            'otp_code' => $otp,
            'otp_expired' => now()->addMinutes(5)
        ]);
        
        // Kirim email dengan link atau OTP
        Mail::send('emails.verification', [
            'user' => $user,
            'token' => $token,
            'otp' => $otp,
            'expired_at' => now()->addMinutes(5)
        ], function($message) use ($user) {
            $message->to($user->email)
                ->subject('Verifikasi Email - Sistem Pendaftaran Kegiatan');
        });
    }
    
    public function sendRegistrationToken($registration) {
        $event = $registration->event;
        $user = $registration->user;
        
        Mail::send('emails.registration_token', [
            'user' => $user,
            'event' => $event,
            'token' => $registration->token
        ], function($message) use ($user) {
            $message->to($user->email)
                ->subject('Token Pendaftaran Kegiatan');
        });
    }
    
    public function sendResetPasswordEmail($user) {
        $token = Str::random(60);
        
        $user->update([
            'reset_password_token' => $token,
            'reset_password_expired' => now()->addHour() // 1 jam
        ]);
        
        Mail::send('emails.reset_password', [
            'user' => $user,
            'token' => $token,
            'expired_at' => now()->addHour()
        ], function($message) use ($user) {
            $message->to($user->email)
                ->subject('Reset Password - Sistem Pendaftaran Kegiatan');
        });
    }
}
```

---

## 11. TOKEN GENERATION SERVICE

```php
// services/TokenService.php

class TokenService {
    public function generateRegistrationToken() {
        // Generate 10 digit angka acak
        do {
            $token = str_pad(rand(0, 9999999999), 10, '0', STR_PAD_LEFT);
            // Cek apakah token sudah ada
            $exists = EventRegistration::where('token', $token)->exists();
        } while ($exists);
        
        return $token;
    }
}
```

---

## 12. DASHBOARD STATISTICS SERVICE

```php
// services/DashboardService.php

class DashboardService {
    public function getMonthlyEventStats($userId = null, $role = null) {
        $query = Event::selectRaw('MONTH(created_at) as bulan, COUNT(*) as jumlah')
            ->whereYear('created_at', now()->year);
        
        // Filter untuk Event Organizer
        if ($role === 'event_organizer' && $userId) {
            $query->where('user_id', $userId);
        }
        
        return $query->groupBy('bulan')->get();
    }
    
    public function getMonthlyParticipantStats($userId = null, $role = null) {
        $query = EventRegistration::selectRaw('MONTH(attendance_at) as bulan, COUNT(*) as jumlah')
            ->where('status', 'attended')
            ->whereYear('attendance_at', now()->year);
        
        // Filter untuk Event Organizer
        if ($role === 'event_organizer' && $userId) {
            $query->join('events', 'event_registrations.event_id', '=', 'events.id')
                ->where('events.user_id', $userId);
        }
        
        return $query->groupBy('bulan')->get();
    }
    
    public function getTop10EventsByParticipants($userId = null, $role = null) {
        $query = Event::selectRaw('
                events.id,
                events.title,
                events.event_date,
                COUNT(event_registrations.id) as jumlah_peserta
            ')
            ->leftJoin('event_registrations', function($join) {
                $join->on('events.id', '=', 'event_registrations.event_id')
                    ->where('event_registrations.status', '=', 'attended');
            })
            ->whereNull('events.deleted_at')
            ->groupBy('events.id');
        
        // Filter untuk Event Organizer
        if ($role === 'event_organizer' && $userId) {
            $query->where('events.user_id', $userId);
        }
        
        return $query->orderBy('jumlah_peserta', 'DESC')
            ->limit(10)
            ->get();
    }
}
```

---

## CONTOH ROUTE DEFINITION

```php
// routes/web.php

// Public Routes
Route::get('/', 'PublicController@katalog');
Route::get('/katalog', 'PublicController@katalog');
Route::post('/katalog/search', 'PublicController@search');

// Auth Routes
Route::get('/register', 'AuthController@showRegister');
Route::post('/register', 'AuthController@register');
Route::get('/login', 'AuthController@showLogin');
Route::post('/login', 'AuthController@login');
Route::post('/logout', 'AuthController@logout');
Route::get('/email/verify/{token}', 'AuthController@verifyEmail');
Route::post('/email/verify/otp', 'AuthController@verifyOtp');
Route::get('/password/reset', 'AuthController@showResetPassword');
Route::post('/password/reset', 'AuthController@requestResetPassword');
Route::get('/password/reset/{token}', 'AuthController@showResetPasswordForm');
Route::post('/password/reset/{token}', 'AuthController@resetPassword');

// User Routes (perlu login + email verified)
Route::middleware(['auth', 'email_verification'])->group(function() {
    Route::get('/dashboard/user', 'User\DashboardController@index');
    Route::get('/events/{id}/register', 'User\EventController@register');
    Route::post('/events/{id}/register', 'User\EventController@storeRegistration');
    Route::get('/events/{id}/attendance', 'User\EventController@showAttendance');
    Route::post('/events/{id}/attendance', 'User\EventController@fillAttendance');
    Route::get('/riwayat', 'User\EventController@riwayat');
    Route::get('/sertifikat', 'User\CertificateController@index');
    Route::get('/sertifikat/{id}/download', 'User\CertificateController@download');
});

// Admin Routes (perlu login + role admin)
Route::middleware(['auth', 'role:admin'])->prefix('admin')->group(function() {
    Route::get('/dashboard', 'Admin\DashboardController@index');
    Route::get('/events', 'Admin\EventController@index');
    Route::get('/events/create', 'Admin\EventController@create');
    Route::post('/events', 'Admin\EventController@store');
    Route::get('/events/{id}/edit', 'Admin\EventController@edit');
    Route::put('/events/{id}', 'Admin\EventController@update');
    Route::delete('/events/{id}', 'Admin\EventController@destroy');
    Route::get('/events/{id}/participants', 'Admin\EventController@participants');
    Route::get('/export/participants', 'Admin\ExportController@exportParticipants');
    Route::get('/users', 'Admin\UserController@index');
    Route::get('/organizers', 'Admin\OrganizerController@index');
});

// Event Organizer Routes (perlu login + role event_organizer)
Route::middleware(['auth', 'role:event_organizer'])->prefix('organizer')->group(function() {
    Route::get('/dashboard', 'EventOrganizer\DashboardController@index');
    Route::get('/events', 'EventOrganizer\EventController@index');
    Route::get('/events/create', 'EventOrganizer\EventController@create');
    Route::post('/events', 'EventOrganizer\EventController@store');
    Route::middleware('event_access')->group(function() {
        Route::get('/events/{id}/edit', 'EventOrganizer\EventController@edit');
        Route::put('/events/{id}', 'EventOrganizer\EventController@update');
        Route::delete('/events/{id}', 'EventOrganizer\EventController@destroy');
        Route::get('/events/{id}/participants', 'EventOrganizer\EventController@participants');
    });
    Route::get('/export/participants', 'EventOrganizer\ExportController@exportParticipants');
});
```

---

## PRIORITAS IMPLEMENTASI MIDDLEWARE

1. **AuthMiddleware** - Wajib untuk semua halaman yang perlu login
2. **SessionTimeoutMiddleware** - Update last_activity setiap request
3. **RoleMiddleware** - Filter akses berdasarkan role
4. **EmailVerificationMiddleware** - Hanya untuk user
5. **EventAccessMiddleware** - Hanya untuk Event Organizer saat edit event

