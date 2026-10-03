<?php
// =========================================================================
// SaNDS Lab & Popular Auto Spare ERP Document Portal - Database Layer
// Dual-Mode Architecture: High-Performance MySQL (InnoDB) with SQLite Fallback
// =========================================================================

// Load optional config.php
$config_candidates = array(
    __DIR__ . '/config.php',
    dirname(__DIR__) . '/config.php',
    __DIR__ . '/popular/config.php'
);
foreach ($config_candidates as $cfg) {
    if (file_exists($cfg)) {
        require_once $cfg;
        break;
    }
}

// Default constants if not defined
if (!defined('DB_DRIVER')) define('DB_DRIVER', 'auto');
if (!defined('DB_HOST')) define('DB_HOST', '127.0.0.1');
if (!defined('DB_PORT')) define('DB_PORT', '3306');
if (!defined('DB_NAME')) define('DB_NAME', 'popular_erp_portal');
if (!defined('DB_USER')) define('DB_USER', 'root');
if (!defined('DB_PASS')) define('DB_PASS', '');
if (!defined('PORTAL_SECRET_SALT')) define('PORTAL_SECRET_SALT', 'SaNDS_Lab_Secured_Token_Key_2026_ERP_Popular');

global $pdo, $db_driver_active;
$pdo = null;
$db_driver_active = 'none';

// Attempt 1: Connect to MySQL if DB_DRIVER is 'mysql' or 'auto'
if (DB_DRIVER === 'mysql' || DB_DRIVER === 'auto') {
    try {
        $dsn = "mysql:host=" . DB_HOST . ";port=" . DB_PORT . ";dbname=" . DB_NAME . ";charset=utf8mb4";
        $options = array(
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
            PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8mb4"
        );
        $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
        $db_driver_active = 'mysql';
    } catch (Exception $e) {
        if (DB_DRIVER === 'mysql') {
            error_log("MySQL Connection Failed: " . $e->getMessage());
        }
    }
}

// Attempt 2: Fallback to SQLite
if (!$pdo) {
    try {
        // Resolve a single canonical SQLite file path across root and /popular/
        $canonical_dir = (basename(__DIR__) === 'popular') ? dirname(__DIR__) : __DIR__;
        $db_file = $canonical_dir . '/.auth_portal.db';
        
        $pdo = new PDO('sqlite:' . $db_file);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        
        // High-concurrency WAL mode & busy timeout
        $pdo->exec("PRAGMA journal_mode = WAL;");
        $pdo->exec("PRAGMA synchronous = NORMAL;");
        $pdo->exec("PRAGMA busy_timeout = 5000;");
        $db_driver_active = 'sqlite';
    } catch (Exception $e) {
        error_log("SQLite Connection Failed: " . $e->getMessage());
    }
}

