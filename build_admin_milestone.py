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
// PHP Backend for Digital Signature & Finalization API (SL-POP-ERP-MS-006)
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

$doc_id = 'SL-POP-ERP-MS-006';

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
                $ins_stmt->execute(array($doc_id, 'Module 6: Enterprise Administration, Facility Management, Fixed Assets, Fleet & Document Control Milestone'));
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
  <title>SL-POP-ERP-MS-006 | Module 6: Enterprise Administration, Facility, Fixed Assets, Fleet & Document Control Milestone & Payment Structure</title>
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

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #f1f5f9;
      color: var(--gray-800);
      line-height: 1.6;
      font-size: 14px;
      -webkit-font-smoothing: antialiased;
    }}

    /* Web Action Header */
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

    .web-action-left {{
      display: flex;
      align-items: center;
      gap: 15px;
    }}

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

    .web-action-right {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

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
      background: #fef3c7;
      color: #b45309;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}

    .badge-success {{
      background: #dcfce7;
      color: #15803d;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}

    /* Global Header Banner */
    .doc-top-bar {{
      background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
      color: var(--white);
      padding: 24px 30px;
      border-bottom: 4px solid var(--accent);
      position: relative;
      box-shadow: var(--shadow-lg);
    }}

    .doc-top-bar-inner {{
      max-width: 1300px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }}

    .logos-cluster {{
      display: flex;
      align-items: center;
      gap: 20px;
    }}

    .logos-cluster img {{
      height: 48px;
      object-fit: contain;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }}

    .logo-divider {{
      width: 1px;
      height: 36px;
      background: rgba(255,255,255,0.25);
    }}

    .doc-meta-badge-group {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .badge-tag {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 30px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .badge-primary {{
      background: rgba(217, 119, 6, 0.2);
      border: 1px solid var(--accent);
      color: var(--accent-gold);
    }}

    .badge-id {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: var(--white);
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Main Container */
    .main-wrapper {{
      max-width: 1300px;
      margin: 30px auto;
      padding: 0 20px;
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 30px;
      position: relative;
    }}

    @media (max-width: 1024px) {{
      .main-wrapper {{
        grid-template-columns: 1fr;
      }}
      .sticky-sidebar {{
        display: none;
      }}
    }}

    /* Sticky Sidebar Navigation */
    .sticky-sidebar {{
      position: sticky;
      top: 70px;
      height: fit-content;
      background: var(--white);
      border-radius: var(--radius-lg);
      padding: 20px;
      box-shadow: var(--shadow-md);
      border: 1px solid var(--gray-200);
    }}

    .sidebar-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      font-weight: 700;
      color: var(--gray-900);
      margin-bottom: 16px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .sidebar-menu {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .sidebar-menu li a {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      border-radius: var(--radius-sm);
      color: var(--gray-600);
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      transition: all 0.2s ease;
    }}

    .sidebar-menu li a:hover,
    .sidebar-menu li a.active {{
      background: var(--gray-100);
      color: var(--primary);
      font-weight: 700;
      border-left: 3px solid var(--accent);
    }}

    .sidebar-menu li a i {{
      width: 18px;
      font-size: 14px;
      color: var(--gray-400);
    }}

    .sidebar-menu li a:hover i,
    .sidebar-menu li a.active i {{
      color: var(--accent);
    }}

    .sidebar-card {{
      margin-top: 20px;
      padding: 16px;
      background: linear-gradient(135deg, var(--gray-50) 0%, var(--gray-100) 100%);
      border-radius: var(--radius-md);
      border: 1px solid var(--gray-200);
      font-size: 12px;
    }}

    .sidebar-card-title {{
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* Main Content Area */
    .content-area {{
      display: flex;
      flex-direction: column;
      gap: 30px;
    }}

    /* Document Hero Card */
    .hero-card {{
      background: var(--white);
      border-radius: var(--radius-xl);
      padding: 40px;
      box-shadow: var(--shadow-md);
      border: 1px solid var(--gray-200);
      position: relative;
      overflow: hidden;
    }}

    .hero-card::after {{
      content: '';
      position: absolute;
      top: 0;
      right: 0;
      width: 300px;
      height: 100%;
      background: radial-gradient(circle at top right, rgba(217, 119, 6, 0.08), transparent 70%);
      pointer-events: none;
    }}

    .doc-pre-title {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 600;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 8px;
    }}

    .doc-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 30px;
      font-weight: 800;
      color: var(--gray-900);
      line-height: 1.25;
      margin-bottom: 12px;
    }}

    .doc-subtitle {{
      font-size: 16px;
      color: var(--gray-600);
      line-height: 1.6;
      max-width: 900px;
      margin-bottom: 24px;
    }}

    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      padding-top: 20px;
      border-top: 1px solid var(--gray-200);
    }}

    .meta-box {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .meta-label {{
      font-size: 11px;
      font-weight: 600;
      color: var(--gray-500);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .meta-val {{
      font-size: 13px;
      font-weight: 700;
      color: var(--gray-800);
    }}

    /* Section Cards */
    .doc-section {{
      background: var(--white);
      border-radius: var(--radius-xl);
      padding: 35px;
      box-shadow: var(--shadow-md);
      border: 1px solid var(--gray-200);
      scroll-margin-top: 30px;
    }}

    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 2px solid var(--gray-100);
      position: relative;
    }}

    .section-header::after {{
      content: '';
      position: absolute;
      bottom: -2px;
      left: 0;
      width: 60px;
      height: 2px;
      background: var(--accent);
    }}

    .section-title-wrap {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .section-num {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 1px;
    }}

    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      font-weight: 800;
      color: var(--gray-900);
    }}

    .section-badge {{
      background: var(--gray-100);
      color: var(--gray-700);
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      text-transform: uppercase;
    }}

    /* Roadmap Box */
    .roadmap-box {{
      background: #ffffff;
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-lg);
      padding: 20px;
      margin: 24px 0;
      box-shadow: var(--shadow-sm);
    }}

    .roadmap-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--gray-200);
    }}

    .roadmap-header h4 {{
      font-family: 'Outfit', sans-serif;
      font-size: 15px;
      color: var(--gray-900);
      font-weight: 700;
    }}

    .roadmap-list {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }}

    @media (max-width: 768px) {{
      .roadmap-list {{
        grid-template-columns: 1fr;
      }}
    }}

    .roadmap-item {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-sm);
      font-size: 12.5px;
      font-weight: 500;
      color: var(--gray-700);
      transition: all 0.2s ease;
    }}

    .roadmap-item.active {{
      background: #eff6ff;
      border: 1.5px solid #2563eb;
      color: #1d4ed8;
      font-weight: 700;
    }}

    .roadmap-item.done {{
      background: #ecfdf5;
      border: 1.5px solid #059669;
      color: #065f46;
      font-weight: 600;
    }}

    .rm-badge {{
      background: var(--gray-200);
      color: var(--gray-700);
      font-size: 11px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
    }}

    .roadmap-item.active .rm-badge {{
      background: #2563eb;
      color: #fff;
    }}

    .roadmap-item.done .rm-badge {{
      background: #059669;
      color: #fff;
    }}

    /* Grid & Cards inside sections */
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }}

    .feature-card {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-lg);
      padding: 24px;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .feature-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: var(--gray-300);
    }}

    .feature-icon {{
      width: 44px;
      height: 44px;
      border-radius: var(--radius-md);
      background: var(--primary);
      color: var(--white);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }}

    .feature-icon.gold {{
      background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%);
    }}

    .feature-icon.emerald {{
      background: linear-gradient(135deg, var(--success) 0%, #10b981 100%);
    }}

    .feature-icon.blue {{
      background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
    }}

    .feature-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: var(--gray-900);
    }}

    .feature-desc {{
      font-size: 13px;
      color: var(--gray-600);
      line-height: 1.6;
    }}

    .feature-tags {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: auto;
      padding-top: 10px;
    }}

    .feature-tag {{
      font-size: 10px;
      font-weight: 700;
      padding: 3px 8px;
      background: var(--white);
      border: 1px solid var(--gray-200);
      border-radius: 4px;
      color: var(--gray-600);
    }}

    /* Callout Boxes */
    .callout-box {{
      background: #eff6ff;
      border-left: 4px solid #3b82f6;
      padding: 20px;
      border-radius: 0 var(--radius-md) var(--radius-md) 0;
      margin: 20px 0;
      display: flex;
      gap: 16px;
      align-items: flex-start;
    }}

    .callout-box.warning {{
      background: #fffbeb;
      border-left-color: var(--accent);
    }}

    .callout-box.success {{
      background: #ecfdf5;
      border-left-color: var(--success);
    }}

    .callout-icon {{
      font-size: 20px;
      color: #3b82f6;
      margin-top: 2px;
    }}

    .callout-box.warning .callout-icon {{
      color: var(--accent);
    }}

    .callout-box.success .callout-icon {{
      color: var(--success);
    }}

    .callout-content {{
      flex: 1;
      font-size: 13px;
      color: var(--gray-700);
    }}

    .callout-title {{
      font-weight: 700;
      color: var(--gray-900);
      margin-bottom: 4px;
      font-size: 14px;
    }}

    /* Data Tables */
    .custom-table-wrap {{
      overflow-x: auto;
      margin: 20px 0;
      border-radius: var(--radius-md);
      border: 1px solid var(--gray-200);
      box-shadow: var(--shadow-sm);
    }}

    table.custom-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }}

    table.custom-table th {{
      background: var(--primary);
      color: var(--white);
      padding: 14px 18px;
      font-weight: 600;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 2px solid var(--primary-dark);
    }}

    table.custom-table td {{
      padding: 14px 18px;
      border-bottom: 1px solid var(--gray-200);
      color: var(--gray-700);
      vertical-align: middle;
    }}

    table.custom-table tbody tr:nth-child(even) {{
      background-color: var(--gray-50);
    }}

    table.custom-table tbody tr:hover {{
      background-color: #f8fafc;
    }}

    table.custom-table tr.total-row td {{
      background: var(--gray-900) !important;
      color: var(--white) !important;
      font-weight: 700;
      font-size: 14px;
    }}

    /* Workflow Stepper */
    .stepper-container {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin: 24px 0;
    }}

    .step-item {{
      display: flex;
      gap: 20px;
      position: relative;
    }}

    .step-item:not(:last-child)::after {{
      content: '';
      position: absolute;
      top: 40px;
      left: 20px;
      bottom: -16px;
      width: 2px;
      background: var(--gray-200);
    }}

    .step-circle {{
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: var(--primary);
      color: var(--white);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 15px;
      flex-shrink: 0;
      z-index: 1;
      box-shadow: 0 0 0 4px var(--gray-100);
    }}

    .step-content {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-lg);
      padding: 20px;
      flex: 1;
    }}

    .step-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 15px;
      font-weight: 700;
      color: var(--gray-900);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .step-desc {{
      font-size: 13px;
      color: var(--gray-600);
      line-height: 1.6;
    }}

    /* Deliverable Checklist */
    .checklist-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }}

    .check-item {{
      display: flex;
      gap: 12px;
      background: var(--gray-50);
      padding: 16px;
      border-radius: var(--radius-md);
      border: 1px solid var(--gray-200);
    }}

    .check-item i {{
      color: var(--success);
      font-size: 16px;
      margin-top: 2px;
    }}

    .check-text {{
      font-size: 13px;
      color: var(--gray-700);
      line-height: 1.5;
    }}

    .check-text strong {{
      color: var(--gray-900);
      display: block;
      margin-bottom: 2px;
    }}

    /* Sign-off Box */
    .signoff-box-container {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 24px;
    }}

    .signoff-card {{
      background: var(--gray-50);
      border: 2px dashed var(--gray-300);
      border-radius: var(--radius-lg);
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      text-align: center;
      position: relative;
    }}

    .signoff-role {{
      font-family: 'Outfit', sans-serif;
      font-size: 15px;
      font-weight: 700;
      color: var(--primary);
    }}

    .signoff-person {{
      font-size: 13px;
      color: var(--gray-600);
    }}

    .signoff-status-badge {{
      display: inline-block;
      margin: 0 auto;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
    }}

    .status-signed {{
      background: rgba(5, 150, 105, 0.1);
      color: var(--success);
      border: 1px solid var(--success);
    }}

    .status-pending {{
      background: rgba(217, 119, 6, 0.1);
      color: var(--accent);
      border: 1px solid var(--accent);
    }}

    .sig-display-area {{
      min-height: 70px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-bottom: 1px solid var(--gray-200);
      padding-bottom: 10px;
    }}

    .sig-display-area img {{
      max-height: 55px;
      max-width: 100%;
    }}

    /* Action Buttons */
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 20px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      border: none;
    }}

    .btn-primary {{
      background: var(--primary);
      color: var(--white);
    }}

    .btn-primary:hover {{
      background: var(--primary-light);
      box-shadow: var(--shadow-sm);
    }}

    .btn-accent {{
      background: var(--accent);
      color: var(--white);
    }}

    .btn-accent:hover {{
      background: var(--accent-light);
    }}

    .btn-outline {{
      background: transparent;
      border: 1px solid var(--gray-300);
      color: var(--gray-700);
    }}

    .btn-outline:hover {{
      background: var(--gray-100);
      border-color: var(--gray-400);
    }}

    /* Modal Styling */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(4px);
      z-index: 9999;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .modal-box {{
      background: var(--white);
      border-radius: var(--radius-xl);
      max-width: 600px;
      width: 100%;
      padding: 30px;
      box-shadow: var(--shadow-xl);
      position: relative;
    }}

    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}

    .modal-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: var(--gray-900);
    }}

    .modal-close {{
      background: transparent;
      border: none;
      font-size: 20px;
      color: var(--gray-400);
      cursor: pointer;
    }}

    canvas.signature-pad {{
      border: 1px solid var(--gray-300);
      border-radius: var(--radius-md);
      background: #fafafa;
      width: 100%;
      height: 180px;
    }}

    /* Print Styles */
    @media print {{
      .web-action-bar {{ display: none !important; }}
      body {{
        background: #fff !important;
        font-size: 11pt;
        color: #000;
      }}
      .doc-top-bar, .sticky-sidebar, .btn, .modal-overlay {{
        display: none !important;
      }}
      .main-wrapper {{
        display: block !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
      }}
      .hero-card, .doc-section {{
        box-shadow: none !important;
        border: 1px solid #ddd !important;
        margin-bottom: 20px !important;
        page-break-inside: avoid;
      }}
    }}
      /* =========================================================================
       COMPREHENSIVE MOBILE RESPONSIVE STYLING
       ========================================================================= */
    @media (max-width: 1100px) {{
      .main-wrapper {{
        grid-template-columns: 240px minmax(0, 1fr) !important;
        gap: 20px !important;
        padding: 0 16px !important;
      }}
      .sticky-sidebar {{
        width: 240px !important;
      }}
    }}

    @media (max-width: 900px) {{
      .main-wrapper {{
        display: block !important;
        grid-template-columns: 1fr !important;
        padding: 0 12px !important;
      }}
      .sticky-sidebar {{
        position: static !important;
        width: 100% !important;
        max-height: none !important;
        margin-bottom: 24px !important;
        top: 0 !important;
      }}
      .sidebar-nav {{
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
      }}
      .sidebar-link {{
        flex: 1 1 calc(50% - 6px) !important;
        padding: 8px 10px !important;
        font-size: 11.5px !important;
      }}
      .hero-stats-grid, .stat-grid, .kpi-grid, .meta-grid {{
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 12px !important;
      }}
      .doc-top-bar-inner, .header-content {{
        flex-direction: column !important;
        text-align: center !important;
        gap: 12px !important;
        padding: 16px 12px !important;
      }}
      .logos-cluster, .header-logos {{
        justify-content: center !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
      }}
      .doc-meta-badge-group, .doc-meta-badge {{
        justify-content: center !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
      }}
      .charts-grid {{
        grid-template-columns: 1fr !important;
      }}
    }}

    @media (max-width: 600px) {{
      .web-action-bar {{
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 10px !important;
        padding: 10px 12px !important;
      }}
      .web-action-left, .web-action-right {{
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 6px !important;
        width: 100% !important;
      }}
      .web-action-bar .btn {{
        flex: 1 1 calc(50% - 6px) !important;
        text-align: center !important;
        justify-content: center !important;
        font-size: 11.5px !important;
        padding: 7px 10px !important;
      }}
      .portal-branding {{
        font-size: 12px !important;
        text-align: center !important;
        width: 100% !important;
        justify-content: center !important;
        display: flex !important;
      }}
      .hero-card, .doc-section, .section-card, .signoff-section {{
        padding: 16px 12px !important;
        border-radius: 10px !important;
        margin-bottom: 16px !important;
      }}
      .hero-title, .section-title {{
        font-size: 18px !important;
      }}
      .hero-stats-grid, .stat-grid, .kpi-grid, .meta-grid {{
        grid-template-columns: 1fr !important;
        gap: 10px !important;
      }}
      .sidebar-link {{
        flex: 1 1 100% !important;
      }}
      .table-container {{
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        width: 100% !important;
        margin: 10px 0 15px 0 !important;
        border-radius: 6px !important;
      }}
      table.milestone-table, table.master-table, table.data-table, table.rate-table {{
        min-width: 540px !important;
      }}
      .modal-box {{
        width: 95% !important;
        max-width: 95% !important;
        padding: 16px !important;
        margin: 10px !important;
      }}
      canvas.signature-pad, .sig-pad-canvas {{
        height: 140px !important;
      }}
      .total-cost-hero-box {{
        flex-direction: column !important;
        text-align: center !important;
        gap: 12px !important;
        padding: 16px !important;
      }}
      .total-cost-amt {{
        font-size: 24px !important;
      }}
    }}
  </style>
