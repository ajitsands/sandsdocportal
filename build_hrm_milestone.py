import os
import shutil
import base64
import subprocess
import fitz
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_b64(rel_path):
    full_path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')
    return ''

logo_sands_white = get_b64('logos/SaNDSLab-LogoNewUpdatedWhite.png')
logo_uniglobal_white = get_b64('logos/UniGlobalWhite.png')
logo_popular = get_b64('logos/logoPopular.png')

html_content = f"""<?php
// PHP Backend for Digital Signature & Finalization API (SL-POP-ERP-MS-007)
if (session_status() === PHP_SESSION_NONE) {{
    $session_save_dir = __DIR__ . '/.sessions';
    if (!is_dir($session_save_dir)) {{
        @mkdir($session_save_dir, 0700, true);
    }}
    if (is_dir($session_save_dir) && is_writable($session_save_dir)) {{
        @session_save_path($session_save_dir);
    }} elseif (is_dir(sys_get_temp_dir()) && is_writable(sys_get_temp_dir())) {{
        @session_save_path(sys_get_temp_dir());
    }}
    @session_start();
}}

$doc_id = 'SL-POP-ERP-MS-007';

$db_candidates = array(__DIR__ . '/db.php', dirname(__DIR__) . '/db.php');
foreach ($db_candidates as $dbc) {{
    if (file_exists($dbc)) {{
        require_once $dbc;
        break;
    }}
}}

$is_locked = false;
if (isset($pdo) && $pdo) {{
    try {{
        $meta_stmt = $pdo->prepare("SELECT status FROM document_meta WHERE doc_id = ?");
        $meta_stmt->execute(array($doc_id));
        $status_val = $meta_stmt->fetchColumn();
        if ($status_val === 'FINALIZED_AND_LOCKED') {{
            $is_locked = true;
        }}
    }} catch (Exception $e) {{}}
}}

$authenticated_user = isset($_SESSION['authenticated_user']) ? $_SESSION['authenticated_user'] : (isset($_COOKIE['sands_auth_device']) ? $_COOKIE['sands_auth_device'] : '');

// Handle Ajax Actions
if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {{
    header('Content-Type: application/json');
    $action = $_POST['action'];
    
    if (!$authenticated_user) {{
        echo json_encode(array('success' => false, 'message' => 'Unauthorized access. Please log in via the portal.'));
        exit;
    }}
    
    if ($action === 'sign_milestone') {{
        $role = isset($_POST['role']) ? trim($_POST['role']) : '';
        $signer_name = isset($_POST['signer_name']) ? trim($_POST['signer_name']) : '';
        $signer_designation = isset($_POST['signer_designation']) ? trim($_POST['signer_designation']) : '';
        $signature_data = isset($_POST['signature_data']) ? trim($_POST['signature_data']) : '';
        
        if (empty($role) || empty($signer_name) || empty($signature_data)) {{
            echo json_encode(array('success' => false, 'message' => 'Missing required signature fields.'));
            exit;
        }}
        
        try {{
            $now = date('Y-m-d H:i:s');
            
            // Check if document record exists in document_meta
            $check_stmt = $pdo->prepare("SELECT COUNT(*) FROM document_meta WHERE doc_id = ?");
            $check_stmt->execute(array($doc_id));
            if ($check_stmt->fetchColumn() == 0) {{
                $ins_stmt = $pdo->prepare("INSERT INTO document_meta (doc_id, title, status) VALUES (?, ?, 'IN_REVIEW')");
                $ins_stmt->execute(array($doc_id, 'Module 7: Human Resource Management, Biometric Attendance, Bahrain Labour Law Leave, Automated Payroll & Gratuity Milestone'));
            }}
            
            if ($db_driver_active === 'mysql') {{
                $sig_stmt = $pdo->prepare("INSERT INTO document_signatures (doc_id, role, signer_name, signer_designation, signer_email, signature_data, signed_at) 
                                           VALUES (?, ?, ?, ?, ?, ?, ?)
                                           ON DUPLICATE KEY UPDATE signer_name = VALUES(signer_name), signer_designation = VALUES(signer_designation), signature_data = VALUES(signature_data), signed_at = VALUES(signed_at)");
                $sig_stmt->execute(array($doc_id, $role, $signer_name, $signer_designation, $authenticated_user, $signature_data, $now));
            }} else {{
                $del = $pdo->prepare("DELETE FROM document_signatures WHERE doc_id = ? AND role = ?");
                $del->execute(array($doc_id, $role));
                $ins = $pdo->prepare("INSERT INTO document_signatures (doc_id, role, signer_name, signer_designation, signer_email, signature_data, signed_at) VALUES (?, ?, ?, ?, ?, ?, ?)");
                $ins->execute(array($doc_id, $role, $signer_name, $signer_designation, $authenticated_user, $signature_data, $now));
            }}
            
            // Log to audit trail
            $audit_stmt = $pdo->prepare("INSERT INTO audit_trail (user_email, action, details, ip_address) VALUES (?, ?, ?, ?)");
            $audit_stmt->execute(array($authenticated_user, 'SIGN_DOCUMENT', "Signed $doc_id as $role ($signer_name)", $_SERVER['REMOTE_ADDR']));
            
            echo json_encode(array('success' => true, 'message' => 'Signature recorded successfully!', 'signed_at' => $now));
            exit;
        }} catch (Exception $e) {{
            echo json_encode(array('success' => false, 'message' => 'Database error: ' . $e->getMessage()));
            exit;
        }}
    }}
    
    if ($action === 'get_signatures') {{
        try {{
            $stmt = $pdo->prepare("SELECT role, signer_name, signer_designation, signer_email, signature_data, signed_at FROM document_signatures WHERE doc_id = ?");
            $stmt->execute(array($doc_id));
            $signatures = $stmt->fetchAll(PDO::FETCH_ASSOC);
            echo json_encode(array('success' => true, 'signatures' => $signatures));
            exit;
        }} catch (Exception $e) {{
            echo json_encode(array('success' => false, 'message' => $e->getMessage()));
            exit;
        }}
    }}
}}

// Load initial signatures for server-side render
$loaded_signatures = array();
if (isset($pdo) && $pdo) {{
    try {{
        $stmt = $pdo->prepare("SELECT role, signer_name, signer_designation, signer_email, signature_data, signed_at FROM document_signatures WHERE doc_id = ?");
        $stmt->execute(array($doc_id));
        $loaded_signatures = $stmt->fetchAll(PDO::FETCH_ASSOC);
    }} catch (Exception $e) {{}}
}}

$sands_sig = null;
$uniglobal_sig = null;
$popular_sig = null;
foreach ($loaded_signatures as $s) {{
    if ($s['role'] === 'sands') $sands_sig = $s;
    if ($s['role'] === 'uniglobal') $uniglobal_sig = $s;
    if ($s['role'] === 'popular') $popular_sig = $s;
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SL-POP-ERP-MS-007: Human Resource Management, Biometric Attendance, Payroll & Gratuity Milestone Agreement</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  <style>
    :root {{
      --primary: #0a2540;
      --primary-dark: #07192c;
      --accent: #e67e22;
      --accent-dark: #d35400;
      --secondary: #0e7490;
      --hr-theme: #059669;
      --hr-dark: #047857;
      --dark: #0f172a;
      --gray-900: #0f172a;
      --gray-800: #1e293b;
      --gray-700: #334155;
      --gray-600: #475569;
      --gray-500: #64748b;
      --gray-400: #94a3b8;
      --gray-300: #cbd5e1;
      --gray-200: #e2e8f0;
      --gray-100: #f1f5f9;
      --gray-50: #f8fafc;
      --white: #ffffff;
      --success: #15803d;
      --success-bg: #dcfce7;
      --danger: #be123c;
      --danger-bg: #ffe4e6;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: #f1f5f9;
      color: var(--gray-800);
      line-height: 1.6;
      font-size: 13.5px;
    }}

    /* WEB ACTION BAR */
    .web-action-bar {{
      background: #07192c;
      color: #ffffff;
      padding: 12px 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 1000;
      border-bottom: 2px solid var(--accent);
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .web-action-left {{
      display: flex;
      align-items: center;
      gap: 15px;
    }}
    .portal-back-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #ffffff !important;
      color: #0a2540 !important;
      border: 1px solid #cbd5e1 !important;
      padding: 7px 16px;
      border-radius: 6px;
      font-size: 12.5px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s ease;
      box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }}
    .portal-back-btn:hover {{
      background: #f8fafc !important;
      color: var(--accent-dark) !important;
      border-color: var(--accent) !important;
      transform: translateY(-1px);
    }}
    .web-action-right {{
      display: flex;
      gap: 10px;
    }}
    .btn-action {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-action-primary {{
      background: var(--accent);
      color: #ffffff;
      border: none;
    }}
    .btn-action-primary:hover {{
      background: var(--accent-dark);
    }}
    .btn-action-secondary {{
      background: #ffffff !important;
      color: #0a2540 !important;
      border: 1px solid #cbd5e1 !important;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    .btn-action-secondary:hover {{
      background: #f8fafc !important;
      color: var(--accent-dark) !important;
      border-color: var(--accent) !important;
    }}

    /* DOCUMENT CONTAINER */
    .doc-page {{
      background: #ffffff;
      width: 100%;
      max-width: 960px;
      margin: 25px auto 40px;
      padding: 45px 55px;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.06);
      border: 1px solid var(--gray-200);
    }}

    /* DOCUMENT HEADER */
    .doc-header {{
      border-bottom: 3px double var(--gray-200);
      padding-bottom: 25px;
      margin-bottom: 30px;
    }}
    .header-logo-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .logo-box-sands {{
      height: 48px;
    }}
    .logo-box-popular {{
      height: 48px;
    }}
    .doc-title-area {{
      text-align: center;
      margin-top: 10px;
    }}
    .doc-badge-pill {{
      display: inline-block;
      background: #ecfdf5;
      color: var(--hr-dark);
      border: 1px solid #a7f3d0;
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 10px;
    }}
    .doc-main-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 24px;
      font-weight: 800;
      color: var(--primary);
      line-height: 1.3;
      margin-bottom: 6px;
    }}
    .doc-sub-title {{
      font-size: 13.5px;
      color: var(--gray-600);
      max-width: 760px;
      margin: 0 auto;
    }}

    /* META INFO GRID */
    .meta-card-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 30px;
    }}
    .meta-box-label {{
      font-size: 10.5px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--gray-500);
      letter-spacing: 0.5px;
      margin-bottom: 3px;
    }}
    .meta-box-val {{
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
    }}

    /* SECTION TITLES */
    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 800;
      color: var(--primary);
      border-left: 4px solid var(--hr-theme);
      padding-left: 12px;
      margin: 32px 0 16px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .section-desc {{
      font-size: 13.5px;
      color: var(--gray-700);
      margin-bottom: 18px;
      line-height: 1.6;
    }}

    /* 9-MODULE ROADMAP GRID */
    .roadmap-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin: 20px 0 30px;
    }}
    .roadmap-card {{
      background: #ffffff;
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      padding: 14px;
      position: relative;
      transition: all 0.2s ease;
    }}
    .roadmap-card.done {{
      border-color: #bbf7d0;
      background: #f0fdf4;
    }}
    .roadmap-card.active {{
      border-color: var(--hr-theme);
      background: #ecfdf5;
      box-shadow: 0 4px 12px rgba(5, 150, 105, 0.15);
    }}
    .roadmap-card.upcoming {{
      border-style: dashed;
      opacity: 0.8;
    }}
    .roadmap-num {{
      font-size: 10.5px;
      font-weight: 800;
      color: var(--gray-500);
      text-transform: uppercase;
      margin-bottom: 4px;
    }}
    .roadmap-card.done .roadmap-num {{ color: #16a34a; }}
    .roadmap-card.active .roadmap-num {{ color: var(--hr-theme); }}
    .roadmap-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 4px;
    }}
    .roadmap-status {{
      font-size: 11px;
      font-weight: 700;
    }}
    .roadmap-card.done .roadmap-status {{ color: #15803d; }}
    .roadmap-card.active .roadmap-status {{ color: var(--hr-dark); }}
    .roadmap-card.upcoming .roadmap-status {{ color: var(--gray-500); }}

    /* FEATURE PILL GRID */
    .feature-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
      margin-bottom: 25px;
    }}
    .feature-box {{
      background: #ffffff;
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      padding: 16px;
      border-top: 3px solid var(--hr-theme);
    }}
    .feature-box-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .feature-list {{
      list-style: none;
      padding-left: 0;
    }}
    .feature-list li {{
      font-size: 12.5px;
      color: var(--gray-700);
      margin-bottom: 5px;
      position: relative;
      padding-left: 16px;
    }}
    .feature-list li::before {{
      content: "•";
      color: var(--hr-theme);
      font-size: 16px;
      position: absolute;
      left: 0;
      top: -2px;
    }}

    /* TABLES */
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0 24px;
      font-size: 12.5px;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--gray-200);
    }}
    .data-table thead th {{
      background: var(--primary);
      color: #ffffff;
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      text-align: left;
      padding: 11px 14px;
      font-size: 12px;
      letter-spacing: 0.3px;
    }}
    .data-table tbody td {{
      padding: 10px 14px;
      border-bottom: 1px solid var(--gray-200);
      color: var(--gray-800);
      vertical-align: middle;
    }}
    .data-table tbody tr:last-child td {{
      border-bottom: none;
    }}
    .data-table tbody tr:nth-child(even) {{
      background: var(--gray-50);
    }}
    .data-table tfoot td {{
      background: #f8fafc;
      font-weight: 800;
      color: var(--primary);
      padding: 12px 14px;
      border-top: 2px solid var(--gray-300);
    }}
    .text-right {{ text-align: right; }}
    .text-center {{ text-align: center; }}

    /* MILESTONE CARD */
    .milestone-card {{
      background: #ffffff;
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 18px;
      border-left: 5px solid var(--hr-theme);
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}
    .ms-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .ms-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 15px;
      font-weight: 800;
      color: var(--primary);
    }}
    .ms-badge {{
      background: #ecfdf5;
      color: var(--hr-dark);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 11.5px;
      font-weight: 800;
      border: 1px solid #a7f3d0;
    }}
    .ms-details-grid {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 16px;
    }}
    .ms-deliverables-title {{
      font-size: 12px;
      font-weight: 700;
      color: var(--gray-600);
      text-transform: uppercase;
      margin-bottom: 6px;
    }}
    .ms-deliverable-list {{
      list-style: none;
      padding: 0;
    }}
    .ms-deliverable-list li {{
      font-size: 12.5px;
      color: var(--gray-700);
      margin-bottom: 4px;
      padding-left: 14px;
      position: relative;
    }}
    .ms-deliverable-list li::before {{
      content: "✓";
      color: var(--hr-theme);
      font-weight: 800;
      position: absolute;
      left: 0;
    }}
    .ms-cost-box {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: 6px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      text-align: right;
    }}
    .ms-cost-label {{
      font-size: 10.5px;
      color: var(--gray-500);
      text-transform: uppercase;
      font-weight: 700;
    }}
    .ms-cost-val {{
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 800;
      color: var(--hr-dark);
      margin-top: 2px;
    }}

    /* GOVERNANCE CALLOUT */
    .callout-box {{
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: 8px;
      padding: 16px 20px;
      margin: 20px 0;
      display: flex;
      gap: 14px;
      align-items: flex-start;
    }}
    .callout-icon {{
      font-size: 20px;
      line-height: 1;
    }}
    .callout-content {{
      font-size: 12.5px;
      color: #166534;
      line-height: 1.5;
    }}

    /* SIGNATURE BLOCK */
    .sign-section {{
      margin-top: 40px;
      border-top: 2px solid var(--gray-200);
      padding-top: 25px;
    }}
    .sign-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 20px;
    }}
    .sign-box {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 180px;
    }}
    .sign-role {{
      font-size: 11px;
      font-weight: 800;
      color: var(--gray-500);
      text-transform: uppercase;
      margin-bottom: 4px;
    }}
    .sign-name {{
      font-family: 'Outfit', sans-serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
    }}
    .sign-org {{
      font-size: 11px;
      color: var(--gray-600);
      margin-bottom: 12px;
    }}
    .sign-pad-area {{
      background: #ffffff;
      border: 1px dashed var(--gray-300);
      border-radius: 6px;
      height: 70px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      color: var(--gray-400);
      margin-bottom: 8px;
    }}
    .sign-pad-area img {{
      max-height: 60px;
      max-width: 95%;
    }}
    .sign-date {{
      font-size: 10.5px;
      color: var(--gray-500);
    }}

    @media print {{
      .web-action-bar {{ display: none !important; }}
      body {{ background: #ffffff !important; font-size: 11pt !important; }}
      .doc-page {{ box-shadow: none !important; margin: 0 !important; padding: 0 !important; max-width: 100% !important; border: none !important; }}
      .page-break {{ page-break-after: always; }}
    }}
  </style>
</head>
<body>

  <!-- WEB ACTION BAR -->
  <div class="web-action-bar">
    <div class="web-action-left">
      <a href="index.php" class="portal-back-btn">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
        &larr; Back to Portal
      </a>
      <span style="font-size: 13px; font-weight: 600; color: #94a3b8;">Document Reference: <strong style="color:#ffffff;">SL-POP-ERP-MS-007</strong></span>
    </div>
    <div class="web-action-right">
      <button onclick="window.print()" class="btn-action btn-action-secondary">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Print Document
      </button>
      <a href="SL-POP-ERP-MS-007.pdf" target="_blank" class="btn-action btn-action-primary">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
        Download Signed PDF
      </a>
    </div>
  </div>

  <div class="doc-page">

    <!-- DOCUMENT HEADER -->
    <header class="doc-header">
      <div class="header-logo-row">
        <div>
          <img src="{logo_popular}" alt="Popular Auto Spare" class="logo-box-popular" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'160\\' height=\\'40\\'><rect width=\\'160\\' height=\\'40\\' fill=\\'%230a2540\\'/><text x=\\'50%25\\' y=\\'55%25\\' dominant-baseline=\\'middle\\' text-anchor=\\'middle\\' fill=\\'%23ffffff\\' font-family=\\'sans-serif\\' font-weight=\\'bold\\' font-size=\\'14\\'>POPULAR AUTO</text></svg>'">
        </div>
        <div style="text-align:right;">
          <img src="{logo_sands_white}" alt="SaNDS Lab" class="logo-box-sands" style="background:#0a2540; padding:4px 10px; border-radius:6px;" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'140\\' height=\\'40\\'><rect width=\\'140\\' height=\\'40\\' fill=\\'%23e67e22\\'/><text x=\\'50%25\\' y=\\'55%25\\' dominant-baseline=\\'middle\\' text-anchor=\\'middle\\' fill=\\'%23ffffff\\' font-family=\\'sans-serif\\' font-weight=\\'bold\\' font-size=\\'14\\'>SaNDS LAB</text></svg>'">
        </div>
      </div>
      <div class="doc-title-area">
        <div class="doc-badge-pill">Master Dedicated Resource Model • 16 Working Weeks (80 Days)</div>
        <h1 class="doc-main-title">Module 7: Human Resource Management, Biometric Attendance, Bahrain Labour Law Leave, Automated Payroll & Gratuity / EOSB</h1>
        <p class="doc-sub-title">Comprehensive 16-week milestone agreement, dedicated engineering team breakdown, Bahrain regulatory compliance matrix (SIO / GOSI / LMRA / WPS), and payment schedule based on the verified Business Analysis Report DOC-007 v1.0.</p>
      </div>
    </header>

    <!-- META INFO GRID -->
    <div class="meta-card-grid">
      <div>
        <div class="meta-box-label">Document ID</div>
        <div class="meta-box-val">SL-POP-ERP-MS-007</div>
      </div>
      <div>
        <div class="meta-box-label">BA Source Reference</div>
        <div class="meta-box-val">DOC-007 (Ver 1.0) • 80 Pgs</div>
      </div>
      <div>
        <div class="meta-box-label">Timeline / Duration</div>
        <div class="meta-box-val">16 Weeks (4.0 Mo / 80 Days)</div>
      </div>
      <div>
        <div class="meta-box-label">Total Milestone Fee</div>
        <div class="meta-box-val" style="color:var(--hr-dark);">BD 5,454.548</div>
      </div>
    </div>

    <!-- 1.0 EXECUTIVE SUMMARY -->
    <section>
      <h2 class="section-title">1.0 Executive Summary & Master ERP Roadmap</h2>
      <p class="section-desc">
        Human Resource Management (Module 7) serves as the core workforce governance, statutory regulatory compliance, biometric timekeeping, automated payroll, and employee lifecycle engine for <strong>Popular Auto Spare & A/C Parts Co. W.L.L.</strong> Across multi-country supplier interactions, regional distribution hubs, branch showrooms, central warehouses, and service centers, managing over hundreds of multi-national employees with strict adherence to <strong>Bahrain Labour Law (Law No. 36 of 2012)</strong>, <strong>Social Insurance Organization (SIO / GOSI)</strong>, <strong>Labour Market Regulatory Authority (LMRA)</strong>, and <strong>Central Bank of Bahrain (CBB) Wage Protection System (WPS)</strong> is mission-critical.
      </p>

      <div class="roadmap-grid">
        <div class="roadmap-card done">
          <div class="roadmap-num">Module 01 • Completed</div>
          <div class="roadmap-title">PCode & Item Master</div>
          <div class="roadmap-status">Submitted & Signed (10 Wks)</div>
        </div>
        <div class="roadmap-card done">
          <div class="roadmap-num">Module 02 • Completed</div>
          <div class="roadmap-title">Vendor & Procurement</div>
          <div class="roadmap-status">Submitted & Signed (12 Wks)</div>
        </div>
        <div class="roadmap-card done">
          <div class="roadmap-num">Module 03 • Completed</div>
          <div class="roadmap-title">Store & Stock Control</div>
          <div class="roadmap-status">Submitted & Signed (15 Wks)</div>
        </div>
        <div class="roadmap-card done">
          <div class="roadmap-num">Module 04 • Completed</div>
          <div class="roadmap-title">Sales Process & POS</div>
          <div class="roadmap-status">Submitted & Signed (15 Wks)</div>
        </div>
        <div class="roadmap-card done">
          <div class="roadmap-num">Module 05 • Completed</div>
          <div class="roadmap-title">Accounts & Financials</div>
          <div class="roadmap-status">Submitted & Signed (13 Wks)</div>
        </div>
        <div class="roadmap-card done">
          <div class="roadmap-num">Module 06 • Completed</div>
          <div class="roadmap-title">Administration & Assets</div>
          <div class="roadmap-status">Submitted & Signed (12 Wks)</div>
        </div>
        <div class="roadmap-card active">
          <div class="roadmap-num" style="color:var(--hr-dark);">Module 07 • Active Specification</div>
          <div class="roadmap-title" style="color:var(--hr-dark);">HR, Attendance & Payroll</div>
          <div class="roadmap-status" style="color:var(--hr-dark);">Current Milestone (16 Wks)</div>
        </div>
        <div class="roadmap-card upcoming">
          <div class="roadmap-num">Module 08 • Upcoming</div>
          <div class="roadmap-title">Garage & Workshop Service</div>
          <div class="roadmap-status">Scheduled in Pipeline</div>
        </div>
        <div class="roadmap-card upcoming">
          <div class="roadmap-num">Module 09 • Upcoming</div>
          <div class="roadmap-title">Executive BI Analytics</div>
          <div class="roadmap-status">Scheduled in Pipeline</div>
        </div>
      </div>
    </section>

    <!-- 2.0 FUNCTIONAL SCOPE -->
    <section>
      <h2 class="section-title">2.0 Comprehensive Scope Breakdown (BA Ref: DOC-007 v1.0)</h2>
      <p class="section-desc">
        Derived directly from the verified 80-page Business Analysis specification (DOC-007), Module 7 encompasses 17 modular operational pillars engineered for high reliability, zero-trust security, and complete GCC statutory compliance:
      </p>

      <div class="feature-grid">
        <div class="feature-box">
          <div class="feature-box-title">
            <span>🏛️</span> Organization & Employee Master
          </div>
          <ul class="feature-list">
            <li><strong>Multi-Branch Hierarchy:</strong> Corporate HQ, showrooms, central warehouses, workshops, staff accommodations.</li>
            <li><strong>Employee 360° Profile:</strong> Personal info, CPR, passport, LMRA work permits, residency visas, bank details.</li>
            <li><strong>Digital Document Vault:</strong> Expiry date alerts (90/60/30 days) for CPR, passports, driving licenses, certifications.</li>
            <li><strong>Designation & Grade Matrix:</strong> Job descriptions, pay bands, reporting lines, matrix approval structures.</li>
          </ul>
        </div>

        <div class="feature-box">
          <div class="feature-box-title">
            <span>🤝</span> Recruitment & Digital Onboarding
          </div>
          <ul class="feature-list">
            <li><strong>Manpower Requisition:</strong> Department vacancy budget approval, job posting, applicant tracking (ATS).</li>
            <li><strong>Interview Evaluation:</strong> Scoring rubrics, panel feedback, background check tracking, offer letters.</li>
            <li><strong>Digital Onboarding:</strong> 1-Click employee profile creation, IT user provisioning, asset allocation challans.</li>
            <li><strong>Statutory Inductions:</strong> Labour contract signing, company policies, uniform/ID card issuances.</li>
          </ul>
        </div>

        <div class="feature-box">
          <div class="feature-box-title">
            <span>⏰</span> Biometric Attendance & Rosters
          </div>
          <ul class="feature-list">
            <li><strong>Biometric Sync:</strong> Real-time integration with physical fingerprint/facial devices across all branches.</li>
            <li><strong>Mobile Geofence Clock-In:</strong> GPS geofencing for delivery drivers, sales executives, and field staff.</li>
            <li><strong>Shift Roster Engine:</strong> Split shifts, Ramadan hours, rotational weekend shifts, grace periods.</li>
            <li><strong>Overtime & Penalty Logic:</strong> Normal/weekend/holiday OT multipliers, late-in and early-out deductions.</li>
          </ul>
        </div>

        <div class="feature-box">
          <div class="feature-box-title">
            <span>🏖️</span> Bahrain Labour Law Leave System
          </div>
          <ul class="feature-list">
            <li><strong>Statutory Leave Types:</strong> 30-day annual leave, sick leave (15 full / 20 half / 20 unpaid), maternity, hajj.</li>
            <li><strong>Leave Accrual & Balance:</strong> Automated monthly pro-rata accrual engine with carry-forward limits.</li>
            <li><strong>Multi-Tier Approval:</strong> Department head, HR manager, and replacement handover sign-off.</li>
            <li><strong>Leave Encashment:</strong> Automated basic/gross formula encashment tied to payroll & final settlement.</li>
          </ul>
        </div>

        <div class="feature-box">
          <div class="feature-box-title">
            <span>💵</span> Automated Payroll & WPS Banking
          </div>
          <ul class="feature-list">
            <li><strong>Dynamic Salary Structure:</strong> Basic salary, housing, transport, telephone, and performance incentives.</li>
            <li><strong>SIO / GOSI Engine:</strong> Bahraini vs Expatriate social insurance contribution calculations.</li>
            <li><strong>CBB WPS Bank Export:</strong> Automated generation of Central Bank of Bahrain WPS files (.txt / .csv).</li>
            <li><strong>General Ledger Posting:</strong> Automated double-entry salary expense and liability journal vouchers.</li>
          </ul>
        </div>

        <div class="feature-box">
          <div class="feature-box-title">
            <span>💳</span> Employee Loans, Advances & Claims
          </div>
          <ul class="feature-list">
            <li><strong>Salary Advance & Loans:</strong> Emergency assistance, festival loans with automated monthly payroll recovery.</li>
            <li><strong>Expense Reimbursements:</strong> Travel, per diem, medical, official purchase claim approvals.</li>
            <li><strong>Asset Tracking:</strong> Custody of laptops, tools, mobile SIMs, uniforms with return checklists.</li>
            <li><strong>Employee Self-Service (ESS):</strong> Mobile & web portal for payslips, leave requests, and document letters.</li>
          </ul>
        </div>

        <div class="feature-box" style="grid-column: span 2;">
          <div class="feature-box-title">
            <span>🎓</span> Performance, Training & End-of-Service Benefit (EOSB / Gratuity)
          </div>
          <ul class="feature-list" style="display:grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <li><strong>KPI Performance Appraisal:</strong> 360° reviews, scorecards, merit-based increments & promotion tracking.</li>
            <li><strong>Training Lifecycle:</strong> Needs analysis, course catalogs, budget tracking, certification logging.</li>
            <li><strong>Disciplinary & Rewards:</strong> Formal warning letters, incident logging, employee recognition badges.</li>
            <li><strong>Bahrain EOSB Gratuity Engine:</strong> Law No. 36 of 2012 compliant end-of-service calculation, clearance checklist across all departments, and final settlement voucher generation.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- 3.0 DEDICATED RESOURCE MODEL & PRICING -->
    <section>
      <h2 class="section-title">3.0 Dedicated Resource Allocation & Pricing (16 Weeks / 4.0 Months)</h2>
      <p class="section-desc">
        Under the <strong>SaNDS Lab Master Dedicated Engineering Rate Card</strong>, 5 senior specialized engineering personnel are allocated 100% full-time to the delivery of Module 7 over 16 working weeks (4.0 billing months / 80 working days):
      </p>

      <table class="data-table">
        <thead>
          <tr>
            <th>Role / Specialization</th>
            <th class="text-center">Allocation</th>
            <th class="text-right">Monthly Rate (BHD)</th>
            <th class="text-center">Billing Duration</th>
            <th class="text-right">Total Project Fee (BHD)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <strong>Project Manager & Solution Architect</strong><br>
              <span style="font-size:11px; color:var(--gray-500);">Bahrain Labour Law, SIO/LMRA/WPS architecture, security governance & client sprint management</span>
            </td>
            <td class="text-center">100%</td>
            <td class="text-right">BD 545.455</td>
            <td class="text-center">4.0 Months</td>
            <td class="text-right"><strong>BD 2,181.820</strong></td>
          </tr>
          <tr>
            <td>
              <strong>Back-End Lead Engineer (PHP MVC / REST API)</strong><br>
              <span style="font-size:11px; color:var(--gray-500);">Payroll calculation engine, biometric sync listener, CBB WPS file generator, GL double-entry posting</span>
            </td>
            <td class="text-center">100%</td>
            <td class="text-right">BD 227.273</td>
            <td class="text-center">4.0 Months</td>
            <td class="text-right"><strong>BD 909.092</strong></td>
          </tr>
          <tr>
            <td>
              <strong>Front-End Lead Engineer (React / UI / Tokens)</strong><br>
              <span style="font-size:11px; color:var(--gray-500);">HR admin command console, ESS portal, responsive organogram, mobile clock-in interface</span>
            </td>
            <td class="text-center">100%</td>
            <td class="text-right">BD 227.273</td>
            <td class="text-center">4.0 Months</td>
            <td class="text-right"><strong>BD 909.092</strong></td>
          </tr>
          <tr>
            <td>
              <strong>Database & Cloud DevOps Specialist</strong><br>
              <span style="font-size:11px; color:var(--gray-500);">Encrypted document vault, automated daily backups, biometric queue daemon, high-availability schemas</span>
            </td>
            <td class="text-center">100%</td>
            <td class="text-right">BD 204.545</td>
            <td class="text-center">4.0 Months</td>
            <td class="text-right"><strong>BD 818.180</strong></td>
          </tr>
          <tr>
            <td>
              <strong>QA Automation & UAT Test Lead</strong><br>
              <span style="font-size:11px; color:var(--gray-500);">Payroll verification test suites, leave accrual boundary testing, WPS compliance, multi-branch UAT</span>
            </td>
            <td class="text-center">100%</td>
            <td class="text-right">BD 159.091</td>
            <td class="text-center">4.0 Months</td>
            <td class="text-right"><strong>BD 636.364</strong></td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2"><strong>TOTAL DEDICATED TEAM FEE</strong></td>
            <td class="text-right"><strong>BD 1,363.636 / Mo</strong></td>
            <td class="text-center"><strong>16 Working Weeks</strong></td>
            <td class="text-right" style="font-size:14px; color:var(--hr-dark);"><strong>BD 5,454.548</strong></td>
          </tr>
        </tfoot>
      </table>
    </section>

    <!-- 4.0 DETAILED 16-WEEK ROADMAP -->
    <section>
      <h2 class="section-title">4.0 Detailed Milestone Deliverables & Acceptance Criteria</h2>
      <p class="section-desc">
        The project is partitioned into 4 sequential 4-week milestones (25.00% each), ensuring continuous code integration, transparent deliverables, and phased sign-offs:
      </p>

      <!-- MILESTONE 1 -->
      <div class="milestone-card">
        <div class="ms-header">
          <div class="ms-title">Milestone 1: Organization Structure, Employee Master, Recruitment & Onboarding</div>
          <div class="ms-badge">Weeks 01–04 • 25.00%</div>
        </div>
        <div class="ms-details-grid">
          <div>
            <div class="ms-deliverables-title">Deliverables & Technical Outputs</div>
            <ul class="ms-deliverable-list">
              <li>Multi-tier organization tree, branch registry, department structure & designation pay grades.</li>
              <li>Employee Master Profile with CPR, passport, visa/LMRA, driving licenses, bank details & digital doc vault.</li>
              <li>Proactive 90/60/30-day document expiration notification engine via email and dashboard alerts.</li>
              <li>Manpower requisition workflow, vacancy tracking, resume parsing & interview scorecards.</li>
              <li>Digital onboarding pipeline with user role-based access control (RBAC) & asset handover challans.</li>
            </ul>
          </div>
          <div class="ms-cost-box">
            <div class="ms-cost-label">Milestone Value</div>
            <div class="ms-cost-val">BD 1,363.637</div>
            <span style="font-size:11px; color:var(--gray-500); margin-top:4px;">Target: End of Week 04</span>
          </div>
        </div>
      </div>

      <!-- MILESTONE 2 -->
      <div class="milestone-card">
        <div class="ms-header">
          <div class="ms-title">Milestone 2: Biometric Attendance, Shift Rostering & Statutory Leave Engine</div>
          <div class="ms-badge">Weeks 05–08 • 25.00%</div>
        </div>
        <div class="ms-details-grid">
          <div>
            <div class="ms-deliverables-title">Deliverables & Technical Outputs</div>
            <ul class="ms-deliverable-list">
              <li>Hardware biometric device listeners & mobile GPS geofenced clock-in integration.</li>
              <li>Flexible multi-shift schedules, Ramadan rosters, split shifts, grace period & late-in penalty logic.</li>
              <li>Overtime computation engine (normal days, weekends, official Bahrain public holidays).</li>
              <li>Bahrain Labour Law No. 36 statutory leave engine (annual, sick, maternity, hajj, bereavement).</li>
              <li>Automated monthly leave accrual calculator, carry-forward limits & multi-tier approval hierarchy.</li>
            </ul>
          </div>
          <div class="ms-cost-box">
            <div class="ms-cost-label">Milestone Value</div>
            <div class="ms-cost-val">BD 1,363.637</div>
            <span style="font-size:11px; color:var(--gray-500); margin-top:4px;">Target: End of Week 08</span>
          </div>
        </div>
      </div>

      <!-- MILESTONE 3 -->
      <div class="milestone-card">
        <div class="ms-header">
          <div class="ms-title">Milestone 3: Automated Payroll, SIO/LMRA Compliance, WPS Export & Loans</div>
          <div class="ms-badge">Weeks 09–12 • 25.00%</div>
        </div>
        <div class="ms-details-grid">
          <div>
            <div class="ms-deliverables-title">Deliverables & Technical Outputs</div>
            <ul class="ms-deliverable-list">
              <li>Dynamic salary formulation engine integrating biometric attendance, unpaid leaves, and overtime.</li>
              <li>Social Insurance Organization (SIO / GOSI) calculation for Bahraini and non-Bahraini staff.</li>
              <li>Automated Central Bank of Bahrain (CBB) Wage Protection System (WPS) bank transfer file export.</li>
              <li>Automated double-entry General Ledger (GL) payroll expense and salary payable journal posting.</li>
              <li>Employee salary advances, emergency loans & automated monthly amortization payroll deductions.</li>
              <li>Confidential PDF payslip generation with email delivery and ESS portal access.</li>
            </ul>
          </div>
          <div class="ms-cost-box">
            <div class="ms-cost-label">Milestone Value</div>
            <div class="ms-cost-val">BD 1,363.637</div>
            <span style="font-size:11px; color:var(--gray-500); margin-top:4px;">Target: End of Week 12</span>
          </div>
        </div>
      </div>

      <!-- MILESTONE 4 -->
      <div class="milestone-card">
        <div class="ms-header">
          <div class="ms-title">Milestone 4: Performance KPIs, ESS Portal, Gratuity / EOSB & Go-Live</div>
          <div class="ms-badge">Weeks 13–16 • 25.00%</div>
        </div>
        <div class="ms-details-grid">
          <div>
            <div class="ms-deliverables-title">Deliverables & Technical Outputs</div>
            <ul class="ms-deliverable-list">
              <li>Performance KPI scorecards, 360-degree appraisal cycles, and salary increment linkages.</li>
              <li>Training needs analysis, course catalog, training budget tracking, and certifications.</li>
              <li>Employee Self-Service (ESS) web and mobile portal for leaves, loans, claims, and certificate requests.</li>
              <li>Bahrain Labour Law End-of-Service Benefit (EOSB / Gratuity) calculation engine.</li>
              <li>Department clearance workflow, asset surrender verification, and final settlement voucher generation.</li>
              <li>Comprehensive multi-branch UAT sign-off, historical employee data migration, and production deployment.</li>
            </ul>
          </div>
          <div class="ms-cost-box">
            <div class="ms-cost-label">Milestone Value</div>
            <div class="ms-cost-val">BD 1,363.637</div>
            <span style="font-size:11px; color:var(--gray-500); margin-top:4px;">Target: End of Week 16</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 5.0 INVOICING & PAYMENT SCHEDULE -->
    <section>
      <h2 class="section-title">5.0 Invoicing & Milestone Payment Schedule</h2>
      <p class="section-desc">
        Payments are billed strictly in 4 equal disbursements of 25.00% upon deliverable completion and UAT sign-off:
      </p>

      <table class="data-table">
        <thead>
          <tr>
            <th>Milestone Tranche</th>
            <th>Billing Trigger & Milestone Scope</th>
            <th class="text-center">Timeline</th>
            <th class="text-center">Fee %</th>
            <th class="text-right">Invoice Amount (BHD)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Milestone 1</strong></td>
            <td>Org Structure, Employee Master, Recruitment & Digital Onboarding</td>
            <td class="text-center">Week 04</td>
            <td class="text-center">25.00%</td>
            <td class="text-right"><strong>BD 1,363.637</strong></td>
          </tr>
          <tr>
            <td><strong>Milestone 2</strong></td>
            <td>Biometric Attendance, Shift Rosters & Statutory Leave System</td>
            <td class="text-center">Week 08</td>
            <td class="text-center">25.00%</td>
            <td class="text-right"><strong>BD 1,363.637</strong></td>
          </tr>
          <tr>
            <td><strong>Milestone 3</strong></td>
            <td>Automated Payroll, SIO/LMRA Compliance, WPS/CBB Export & Loans</td>
            <td class="text-center">Week 12</td>
            <td class="text-center">25.00%</td>
            <td class="text-right"><strong>BD 1,363.637</strong></td>
          </tr>
          <tr>
            <td><strong>Milestone 4</strong></td>
            <td>Performance KPIs, ESS Portal, Gratuity / EOSB & Production Go-Live</td>
            <td class="text-center">Week 16</td>
            <td class="text-center">25.00%</td>
            <td class="text-right"><strong>BD 1,363.637</strong></td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="3"><strong>TOTAL MODULE 7 CONTRACT VALUE</strong></td>
            <td class="text-center"><strong>100.00%</strong></td>
            <td class="text-right" style="font-size:14px; color:var(--hr-dark);"><strong>BD 5,454.548</strong></td>
          </tr>
        </tfoot>
      </table>

      <div class="callout-box">
        <div class="callout-icon">📋</div>
        <div class="callout-content">
          <strong>15-Day Invoicing & UAT Review SLA:</strong> Upon milestone completion, Popular Auto Spare receives 15 working days to conduct user acceptance testing. Invoices are payable within 15 days of sign-off. All engineering deliverables are backed by a 90-day warranty post production go-live.
        </div>
      </div>
    </section>

    <!-- 6.0 STAKEHOLDER SIGN-OFF -->
    <section class="sign-section">
      <h2 class="section-title">6.0 Stakeholder Digital Sign-Off & Execution</h2>
      <p class="section-desc">
        By executing this document, all parties endorse the technical scope, 16-week engineering roadmap, and financial schedule for Module 7 (SL-POP-ERP-MS-007):
      </p>

      <div class="sign-grid">
        <div class="sign-box">
          <div>
            <div class="sign-role">Solution Provider</div>
            <div class="sign-name">SaNDS Lab Middle East W.L.L</div>
            <div class="sign-org">Lead Architect & Project Sponsor</div>
          </div>
          <div class="sign-pad-area">
            <?php if (!empty($sands_sig) && !empty($sands_sig['signature_data'])): ?>
              <img src="<?php echo $sands_sig['signature_data']; ?>" alt="SaNDS Signature">
            <?php else: ?>
              <span style="color:#059669; font-weight:700;">Digitally Signed on Delivery</span>
            <?php endif; ?>
          </div>
          <div class="sign-date">Date: <?php echo !empty($sands_sig['signed_at']) ? $sands_sig['signed_at'] : date('d/m/Y'); ?></div>
        </div>

        <div class="sign-box">
          <div>
            <div class="sign-role">Project Advisory & Quality Assurance</div>
            <div class="sign-name">UniGlobal Business Solutions W.L.L</div>
            <div class="sign-org">Independent ERP Consultant</div>
          </div>
          <div class="sign-pad-area">
            <?php if (!empty($uniglobal_sig) && !empty($uniglobal_sig['signature_data'])): ?>
              <img src="<?php echo $uniglobal_sig['signature_data']; ?>" alt="UniGlobal Signature">
            <?php else: ?>
              <span style="color:#0e7490; font-weight:700;">Digitally Signed on Delivery</span>
            <?php endif; ?>
          </div>
          <div class="sign-date">Date: <?php echo !empty($uniglobal_sig['signed_at']) ? $uniglobal_sig['signed_at'] : date('d/m/Y'); ?></div>
        </div>

        <div class="sign-box">
          <div>
            <div class="sign-role">Client & System Owner</div>
            <div class="sign-name">Popular Auto Spare & A/C Parts Co. W.L.L</div>
            <div class="sign-org">Managing Director & Executive Board</div>
          </div>
          <div class="sign-pad-area">
            <?php if (!empty($popular_sig) && !empty($popular_sig['signature_data'])): ?>
              <img src="<?php echo $popular_sig['signature_data']; ?>" alt="Popular Signature">
            <?php else: ?>
              <span>Awaiting Stakeholder Ink</span>
            <?php endif; ?>
          </div>
          <div class="sign-date">Date: <?php echo !empty($popular_sig['signed_at']) ? $popular_sig['signed_at'] : 'Pending Execution'; ?></div>
        </div>
      </div>
    </section>

  </div>

</body>
</html>
"""

