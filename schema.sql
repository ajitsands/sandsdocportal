-- =========================================================================
-- SaNDS Lab & Popular Auto Spare ERP Document Portal
-- Enterprise MySQL Database Schema (MySQL 8.0+ / MariaDB 10.4+)
-- Import directly into your database (e.g. sandsl23_docs_db)
-- =========================================================================

-- 1. Authorized Stakeholders Registry
CREATE TABLE IF NOT EXISTS `authorized_users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `email` VARCHAR(191) NOT NULL UNIQUE,
  `full_name` VARCHAR(255) NOT NULL,
  `organization` VARCHAR(255) NOT NULL,
  `role` VARCHAR(100) NOT NULL,
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_user_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Authenticated Remembered Devices (256-bit Token Engine)
CREATE TABLE IF NOT EXISTS `authenticated_devices` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `email` VARCHAR(191) NOT NULL,
  `device_token` VARCHAR(255) NOT NULL UNIQUE,
  `device_name` VARCHAR(255),
  `ip_address` VARCHAR(64),
  `location` VARCHAR(255),
  `verified_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `last_active` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_dev_email` (`email`),
  INDEX `idx_dev_token` (`device_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Document Lifecycle & Lock States
CREATE TABLE IF NOT EXISTS `document_meta` (
  `doc_id` VARCHAR(100) PRIMARY KEY,
  `title` VARCHAR(255) NOT NULL,
  `status` VARCHAR(50) DEFAULT 'IN_REVIEW',
  `finalized_by` VARCHAR(191),
  `finalized_at` DATETIME,
  `finalized_notes` TEXT,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Digital Signatures & Disagreements (Isolated Strictly Per doc_id and email)
CREATE TABLE IF NOT EXISTS `document_signatures` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `doc_id` VARCHAR(100) NOT NULL,
  `email` VARCHAR(191) NOT NULL,
  `full_name` VARCHAR(255),
  `organization` VARCHAR(255),
  `role` VARCHAR(100),
  `status` VARCHAR(50) DEFAULT 'SIGNED', -- 'SIGNED' or 'DISAGREED'
  `signature_data` MEDIUMTEXT,
  `disagree_reason` TEXT,
  `ip_address` VARCHAR(64),
  `device_name` VARCHAR(255),
  `signed_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `uq_doc_user` (`doc_id`, `email`),
  INDEX `idx_sig_doc` (`doc_id`),
  INDEX `idx_sig_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Comprehensive Access Audit Logs
CREATE TABLE IF NOT EXISTS `document_access_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `email` VARCHAR(191),
  `doc_id` VARCHAR(100),
  `doc_title` VARCHAR(255),
  `action_type` VARCHAR(100),
  `ip_address` VARCHAR(64),
  `device_name` VARCHAR(255),
  `user_agent` TEXT,
  `location` VARCHAR(255),
  `accessed_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_log_email` (`email`),
  INDEX `idx_log_doc` (`doc_id`),
  INDEX `idx_log_time` (`accessed_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. OTP Verification Logs
CREATE TABLE IF NOT EXISTS `otp_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `email` VARCHAR(191) NOT NULL,
  `otp_code` VARCHAR(10) NOT NULL,
  `ip_address` VARCHAR(64),
  `location` VARCHAR(255),
  `dispatched_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_otp_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Geolocation Fast Cache
CREATE TABLE IF NOT EXISTS `ip_cache` (
  `ip` VARCHAR(64) PRIMARY KEY,
  `location` VARCHAR(255),
  `cached_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Initial Seed Data: Authorized Stakeholders
INSERT INTO `authorized_users` (`email`, `full_name`, `organization`, `role`, `is_active`) VALUES
('ajit@sandslab.com', 'Ajit Kumar KV', 'SaNDS Lab Middle East W.L.L', 'Super Admin', 1),
('projects@sandslab.com', 'SaNDS Lab Administration', 'SaNDS Lab Middle East W.L.L', 'Admin', 1),
('director@popularbahrain.com', 'Managing Director', 'Popular Auto Spare & A/C Parts Co. W.L.L', 'Client Director', 1),
('popularpartsbh@gmail.com', 'Executive Team', 'Popular Auto Spare & A/C Parts Co. W.L.L', 'Client', 1),
('cto@popularbahrain.com', 'Chief Technology Officer', 'Popular Auto Spare & A/C Parts Co. W.L.L', 'Client CTO', 1),
('consultant@uniglobal.com', 'Lead IT Consultant', 'UniGlobal Consultancy', 'Consultant', 1),
('uniglobalconsult@gmail.com', 'IT Architecture Team', 'UniGlobal Consultancy', 'Consultant', 1)
ON DUPLICATE KEY UPDATE `full_name`=VALUES(`full_name`);

-- Initial Seed Data: Document Metadata
INSERT INTO `document_meta` (`doc_id`, `title`, `status`) VALUES
('SL-POP-ERP-MS-001', 'Module 1: PCode Generation & Item Master Milestone & Payment Structure', 'IN_REVIEW'),
('SL-POP-ERP-MS-002', 'Module 2: Centralized Vendor & Purchase Process Flow Milestone & Payment Structure', 'IN_REVIEW'),
('SL-POP-ERP-MS-003', 'Module 3: Store Verification, Stock Control & Location Management Milestone & Payment Structure', 'IN_REVIEW'),
('SL-POP-ERP-ARCH-001', 'ERP Technical Architecture & Cybersecurity Specification', 'IN_REVIEW')
ON DUPLICATE KEY UPDATE `title`=VALUES(`title`);