</head>
<body>

  <!-- ==================== WEB PORTAL TOP ACTION BAR ==================== -->
  <div class="web-action-bar">
    <div class="web-action-left">
      <a href="index.php" class="portal-branding">
        <span style="background:#0284c7; color:#fff; border-radius:4px; padding:2px 6px; font-size:11px;">PORTAL</span>
        SaNDS Lab • Popular ERP Governance
      </a>
      <span style="color:#64748b;">|</span>
      <span style="font-family:'JetBrains Mono', monospace; font-size:12px; color:#38bdf8;">DOC: SL-POP-ERP-MS-006</span>
      <?php if ($is_locked): ?>
        <span class="badge badge-success">🔒 FINALIZED & LOCKED</span>
      <?php else: ?>
        <span class="badge badge-accent">📝 IN ACTIVE REVIEW</span>
      <?php endif; ?>
    </div>
    <div class="web-action-right">
      <a href="index.php" class="btn btn-outline">← Back to Portal</a>
      <button onclick="window.print();" class="btn btn-outline">🖨️ Print Document</button>
      <a href="SL-POP-ERP-MS-006.pdf" download class="btn btn-accent">📥 Download Signed PDF</a>
    </div>
  </div>

  <!-- Top Header Navigation -->
  <header class="doc-top-bar">
    <div class="doc-top-bar-inner">
      <div class="logos-cluster">
        <img src="{logo_sands_white}" alt="SaNDS Lab">
        <div class="logo-divider"></div>
        <img src="{logo_popular}" alt="Popular Auto Spare Parts">
        <div class="logo-divider"></div>
        <img src="{logo_uniglobal_white}" alt="UniGlobal">
      </div>
      <div class="doc-meta-badge-group">
        <span class="badge-tag badge-id"><i class="fas fa-file-contract"></i> SL-POP-ERP-MS-006</span>
        <span class="badge-tag badge-primary"><i class="fas fa-layer-group"></i> Module 6 / 9</span>
        <span class="badge-tag badge-success"><i class="fas fa-check-double"></i> Verified BA Ref: DOC-006</span>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <div class="main-wrapper">
    
    <!-- Sticky Navigation Sidebar -->
    <aside class="sticky-sidebar">
      <div class="sidebar-title">
        <i class="fas fa-compass"></i> Navigation
      </div>
      <ul class="sidebar-menu">
        <li><a href="#executive-summary" class="active"><i class="fas fa-info-circle"></i> Executive Summary</a></li>
        <li><a href="#module-scope"><i class="fas fa-sitemap"></i> Functional Scope (DOC-006)</a></li>
        <li><a href="#pricing-matrix"><i class="fas fa-calculator"></i> Resource Pricing (12 Wks)</a></li>
        <li><a href="#detailed-milestones"><i class="fas fa-tasks"></i> Milestone Roadmap (1-4)</a></li>
        <li><a href="#payment-schedule"><i class="fas fa-credit-card"></i> Invoicing Schedule</a></li>
        <li><a href="#governance-sla"><i class="fas fa-shield-alt"></i> SLA, Grace Period & Terms</a></li>
        <li><a href="#digital-signoff"><i class="fas fa-file-signature"></i> Digital Sign-Off</a></li>
      </ul>

      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Module 6 At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Timeline:</strong> 12 Weeks (3.0 Mo)</div>
          <div><strong>Total Baseline:</strong> BD 4,090.909</div>
          <div><strong>Milestones:</strong> 4 x 25% Phases</div>
          <div><strong>BA Source:</strong> DOC-006 v1.0 (25 pgs)</div>
          <div><strong>Scope:</strong> Facility, Assets, Fleet & Docs</div>
        </div>
        <button class="btn btn-primary" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>
    </aside>

    <!-- Main Content Stream -->
    <main class="content-area">
      
      <!-- Hero Card -->
      <section class="hero-card">
        <div class="doc-pre-title">Enterprise ERP Implementation Roadmap & Payment Governance</div>
        <h1 class="doc-title">Module 6: Enterprise Administration, Facility Management, Fixed Assets, Fleet & Corporate Document Control</h1>
        <p class="doc-subtitle">
          Comprehensive 12-week milestone agreement, engineering effort breakdown, resource cost schedule, and acceptance criteria based on the verified Business Analysis Report <strong>DOC-006 v1.0</strong> for <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong>.
        </p>

        <div class="meta-grid">
          <div class="meta-box">
            <span class="meta-label">Document ID</span>
            <span class="meta-val">SL-POP-ERP-MS-006</span>
          </div>
          <div class="meta-box">
            <span class="meta-label">BA Reference Document</span>
            <span class="meta-val">DOC-006 v1.0 (04-July-2026)</span>
          </div>
          <div class="meta-box">
            <span class="meta-label">Total Engineering Effort</span>
            <span class="meta-val">12 Working Weeks (3.0 Months)</span>
          </div>
          <div class="meta-box">
            <span class="meta-label">Fixed Project Cost</span>
            <span class="meta-val" style="color: var(--accent); font-size: 15px;">BD 4,090.909</span>
          </div>
          <div class="meta-box">
            <span class="meta-label">Target Architecture</span>
            <span class="meta-val">Multi-Branch Admin & Asset Tracking</span>
          </div>
          <div class="meta-box">
            <span class="meta-label">Document Status</span>
            <span class="meta-val"><span class="badge-tag badge-success" style="padding: 2px 8px; font-size: 10px;">FINAL PROPOSAL</span></span>
          </div>
        </div>
      </section>

      <!-- Section 1: Executive Summary -->
      <section class="doc-section" id="executive-summary">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 1.0</span>
            <h2 class="section-title">Executive Summary & Master ERP Context</h2>
          </div>
          <span class="section-badge">Strategic Alignment</span>
        </div>

        <p>
          The <strong>Enterprise Administration Modules</strong> (Module 6) provide the operational infrastructure, asset tracking, facility governance, fleet control, and statutory legal document compliance framework for Popular Auto Spare & A/C Parts Co. W.L.L. As the enterprise expands across regional distribution hubs, retail branches, and central warehouses, managing physical facilities, tracking fixed assets with QR codes, optimizing fleet operations, and safeguarding legal corporate records become vital for cost control, security, and statutory readiness.
        </p>

        <div class="callout-box">
          <i class="fas fa-lightbulb callout-icon"></i>
          <div class="callout-content">
            <div class="callout-title">Core Objective & Business Purpose</div>
            To establish an integrated administrative operations platform consolidating Workplace Facility Management, QR-based Fixed Asset Lifecycle Tracking & Depreciation, Commercial Fleet & Vehicle Logistics Management, Staff Physical Locker Allocations, and Secure Digital Document & Statutory Renewal Governance.
          </div>
        </div>

        <!-- Master ERP Transformation Architecture (9 Core Modules) -->
        <div class="roadmap-box">
          <div class="roadmap-header">
            <h4>Master ERP Transformation Architecture (9 Core Process Modules)</h4>
            <span class="badge-tag badge-primary" style="font-size: 10.5px; padding: 4px 12px; letter-spacing: 0.5px;">CURRENT SCOPE: MODULE 06 ACTIVE</span>
          </div>
          <div class="roadmap-list">
            <div class="roadmap-item done">
              <span class="rm-badge">01</span>
              <span class="rm-name">PCode Gen & Item Master</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">02</span>
              <span class="rm-name">Vendor & Purchase Flow</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">03</span>
              <span class="rm-name">Stock Verification & Location</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">04</span>
              <span class="rm-name">Sales & POS Checkout</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">05</span>
              <span class="rm-name">Finance, Tax & VAT Accounting</span>
            </div>
            <div class="roadmap-item active">
              <span class="rm-badge">06</span>
              <span class="rm-name">Administration & Security</span>
            </div>
            <div class="roadmap-item">
              <span class="rm-badge">07</span>
              <span class="rm-name">HRMS & Biometric Payroll</span>
            </div>
            <div class="roadmap-item">
              <span class="rm-badge">08</span>
              <span class="rm-name">Hardware & Barcode Infrastructure</span>
            </div>
            <div class="roadmap-item">
              <span class="rm-badge">09</span>
              <span class="rm-name">Executive BI & Mobile Analytics</span>
            </div>
          </div>
        </div>

        <div class="grid-3">
          <div class="feature-card">
            <div class="feature-icon gold"><i class="fas fa-building"></i></div>
            <div class="feature-title">Facility, Lease & Utility Control</div>
            <div class="feature-desc">Centralized facility registry, preventive/corrective work orders, utility expense tracking, property lease renewal alerts, and visitor access control.</div>
            <div class="feature-tags">
              <span class="feature-tag">Facility Master</span>
              <span class="feature-tag">Lease Alerts</span>
              <span class="feature-tag">Utility Log</span>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon emerald"><i class="fas fa-qrcode"></i></div>
            <div class="feature-title">QR Fixed Asset Lifecycle & Audit</div>
            <div class="feature-desc">QR code tagging, custodian assignment, multi-branch asset transfers, straight-line depreciation calculation, and annual physical audit verification.</div>
            <div class="feature-tags">
              <span class="feature-tag">QR Tagging</span>
              <span class="feature-tag">Depreciation</span>
              <span class="feature-tag">Asset Audit</span>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon blue"><i class="fas fa-truck-moving"></i></div>
            <div class="feature-title">Fleet Logistics & Document Vault</div>
            <div class="feature-desc">Commercial vehicle tracking, driver bookings, fuel consumption logs, insurance/road tax compliance, physical locker allocation, and corporate digital document repository.</div>
            <div class="feature-tags">
              <span class="feature-tag">Fleet TCO</span>
              <span class="feature-tag">Fuel Log</span>
              <span class="feature-tag">Digital Vault</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 2: Functional Scope Breakdown (DOC-006) -->
      <section class="doc-section" id="module-scope">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 2.0</span>
            <h2 class="section-title">Module 6: Functional Scope & Architecture Breakdown (BA Ref: DOC-006)</h2>
          </div>
          <span class="section-badge">Full Specification Mapping</span>
        </div>

        <p>
          Derived directly from the 25 pages of <strong>DOC-006: Administration Modules Business Analysis Report</strong>, the implementation scope is structured across 4 core operational pillars:
        </p>

        <div class="grid-2" style="margin-top: 24px;">
          
          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-city"></i> 2.1 Facility & Workplace Office Management
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Facility Master:</strong> Centralized registry of corporate offices, regional branches, central warehouses, workshops, retail outlets, and staff accommodations.</li>
                <li><strong>Maintenance Work Orders:</strong> Preventive scheduled maintenance calendars, AMC vendor contracts, breakdown ticketing, and repair sign-off.</li>
                <li><strong>Employee Service Requests:</strong> Internal ticketing portal for electrical, HVAC/air conditioning, plumbing, carpentry, and IT infrastructure requests.</li>
                <li><strong>Utility & Consumption Control:</strong> Monthly tracking of electricity, water, internet, telephone, gas, and generator fuel with budget variance analysis.</li>
                <li><strong>Visitor Management (VMS):</strong> Digital visitor registration, badge generation, host employee notification, and entry/exit timestamp logging.</li>
                <li><strong>Lease & Property Governance:</strong> Landlord agreements, rent payment schedules, commercial lease terms, and automated renewal notifications.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-barcode"></i> 2.2 Fixed Asset Management & QR Lifecycle Tracking
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Asset Master Registry:</strong> Comprehensive cataloging of IT equipment, warehouse machinery, tools, office furniture, vehicles, and facilities.</li>
                <li><strong>QR Code Tagging & Scanner:</strong> Unique asset QR label generation with handheld scanner integration for rapid location identification and audits.</li>
                <li><strong>Asset Custody & Movements:</strong> Tracking of employee custodians, department assignments, and inter-branch transfer delivery challans.</li>
                <li><strong>Warranty & AMC Management:</strong> Supplier warranty coverage tracking, AMC renewal alerts, and maintenance history logging.</li>
                <li><strong>Depreciation Engine:</strong> Automated straight-line and reducing-balance depreciation posting integrated directly with General Ledger (GL).</li>
                <li><strong>Physical Audit & Disposal:</strong> Periodic physical inventory verification, variance logging, asset write-off, and scrap disposal workflows.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-truck"></i> 2.3 Fleet Logistics, Vehicle Maintenance & Total Cost of Ownership
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Vehicle Master Registry:</strong> Profile management for commercial delivery vans, heavy transport trucks, pickups, and corporate cars.</li>
                <li><strong>Vehicle Allocation & Booking:</strong> Driver assignment, delivery route scheduling, key management, and trip odometer logging.</li>
                <li><strong>GPS & Route Monitoring:</strong> Integration with telematics for real-time delivery tracking and mileage verification.</li>
                <li><strong>Preventive Maintenance:</strong> Service intervals by mileage/date, oil changes, tire replacement logs, and workshop repair history.</li>
                <li><strong>Fuel Management:</strong> Fuel card reconciliation, fuel receipt uploads, kilometer-per-liter efficiency analysis, and fuel theft anomaly detection.</li>
                <li><strong>Statutory Vehicle Compliance:</strong> Traffic registration renewals, comprehensive insurance policies, fitness certificates, and accident claim workflows.</li>
                <li><strong>Vehicle TCO Analytics:</strong> Real-time Total Cost of Ownership (TCO) tracking per vehicle combining fuel, maintenance, insurance, and depreciation.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-folder-open"></i> 2.4 Staff Locker & Corporate Document Management System
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Staff Locker Management:</strong> Branch physical locker registry, employee key allocation, locker inspections, and surrender protocols.</li>
                <li><strong>Digital Document Repository:</strong> Encrypted digital vault for Commercial Registrations (CR), municipality licenses, lease agreements, vehicle titles, and contracts.</li>
                <li><strong>Role-Based Access Control (RBAC):</strong> Granular permissions restricting document access to authorized executive and HR/Admin personnel.</li>
                <li><strong>Physical Document Movement:</strong> Barcoded checkout/check-in tracking for original legal deeds, bank guarantees, and official certificates.</li>
                <li><strong>Automated Expiry & Renewal Alerts:</strong> Proactive 90/60/30-day notifications for CR renewals, chamber of commerce, civil defense, and trade permits.</li>
                <li><strong>Compliance Audit Readiness:</strong> Full historical audit trail of document uploads, version updates, downloads, and custodian modifications.</li>
              </ul>
            </div>
          </div>

        </div>
      </section>

      <!-- Section 3: Pricing Matrix (12 Weeks) -->
      <section class="doc-section" id="pricing-matrix">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 3.0</span>
            <h2 class="section-title">Project Team Structure & Dedicated Resource Pricing (12 Weeks / 3.0 Months)</h2>
          </div>
          <span class="section-badge">Standard Rate Card</span>
        </div>

        <p>
          In strict accordance with the <strong>SaNDS Lab Dedicated Engineering Rate Card</strong>, the resource allocation and cost breakdown for the 12-week (3.0 months / 60 working days) delivery of Module 6 is structured as follows (all figures in Bahraini Dinars - BHD):
        </p>

        <div class="custom-table-wrap">
          <table class="custom-table">
            <thead>
              <tr>
                <th>Engineering Role</th>
                <th>Monthly Rate (BHD)</th>
                <th>Weekly Rate (BHD)</th>
                <th>Hourly Rate (160h/mo)</th>
                <th>Effort Allocation</th>
                <th>Total Cost (BHD)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Project Manager & Enterprise Solutions Architect</strong></td>
                <td><strong>BD 545.455</strong></td>
                <td>BD 136.364</td>
                <td>BD 3.409</td>
                <td>3.0 Months (12 Wks)</td>
                <td><strong>BD 1,636.365</strong></td>
              </tr>
              <tr>
                <td><strong>Back-End Lead Engineer (PHP MVC / REST APIs)</strong></td>
                <td><strong>BD 227.273</strong></td>
                <td>BD 56.818</td>
                <td>BD 1.420</td>
                <td>3.0 Months (12 Wks)</td>
                <td><strong>BD 681.819</strong></td>
              </tr>
              <tr>
                <td><strong>Front-End Lead Engineer (Admin UI / React Dashboards)</strong></td>
                <td><strong>BD 227.273</strong></td>
                <td>BD 56.818</td>
                <td>BD 1.420</td>
                <td>3.0 Months (12 Wks)</td>
                <td><strong>BD 681.819</strong></td>
              </tr>
              <tr>
                <td><strong>Database & Cloud Infrastructure Architect</strong></td>
                <td><strong>BD 204.545</strong></td>
                <td>BD 51.136</td>
                <td>BD 1.278</td>
                <td>3.0 Months (12 Wks)</td>
                <td><strong>BD 613.635</strong></td>
              </tr>
              <tr>
                <td><strong>QA & System Test Automation Lead Engineer</strong></td>
                <td><strong>BD 159.091</strong></td>
                <td>BD 39.773</td>
                <td>BD 0.994</td>
                <td>3.0 Months (12 Wks)</td>
                <td><strong>BD 477.273</strong></td>
              </tr>
              <tr class="total-row">
                <td><strong>Total Dedicated Engineering Team</strong></td>
                <td><strong>BD 1,363.636 / mo</strong></td>
                <td><strong>BD 340.909 / wk</strong></td>
                <td><strong>BD 8.523 / hr</strong></td>
                <td><strong>12 Weeks (3.0 Mo)</strong></td>
                <td><strong>BD 4,090.909</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="callout-box success">
          <i class="fas fa-check-circle callout-icon"></i>
          <div class="callout-content">
            <div class="callout-title">Fixed Price Guarantee</div>
            Total project investment for Module 6 is fixed at <strong>BD 4,090.909</strong>. No hidden deployment, integration, or hourly surcharges apply within the agreed functional scope.
          </div>
        </div>
      </section>

      <!-- Section 4: Detailed Milestone Roadmap (12 Weeks) -->
      <section class="doc-section" id="detailed-milestones">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 4.0</span>
            <h2 class="section-title">Detailed Milestone Breakdown & Deliverables (12-Week Roadmap)</h2>
          </div>
          <span class="section-badge">Sprint Execution Plan</span>
        </div>

        <p>
          The implementation is organized into 4 sequential 3-week milestones (25.00% each), guaranteeing focused execution, continuous integration, and transparent deliverable acceptance:
        </p>

        <div class="stepper-container">
          
          <!-- Milestone 1 -->
          <div class="step-item">
            <div class="step-circle">1</div>
            <div class="step-content">
              <div class="step-title">
                <span>Milestone 1: Facility & Workplace Management, Work Orders & Utility Control</span>
                <span class="badge-tag badge-primary">Weeks 1 – 3 (3 Wks)</span>
              </div>
              <p class="step-desc">
                Setup of centralized Facility Master, preventive/corrective maintenance work orders, employee complaint ticketing, utility consumption logs, visitor registration (VMS), and commercial property lease agreement renewals.
              </p>
              <div class="checklist-grid" style="margin-top: 12px;">
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Facility Master & Zones</strong> Centralized repository of all corporate branches, warehouses, and accommodation units.</div>
                </div>
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Work Orders & Ticketing</strong> Maintenance calendar, AMC vendor contracts, and employee service request portal.</div>
                </div>
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Utility & Lease Control</strong> Electricity/water cost tracking, budget variance, and automated lease renewal notifications.</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Milestone 2 -->
          <div class="step-item">
            <div class="step-circle">2</div>
            <div class="step-content">
              <div class="step-title">
                <span>Milestone 2: Fixed Asset Master, QR Tagging, Custodian Tracking & Depreciation</span>
                <span class="badge-tag badge-primary">Weeks 4 – 6 (3 Wks)</span>
              </div>
              <p class="step-desc">
                Engineering of Fixed Asset Master Registry, QR label generation, custodian assignments, inter-branch asset transfers, straight-line/reducing depreciation calculation, and physical audit verification tools.
              </p>
              <div class="checklist-grid" style="margin-top: 12px;">
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>QR Code Asset Tagging</strong> Unique QR label generation with handheld scanner barcode integration.</div>
                </div>
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Asset Custody & Transfers</strong> Inter-branch transfer tracking, custodian sign-off, and movement history.</div>
                </div>
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Depreciation & Audit Engine</strong> Automated monthly depreciation GL postings, warranty tracking, and scrap disposal.</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Milestone 3 -->
          <div class="step-item">
            <div class="step-circle">3</div>
            <div class="step-content">
              <div class="step-title">
                <span>Milestone 3: Fleet Logistics, Vehicle Bookings, Fuel Logs & TCO Analytics</span>
                <span class="badge-tag badge-primary">Weeks 7 – 9 (3 Wks)</span>
              </div>
              <p class="step-desc">
                Development of Vehicle Master Registry, driver allocation, GPS tracking integration, fuel consumption and card reconciliation, tire/parts service logs, insurance/road tax renewals, and total vehicle TCO analytics.
              </p>
              <div class="checklist-grid" style="margin-top: 12px;">
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Vehicle Master & Bookings</strong> Fleet vehicle profiles, driver assignments, delivery trips, and key tracking.</div>
                </div>
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Fuel & Mileage Analysis</strong> Fuel receipts, mileage efficiency (km/L), and fuel anomaly detection.</div>
                </div>
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Compliance & TCO Dashboard</strong> Insurance/registration renewal alerts, maintenance logs, and vehicle TCO cockpit.</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Milestone 4 -->
          <div class="step-item">
            <div class="step-circle">4</div>
            <div class="step-content">
              <div class="step-title">
                <span>Milestone 4: Staff Locker Control, Secure Digital Document Vault & Final UAT</span>
                <span class="badge-tag badge-primary">Weeks 10 – 12 (3 Wks)</span>
              </div>
              <p class="step-desc">
                Implementation of Physical Locker Management, encrypted Digital Document Repository, physical document barcode movement tracking, automated statutory license renewal alerts (CR, Municipality), and multi-branch UAT sign-off.
              </p>
              <div class="checklist-grid" style="margin-top: 12px;">
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Staff Locker Registry</strong> Branch locker allocation, key handovers, and locker inspection audits.</div>
                </div>
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Secure Digital Document Vault</strong> Encrypted repository for trade licenses, CRs, title deeds, with RBAC security.</div>
                </div>
                <div class="check-item">
                  <i class="fas fa-check"></i>
                  <div class="check-text"><strong>Statutory Renewal Engine & UAT</strong> Automated CR/permit renewal reminders, document movement tracking, and final UAT.</div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Section 5: Payment Structure -->
      <section class="doc-section" id="payment-schedule">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 5.0</span>
            <h2 class="section-title">Milestone Payment Structure & Invoicing Schedule (12-Week Model)</h2>
          </div>
          <span class="section-badge">Deliverable-Based Invoicing</span>
        </div>

        <p>
          Payments are structured in 4 equal milestone disbursements of <strong>25.00% (BD 1,022.727 each)</strong>, tied strictly to formal milestone deliverables and client sign-off:
        </p>

        <div class="custom-table-wrap">
          <table class="custom-table">
            <thead>
              <tr>
                <th>Milestone Phase</th>
                <th>Deliverable Description</th>
                <th>Timeline</th>
                <th>Percentage</th>
                <th>Amount (BHD)</th>
                <th>Payment Trigger & Acceptance Criteria</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Milestone 1</strong></td>
                <td>Facility & Workplace Management, Work Orders & Utility Control</td>
                <td>Weeks 1–3</td>
                <td>25.00%</td>
                <td><strong>BD 1,022.727</strong></td>
                <td>Demonstration of Facility Master, Service Ticketing, Utility Logs & Lease Alerts</td>
              </tr>
              <tr>
                <td><strong>Milestone 2</strong></td>
                <td>Fixed Asset Master, QR Tagging, Custodian Tracking & Depreciation</td>
                <td>Weeks 4–6</td>
                <td>25.00%</td>
                <td><strong>BD 1,022.727</strong></td>
                <td>Sign-off of QR Asset Tagging, Scanner Integration, Transfers & Depreciation Engine</td>
              </tr>
              <tr>
                <td><strong>Milestone 3</strong></td>
                <td>Fleet Logistics, Vehicle Bookings, Fuel Logs & TCO Analytics</td>
                <td>Weeks 7–9</td>
                <td>25.00%</td>
                <td><strong>BD 1,022.727</strong></td>
                <td>Demonstration of Vehicle Master, Driver Bookings, Fuel Reconciliation & TCO Dashboard</td>
              </tr>
              <tr>
                <td><strong>Milestone 4</strong></td>
                <td>Staff Locker Control, Secure Digital Document Vault & Final UAT</td>
                <td>Weeks 10–12</td>
                <td>25.00%</td>
                <td><strong>BD 1,022.727</strong></td>
                <td>Delivery of Locker Registry, Digital Document Vault, CR Renewal Alerts & Final Multi-Branch Sign-off</td>
              </tr>
              <tr class="total-row">
                <td><strong>Total Milestone Project Cost</strong></td>
                <td><strong>Complete Module 6 ERP Scope Delivery</strong></td>
                <td><strong>12 Weeks</strong></td>
                <td><strong>100.00%</strong></td>
                <td><strong>BD 4,090.909</strong></td>
                <td><strong>Formal Acceptance & Sign-off</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Section 6: Governance, SLA, Terms -->
      <section class="doc-section" id="governance-sla">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 6.0</span>
            <h2 class="section-title">Working Calendar, SLA, 15-Day Grace Period & Legal Terms</h2>
          </div>
          <span class="section-badge">Governance Framework</span>
        </div>

        <div class="grid-2">
          <div class="feature-card">
            <div class="feature-title"><i class="fas fa-calendar-check" style="color: var(--accent);"></i> Working Calendar & Team Hours</div>
            <div class="feature-desc">
              Development operates on a 5-day standard work week (Sunday to Thursday, 09:00 to 18:00 AST), aligning with GCC financial business hours. Sprint demos are scheduled at the end of each 3-week milestone.
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title"><i class="fas fa-clock" style="color: var(--success);"></i> 15-Day Milestone Review & Grace Period</div>
            <div class="feature-desc">
              Client is granted a formal 15-calendar-day review window following each sprint deployment to verify deliverables and audit tracking before milestone invoice closure.
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title"><i class="fas fa-shield-virus" style="color: #2563eb;"></i> SLA & Defect Severity Matrix</div>
            <div class="feature-desc">
              Critical Asset/Document Security Blockers (Severity 1) resolved within 4 hours; Major Functional Defects (Severity 2) within 24 hours; Minor UI adjustments (Severity 3) within 3 business days.
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title"><i class="fas fa-file-contract" style="color: var(--gray-700);"></i> Scope Control & Document Security</div>
            <div class="feature-desc">
              Features adhere strictly to the 25-page specifications in DOC-006. All legal document uploads and sensitive vehicle records are encrypted with AES-256 for corporate confidentiality.
            </div>
          </div>
        </div>
      </section>

      <!-- Section 7: Digital Sign-Off -->
      <section class="doc-section" id="digital-signoff">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 7.0</span>
            <h2 class="section-title">Stakeholder Authorization & Sign-Off</h2>
          </div>
          <span class="section-badge">Digital Verification</span>
        </div>

        <p>
          By digitally endorsing this Milestone & Payment Structure document, all parties confirm adherence to the deliverables, 12-week timeline, and financial schedule defined for <strong>SL-POP-ERP-MS-006</strong>:
        </p>

        <div class="signoff-box-container">
          
          <!-- Prepared By -->
          <div class="signoff-card" id="card_prepared">
            <div class="signoff-role">DEVELOPER / ARCHITECT</div>
            <div class="signoff-person">Ancy Varghese Thekkan<br><small>Software Architect, SaNDS Lab</small></div>
            <div class="sig-display-area" id="sig_area_developer">
              <span class="badge-tag badge-success"><i class="fas fa-check"></i> Prepared (18-June-2026)</span>
            </div>
            <span class="signoff-status-badge status-signed">COMPLETED</span>
          </div>

          <!-- Verified By -->
          <div class="signoff-card" id="card_verified">
            <div class="signoff-role">VERIFIED BY (DEVELOPER)</div>
            <div class="signoff-person">Ajit Kumar KV<br><small>CEO & Managing Director, SaNDS Lab</small></div>
            <div class="sig-display-area" id="sig_area_verified">
              <span class="badge-tag badge-success"><i class="fas fa-check"></i> Verified (04-July-2026)</span>
            </div>
            <span class="signoff-status-badge status-signed">CHECKED & VERIFIED</span>
          </div>

          <!-- Consultant Review -->
          <div class="signoff-card" id="card_consultant">
            <div class="signoff-role">CONSULTANT REVIEW</div>
            <div class="signoff-person">UniGlobal Business Solutions<br><small>Project Management Consultant</small></div>
            <div class="sig-display-area" id="sig_area_consultant">
              <span class="badge-tag badge-primary"><i class="fas fa-clock"></i> Pending Review</span>
            </div>
            <span class="signoff-status-badge status-pending" id="badge_consultant">IN REVIEW</span>
            <button class="btn btn-outline" style="margin-top: 8px; font-size: 11px;" onclick="openSignModal('consultant', 'UniGlobal Consultant')">
              <i class="fas fa-pen-nib"></i> Sign as Consultant
            </button>
          </div>

          <!-- Client Approval -->
          <div class="signoff-card" id="card_client">
            <div class="signoff-role">CLIENT APPROVAL</div>
            <div class="signoff-person">Popular Auto Spare & A/C Parts<br><small>Authorized Executive Signatory</small></div>
            <div class="sig-display-area" id="sig_area_client">
              <span class="badge-tag badge-primary"><i class="fas fa-clock"></i> Pending Approval</span>
            </div>
            <span class="signoff-status-badge status-pending" id="badge_client">PENDING SIGNATURE</span>
            <button class="btn btn-accent" style="margin-top: 8px; font-size: 11px;" onclick="openSignModal('client', 'Popular Executive Signatory')">
              <i class="fas fa-file-signature"></i> Sign Document
            </button>
          </div>

        </div>
      </section>

    </main>
  </div>

  <!-- Signature Modal -->
  <div class="modal-overlay" id="signModal">
    <div class="modal-box">
      <div class="modal-header">
        <h3 class="modal-title" id="modalSignTitle">Digital Endorsement</h3>
        <button class="modal-close" onclick="closeSignModal()">&times;</button>
      </div>
      <form id="signForm" onsubmit="handleSignatureSubmit(event)">
        <input type="hidden" id="modal_role" name="role" value="">
        <div style="margin-bottom: 14px;">
          <label style="display: block; font-size: 12px; font-weight: 700; color: var(--gray-700); margin-bottom: 4px;">Signatory Full Name</label>
          <input type="text" id="signer_name" required style="width: 100%; padding: 10px; border-radius: var(--radius-sm); border: 1px solid var(--gray-300); font-size: 13px;">
        </div>
        <div style="margin-bottom: 14px;">
          <label style="display: block; font-size: 12px; font-weight: 700; color: var(--gray-700); margin-bottom: 4px;">Signatory Designation</label>
          <input type="text" id="signer_designation" required style="width: 100%; padding: 10px; border-radius: var(--radius-sm); border: 1px solid var(--gray-300); font-size: 13px;">
        </div>
        <div style="margin-bottom: 14px;">
          <label style="display: block; font-size: 12px; font-weight: 700; color: var(--gray-700); margin-bottom: 4px;">Draw Digital Signature</label>
          <canvas id="sigCanvas" class="signature-pad"></canvas>
          <button type="button" class="btn btn-outline" style="margin-top: 6px; padding: 4px 10px; font-size: 11px;" onclick="clearSignatureCanvas()">Clear Canvas</button>
        </div>
        <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;">
          <button type="button" class="btn btn-outline" onclick="closeSignModal()">Cancel</button>
          <button type="submit" class="btn btn-primary" id="btnSubmitSign">Confirm & Apply Signature</button>
        </div>
      </form>
    </div>
  </div>

  <script>
    // Smooth Scroll Spy for Navigation
    const navLinks = document.querySelectorAll('.sidebar-menu li a');
    const sections = document.querySelectorAll('.doc-section, .hero-card');

    window.addEventListener('scroll', () => {{
      let current = '';
      sections.forEach(section => {{
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= (sectionTop - 120)) {{
          current = section.getAttribute('id');
        }}
      }});

      navLinks.forEach(link => {{
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${{current}}`) {{
          link.classList.add('active');
        }}
      }});
    }});

    // Signature Pad logic
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

    canvas.addEventListener('mousedown', (e) => {{
      isDrawing = true;
      ctx.beginPath();
      ctx.moveTo(e.offsetX, e.offsetY);
    }});

    canvas.addEventListener('mousemove', (e) => {{
      if (isDrawing) {{
        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
      }}
    }});

    canvas.addEventListener('mouseup', () => isDrawing = false);
    canvas.addEventListener('mouseleave', () => isDrawing = false);

    // Touch support for mobile signature
    canvas.addEventListener('touchstart', (e) => {{
      e.preventDefault();
      const rect = canvas.getBoundingClientRect();
      const touch = e.touches[0];
      isDrawing = true;
      ctx.beginPath();
      ctx.moveTo(touch.clientX - rect.left, touch.clientY - rect.top);
    }});

    canvas.addEventListener('touchmove', (e) => {{
      e.preventDefault();
      if (isDrawing) {{
        const rect = canvas.getBoundingClientRect();
        const touch = e.touches[0];
        ctx.lineTo(touch.clientX - rect.left, touch.clientY - rect.top);
        ctx.stroke();
      }}
    }});

    canvas.addEventListener('touchend', () => isDrawing = false);

    function clearSignatureCanvas() {{
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }}

    function openSignModal(role, title) {{
      document.getElementById('modal_role').value = role;
      document.getElementById('modalSignTitle').textContent = 'Endorse as ' + title;
      document.getElementById('signModal').style.display = 'flex';
      setTimeout(resizeCanvas, 50);
    }}

    function closeSignModal() {{
      document.getElementById('signModal').style.display = 'none';
      clearSignatureCanvas();
    }}

    function handleSignatureSubmit(e) {{
      e.preventDefault();
      const role = document.getElementById('modal_role').value;
      const name = document.getElementById('signer_name').value;
      const designation = document.getElementById('signer_designation').value;
      const sigData = canvas.toDataURL('image/png');

      const formData = new FormData();
      formData.append('action', 'sign_milestone');
      formData.append('role', role);
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
          alert('Signature successfully applied to SL-POP-ERP-MS-006!');
          window.location.reload();
        }} else {{
          alert('Error: ' + data.message);
          document.getElementById('btnSubmitSign').disabled = false;
          document.getElementById('btnSubmitSign').textContent = 'Confirm & Apply Signature';
        }}
      }})
      .catch(err => {{
        alert('Network or server error: ' + err);
        document.getElementById('btnSubmitSign').disabled = false;
        document.getElementById('btnSubmitSign').textContent = 'Confirm & Apply Signature';
      }});
    }}

    // Load existing signatures on page load
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

# 1. Save HTML to SL-POP-ERP-MS-006.html and Administration_Milestone_and_Payment_Structure.html
html_path_1 = os.path.join(BASE_DIR, 'SL-POP-ERP-MS-006.html')
html_path_2 = os.path.join(BASE_DIR, 'Administration_Milestone_and_Payment_Structure.html')
with open(html_path_1, 'w', encoding='utf-8') as f:
    f.write(html_content)
with open(html_path_2, 'w', encoding='utf-8') as f:
    f.write(html_content)

# Copy to popular/ folder
popular_html_1 = os.path.join(BASE_DIR, 'popular', 'SL-POP-ERP-MS-006.html')
popular_html_2 = os.path.join(BASE_DIR, 'popular', 'Administration_Milestone_and_Payment_Structure.html')
shutil.copyfile(html_path_1, popular_html_1)
shutil.copyfile(html_path_1, popular_html_2)

print('Generated and distributed HTML files.')

# 2. Render through PHP and generate PDF with Chrome Headless
rendered_html_path = os.path.join(BASE_DIR, 'rendered_ms006.html')
with open(rendered_html_path, 'w', encoding='utf-8') as rf:
    subprocess.run(['php', '-f', html_path_1], stdout=rf, check=True, cwd=BASE_DIR)

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
pdf_output_root_1 = os.path.join(BASE_DIR, 'SL-POP-ERP-MS-006.pdf')
pdf_output_root_2 = os.path.join(BASE_DIR, 'Administration_Milestone_and_Payment_Structure.pdf')

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
print('PDF conversion exit code:', res.returncode)

if os.path.exists(rendered_html_path):
    os.remove(rendered_html_path)

shutil.copyfile(pdf_output_root_1, pdf_output_root_2)

# Copy to popular/ folder
popular_pdf_1 = os.path.join(BASE_DIR, 'popular', 'SL-POP-ERP-MS-006.pdf')
popular_pdf_2 = os.path.join(BASE_DIR, 'popular', 'Administration_Milestone_and_Payment_Structure.pdf')
shutil.copyfile(pdf_output_root_1, popular_pdf_1)
shutil.copyfile(pdf_output_root_1, popular_pdf_2)

print('Distributed PDF files successfully.')

# 3. Open PDF with PyMuPDF to check pages
doc = fitz.open(pdf_output_root_1)
print(f'Generated PDF Page Count: {len(doc)}')
for i, page in enumerate(doc):
    print(f'Page {i+1} text length: {len(page.get_text())}')
    pix = page.get_pixmap(dpi=150)
    pix.save(os.path.join(BASE_DIR, f'scratch/ms006_page_{i+1}.png'))

print('All pages preview images saved.')

# 4. Insert into SQLite .auth_portal.db
db_paths = [os.path.join(BASE_DIR, '.auth_portal.db'), os.path.join(BASE_DIR, 'popular', '.auth_portal.db')]
for db_p in db_paths:
    if os.path.exists(db_p):
        try:
            conn = sqlite3.connect(db_p)
            cur = conn.cursor()
            cur.execute("INSERT OR REPLACE INTO document_meta (doc_id, title, status) VALUES (?, ?, ?)",
                        ('SL-POP-ERP-MS-006', 'Module 6: Enterprise Administration, Facility, Fixed Assets, Fleet & Document Control Milestone', 'IN_REVIEW'))
            conn.commit()
            conn.close()
            print(f'Updated document_meta in {db_p}')
        except Exception as e:
            print(f'DB update error for {db_p}:', e)
