# RINGKASAN PERBANDINGAN 3 ROLE

## TABEL PERBANDINGAN FITUR

| Fitur | USER | ADMIN | EVENT ORGANIZER |
|-------|------|-------|-----------------|
| **Registrasi Akun** | ✅ (Dengan verifikasi email) | ❌ (Dibuat manual/database) | ❌ (Dibuat manual/database) |
| **Login** | ✅ | ✅ | ✅ |
| **Verifikasi Email** | ✅ Wajib (OTP/Link) | ❌ Tidak perlu | ❌ Tidak perlu |
| **Lihat Katalog Kegiatan** | ✅ | ✅ | ✅ |
| **Pencarian Kegiatan** | ✅ | ✅ | ✅ |
| **Mendaftar Kegiatan** | ✅ | ❌ | ❌ |
| **Mengisi Daftar Hadir** | ✅ (Dengan token) | ❌ | ❌ |
| **Melihat Sertifikat** | ✅ (Sertifikat sendiri) | ❌ | ❌ |
| **Riwayat Kegiatan** | ✅ (Kegiatan sendiri) | ❌ | ❌ |
| **Reset Password** | ✅ | ✅ | ✅ |
| **Membuat Kegiatan** | ❌ | ✅ (Maksimal H-3) | ✅ (Maksimal H-3) |
| **Mengelola Kegiatan** | ❌ | ✅ **Semua Kegiatan** | ✅ **Hanya Kegiatan Sendiri** |
| **Dashboard Statistik** | ❌ | ✅ (Semua Data) | ✅ (Data Kegiatan Sendiri) |
| **Grafik Kegiatan per Bulan** | ❌ | ✅ Semua | ✅ Hanya Sendiri |
| **Grafik Peserta per Bulan** | ❌ | ✅ Semua | ✅ Hanya Sendiri |
| **Top 10 Kegiatan** | ❌ | ✅ Semua | ✅ Hanya Sendiri |
| **Ekspor Data Peserta** | ❌ | ✅ Semua Peserta | ✅ Peserta Kegiatan Sendiri |
| **Kelola User** | ❌ | ✅ | ❌ |
| **Kelola Event Organizer** | ❌ | ✅ | ❌ |

---

## PERBEDAAN UTAMA DALAM IMPLEMENTASI

### 1. AKSES KEGIATAN

**ADMIN:**
```sql
-- Bisa melihat semua kegiatan
SELECT * FROM events WHERE deleted_at IS NULL
```

**EVENT ORGANIZER:**
```sql
-- Hanya bisa melihat kegiatan sendiri
SELECT * FROM events 
WHERE user_id = current_user_id 
AND deleted_at IS NULL
```

**USER:**
```sql
-- Hanya bisa melihat katalog publik
SELECT * FROM events 
WHERE status = 'published' 
AND deleted_at IS NULL
AND registration_closed_at > NOW()
```

---

### 2. DASHBOARD STATISTIK

#### Admin Dashboard:
- **Semua data** dari semua kegiatan
- Tidak ada filter `user_id`

#### Event Organizer Dashboard:
- **Hanya data kegiatan sendiri**
- Selalu filter `WHERE events.user_id = current_user_id`

#### Query Contoh:

**Admin - Jumlah Kegiatan per Bulan:**
```sql
SELECT MONTH(created_at) as bulan, COUNT(*) as jumlah
FROM events
WHERE YEAR(created_at) = YEAR(NOW())
GROUP BY MONTH(created_at)
```

**Event Organizer - Jumlah Kegiatan per Bulan:**
```sql
SELECT MONTH(created_at) as bulan, COUNT(*) as jumlah
FROM events
WHERE user_id = current_user_id
AND YEAR(created_at) = YEAR(NOW())
GROUP BY MONTH(created_at)
```

---

### 3. EKSPOR DATA

