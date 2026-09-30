import os
import shutil
import base64
import subprocess
import fitz
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
// PHP Backend for Digital Signature & Finalization API (SL-POP-ERP-MS-003)
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

$doc_id = 'SL-POP-ERP-MS-003';

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
                $ins_stmt->execute(array($doc_id, 'Module 3: Store Verification & Stock Control Milestone & Payment Structure'));
            }}
            
            // Check if column exists or update document_signatures
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
            echo json_encode(array('success' => false, 'message' => 'Error fetching signatures: ' . $e->getMessage()));
            exit;
        }}
    }}
    
    echo json_encode(array('success' => false, 'message' => 'Unknown action.'));
    exit;
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SL-POP-ERP-MS-003 | Module 3: Store Verification & Stock Control Milestone & Payment Structure</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <style>
    :root {{
      --primary: #0a2540;
      --primary-dark: #07192c;
      --primary-light: #163e67;
      --accent: #d97706;
      --accent-light: #f59e0b;
      --accent-gold: #fbbf24;
      --success: #059669;
      --success-dark: #047857;
      --danger: #dc2626;
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
      --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
      --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
      --shadow-lg: 0 10px 25px -5px rgba(0,0,0,0.1);
      --shadow-xl: 0 20px 35px -10px rgba(0,0,0,0.15);
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --radius-xl: 24px;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #f1f5f9;
      color: var(--gray-800);
      line-height: 1.6;
      font-size: 14px;
      -webkit-font-smoothing: antialiased;
    }}

    .web-action-bar {{
      background: #0f172a;
      color: #ffffff;
      padding: 12px 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .web-action-left {{ display: flex; align-items: center; gap: 15px; }}
    .portal-branding {{
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 14px;
      color: #ffffff;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .web-action-right {{ display: flex; align-items: center; gap: 10px; }}
    .web-action-bar .btn {{
      font-family: 'Inter', sans-serif;
      font-size: 12px;
      font-weight: 600;
      padding: 7px 14px;
      border-radius: 6px;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }}
    .web-action-bar .btn-outline {{
      background: rgba(255, 255, 255, 0.12) !important;
      border: 1px solid rgba(255, 255, 255, 0.45) !important;
      color: #ffffff !important;
    }}
    .web-action-bar .btn-outline:hover {{
      background: rgba(255, 255, 255, 0.25) !important;
      border-color: #ffffff !important;
      color: #ffffff !important;
    }}
    .web-action-bar .btn-accent {{
      background: #d97706 !important;
      border: 1px solid #d97706 !important;
      color: #ffffff !important;
      font-weight: 700 !important;
    }}
    .web-action-bar .btn-accent:hover {{
      background: #b45309 !important;
      border-color: #b45309 !important;
    }}
    .badge-accent {{
      background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; text-transform: uppercase;
    }}
    .badge-success {{
      background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; text-transform: uppercase;
    }}

    .doc-top-bar {{
      background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
      color: var(--white);
      padding: 30px 40px;
      border-bottom: 4px solid var(--accent);
    }}
    .header-content {{
      max-width: 1300px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 20px;
    }}
    .header-logos {{ display: flex; align-items: center; gap: 20px; }}
    .header-logos img {{ height: 48px; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); }}
    .divider-line {{ width: 1px; height: 40px; background: rgba(255, 255, 255, 0.25); }}
    .doc-meta-badge {{
      background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); padding: 8px 16px; border-radius: var(--radius-md); text-align: right;
    }}
    .doc-meta-badge .doc-ref {{
      font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--accent-gold); font-weight: 600; display: block;
    }}
    .doc-meta-badge .doc-date {{ font-size: 11px; color: var(--gray-300); }}

    .main-wrapper {{
      max-width: 1300px; margin: 30px auto 60px auto; padding: 0 20px; display: grid; grid-template-columns: 280px 1fr; gap: 30px;
    }}
    @media (max-width: 1024px) {{
      .main-wrapper {{ grid-template-columns: 1fr; }}
      .sticky-sidebar {{ display: none; }}
    }}

    .sticky-sidebar {{
      position: sticky; top: 20px; height: fit-content; background: var(--white); border-radius: var(--radius-lg); padding: 20px; box-shadow: var(--shadow-md); border: 1px solid var(--gray-200);
    }}
    .sidebar-title {{
      font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 700; color: var(--gray-900); margin-bottom: 14px; text-transform: uppercase; letter-spacing: 0.5px; display: flex; align-items: center; gap: 8px;
    }}
    .sidebar-menu {{ list-style: none; display: flex; flex-direction: column; gap: 6px; }}
    .sidebar-menu li a {{
      display: flex; align-items: center; gap: 10px; padding: 9px 12px; border-radius: var(--radius-sm); color: var(--gray-600); text-decoration: none; font-size: 12.5px; font-weight: 500; transition: all 0.2s ease;
    }}
    .sidebar-menu li a:hover, .sidebar-menu li a.active {{
      background: var(--gray-100); color: var(--primary); font-weight: 700; border-left: 3px solid var(--accent);
    }}

    .content-area {{ display: flex; flex-direction: column; gap: 30px; }}

    .hero-card {{
      background: var(--white); border-radius: var(--radius-xl); padding: 35px 40px; box-shadow: var(--shadow-md); border: 1px solid var(--gray-200); position: relative; overflow: hidden;
    }}
    .hero-card::before {{
      content: ''; position: absolute; top: 0; left: 0; width: 6px; height: 100%; background: linear-gradient(to bottom, var(--primary), var(--accent));
    }}
    .hero-badge-pill {{
      display: inline-flex; align-items: center; gap: 6px; background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 15px;
    }}
    .hero-title {{
      font-family: 'Outfit', sans-serif; font-size: 28px; font-weight: 800; color: var(--dark); line-height: 1.25; margin-bottom: 10px;
    }}
    .hero-subtitle {{
      font-size: 15px; color: var(--gray-600); margin-bottom: 25px; max-width: 950px; line-height: 1.6;
    }}
    .meta-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; padding-top: 20px; border-top: 1px solid var(--gray-200);
    }}
    .meta-box {{
      background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: var(--radius-md); padding: 12px 16px;
    }}
    .meta-label {{ font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--gray-500); font-weight: 600; margin-bottom: 3px; }}
    .meta-val {{ font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 800; color: var(--primary); }}

    .stat-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
    @media (max-width: 900px) {{ .stat-row {{ grid-template-columns: repeat(2, 1fr); }} }}

    .stat-card {{
      background: var(--white); border-radius: var(--radius-lg); padding: 20px; border: 1px solid var(--gray-200); box-shadow: var(--shadow-sm); display: flex; align-items: flex-start; gap: 14px;
    }}
    .stat-icon {{
      width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;
    }}
    .icon-navy {{ background: #e0e7ff; color: #4338ca; }}
    .icon-amber {{ background: #fef3c7; color: #d97706; }}
    .icon-emerald {{ background: #dcfce7; color: #059669; }}
    .icon-blue {{ background: #dbeafe; color: #2563eb; }}
    .stat-info .stat-num {{ font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 800; color: var(--dark); line-height: 1.1; }}
    .stat-info .stat-title {{ font-size: 11px; font-weight: 600; color: var(--gray-500); margin-top: 3px; }}

    .doc-section {{
      background: var(--white); border-radius: var(--radius-xl); padding: 35px; box-shadow: var(--shadow-md); border: 1px solid var(--gray-200); scroll-margin-top: 30px;
    }}
    .section-header {{
      display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid var(--gray-100); position: relative;
    }}
    .section-header::after {{
      content: ''; position: absolute; bottom: -2px; left: 0; width: 60px; height: 2px; background: var(--accent);
    }}
    .section-title-wrap {{ display: flex; flex-direction: column; gap: 4px; }}
    .section-num {{
      font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 1px;
    }}
    .section-title {{ font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 700; color: var(--dark); }}
    .section-desc {{ font-size: 13px; color: var(--gray-600); line-height: 1.6; margin-bottom: 20px; }}

    .features-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin: 20px 0;
    }}
    .feature-card {{
      background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: var(--radius-md); padding: 18px; border-left: 4px solid var(--primary);
    }}
    .feature-card-title {{
      font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 14px; color: var(--dark); margin-bottom: 8px; display: flex; align-items: center; gap: 8px;
    }}
    .feature-card-text {{ font-size: 12.5px; color: var(--gray-700); line-height: 1.5; }}

    .table-container {{
      overflow-x: auto; margin: 15px 0 20px 0; border-radius: var(--radius-md); border: 1px solid var(--gray-200);
    }}
    table.master-table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: left; }}
    table.master-table thead {{ background: var(--primary); color: var(--white); }}
    table.master-table th {{
      padding: 12px 14px; font-weight: 600; font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid var(--accent);
    }}
    table.master-table td {{ padding: 12px 14px; border-bottom: 1px solid var(--gray-200); vertical-align: middle; }}
    table.master-table tbody tr:nth-child(even) {{ background: #f8fafc; }}
    table.master-table tbody tr:hover {{ background: #eff6ff; }}
    table.master-table tfoot {{ background: var(--dark); color: var(--white); font-weight: 700; }}
    table.master-table tfoot td {{ padding: 14px; font-size: 13.5px; border-top: 2px solid var(--accent); }}
    .currency-bhd {{ font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--primary); }}

    .rate-card-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0;
    }}
    .rate-box {{
      background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: var(--radius-md); padding: 16px; text-align: center;
    }}
    .rate-box .role-name {{ font-weight: 700; font-size: 13px; color: var(--dark); margin-bottom: 6px; }}
    .rate-box .bhd-val {{ font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 800; color: var(--primary); }}
    .rate-box .bhd-sub {{ font-size: 11px; color: var(--gray-600); margin-top: 3px; font-family: 'JetBrains Mono', monospace; }}
    .rate-box .alloc-val {{
      display: inline-block; margin-top: 8px; background: #e2e8f0; color: var(--gray-700); font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 4px;
    }}

    .terms-box {{
      background: #f8fafc; border-left: 4px solid var(--accent); padding: 20px; border-radius: var(--radius-md); margin: 15px 0;
    }}
    .terms-box h4 {{ font-family: 'Outfit', sans-serif; color: var(--dark); font-size: 14.5px; margin-bottom: 8px; }}
    .terms-box ul {{ padding-left: 20px; font-size: 12.5px; color: var(--gray-700); line-height: 1.6; }}

    .signoff-section {{
      background: var(--white); border-radius: var(--radius-xl); padding: 35px 40px; border: 1px solid var(--gray-200); box-shadow: var(--shadow-md);
    }}
    .signoff-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin-top: 25px; }}
    @media (max-width: 850px) {{ .signoff-grid {{ grid-template-columns: 1fr; }} }}

    .signoff-card {{
      background: var(--gray-50); border: 1px solid var(--gray-200); border-radius: var(--radius-md); padding: 20px; display: flex; flex-direction: column; justify-content: space-between;
    }}
    .signoff-card-title {{ font-family: 'Outfit', sans-serif; font-size: 14px; font-weight: 700; color: var(--dark); margin-bottom: 4px; }}
    .signoff-card-sub {{ font-size: 11px; color: var(--gray-500); margin-bottom: 15px; }}
    .signoff-box-area {{
      height: 110px; background: var(--white); border: 1px dashed var(--gray-300); border-radius: var(--radius-sm); display: flex; flex-direction: column; align-items: center; justify-content: center; margin-bottom: 12px; overflow: hidden; padding: 5px; text-align: center;
    }}
    .signoff-box-area img {{ max-height: 80px; max-width: 100%; object-fit: contain; }}
    .signoff-status-badge {{
      display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;
    }}
    .status-pending {{ background: #fef3c7; color: #b45309; }}
    .status-signed {{ background: #dcfce7; color: #15803d; }}
    .btn-sign {{
      background: var(--primary); color: var(--white); border: none; padding: 8px 14px; border-radius: var(--radius-sm); font-weight: 600; font-size: 12px; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 6px; transition: background 0.2s ease; width: 100%;
    }}
    .btn-sign:hover {{ background: var(--primary-light); }}

    .modal-overlay {{
      display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(4px); z-index: 2000; align-items: center; justify-content: center;
    }}
    .modal-box {{
      background: var(--white); border-radius: var(--radius-lg); width: 90%; max-width: 500px; padding: 25px; box-shadow: var(--shadow-xl); border: 1px solid var(--gray-200);
    }}
    .modal-header {{
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid var(--gray-200);
    }}
    .modal-title {{ font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 700; color: var(--dark); }}
    .close-modal {{ background: transparent; border: none; font-size: 18px; color: var(--gray-400); cursor: pointer; }}
    .sig-pad-canvas {{
      border: 1px solid var(--gray-300); border-radius: var(--radius-sm); background: #fafafa; width: 100%; height: 160px; touch-action: none; cursor: crosshair;
    }}
    .form-group {{ margin-bottom: 12px; }}
    .form-group label {{
      display: block; font-size: 11px; font-weight: 600; color: var(--gray-700); margin-bottom: 4px; text-transform: uppercase;
    }}
    .form-control {{
      width: 100%; padding: 8px 12px; border: 1px solid var(--gray-300); border-radius: var(--radius-sm); font-size: 13px; font-family: 'Inter', sans-serif;
    }}
    .modal-actions {{ display: flex; justify-content: flex-end; gap: 10px; margin-top: 15px; }}

    .doc-footer {{
      margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--gray-300); font-size: 11px; color: var(--gray-500); display: flex; justify-content: space-between; align-items: center;
    }}

    @media print {{
      .web-action-bar, .modal-overlay, .btn-sign, .sticky-sidebar {{ display: none !important; }}
      .main-wrapper {{ grid-template-columns: 1fr !important; margin: 0 !important; padding: 0 !important; }}
      .hero-card, .doc-section, .stat-card, .signoff-section {{ box-shadow: none !important; border: 1px solid #ccc !important; page-break-inside: avoid; }}
    }}
  </style>
</head>
<body>

  <div class="web-action-bar">
    <div class="web-action-left">
      <a href="index.php" class="portal-branding"><i class="fa-solid fa-arrow-left"></i> Popular ERP Document Portal</a>
      <span class="badge-accent">Module 3 Document</span>
      <span class="badge-success">Ready for Sign-off</span>
    </div>
    <div class="web-action-right">
      <button onclick="window.print()" class="btn btn-outline"><i class="fa-solid fa-print"></i> Print / Save PDF</button>
      <a href="SL-POP-ERP-MS-003.pdf" target="_blank" class="btn btn-accent"><i class="fa-solid fa-file-pdf"></i> Download Official PDF</a>
    </div>
  </div>

  <div class="doc-top-bar">
    <div class="header-content">
      <div class="header-logos">
        <img src="{logo_popular}" alt="Popular Auto Spare Logo">
        <div class="divider-line"></div>
        <img src="{logo_sands_white}" alt="SaNDS Lab Logo">
        <div class="divider-line"></div>
        <img src="{logo_uniglobal_white}" alt="UniGlobal Logo">
      </div>
      <div class="doc-meta-badge">
        <span class="doc-ref">DOC ID: SL-POP-ERP-MS-003</span>
        <span class="doc-date">Version: 1.0 Final &bull; Date: 27/09/2026</span>
      </div>
    </div>
  </div>

  <div class="main-wrapper">
    <aside class="sticky-sidebar">
      <div class="sidebar-title"><i class="fa-solid fa-compass"></i> Document Sections</div>
      <ul class="sidebar-menu">
        <li><a href="#sec-exec" class="active"><i class="fa-solid fa-circle-info"></i> Executive Summary</a></li>
        <li><a href="#sec-scope"><i class="fa-solid fa-cubes"></i> Functional Scope</a></li>
        <li><a href="#sec-team"><i class="fa-solid fa-users-gear"></i> Dedicated Team</a></li>
        <li><a href="#sec-roadmap"><i class="fa-solid fa-timeline"></i> Milestone Roadmap</a></li>
        <li><a href="#sec-payment"><i class="fa-solid fa-money-bill-transfer"></i> Payment Schedule</a></li>
        <li><a href="#sec-terms"><i class="fa-solid fa-scale-balanced"></i> SLA & Governance</a></li>
        <li><a href="#sec-signoff"><i class="fa-solid fa-signature"></i> Digital Sign-Off</a></li>
      </ul>
    </aside>

    <main class="content-area">
      <div class="hero-card" id="sec-exec">
        <div class="hero-badge-pill"><i class="fa-solid fa-warehouse"></i> Multi-Warehouse & Store Verification Engine</div>
        <h1 class="hero-title">Module 3: Store Verification, Stock Control & Location Management</h1>
        <p class="hero-subtitle">
          Comprehensive 15-week implementation roadmap for Inward Store Verification (PVN), 60/40 sampling daily stock audits, 5-tier location spatial layout, multi-branch stock transfers (GIT) with handheld QR scanning, and FIFO valuation for <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong>.
        </p>

        <div class="meta-grid">
          <div class="meta-box">
            <div class="meta-label">Total Module Fee</div>
            <div class="meta-val" style="color: #d97706;">BD 5,113.636</div>
          </div>
          <div class="meta-box">
            <div class="meta-label">Implementation Timeline</div>
            <div class="meta-val">15 Working Weeks</div>
          </div>
          <div class="meta-box">
            <div class="meta-label">Delivery Effort</div>
            <div class="meta-val">3.75 Engineering Months</div>
          </div>
          <div class="meta-box">
            <div class="meta-label">Milestone Tranches</div>
            <div class="meta-val">4 Verified Gates (25%)</div>
          </div>
        </div>
      </div>

      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-icon icon-navy"><i class="fa-solid fa-layer-group"></i></div>
          <div class="stat-info">
            <div class="stat-num">5 Tiers</div>
            <div class="stat-title">Zone/Aisle/Rack/Shelf/Bin</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon icon-amber"><i class="fa-solid fa-qrcode"></i></div>
          <div class="stat-info">
            <div class="stat-num">Android PDA</div>
            <div class="stat-title">QR Scanner Sync Engine</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon icon-emerald"><i class="fa-solid fa-truck-ramp-box"></i></div>
          <div class="stat-info">
            <div class="stat-num">7-Stage GIT</div>
            <div class="stat-title">Branch Transfer Custody</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon icon-blue"><i class="fa-solid fa-shield-halved"></i></div>
          <div class="stat-info">
            <div class="stat-num">15-Day UAT</div>
            <div class="stat-title">Acceptance SLA</div>
          </div>
        </div>
      </div>

      <section class="doc-section" id="sec-scope">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 01</span>
            <h2 class="section-title">Functional Scope & Warehouse Architecture Breakdown</h2>
          </div>
          <span class="badge-accent">Warehouse Scope</span>
        </div>
        <p class="section-desc">
          Module 3 transforms Popular's central warehouse and multi-branch stores into real-time, scanner-driven distribution centers with zero stock loss, automated bin navigation, and rigorous daily physical count audits.
        </p>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-card-title"><i class="fa-solid fa-cubes-stacked"></i> 5-Tier Spatial Location Matrix</div>
            <div class="feature-card-text">
              Precise bin coordinate tracking (Warehouse &rarr; Zone &rarr; Aisle &rarr; Rack &rarr; Shelf &rarr; Bin) with printed QR codes for instantaneous pick-and-pack routing.
            </div>
          </div>
          <div class="feature-card">
            <div class="feature-card-title"><i class="fa-solid fa-clipboard-check"></i> Blind 60/40 Cycle Count Engine</div>
            <div class="feature-card-text">
              Dynamic physical inventory audits (60% high-value/fast-moving + 40% random SKUs) with day-closing hard locks preventing unaccounted inventory leakages.
            </div>
          </div>
          <div class="feature-card">
            <div class="feature-card-title"><i class="fa-solid fa-truck-moving"></i> Goods-in-Transit (GIT) Transfer</div>
            <div class="feature-card-text">
              7-stage transfer lifecycle with driver handheld confirmation, destination warehouse receiving scans, and automatic variance logging.
            </div>
          </div>
          <div class="feature-card">
            <div class="feature-card-title"><i class="fa-solid fa-boxes-stacked"></i> Min/Max Auto-Replenishment</div>
            <div class="feature-card-text">
              Automated branch reorder alerts calculated from 90-day sales velocity, seasonal demand spikes, and supplier lead times.
            </div>
          </div>
        </div>
      </section>

      <section class="doc-section" id="sec-team">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 02</span>
            <h2 class="section-title">Dedicated Engineering Team & Resource Rate Matrix (BHD)</h2>
          </div>
          <span class="badge-success">Transparent Rates</span>
        </div>
        <p class="section-desc">
          Pricing for Module 3 is calculated strictly using the dedicated 5-person engineering team across 15 working weeks (3.75 calendar months):
        </p>

        <div class="rate-card-grid">
          <div class="rate-box">
            <div class="role-name">Project Manager & Solutions Architect</div>
            <div class="bhd-val">BD 545.455</div>
            <div class="bhd-sub">BD 136.364 / Wk &bull; 3.75 Mo = BD 2,045.456</div>
            <div class="alloc-val">100% Dedicated</div>
          </div>
          <div class="rate-box">
            <div class="role-name">Back-End Lead Engineer (PHP MVC)</div>
            <div class="bhd-val">BD 227.273</div>
            <div class="bhd-sub">BD 56.818 / Wk &bull; 3.75 Mo = BD 852.274</div>
            <div class="alloc-val">100% Dedicated</div>
          </div>
          <div class="rate-box">
            <div class="role-name">Front-End Lead Engineer (React 18)</div>
            <div class="bhd-val">BD 227.273</div>
            <div class="bhd-sub">BD 56.818 / Wk &bull; 3.75 Mo = BD 852.274</div>
            <div class="alloc-val">100% Dedicated</div>
          </div>
          <div class="rate-box">
            <div class="role-name">Database & Cloud DevOps Specialist</div>
            <div class="bhd-val">BD 204.545</div>
            <div class="bhd-sub">BD 51.136 / Wk &bull; 3.75 Mo = BD 767.044</div>
            <div class="alloc-val">100% Dedicated</div>
          </div>
          <div class="rate-box">
            <div class="role-name">QA Automation & Test Lead</div>
            <div class="bhd-val">BD 159.091</div>
            <div class="bhd-sub">BD 39.773 / Wk &bull; 3.75 Mo = BD 596.591</div>
            <div class="alloc-val">100% Dedicated</div>
          </div>
        </div>

        <div class="table-container" style="margin-top: 20px;">
          <table class="master-table">
            <thead>
              <tr>
                <th>Engineering Designation</th>
                <th>Monthly Rate (BHD)</th>
                <th>Weekly Rate (BHD)</th>
                <th>Hourly Rate (160h)</th>
                <th>Effort Allocation</th>
                <th>Total Cost (BHD)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Project Manager & Enterprise Solutions Architect</strong></td>
                <td>BD 545.455</td>
                <td>BD 136.364</td>
                <td>BD 3.409</td>
                <td>3.75 Months (15 Wks)</td>
                <td><span class="currency-bhd">BD 2,045.456</span></td>
              </tr>
              <tr>
                <td><strong>Back-End Lead Engineer (PHP MVC / REST APIs)</strong></td>
                <td>BD 227.273</td>
                <td>BD 56.818</td>
                <td>BD 1.420</td>
                <td>3.75 Months (15 Wks)</td>
                <td><span class="currency-bhd">BD 852.274</span></td>
              </tr>
              <tr>
                <td><strong>Front-End Lead Engineer (Admin UI / React Tokens)</strong></td>
                <td>BD 227.273</td>
                <td>BD 56.818</td>
                <td>BD 1.420</td>
                <td>3.75 Months (15 Wks)</td>
                <td><span class="currency-bhd">BD 852.274</span></td>
              </tr>
              <tr>
                <td><strong>Database & Cloud Infrastructure Architect</strong></td>
                <td>BD 204.545</td>
                <td>BD 51.136</td>
                <td>BD 1.278</td>
                <td>3.75 Months (15 Wks)</td>
                <td><span class="currency-bhd">BD 767.044</span></td>
              </tr>
              <tr>
                <td><strong>QA & System Test Automation Lead Engineer</strong></td>
                <td>BD 159.091</td>
                <td>BD 39.773</td>
                <td>BD 0.994</td>
                <td>3.75 Months (15 Wks)</td>
                <td><span class="currency-bhd">BD 596.591</span></td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="4"><strong>TOTAL MODULE 3 DEDICATED ENGINEERING INVESTMENT</strong></td>
                <td><strong>15 Working Weeks</strong></td>
                <td><strong style="color: var(--accent-gold); font-size: 15px;">BD 5,113.636</strong></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </section>

      <section class="doc-section" id="sec-roadmap">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 03</span>
            <h2 class="section-title">Milestone Delivery Breakdown & Payment Tranches</h2>
          </div>
          <span class="badge-accent">4 Tranches @ 25%</span>
        </div>

        <div class="table-container" id="sec-payment">
          <table class="master-table">
            <thead>
              <tr>
                <th>Milestone Phase</th>
                <th>Deliverable Description & Scope</th>
                <th>Timeline</th>
                <th>Share (%)</th>
                <th>Invoice Amount (BHD)</th>
                <th>Acceptance Verification Trigger</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Milestone 1</strong></td>
                <td>Warehouse Spatial Hierarchy (5 Tiers), Bin Matrix & Inward PVN Setup</td>
                <td>Weeks 1–4</td>
                <td>25.00%</td>
                <td><span class="currency-bhd">BD 1,278.409</span></td>
                <td>Demonstration of Warehouse spatial master, Bin QR generator & Inward PVN</td>
              </tr>
              <tr>
                <td><strong>Milestone 2</strong></td>
                <td>Handheld Scanner Engine, Blind 60/40 Cycle Counts & Variance Alerts</td>
                <td>Weeks 5–8</td>
                <td>25.00%</td>
                <td><span class="currency-bhd">BD 1,278.409</span></td>
                <td>Sign-off of Android PDA scanner integration & blind stock audit reconciliation</td>
              </tr>
              <tr>
                <td><strong>Milestone 3</strong></td>
                <td>Inter-Branch Stock Transfers (GIT), Multi-Tier Discrepancy & FIFO Valuation</td>
                <td>Weeks 9–12</td>
                <td>25.00%</td>
                <td><span class="currency-bhd">BD 1,278.409</span></td>
                <td>Verification of 7-stage GIT transfers, driver sign-off & FIFO valuation math</td>
              </tr>
              <tr>
                <td><strong>Milestone 4</strong></td>
                <td>Min/Max Safety Stock Auto-Replenishment, Aging & Final Warehouse Sign-Off</td>
                <td>Weeks 13–15</td>
                <td>25.00%</td>
                <td><span class="currency-bhd">BD 1,278.409</span></td>
                <td>Formal multi-warehouse UAT sign-off and final production deployment</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="2"><strong>TOTAL MODULE 3 CONTRACT VALUE</strong></td>
                <td><strong>15 Weeks</strong></td>
                <td><strong>100.00%</strong></td>
                <td colspan="2"><strong style="color: var(--accent-gold); font-size: 15px;">BD 5,113.636</strong></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </section>

      <section class="doc-section" id="sec-terms">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 04</span>
            <h2 class="section-title">Terms, SLA & Governance Protocols</h2>
          </div>
          <span class="badge-success">Enterprise Standard</span>
        </div>

        <div class="terms-box">
          <h4>1. 15-Day UAT Review SLA</h4>
          <ul>
            <li>Popular Auto Spare is allocated a 15-calendar-day UAT review window per milestone to test all warehouse scanning and inventory transfers.</li>
          </ul>
        </div>
        <div class="terms-box">
          <h4>2. Source Code & IP Transfer</h4>
          <ul>
            <li>Full proprietary ownership of warehouse spatial models, barcode scanner event listeners, and audit engines transfers to Popular Auto Spare Co.</li>
          </ul>
        </div>
      </section>

      <section class="signoff-section" id="sec-signoff">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 05</span>
            <h2 class="section-title">Stakeholder Authorization & Digital Sign-Off Console</h2>
          </div>
          <span class="badge-accent">Official Sign-Off</span>
        </div>
        <p style="font-size: 13px; color: var(--gray-700); margin-bottom: 20px;">
          By affixing digital signatures below, authorized executive representatives formalize the approval and scope ratification for <strong>Module 3: Store Verification & Stock Control Milestone</strong>.
        </p>

        <div class="signoff-grid">
          <div class="signoff-card">
            <div>
              <div class="signoff-card-title">Popular Auto Spare Co. W.L.L</div>
              <div class="signoff-card-sub">Client Executive Sign-off & Commercial Approval</div>
              <div class="signoff-box-area" id="sig_area_client">
                <span style="font-size: 11px; color: var(--gray-400);">No Signature on Record</span>
              </div>
              <span class="signoff-status-badge status-pending" id="badge_client">PENDING SIGN-OFF</span>
            </div>
            <button class="btn-sign" onclick="openSignModal('client', 'Popular Auto Spare Co. W.L.L', 'Managing Director / Commercial Lead')">
              <i class="fa-solid fa-pen-nib"></i> Sign as Client Executive
            </button>
          </div>

          <div class="signoff-card">
            <div>
              <div class="signoff-card-title">SaNDS Lab Middle East W.L.L</div>
              <div class="signoff-card-sub">Lead Solutions Architect & Engineering Director</div>
              <div class="signoff-box-area" id="sig_area_architect">
                <span style="font-size: 11px; color: var(--gray-400);">No Signature on Record</span>
              </div>
              <span class="signoff-status-badge status-pending" id="badge_architect">PENDING SIGN-OFF</span>
            </div>
            <button class="btn-sign" onclick="openSignModal('architect', 'SaNDS Lab Middle East W.L.L', 'Enterprise Solutions Architect')">
              <i class="fa-solid fa-pen-nib"></i> Sign as Solutions Architect
            </button>
          </div>

          <div class="signoff-card">
            <div>
              <div class="signoff-card-title">UniGlobal Consultancy</div>
              <div class="signoff-card-sub">Executive Strategic Advisor & Governance Lead</div>
              <div class="signoff-box-area" id="sig_area_advisor">
                <span style="font-size: 11px; color: var(--gray-400);">No Signature on Record</span>
              </div>
              <span class="signoff-status-badge status-pending" id="badge_advisor">PENDING SIGN-OFF</span>
            </div>
            <button class="btn-sign" onclick="openSignModal('advisor', 'UniGlobal Consultancy', 'Senior Strategic Advisor')">
              <i class="fa-solid fa-pen-nib"></i> Sign as Strategic Advisor
            </button>
          </div>
        </div>
      </section>

      <footer class="doc-footer">
        <div><strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong> &bull; Kingdom of Bahrain</div>
        <div>SaNDS Lab Middle East W.L.L &copy; 2026. All Rights Reserved.</div>
      </footer>
    </main>
  </div>

  <div class="modal-overlay" id="sigModal">
    <div class="modal-box">
      <div class="modal-header">
        <div class="modal-title"><i class="fa-solid fa-signature"></i> Digital Signature Capture</div>
        <button class="close-modal" onclick="closeSignModal()">&times;</button>
      </div>
      <div class="form-group">
        <label>Signer Full Name</label>
        <input type="text" class="form-control" id="signerName" placeholder="Enter full name">
      </div>
      <div class="form-group">
        <label>Signer Designation</label>
        <input type="text" class="form-control" id="signerDesignation" placeholder="e.g. Managing Director">
      </div>
      <div class="form-group">
        <label>Draw Signature</label>
        <canvas class="sig-pad-canvas" id="sigCanvas"></canvas>
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <button type="button" class="btn btn-outline" style="color: var(--gray-700); font-size: 11px;" onclick="clearCanvas()">
          <i class="fa-solid fa-eraser"></i> Clear Canvas
        </button>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" style="color: var(--gray-700);" onclick="closeSignModal()">Cancel</button>
          <button type="button" class="btn btn-accent" id="btnSubmitSign" onclick="submitSignature()">Confirm & Apply</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    let currentRole = '';
    const canvas = document.getElementById('sigCanvas');
    const ctx = canvas.getContext('2d');
    let isDrawing = false;

    function resizeCanvas() {{
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
      ctx.lineWidth = 2;
      ctx.lineCap = 'round';
      ctx.strokeStyle = '#0a2540';
    }}

    function getPos(e) {{
      const rect = canvas.getBoundingClientRect();
      const clientX = e.touches ? e.touches[0].clientX : e.clientX;
      const clientY = e.touches ? e.touches[0].clientY : e.clientY;
      return {{ x: clientX - rect.left, y: clientY - rect.top }};
    }}

    function startDrawing(e) {{
      isDrawing = true;
      const pos = getPos(e);
      ctx.beginPath();
      ctx.moveTo(pos.x, pos.y);
      e.preventDefault();
    }}

    function draw(e) {{
      if (!isDrawing) return;
      const pos = getPos(e);
      ctx.lineTo(pos.x, pos.y);
      ctx.stroke();
      e.preventDefault();
    }}

    function stopDrawing() {{ isDrawing = false; }}

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    window.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('touchstart', startDrawing, {{ passive: false }});
    canvas.addEventListener('touchmove', draw, {{ passive: false }});
    canvas.addEventListener('touchend', stopDrawing);

    function clearCanvas() {{ ctx.clearRect(0, 0, canvas.width, canvas.height); }}

    function openSignModal(role, orgName, defaultDesignation) {{
      currentRole = role;
      document.getElementById('sigModal').style.display = 'flex';
      document.getElementById('signerDesignation').value = defaultDesignation;
      resizeCanvas();
      clearCanvas();
    }}

    function closeSignModal() {{
      document.getElementById('sigModal').style.display = 'none';
      currentRole = '';
    }}

    function submitSignature() {{
      const name = document.getElementById('signerName').value.trim();
      const designation = document.getElementById('signerDesignation').value.trim();
      if (!name) {{
        alert('Please enter your full name.');
        return;
      }}
      const sigData = canvas.toDataURL('image/png');

      const formData = new FormData();
      formData.append('action', 'sign_milestone');
      formData.append('role', currentRole);
      formData.append('signer_name', name);
      formData.append('signer_designation', designation);
      formData.append('signature_data', sigData);

      document.getElementById('btnSubmitSign').disabled = true;
      document.getElementById('btnSubmitSign').textContent = 'Recording Signature...';

      fetch(window.location.href, {{
        method: 'POST',
        body: formData
      }})
      .then(res => res.json())
      .then(data => {{
        if (data.success) {{
          alert('Signature applied successfully to SL-POP-ERP-MS-003!');
          window.location.reload();
        }} else {{
          alert('Error: ' + data.message);
          document.getElementById('btnSubmitSign').disabled = false;
          document.getElementById('btnSubmitSign').textContent = 'Confirm & Apply';
        }}
      }})
      .catch(err => {{
        alert('Server communication error: ' + err);
        document.getElementById('btnSubmitSign').disabled = false;
        document.getElementById('btnSubmitSign').textContent = 'Confirm & Apply';
      }});
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      const formData = new FormData();
      formData.append('action', 'get_signatures');
      fetch(window.location.href, {{
        method: 'POST',
        body: formData
      }})
      .then(res => res.json())
      .then(data => {{
        if (data.success && data.signatures) {{
          data.signatures.forEach(sig => {{
            const sigArea = document.getElementById(`sig_area_${{sig.role}}`);
            const badge = document.getElementById(`badge_${{sig.role}}`);
            if (sigArea) {{
              sigArea.innerHTML = `<img src="${{sig.signature_data}}" alt="Signature"><br><small style="font-size: 10px; color: var(--gray-600);">${{sig.signer_name}} (${{sig.signed_at}})</small>`;
            }}
            if (badge) {{
              badge.textContent = 'SIGNED & APPROVED';
              badge.className = 'signoff-status-badge status-signed';
            }}
          }});
        }}
      }})
      .catch(e => console.log('Sig load info:', e));
    }});
  </script>
</body>
</html>
"""

# Write to root and popular/
html_path_1 = os.path.join(BASE_DIR, 'SL-POP-ERP-MS-003.html')
html_path_2 = os.path.join(BASE_DIR, 'Store_Verification_Milestone_and_Payment_Structure.html')
with open(html_path_1, 'w', encoding='utf-8') as f:
    f.write(html_content)
with open(html_path_2, 'w', encoding='utf-8') as f:
    f.write(html_content)

pop_html_1 = os.path.join(BASE_DIR, 'popular', 'SL-POP-ERP-MS-003.html')
pop_html_2 = os.path.join(BASE_DIR, 'popular', 'Store_Verification_Milestone_and_Payment_Structure.html')
shutil.copyfile(html_path_1, pop_html_1)
shutil.copyfile(html_path_1, pop_html_2)

# Overwrite build_store_verification_milestone.py
with open(os.path.join(BASE_DIR, 'build_store_verification_milestone.py'), 'w', encoding='utf-8') as f:
    f.write(f'# Auto-generated Module 3 build script\\nhtml_content = \"\"\"{html_content}\"\"\"\\n')

# Render PDF
rendered_html_path = os.path.join(BASE_DIR, 'rendered_ms003.html')
with open(rendered_html_path, 'w', encoding='utf-8') as rf:
    subprocess.run(['php', '-f', html_path_1], stdout=rf, check=True, cwd=BASE_DIR)

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
pdf_output_root_1 = os.path.join(BASE_DIR, 'SL-POP-ERP-MS-003.pdf')
pdf_output_root_2 = os.path.join(BASE_DIR, 'Store_Verification_Milestone_and_Payment_Structure.pdf')

cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={pdf_output_root_1}',
    '--no-pdf-header-footer',
    rendered_html_path
]
res = subprocess.run(cmd, capture_output=True, text=True)
print('M3 PDF conversion exit code:', res.returncode)

if os.path.exists(rendered_html_path):
    os.remove(rendered_html_path)

shutil.copyfile(pdf_output_root_1, pdf_output_root_2)
shutil.copyfile(pdf_output_root_1, os.path.join(BASE_DIR, 'popular', 'SL-POP-ERP-MS-003.pdf'))
shutil.copyfile(pdf_output_root_1, os.path.join(BASE_DIR, 'popular', 'Store_Verification_Milestone_and_Payment_Structure.pdf'))

doc = fitz.open(pdf_output_root_1)
print(f'M3 PDF Page Count: {len(doc)}')

# Update database
for db_p in [os.path.join(BASE_DIR, '.auth_portal.db'), os.path.join(BASE_DIR, 'popular', '.auth_portal.db')]:
    if os.path.exists(db_p):
        conn = sqlite3.connect(db_p)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO document_meta (doc_id, title, status) VALUES (?, ?, ?)",
                    ('SL-POP-ERP-MS-003', 'Module 3: Store Verification & Stock Control Milestone & Payment Structure', 'IN_REVIEW'))
        conn.commit()
        conn.close()

print('Module 3 successfully rebuilt and synced.')
