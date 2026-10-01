import os, re, subprocess, shutil

summary_builder = 'build_master_summary.py'
with open(summary_builder, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add CSS rules with double braces for f-string
old_css_snippet = """.currency-bhd {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--primary);
    }}"""

new_css_snippet = """.currency-bhd {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--primary);
      white-space: nowrap;
    }}

    .mod-doc-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: #0a2540;
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      white-space: nowrap;
      letter-spacing: 0.3px;
      box-shadow: 0 1px 2px rgba(10,37,64,0.15);
    }}

    .mod-ba-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: #f1f5f9;
      color: #475569;
      font-size: 10.5px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
      white-space: nowrap;
    }}

    .mod-domain-title {{
      font-size: 13.5px;
      font-weight: 700;
      color: #0a2540;
      line-height: 1.35;
      margin-top: 2px;
    }}

    .gate-pill {{
      display: inline-block;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 11.5px;
      font-weight: 600;
      color: #334155;
      white-space: nowrap;
    }}

    .share-badge {{
      display: inline-block;
      background: #eff6ff;
      color: #1d4ed8;
      font-weight: 700;
      font-size: 11.5px;
      padding: 2px 8px;
      border-radius: 12px;
      border: 1px solid #dbeafe;
      white-space: nowrap;
    }}"""

if old_css_snippet in code:
    code = code.replace(old_css_snippet, new_css_snippet)
    print("Inserted CSS rules with double braces.")

# Also ensure html_content starts with <!DOCTYPE html> and does not contain raw PHP code
old_header_php = """html_content = f\"\"\"<?php
// PHP Backend for Digital Signature & Finalization API (SL-POP-ERP-SUMMARY-001)
if (session_status() === PHP_SESSION_NONE) {
    $session_save_dir = __DIR__ . '/.sessions';
    if (!is_dir($session_save_dir)) {
        @mkdir($session_save_dir, 0700, true);
    }
    if (is_dir($session_save_dir) && is_writable($session_save_dir)) {
        @session_save_path($session_save_dir);
    } elseif (is_dir(sys_get_temp_dir()) && is_writable(sys_get_temp_dir())) {
        @session_save_path(sys_get_temp_dir());
    }
    @session_start();
}

$doc_id = 'SL-POP-ERP-SUMMARY-001';

$db_candidates = array(__DIR__ . '/db.php', dirname(__DIR__) . '/db.php');
foreach ($db_candidates as $dbc) {
    if (file_exists($dbc)) {
        require_once $dbc;
        break;
    }
}

$is_locked = false;
if (isset($pdo) && $pdo) {
    try {
        $meta_stmt = $pdo->prepare("SELECT status FROM document_meta WHERE doc_id = ?");
        $meta_stmt->execute(array($doc_id));
        $status_val = $meta_stmt->fetchColumn();
        if ($status_val === 'FINALIZED_AND_LOCKED') {
            $is_locked = true;
        }
    } catch (Exception $e) {}
}

$authenticated_user = isset($_SESSION['authenticated_user']) ? $_SESSION['authenticated_user'] : (isset($_COOKIE['sands_auth_device']) ? $_COOKIE['sands_auth_device'] : '');

// Handle Ajax Actions
if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    header('Content-Type: application/json');
    $action = $_POST['action'];
    
    if (!$authenticated_user) {
        echo json_encode(array('success' => false, 'message' => 'Unauthorized access. Please log in via the portal.'));
        exit;
    }
    
    if ($action === 'sign_milestone') {
        $signer_name = isset($_POST['signer_name']) ? trim($_POST['signer_name']) : '';
        $signer_role = isset($_POST['signer_role']) ? trim($_POST['signer_role']) : '';
        $signature_data = isset($_POST['signature_data']) ? trim($_POST['signature_data']) : '';
        
        if (empty($signer_name) || empty($signature_data)) {
            echo json_encode(array('success' => false, 'message' => 'Signer Name and Signature are mandatory.'));
            exit;
        }
        
        if ($pdo) {
            try {
                $check = $pdo->prepare("SELECT id FROM document_signatures WHERE doc_id = ? AND LOWER(email) = LOWER(?)");
                $check->execute(array($doc_id, $authenticated_user));
                $exist_id = $check->fetchColumn();
                $now_str = date('Y-m-d H:i:s');
                $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '127.0.0.1';
                $ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
                
                if ($exist_id) {
                    $up = $pdo->prepare("UPDATE document_signatures SET full_name = ?, role = ?, status = 'SIGNED', signature_data = ?, ip_address = ?, device_name = ?, signed_at = ? WHERE id = ?");
                    $up->execute(array($signer_name, $signer_role, $signature_data, $ip, $ua, $now_str, $exist_id));
                } else {
                    $ins = $pdo->prepare("INSERT INTO document_signatures (doc_id, email, full_name, organization, role, status, signature_data, ip_address, device_name, signed_at) VALUES (?, ?, ?, ?, ?, 'SIGNED', ?, ?, ?, ?)");
                    $ins->execute(array($doc_id, $authenticated_user, $signer_name, 'Executive Stakeholder', $signer_role, $signature_data, $ip, $ua, $now_str));
                }
                echo json_encode(array('success' => true, 'message' => 'Milestone Signature Recorded Successfully!'));
                exit;
            } catch (Exception $e) {
                echo json_encode(array('success' => false, 'message' => 'Database Error: ' . $e->getMessage()));
                exit;
            }
        }
        echo json_encode(array('success' => false, 'message' => 'Database connection failed.'));
        exit;
    }
}
?>
<!DOCTYPE html>"""

new_header_html = """html_content = f\"\"\"<!DOCTYPE html>"""

if old_header_php in code:
    code = code.replace(old_header_php, new_header_html)
    print("Replaced PHP header with pure HTML.")

# Update rendered_html generation without php -f
code = code.replace(
    "subprocess.run(['php', '-f', html_path_1], stdout=rf, check=True, cwd=BASE_DIR)",
    "rf.write(html_content)"
)

with open(summary_builder, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved build_master_summary.py successfully.")