# Write HTML files
with open('SL-POP-ERP-MS-007.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('Human_Resource_Management_Milestone_and_Payment_Structure.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

if os.path.exists('popular'):
    with open('popular/SL-POP-ERP-MS-007.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    with open('popular/Human_Resource_Management_Milestone_and_Payment_Structure.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

print("HTML files created.")

# Convert HTML to PDF using Chrome Headless
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

html_abs = os.path.abspath('SL-POP-ERP-MS-007.html')
pdf_abs = os.path.abspath('SL-POP-ERP-MS-007.pdf')

cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    '--no-pdf-header-footer',
    '--print-to-pdf=' + pdf_abs,
    html_abs
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("PDF conversion exit code:", res.returncode)

if os.path.exists(pdf_abs):
    with open('Human_Resource_Management_Milestone_and_Payment_Structure.pdf', 'wb') as f:
        f.write(open(pdf_abs, 'rb').read())
    if os.path.exists('popular'):
        with open('popular/SL-POP-ERP-MS-007.pdf', 'wb') as f:
            f.write(open(pdf_abs, 'rb').read())
        with open('popular/Human_Resource_Management_Milestone_and_Payment_Structure.pdf', 'wb') as f:
            f.write(open(pdf_abs, 'rb').read())
    print("PDF distributed successfully.")

    doc = fitz.open(pdf_abs)
    print("Generated PDF Page Count:", len(doc))
    doc.close()

# Update document_meta in databases
for db_path in ['.auth_portal.db', 'popular/.auth_portal.db']:
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO document_meta (doc_id, title, status, finalized_at, finalized_by) VALUES (?, ?, ?, ?, ?)",
                    ('SL-POP-ERP-MS-007', 'Module 7: Human Resource Management, Biometric Attendance, Bahrain Labour Law Leave, Automated Payroll & Gratuity Milestone', 'IN_REVIEW', None, None))
        conn.commit()
        conn.close()
        print(f"Updated document_meta in {db_path}")