**Admin Ekspor:**
- Semua peserta dari semua kegiatan
- File: `semua_peserta_kegiatan.xls`

**Event Organizer Ekspor:**
- Hanya peserta dari kegiatan yang dibuatnya
- File: `peserta_kegiatan_saya.xls`

**Query Contoh:**

**Admin:**
```sql
SELECT 
    e.title,
    e.event_date,
    u.name,
    u.email,
    er.status,
    er.attendance_at
FROM event_registrations er
JOIN events e ON er.event_id = e.id
JOIN users u ON er.user_id = u.id
ORDER BY e.event_date DESC
```

**Event Organizer:**
```sql
SELECT 
    e.title,
    e.event_date,
    u.name,
    u.email,
    er.status,
    er.attendance_at
FROM event_registrations er
JOIN events e ON er.event_id = e.id
JOIN users u ON er.user_id = u.id
WHERE e.user_id = current_user_id  -- FILTER INI
ORDER BY e.event_date DESC
```

---

### 4. MIDDLEWARE & AKSES

#### Event Access:

**Admin:**
- Tidak perlu middleware khusus
- Bisa akses semua event langsung

**Event Organizer:**
- Perlu `EventAccessMiddleware`
- Cek: `event.user_id == current_user.id`

**Code:**
```php
// Admin: Bisa langsung
Route::get('/events/{id}/edit', 'Admin\EventController@edit');

// Event Organizer: Perlu middleware
Route::middleware('event_access')->group(function() {
    Route::get('/events/{id}/edit', 'EventOrganizer\EventController@edit');
});
```

---

### 5. VALIDASI PENDATAN EVENT

**Semua Role (Admin & Event Organizer):**
- Aturan H-3: `event_date >= TODAY + 3 days`
- Validasi sama untuk kedua role

**Code:**
```php
public function createEvent($data, $userId) {
    $minDate = now()->addDays(3);
    if (Carbon::parse($data['event_date'])->lt($minDate)) {
        throw new ValidationException('Kegiatan harus dibuat minimal H-3');
    }
    // ... create event
}
```

---

### 6. SESSION TIMEOUT

**Semua Role:**
- Aturan sama: 5 menit tidak aktif = logout
- Implementasi middleware sama

---

## CONTOH KASUS PENGGUNAAN

### Kasus 1: Event Organizer Membuat Kegiatan

1. **Event Organizer A** login
2. Membuat kegiatan "Workshop PHP"
3. Kegiatan tersimpan dengan `user_id = Event Organizer A`
4. **Event Organizer B** tidak bisa edit/hapus kegiatan "Workshop PHP"
5. **Admin** bisa edit/hapus semua kegiatan termasuk "Workshop PHP"

---

### Kasus 2: Dashboard Statistik

**Event Organizer A:**
- Dashboard hanya menampilkan:
  - Kegiatan yang dibuat Event Organizer A
  - Peserta dari kegiatan Event Organizer A
  - Statistik hanya untuk Event Organizer A

**Admin:**
- Dashboard menampilkan:
  - Semua kegiatan (dari semua Admin + semua Event Organizer)
  - Semua peserta dari semua kegiatan
  - Statistik global

---

### Kasus 3: Ekspor Data

**Event Organizer A:**
- Ekspor file berisi:
  - Hanya peserta dari kegiatan Event Organizer A
  - Tidak ada peserta dari kegiatan Event Organizer B
  - Tidak ada peserta dari kegiatan Admin

**Admin:**
- Ekspor file berisi:
  - Semua peserta dari semua kegiatan
  - Termasuk peserta dari semua Event Organizer

---

## STRUKTUR MENU BERDASARKAN ROLE

### USER Menu:
```
- Dashboard
- Katalog Kegiatan
- Riwayat Kegiatan
- Sertifikat
- Profil
```

### ADMIN Menu:
```
- Dashboard (Statistik Global)
- Kelola Kegiatan (Semua)
- Tambah Kegiatan
- Kelola User
- Kelola Event Organizer
- Ekspor Data (Semua)
- Profil
```