// Initialize Schema & Seed Data if connected
if ($pdo) {
    try {
        if ($db_driver_active === 'mysql') {
            $pdo->exec("CREATE TABLE IF NOT EXISTS `authorized_users` (
              `id` INT AUTO_INCREMENT PRIMARY KEY,
              `email` VARCHAR(191) NOT NULL UNIQUE,
              `full_name` VARCHAR(255) NOT NULL,
              `organization` VARCHAR(255) NOT NULL,
              `role` VARCHAR(100) NOT NULL,
              `is_active` TINYINT(1) DEFAULT 1,
              `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
              INDEX `idx_user_email` (`email`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

            $pdo->exec("CREATE TABLE IF NOT EXISTS `authenticated_devices` (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

            $pdo->exec("CREATE TABLE IF NOT EXISTS `document_meta` (
              `doc_id` VARCHAR(100) PRIMARY KEY,
              `title` VARCHAR(255) NOT NULL,
              `status` VARCHAR(50) DEFAULT 'IN_REVIEW',
              `finalized_by` VARCHAR(191),
              `finalized_at` DATETIME,
              `finalized_notes` TEXT,
              `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

            $pdo->exec("CREATE TABLE IF NOT EXISTS `document_signatures` (
              `id` INT AUTO_INCREMENT PRIMARY KEY,
              `doc_id` VARCHAR(100) NOT NULL,
              `email` VARCHAR(191) NOT NULL,
              `full_name` VARCHAR(255),
              `organization` VARCHAR(255),
              `role` VARCHAR(100),
              `status` VARCHAR(50) DEFAULT 'SIGNED',
              `signature_data` MEDIUMTEXT,
              `disagree_reason` TEXT,
              `ip_address` VARCHAR(64),
              `device_name` VARCHAR(255),
              `signed_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
              UNIQUE KEY `uq_doc_user` (`doc_id`, `email`),
              INDEX `idx_sig_doc` (`doc_id`),
              INDEX `idx_sig_email` (`email`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

            $pdo->exec("CREATE TABLE IF NOT EXISTS `document_access_logs` (
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
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

            $pdo->exec("CREATE TABLE IF NOT EXISTS `otp_logs` (
              `id` INT AUTO_INCREMENT PRIMARY KEY,
              `email` VARCHAR(191) NOT NULL,
              `otp_code` VARCHAR(10) NOT NULL,
              `ip_address` VARCHAR(64),
              `location` VARCHAR(255),
              `dispatched_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
              INDEX `idx_otp_email` (`email`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

            $pdo->exec("CREATE TABLE IF NOT EXISTS `ip_cache` (
              `ip` VARCHAR(64) PRIMARY KEY,
              `location` VARCHAR(255),
              `cached_at` DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

        } else {
            // SQLite Tables
            $pdo->exec("CREATE TABLE IF NOT EXISTS authorized_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                organization TEXT NOT NULL,
                role TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT (datetime('now'))
            )");

            $pdo->exec("CREATE TABLE IF NOT EXISTS authenticated_devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                device_token TEXT UNIQUE NOT NULL,
                device_name TEXT,
                ip_address TEXT,
                location TEXT,
                verified_at DATETIME DEFAULT (datetime('now')),
                last_active DATETIME DEFAULT (datetime('now'))
            )");

            $pdo->exec("CREATE TABLE IF NOT EXISTS document_meta (
                doc_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'IN_REVIEW',
                finalized_by TEXT,
                finalized_at DATETIME,
                finalized_notes TEXT
            )");

            $pdo->exec("CREATE TABLE IF NOT EXISTS document_signatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT NOT NULL,
                email TEXT NOT NULL,
                full_name TEXT,
                organization TEXT,
                role TEXT,
                status TEXT DEFAULT 'SIGNED',
                signature_data TEXT,
                disagree_reason TEXT,
                ip_address TEXT,
                device_name TEXT,
                signed_at DATETIME DEFAULT (datetime('now')),
                UNIQUE(doc_id, email)
            )");

            $pdo->exec("CREATE TABLE IF NOT EXISTS document_access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                doc_id TEXT,
                doc_title TEXT,
                action_type TEXT,
                ip_address TEXT,
                device_name TEXT,
                user_agent TEXT,
                location TEXT,
                accessed_at DATETIME DEFAULT (datetime('now'))
            )");

            $pdo->exec("CREATE TABLE IF NOT EXISTS otp_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                otp_code TEXT NOT NULL,
                ip_address TEXT,
                location TEXT,
                dispatched_at DATETIME DEFAULT (datetime('now'))
            )");

            $pdo->exec("CREATE TABLE IF NOT EXISTS ip_cache (
                ip TEXT PRIMARY KEY,
                location TEXT,
                cached_at DATETIME DEFAULT (datetime('now'))
            )");
        }

        // Seed Users
        $cnt = $pdo->query("SELECT COUNT(*) FROM authorized_users")->fetchColumn();
        if ($cnt == 0) {
            $initial_users = array(
                array('ajit@sandslab.com', 'Ajit Kumar KV', 'SaNDS Lab Middle East W.L.L', 'Super Admin', 1),
                array('projects@sandslab.com', 'SaNDS Lab Administration', 'SaNDS Lab Middle East W.L.L', 'Admin', 1),
                array('director@popularbahrain.com', 'Managing Director', 'Popular Auto Spare & A/C Parts Co. W.L.L', 'Client Director', 1),
                array('popularpartsbh@gmail.com', 'Executive Team', 'Popular Auto Spare & A/C Parts Co. W.L.L', 'Client', 1),
                array('cto@popularbahrain.com', 'Chief Technology Officer', 'Popular Auto Spare & A/C Parts Co. W.L.L', 'Client CTO', 1),
                array('consultant@uniglobal.com', 'Lead IT Consultant', 'UniGlobal Consultancy', 'Consultant', 1),
                array('uniglobalconsult@gmail.com', 'IT Architecture Team', 'UniGlobal Consultancy', 'Consultant', 1),
            );
            $stmt = ($db_driver_active === 'mysql') 
                ? $pdo->prepare("INSERT IGNORE INTO authorized_users (email, full_name, organization, role, is_active) VALUES (?, ?, ?, ?, ?)")
                : $pdo->prepare("INSERT OR IGNORE INTO authorized_users (email, full_name, organization, role, is_active) VALUES (?, ?, ?, ?, ?)");
            foreach ($initial_users as $u) {
                $stmt->execute($u);
            }
        }

        // Seed Document Meta
        $mcnt = $pdo->query("SELECT COUNT(*) FROM document_meta")->fetchColumn();
        if ($mcnt == 0) {
            $init_docs = array(
                array('SL-POP-ERP-MS-001', 'Module 1: PCode Generation & Item Master Milestone & Payment Structure', 'IN_REVIEW'),
                array('SL-POP-ERP-ARCH-001', 'ERP Technical Architecture & Cybersecurity Specification', 'IN_REVIEW')
            );
            $mstmt = ($db_driver_active === 'mysql')
                ? $pdo->prepare("INSERT IGNORE INTO document_meta (doc_id, title, status) VALUES (?, ?, ?)")
                : $pdo->prepare("INSERT OR IGNORE INTO document_meta (doc_id, title, status) VALUES (?, ?, ?)");
            foreach ($init_docs as $d) {
                $mstmt->execute($d);
            }
        }

    } catch (Exception $e) {
        error_log("DB Init Error: " . $e->getMessage());
    }
}
