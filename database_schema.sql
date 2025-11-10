-- ============================================
-- DATABASE SCHEMA: SISTEM PENDAFTARAN KEGIATAN
-- 3 ROLE: USER, ADMIN, EVENT ORGANIZER
-- ============================================

-- Table: users
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL COMMENT 'Nama lengkap',
    email VARCHAR(255) UNIQUE NOT NULL COMMENT 'Alamat email (unique)',
    phone VARCHAR(20) NOT NULL COMMENT 'No handphone',
    address TEXT NOT NULL COMMENT 'Alamat tempat tinggal',
    education VARCHAR(100) NOT NULL COMMENT 'Pendidikan terakhir',
    password VARCHAR(255) NOT NULL COMMENT 'Password yang sudah di-hash',
    role ENUM('user', 'admin', 'event_organizer') NOT NULL DEFAULT 'user' COMMENT 'Role: user, admin, atau event_organizer',
    
    -- Email verification
    email_verified_at TIMESTAMP NULL COMMENT 'Tanggal email diverifikasi',
    email_verification_token VARCHAR(255) NULL COMMENT 'Token untuk link aktivasi email',
    email_verification_expired TIMESTAMP NULL COMMENT 'Tanggal expired link aktivasi',
    otp_code VARCHAR(6) NULL COMMENT 'OTP code untuk verifikasi',
    otp_expired TIMESTAMP NULL COMMENT 'Tanggal expired OTP (minimal 5 menit)',
    
    -- Password reset
    reset_password_token VARCHAR(255) NULL COMMENT 'Token untuk reset password',
    reset_password_expired TIMESTAMP NULL COMMENT 'Tanggal expired reset token',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_email_verification_token (email_verification_token),
    INDEX idx_otp_code (otp_code),
    INDEX idx_reset_password_token (reset_password_token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: events (kegiatan)
CREATE TABLE events (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT 'ID pembuat kegiatan (admin atau event_organizer)',
    title VARCHAR(255) NOT NULL COMMENT 'Judul kegiatan/event',
    description TEXT COMMENT 'Deskripsi kegiatan',
    event_date DATE NOT NULL COMMENT 'Tanggal kegiatan berlangsung',
    event_time TIME NOT NULL COMMENT 'Waktu/jam kegiatan berlangsung',
    location VARCHAR(255) NOT NULL COMMENT 'Lokasi kegiatan',
    flyer_path VARCHAR(500) NULL COMMENT 'Path file flyer kegiatan',
    certificate_template_path VARCHAR(500) NULL COMMENT 'Path template sertifikat',
    registration_closed_at TIMESTAMP NULL COMMENT 'Waktu tutup pendaftaran (event_date + event_time)',
    status ENUM('draft', 'published', 'completed', 'cancelled') DEFAULT 'draft' COMMENT 'Status kegiatan',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL COMMENT 'Soft delete',
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_event_date (event_date),
    INDEX idx_event_date_time (event_date, event_time),
    INDEX idx_status (status),
    INDEX idx_registration_closed_at (registration_closed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: event_registrations (pendaftaran peserta)
CREATE TABLE event_registrations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    event_id BIGINT NOT NULL COMMENT 'ID kegiatan',
    user_id BIGINT NOT NULL COMMENT 'ID peserta/user',
    token VARCHAR(10) NOT NULL UNIQUE COMMENT 'Token 10 digit untuk daftar hadir',
    token_sent_at TIMESTAMP NULL COMMENT 'Waktu token dikirim ke email',
    status ENUM('registered', 'attended', 'absent') DEFAULT 'registered' COMMENT 'Status kehadiran',
    attendance_at TIMESTAMP NULL COMMENT 'Waktu mengisi daftar hadir',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_event_user (event_id, user_id) COMMENT 'Satu user hanya bisa daftar sekali per event',
    INDEX idx_event_id (event_id),
    INDEX idx_user_id (user_id),
    INDEX idx_token (token),
    INDEX idx_status (status),
    INDEX idx_attendance_at (attendance_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: sessions (untuk session timeout 5 menit)
CREATE TABLE sessions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT 'ID user yang login',
    token VARCHAR(255) NOT NULL UNIQUE COMMENT 'Session token',
    last_activity TIMESTAMP NOT NULL COMMENT 'Waktu aktivitas terakhir',
    expired_at TIMESTAMP NOT NULL COMMENT 'Waktu session expired (last_activity + 5 menit)',
    ip_address VARCHAR(45) NULL COMMENT 'IP address user',
    user_agent VARCHAR(500) NULL COMMENT 'User agent browser',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_token (token),
    INDEX idx_expired_at (expired_at),
    INDEX idx_last_activity (last_activity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: certificates (sertifikat peserta)
CREATE TABLE certificates (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    event_registration_id BIGINT NOT NULL COMMENT 'ID pendaftaran yang terkait',
    event_id BIGINT NOT NULL COMMENT 'ID kegiatan',
    user_id BIGINT NOT NULL COMMENT 'ID peserta',
    certificate_path VARCHAR(500) NOT NULL COMMENT 'Path file sertifikat yang sudah di-generate',
    certificate_number VARCHAR(100) NULL COMMENT 'Nomor sertifikat',
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Waktu sertifikat di-generate',
    downloaded_at TIMESTAMP NULL COMMENT 'Waktu terakhir sertifikat di-download',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (event_registration_id) REFERENCES event_registrations(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_registration_certificate (event_registration_id) COMMENT 'Satu pendaftaran = satu sertifikat',
    INDEX idx_event_id (event_id),
    INDEX idx_user_id (user_id),
    INDEX idx_certificate_number (certificate_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: activity_logs (opsional: log aktivitas)
CREATE TABLE activity_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NULL COMMENT 'ID user yang melakukan aktivitas',
    action VARCHAR(100) NOT NULL COMMENT 'Aksi yang dilakukan',
    description TEXT NULL COMMENT 'Deskripsi detail',
    ip_address VARCHAR(45) NULL,
    user_agent VARCHAR(500) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TRIGGER: Auto set registration_closed_at
-- ============================================
DELIMITER $$
CREATE TRIGGER set_registration_closed_at
BEFORE INSERT ON events
FOR EACH ROW
BEGIN
    -- Set registration_closed_at = event_date + event_time
    SET NEW.registration_closed_at = CONCAT(NEW.event_date, ' ', NEW.event_time);
END$$
DELIMITER ;

-- ============================================
-- VIEW: Event Statistics for Admin
-- ============================================
CREATE VIEW v_events_stats_admin AS
SELECT 
    MONTH(e.created_at) as bulan,
    COUNT(DISTINCT e.id) as jumlah_kegiatan,
    COUNT(DISTINCT er.id) as jumlah_peserta_total,
    COUNT(DISTINCT CASE WHEN er.status = 'attended' THEN er.id END) as jumlah_peserta_hadir
FROM events e
LEFT JOIN event_registrations er ON e.id = er.event_id
WHERE YEAR(e.created_at) = YEAR(NOW())
GROUP BY MONTH(e.created_at);

-- ============================================
-- VIEW: Event Statistics for Event Organizer
-- ============================================
CREATE VIEW v_events_stats_organizer AS
SELECT 
    e.user_id,
    MONTH(e.created_at) as bulan,
    COUNT(DISTINCT e.id) as jumlah_kegiatan,
    COUNT(DISTINCT er.id) as jumlah_peserta_total,
    COUNT(DISTINCT CASE WHEN er.status = 'attended' THEN er.id END) as jumlah_peserta_hadir
FROM events e
LEFT JOIN event_registrations er ON e.id = er.event_id
WHERE YEAR(e.created_at) = YEAR(NOW())
GROUP BY e.user_id, MONTH(e.created_at);

-- ============================================
-- STORED PROCEDURE: Get Top 10 Events by Participants
-- ============================================
DELIMITER $$
CREATE PROCEDURE sp_get_top_10_events_by_participants(
    IN p_user_id BIGINT,
    IN p_role VARCHAR(20)
)
BEGIN
    IF p_role = 'admin' THEN
        -- Admin: semua event
        SELECT 
            e.id,
            e.title,
            e.event_date,
            e.location,
            COUNT(DISTINCT er.id) as jumlah_peserta
        FROM events e
        LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'attended'
        WHERE e.deleted_at IS NULL
        GROUP BY e.id
        ORDER BY jumlah_peserta DESC
        LIMIT 10;
    ELSE
        -- Event Organizer: hanya event sendiri
        SELECT 
            e.id,
            e.title,
            e.event_date,
            e.location,
            COUNT(DISTINCT er.id) as jumlah_peserta
        FROM events e
        LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'attended'
        WHERE e.user_id = p_user_id AND e.deleted_at IS NULL
        GROUP BY e.id
        ORDER BY jumlah_peserta DESC
        LIMIT 10;
    END IF;
END$$
DELIMITER ;

-- ============================================
-- SEED DATA: Admin Default
-- ============================================
-- Password: Admin123# (harus di-hash dengan bcrypt)
-- Untuk development, gunakan hash: $2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi
INSERT INTO users (name, email, phone, address, education, password, role, email_verified_at) 
VALUES ('Administrator', 'admin@example.com', '081234567890', 'Alamat Admin', 'S1', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin', NOW());

-- ============================================
-- INDEXES untuk performa query
-- ============================================

-- Index untuk pencarian event berdasarkan keyword
ALTER TABLE events ADD FULLTEXT INDEX ft_title_description (title, description);

-- Index untuk filter event berdasarkan tanggal (katalog urut terdekat)
CREATE INDEX idx_event_date_time_status ON events(event_date, event_time, status);