### EVENT ORGANIZER Menu:
```
- Dashboard (Statistik Kegiatan Sendiri)
- Kelola Kegiatan (Hanya Sendiri)
- Tambah Kegiatan
- Ekspor Data (Kegiatan Sendiri)
- Profil
```

---

## CATATAN PENTING UNTUK DEVELOPER

### 1. Selalu Filter untuk Event Organizer
```php
// ❌ SALAH - Event Organizer bisa lihat semua
$events = Event::all();

// ✅ BENAR - Event Organizer hanya lihat sendiri
if (auth()->user()->role === 'event_organizer') {
    $events = Event::where('user_id', auth()->id())->get();
} else {
    $events = Event::all(); // Admin
}
```

### 2. Middleware untuk Edit/Delete Event
```php
// Pastikan Event Organizer tidak bisa edit event orang lain
Route::middleware(['auth', 'event_access'])
    ->group(function() {
        Route::put('/events/{id}', 'EventController@update');
        Route::delete('/events/{id}', 'EventController@destroy');
    });
```

### 3. Dashboard Query
```php
// Pastikan filter user_id untuk Event Organizer
public function getMonthlyStats() {
    $query = Event::selectRaw('MONTH(created_at) as bulan, COUNT(*) as jumlah');
    
    if (auth()->user()->role === 'event_organizer') {
        $query->where('user_id', auth()->id());
    }
    
    return $query->groupBy('bulan')->get();
}
```

### 4. Export Data
```php
// Pastikan filter untuk Event Organizer
public function exportParticipants() {
    $query = EventRegistration::with(['event', 'user']);
    
    if (auth()->user()->role === 'event_organizer') {
        $query->whereHas('event', function($q) {
            $q->where('user_id', auth()->id());
        });
    }
    
    // ... generate file
}
```

---

## TESTING SCENARIOS

### Test 1: Event Organizer Akses Kegiatan Orang Lain
```
1. Event Organizer A membuat Kegiatan 1
2. Event Organizer B login
3. Event Organizer B coba akses /events/1/edit (Kegiatan A)
Expected: Redirect dengan error "Tidak memiliki akses"
```

### Test 2: Admin Akses Semua Kegiatan
```
1. Event Organizer A membuat Kegiatan 1
2. Event Organizer B membuat Kegiatan 2
3. Admin login
4. Admin akses /events/1/edit
Expected: Bisa edit (berhasil)
5. Admin akses /events/2/edit
Expected: Bisa edit (berhasil)
```

### Test 3: Dashboard Statistik Event Organizer
```
1. Event Organizer A membuat 5 kegiatan
2. Event Organizer B membuat 3 kegiatan
3. Event Organizer A login, buka dashboard
Expected: Hanya menampilkan 5 kegiatan (kegiatan sendiri)
```

### Test 4: Ekspor Data Event Organizer
```
1. Event Organizer A membuat Kegiatan 1 (10 peserta)
2. Event Organizer B membuat Kegiatan 2 (15 peserta)
3. Event Organizer A ekspor data
Expected: File hanya berisi 10 peserta (dari Kegiatan 1)
```

---

## KESIMPULAN

**Perbedaan Inti:**
- **ADMIN** = Full access, semua data
- **EVENT ORGANIZER** = Terbatas pada kegiatan sendiri
- **USER** = Hanya partisipasi (daftar, hadir, sertifikat)

**Prinsip Implementasi:**
1. **Admin**: Tidak perlu filter `user_id`
2. **Event Organizer**: Selalu filter `WHERE user_id = current_user_id`
3. **User**: Hanya akses publik + data sendiri

**Keamanan:**
- Selalu validasi role di middleware
- Pastikan Event Organizer tidak bisa akses data orang lain
- Gunakan middleware `event_access` untuk edit/delete event

