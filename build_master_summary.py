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
// PHP Backend for Digital Signature & Finalization API (SL-POP-ERP-SUMMARY-001)
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

$doc_id = 'SL-POP-ERP-SUMMARY-001';

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
                $ins_stmt->execute(array($doc_id, 'Master Executive Milestone Summary & Complete 9-Module Budgeting Roadmap'));
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
            
            echo json_encode(array('success' => true, 'message' => 'Master Summary Signature recorded successfully!', 'signed_at' => $now));
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
  <title>SL-POP-ERP-SUMMARY-001 | Master Executive Milestone Summary & Complete 9-Module Budgeting Roadmap</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  
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
      padding: 30px 40px;
      border-bottom: 4px solid var(--accent);
      position: relative;
    }}

    .header-content {{
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
    }}

    .header-logos {{
      display: flex;
      align-items: center;
      gap: 20px;
    }}

    .header-logos img {{
      height: 48px;
      object-fit: contain;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }}

    .header-logos .divider-line {{
      width: 1px;
      height: 40px;
      background: rgba(255, 255, 255, 0.25);
    }}

    .doc-meta-badge {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 8px 16px;
      border-radius: var(--radius-md);
      text-align: right;
    }}

    .doc-meta-badge .doc-ref {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: var(--accent-gold);
      font-weight: 600;
      display: block;
    }}

    .doc-meta-badge .doc-date {{
      font-size: 11px;
      color: var(--gray-300);
    }}

    /* Container */
    .container {{
      max-width: 1200px;
      margin: 30px auto 60px auto;
      padding: 0 20px;
    }}

    /* Hero Card */
    .hero-card {{
      background: var(--white);
      border-radius: var(--radius-lg);
      padding: 35px 40px;
      box-shadow: var(--shadow-md);
      margin-bottom: 30px;
      border: 1px solid var(--gray-200);
      position: relative;
      overflow: hidden;
    }}

    .hero-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 6px;
      height: 100%;
      background: linear-gradient(to bottom, var(--primary), var(--accent));
    }}

    .hero-badge-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1e40af;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 15px;
    }}

    .hero-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 28px;
      font-weight: 800;
      color: var(--dark);
      line-height: 1.25;
      margin-bottom: 10px;
    }}

    .hero-subtitle {{
      font-size: 15px;
      color: var(--gray-600);
      margin-bottom: 25px;
      max-width: 950px;
      line-height: 1.6;
    }}

    .hero-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 15px;
      margin-top: 20px;
      padding-top: 20px;
      border-top: 1px solid var(--gray-200);
    }}

    .hero-stat-box {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-md);
      padding: 14px 18px;
    }}

    .hero-stat-box .label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--gray-500);
      font-weight: 600;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .hero-stat-box .value {{
      font-family: 'Outfit', sans-serif;
      font-size: 20px;
      font-weight: 800;
      color: var(--primary);
    }}

    .hero-stat-box .subvalue {{
      font-size: 11px;
      color: var(--gray-500);
      margin-top: 2px;
    }}

    /* Stat Cards Row */
    .stat-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin-bottom: 30px;
    }}

    @media (max-width: 900px) {{
      .stat-row {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 550px) {{
      .stat-row {{ grid-template-columns: 1fr; }}
    }}

    .stat-card {{
      background: var(--white);
      border-radius: var(--radius-lg);
      padding: 22px;
      border: 1px solid var(--gray-200);
      box-shadow: var(--shadow-sm);
      display: flex;
      align-items: flex-start;
      gap: 16px;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .stat-card:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }}

    .stat-icon {{
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      flex-shrink: 0;
    }}

    .icon-navy {{ background: #e0e7ff; color: #4338ca; }}
    .icon-amber {{ background: #fef3c7; color: #d97706; }}
    .icon-emerald {{ background: #dcfce7; color: #059669; }}
    .icon-blue {{ background: #dbeafe; color: #2563eb; }}

    .stat-info .stat-num {{
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      font-weight: 800;
      color: var(--dark);
      line-height: 1.1;
    }}

    .stat-info .stat-title {{
      font-size: 12px;
      font-weight: 600;
      color: var(--gray-500);
      margin-top: 4px;
    }}

    .stat-info .stat-desc {{
      font-size: 11px;
      color: var(--gray-400);
      margin-top: 2px;
    }}

    /* Section Cards */
    .section-card {{
      background: var(--white);
      border-radius: var(--radius-lg);
      padding: 30px;
      margin-bottom: 30px;
      border: 1px solid var(--gray-200);
      box-shadow: var(--shadow-sm);
    }}

    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 22px;
      padding-bottom: 14px;
      border-bottom: 2px solid var(--gray-100);
    }}

    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 20px;
      font-weight: 700;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .section-title i {{
      color: var(--accent);
      font-size: 18px;
    }}

    .section-subtitle {{
      font-size: 13px;
      color: var(--gray-500);
      margin-top: 3px;
    }}

    /* Visual Charts Grid */
    .charts-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 25px;
      margin-bottom: 25px;
    }}

    @media (max-width: 850px) {{
      .charts-grid {{ grid-template-columns: 1fr; }}
    }}

    .chart-box {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-md);
      padding: 20px;
      position: relative;
    }}

    .chart-box-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 15px;
      font-weight: 700;
      color: var(--dark);
      margin-bottom: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .chart-wrapper {{
      position: relative;
      height: 280px;
      width: 100%;
    }}

    /* Module Card Grid */
    .modules-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 20px;
      margin-top: 10px;
    }}

    .mod-card {{
      background: var(--white);
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-md);
      padding: 22px;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
    }}

    .mod-card:hover {{
      border-color: var(--accent);
      box-shadow: var(--shadow-md);
      transform: translateY(-3px);
    }}

    .mod-card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }}

    .mod-tag {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      background: var(--primary);
      color: var(--white);
      padding: 3px 8px;
      border-radius: 4px;
    }}

    .mod-cost-tag {{
      font-family: 'Outfit', sans-serif;
      font-size: 15px;
      font-weight: 800;
      color: var(--accent);
      background: #fef3c7;
      padding: 3px 10px;
      border-radius: 6px;
    }}

    .mod-name {{
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: var(--dark);
      margin-bottom: 8px;
      line-height: 1.3;
    }}

    .mod-desc {{
      font-size: 12px;
      color: var(--gray-600);
      margin-bottom: 15px;
      line-height: 1.5;
      flex-grow: 1;
    }}

    .mod-meta-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px dashed var(--gray-200);
      font-size: 11px;
      color: var(--gray-500);
    }}

    .mod-link-btn {{
      font-size: 11px;
      font-weight: 700;
      color: var(--primary);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: color 0.2s ease;
    }}

    .mod-link-btn:hover {{
      color: var(--accent);
    }}

    /* Custom Tables */
    .table-container {{
      overflow-x: auto;
      margin: 15px 0 20px 0;
      border-radius: var(--radius-md);
      border: 1px solid var(--gray-200);
    }}

    table.master-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
      text-align: left;
    }}

    table.master-table thead {{
      background: var(--primary);
      color: var(--white);
    }}

    table.master-table th {{
      padding: 12px 14px;
      font-weight: 600;
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 2px solid var(--accent);
    }}

    table.master-table td {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--gray-200);
      vertical-align: middle;
    }}

    table.master-table tbody tr:nth-child(even) {{
      background: #f8fafc;
    }}

    table.master-table tbody tr:hover {{
      background: #eff6ff;
    }}

    table.master-table tfoot {{
      background: var(--dark);
      color: var(--white);
      font-weight: 700;
    }}

    table.master-table tfoot td {{
      padding: 14px;
      font-size: 13.5px;
      border-top: 2px solid var(--accent);
    }}

    .currency-bhd {{
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
    }}

    /* Milestone Phase Accordion Cards */
    .phase-module-box {{
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-md);
      margin-bottom: 16px;
      overflow: hidden;
      background: var(--white);
    }}

    .phase-module-header {{
      background: #f8fafc;
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      border-bottom: 1px solid var(--gray-200);
      transition: background 0.2s ease;
    }}

    .phase-module-header:hover {{
      background: #f1f5f9;
    }}

    .phase-title-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .phase-title-text {{
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 14px;
      color: var(--dark);
    }}

    .phase-pills {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .phase-grid {{
      padding: 18px 20px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 15px;
      background: var(--white);
    }}

    .phase-item-card {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-sm);
      padding: 12px 14px;
      border-left: 3px solid var(--primary);
    }}

    .phase-item-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }}

    .phase-item-tag {{
      font-size: 10px;
      font-weight: 700;
      color: var(--primary);
      text-transform: uppercase;
    }}

    .phase-item-amt {{
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 11px;
      color: var(--accent);
    }}

    .phase-item-desc {{
      font-size: 11.5px;
      color: var(--gray-700);
      line-height: 1.4;
      margin-bottom: 6px;
    }}

    .phase-item-time {{
      font-size: 10px;
      color: var(--gray-500);
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    /* Resource Rate Card Banner */
    .rate-card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 15px;
      margin: 15px 0;
    }}

    .rate-box {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-md);
      padding: 16px;
      text-align: center;
    }}

    .rate-box .role-name {{
      font-weight: 700;
      font-size: 13px;
      color: var(--dark);
      margin-bottom: 6px;
    }}

    .rate-box .bhd-val {{
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 800;
      color: var(--primary);
    }}

    .rate-box .bhd-sub {{
      font-size: 11px;
      color: var(--gray-600);
      margin-top: 3px;
      font-family: 'JetBrains Mono', monospace;
    }}

    .rate-box .alloc-val {{
      display: inline-block;
      margin-top: 8px;
      background: #e2e8f0;
      color: var(--gray-700);
      font-size: 10px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 4px;
    }}

    /* Total Cost Highlight Box */
    .total-cost-hero-box {{
      background: linear-gradient(135deg, #07192c 0%, #0a2540 100%);
      border: 2px solid var(--accent);
      border-radius: var(--radius-lg);
      padding: 25px 30px;
      color: #ffffff;
      margin: 20px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }}

    .total-cost-left {{
      max-width: 650px;
    }}

    .total-cost-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: var(--accent-gold);
      margin-bottom: 6px;
    }}

    .total-cost-desc {{
      font-size: 13px;
      color: var(--gray-300);
      line-height: 1.5;
    }}

    .total-cost-right {{
      text-align: right;
    }}

    .total-cost-amt {{
      font-family: 'Outfit', sans-serif;
      font-size: 32px;
      font-weight: 900;
      color: #ffffff;
      line-height: 1.1;
    }}

    .total-cost-words {{
      font-size: 11px;
      color: var(--accent-gold);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 600;
      margin-top: 4px;
    }}

    /* Terms & Governance */
    .terms-box {{
      background: #f8fafc;
      border-left: 4px solid var(--accent);
      padding: 20px;
      border-radius: var(--radius-md);
      margin: 20px 0;
    }}

    .terms-box h4 {{
      font-family: 'Outfit', sans-serif;
      color: var(--dark);
      font-size: 15px;
      margin-bottom: 8px;
    }}

    .terms-box ul {{
      padding-left: 20px;
      font-size: 12.5px;
      color: var(--gray-700);
      line-height: 1.6;
    }}

    /* Sign-off Section */
    .signoff-section {{
      background: var(--white);
      border-radius: var(--radius-lg);
      padding: 35px 40px;
      border: 1px solid var(--gray-200);
      box-shadow: var(--shadow-md);
      margin-top: 40px;
    }}

    .signoff-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 25px;
      margin-top: 25px;
    }}

    @media (max-width: 850px) {{
      .signoff-grid {{ grid-template-columns: 1fr; }}
    }}

    .signoff-card {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .signoff-card-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      font-weight: 700;
      color: var(--dark);
      margin-bottom: 4px;
    }}

    .signoff-card-sub {{
      font-size: 11px;
      color: var(--gray-500);
      margin-bottom: 15px;
    }}

    .signoff-box-area {{
      height: 110px;
      background: var(--white);
      border: 1px dashed var(--gray-300);
      border-radius: var(--radius-sm);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin-bottom: 12px;
      overflow: hidden;
      padding: 5px;
      text-align: center;
    }}

    .signoff-box-area img {{
      max-height: 80px;
      max-width: 100%;
      object-fit: contain;
    }}

    .signoff-status-badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 10px;
    }}

    .status-pending {{
      background: #fef3c7;
      color: #b45309;
    }}

    .status-signed {{
      background: #dcfce7;
      color: #15803d;
    }}

    .btn-sign {{
      background: var(--primary);
      color: var(--white);
      border: none;
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      font-weight: 600;
      font-size: 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: background 0.2s ease;
      width: 100%;
    }}

    .btn-sign:hover {{
      background: var(--primary-light);
    }}

    /* Signature Modal */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(4px);
      z-index: 2000;
      align-items: center;
      justify-content: center;
    }}

    .modal-box {{
      background: var(--white);
      border-radius: var(--radius-lg);
      width: 90%;
      max-width: 500px;
      padding: 25px;
      box-shadow: var(--shadow-xl);
      border: 1px solid var(--gray-200);
    }}

    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--gray-200);
    }}

    .modal-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: var(--dark);
    }}

    .close-modal {{
      background: transparent;
      border: none;
      font-size: 18px;
      color: var(--gray-400);
      cursor: pointer;
    }}

    .sig-pad-canvas {{
      border: 1px solid var(--gray-300);
      border-radius: var(--radius-sm);
      background: #fafafa;
      width: 100%;
      height: 160px;
      touch-action: none;
      cursor: crosshair;
    }}

    .form-group {{
      margin-bottom: 12px;
    }}

    .form-group label {{
      display: block;
      font-size: 11px;
      font-weight: 600;
      color: var(--gray-700);
      margin-bottom: 4px;
      text-transform: uppercase;
    }}

    .form-control {{
      width: 100%;
      padding: 8px 12px;
      border: 1px solid var(--gray-300);
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-family: 'Inter', sans-serif;
    }}

    .modal-actions {{
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      margin-top: 15px;
    }}

    /* Footer */
    .doc-footer {{
      margin-top: 50px;
      padding-top: 20px;
      border-top: 1px solid var(--gray-300);
      font-size: 11px;
      color: var(--gray-500);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* Print Optimizations */
    @media print {{
      .web-action-bar, .modal-overlay, .btn-sign, .mod-link-btn {{
        display: none !important;
      }}
      body {{
        background: #ffffff;
        font-size: 11pt;
      }}
      .container {{
        max-width: 100%;
        margin: 0;
        padding: 0;
      }}
      .hero-card, .section-card, .stat-card, .signoff-section, .total-cost-hero-box {{
        box-shadow: none !important;
        border: 1px solid #ccc !important;
        page-break-inside: avoid;
      }}
      .charts-grid {{
        display: block !important;
      }}
      .chart-box {{
        page-break-inside: avoid;
        margin-bottom: 15px;
      }}
    }}
  </style>
</head>
<body>

  <!-- Web Action Bar -->
  <div class="web-action-bar">
    <div class="web-action-left">
      <a href="index.php" class="portal-branding">
        <i class="fa-solid fa-arrow-left"></i> Popular ERP Document Portal
      </a>
      <span class="badge-accent">Master Executive Summary</span>
      <span class="badge-success">Consolidated 9-Module Scope</span>
    </div>
    <div class="web-action-right">
      <button onclick="window.print()" class="btn btn-outline">
        <i class="fa-solid fa-print"></i> Print / Save PDF
      </button>
      <a href="SL-POP-ERP-SUMMARY-001.pdf" target="_blank" class="btn btn-accent">
        <i class="fa-solid fa-file-pdf"></i> Download Official Master PDF
      </a>
    </div>
  </div>

  <!-- Header Banner -->
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
        <span class="doc-ref">DOC ID: SL-POP-ERP-SUMMARY-001</span>
        <span class="doc-date">Consolidated Release: October 2026 &bull; Ver 1.0 Final</span>
      </div>
    </div>
  </div>

  <!-- Main Container -->
  <div class="container">

    <!-- Hero Card -->
    <div class="hero-card">
      <div class="hero-badge-pill">
        <i class="fa-solid fa-chart-line"></i> Master Executive Portfolio & Financial Roadmap
      </div>
      <h1 class="hero-title">Popular Auto Spare ERP — Complete 9-Module Master Milestone & Budget Summary</h1>
      <p class="hero-subtitle">
        Executive consolidated milestone breakdown, multi-module timeline mapping, engineering resource matrix, and grand commercial investment schedule for <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong>. Prepared by <strong>SaNDS Lab Middle East W.L.L</strong> in strategic alignment with <strong>UniGlobal Consultancy</strong>.
      </p>

      <div class="hero-grid">
        <div class="hero-stat-box">
          <div class="label"><i class="fa-solid fa-cubes"></i> Total Modules</div>
          <div class="value">9 Modules</div>
          <div class="subvalue">End-to-End Automotive ERP</div>
        </div>
        <div class="hero-stat-box">
          <div class="label"><i class="fa-solid fa-money-bill-wave"></i> Total Investment</div>
          <div class="value" style="color: #d97706;">BD 34,090.910</div>
          <div class="subvalue">Fixed Baseline in Bahraini Dinars</div>
        </div>
        <div class="hero-stat-box">
          <div class="label"><i class="fa-solid fa-calendar-days"></i> Cumulative Effort</div>
          <div class="value">88 Weeks</div>
          <div class="subvalue">17.6 Engineering Months</div>
        </div>
        <div class="hero-stat-box">
          <div class="label"><i class="fa-solid fa-users-gear"></i> Dedicated Team</div>
          <div class="value">5 Specialists</div>
          <div class="subvalue">100% Dedicated Full-Time</div>
        </div>
        <div class="hero-stat-box">
          <div class="label"><i class="fa-solid fa-shield-check"></i> Verification Tranches</div>
          <div class="value">35 Gates</div>
          <div class="subvalue">Zero-Risk Milestones</div>
        </div>
      </div>
    </div>

    <!-- 4 Quick Stat Row -->
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-icon icon-navy"><i class="fa-solid fa-file-contract"></i></div>
        <div class="stat-info">
          <div class="stat-num">9 / 9</div>
          <div class="stat-title">Modules Documented</div>
          <div class="stat-desc">Complete functional & technical specs</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon icon-amber"><i class="fa-solid fa-coins"></i></div>
        <div class="stat-info">
          <div class="stat-num">BD 1,363.636</div>
          <div class="stat-title">Monthly Team Burn-Rate</div>
          <div class="stat-desc">Fixed transparent rate card</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon icon-emerald"><i class="fa-solid fa-code-branch"></i></div>
        <div class="stat-info">
          <div class="stat-num">100% Multi-Branch</div>
          <div class="stat-title">Enterprise Coverage</div>
          <div class="stat-desc">Warehouses, POS counters, mobile floor</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon icon-blue"><i class="fa-solid fa-award"></i></div>
        <div class="stat-info">
          <div class="stat-num">15-Day UAT</div>
          <div class="stat-title">Acceptance Grace SLA</div>
          <div class="stat-desc">Rigorous milestone verification</div>
        </div>
      </div>
    </div>

    <!-- Total Project Cost Callout -->
    <div class="total-cost-hero-box">
      <div class="total-cost-left">
        <div class="total-cost-title"><i class="fa-solid fa-hand-holding-dollar"></i> Total Fixed Project Investment (All 9 Modules)</div>
        <div class="total-cost-desc">
          Unified contract value covering the complete design, engineering, multi-branch testing, data migration, hardware integrations, training, and production deployment across all 9 modules for Popular Auto Spare & A/C Parts Co. W.L.L.
        </div>
      </div>
      <div class="total-cost-right">
        <div class="total-cost-amt">BD 34,090.910</div>
        <div class="total-cost-words">Thirty-Four Thousand Ninety Bahraini Dinars & 910 Fils</div>
      </div>
    </div>

    <!-- SECTION 1: Visual Graphical Analytics -->
    <div class="section-card">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-chart-pie"></i> Visual Milestone & Budget Analytics</div>
          <div class="section-subtitle">Visualizing budget distribution and engineering effort allocation across all 9 modules</div>
        </div>
        <span class="badge-accent">Interactive Visual Insights</span>
      </div>

      <div class="charts-grid">
        <div class="chart-box">
          <div class="chart-box-title">
            <span><i class="fa-solid fa-pie-chart"></i> Budget Distribution by Module (BHD)</span>
            <small style="font-size: 11px; color: var(--gray-500);">Total: BD 34,090.910</small>
          </div>
          <div class="chart-wrapper">
            <canvas id="budgetChart"></canvas>
          </div>
        </div>
        <div class="chart-box">
          <div class="chart-box-title">
            <span><i class="fa-solid fa-chart-bar"></i> Engineering Timeline by Module (Weeks)</span>
            <small style="font-size: 11px; color: var(--gray-500);">Total: 88 Working Weeks</small>
          </div>
          <div class="chart-wrapper">
            <canvas id="timelineChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- SECTION 2: Master Consolidated Milestone & Budget Table -->
    <div class="section-card">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-table-list"></i> Master 9-Module Budgeting & Milestone Matrix (BHD)</div>
          <div class="section-subtitle">At-a-glance comparative overview of all 9 modules, timelines, effort, deliverables, and total fees in Bahraini Dinars</div>
        </div>
        <span class="badge-success">All Amounts in Bahraini Dinars (BHD)</span>
      </div>

      <div class="table-container">
        <table class="master-table">
          <thead>
            <tr>
              <th style="width: 35px; text-align: center;">#</th>
              <th>Module Scope & Implementation Domain</th>
              <th>Timeline</th>
              <th>Effort</th>
              <th>Milestone Gates</th>
              <th>Total Cost (BHD)</th>
              <th>Weekly Burn</th>
              <th>Share (%)</th>
              <th style="text-align: center;">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">1</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-001</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-001 v1.0</span>
                </div>
                <div class="mod-domain-title">PCode Generation, Cataloguing & Item Master Engine</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">10 Weeks</span></td>
              <td>2.50 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 3,409.091</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">10.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-001.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">2</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-002</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-002 v1.0</span>
                </div>
                <div class="mod-domain-title">Vendor & Purchase Management, Supplier Portal & 3-Way Match</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">12 Weeks</span></td>
              <td>3.00 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 4,090.909</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">12.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-002.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">3</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-003</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-003 v1.0</span>
                </div>
                <div class="mod-domain-title">Store Verification, Multi-Warehouse Stock & Location Matrix</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">15 Weeks</span></td>
              <td>3.75 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 5,113.636</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">15.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-003.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">4</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-004</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-004 v1.0</span>
                </div>
                <div class="mod-domain-title">Sales Process, Mobile POS, Multi-Branch Billing & Return Control</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">15 Weeks</span></td>
              <td>3.75 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 5,113.636</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">15.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-004.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">5</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-005</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-005 v1.0</span>
                </div>
                <div class="mod-domain-title">Accounting & Financial Management, General Ledger, AP/AR & VAT</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">13 Weeks</span></td>
              <td>3.25 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 4,431.818</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">13.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-005.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">6</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-006</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-006 v1.0</span>
                </div>
                <div class="mod-domain-title">Enterprise Administration, Facility, Fixed Assets, Fleet & Vault</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">12 Weeks</span></td>
              <td>3.00 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 4,090.909</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">12.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-006.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">7</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-007</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-007 v1.0</span>
                </div>
                <div class="mod-domain-title">Human Resource Management, Biometrics, Leave, Payroll & Gratuity</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">16 Weeks</span></td>
              <td>4.00 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 5,454.548</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">16.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-007.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">8</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-008</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: ARCH-001 v1.0</span>
                </div>
                <div class="mod-domain-title">Hardware Setup, Handheld QR Devices, ESC/POS & Cloud Cluster</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">3 Weeks</span></td>
              <td>0.75 Mo</td>
              <td><span class="gate-pill">3 Gates (33%)</span></td>
              <td><span class="currency-bhd">BD 1,022.727</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">3.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-008.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">9</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-009</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-009 v1.0</span>
                </div>
                <div class="mod-domain-title">Executive Management Dashboard, 8-Module BI & Mobile Cockpit</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">4 Weeks</span></td>
              <td>1.00 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 1,363.636</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">4.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-009.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="2"><strong>GRAND TOTAL: COMPLETE 9-MODULE AUTOMOTIVE ERP PORTFOLIO</strong></td>
              <td><strong>88 Weeks</strong></td>
              <td><strong>17.60 Mo</strong></td>
              <td><strong>35 Gates</strong></td>
              <td><span class="currency-bhd" style="font-size: 15px; color: var(--accent-gold);">BD 34,090.910</span></td>
              <td><strong>BD 387.397</strong></td>
              <td><strong>100.00%</strong></td>
              <td style="text-align: center;"><strong>Full Suite</strong></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>

    <!-- SECTION 3: Card Portfolio Grid with Key Architectural Scope -->
    <div class="section-card">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-layer-group"></i> 9-Module Architectural Scope & Deliverable Pillars</div>
          <div class="section-subtitle">Key functional scope, core modules, and business impact for Popular Auto Spare Co.</div>
        </div>
        <span class="badge-accent">Functional Portfolio</span>
      </div>

      <div class="modules-grid">
        <!-- Mod 1 -->
        <div class="mod-card">
          <div>
            <div class="mod-card-header">
              <span class="mod-tag">MODULE 1</span>
              <span class="mod-cost-tag">BD 3,409.091</span>
            </div>
            <div class="mod-name">PCode Generation & Universal Item Master</div>
            <div class="mod-desc">
              Automated smart PCode generation algorithms, multi-brand hierarchy (Car Make/Model/Year), 1-to-Many OEM cross-reference matrix, 50,000+ SKU legacy data cleansing, and sub-100ms multi-parameter fuzzy search.
            </div>
          </div>
          <div class="mod-meta-row">
            <span><i class="fa-solid fa-clock"></i> 10 Weeks (2.5 Mo)</span>
            <a href="SL-POP-ERP-MS-001.html" class="mod-link-btn" target="_blank">Full Doc <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>

        <!-- Mod 2 -->
        <div class="mod-card">
          <div>
            <div class="mod-card-header">
              <span class="mod-tag">MODULE 2</span>
              <span class="mod-cost-tag">BD 4,090.909</span>
            </div>
            <div class="mod-name">Vendor & Purchase Management with 3-Way Match</div>
            <div class="mod-desc">
              Multi-country vendor master, tokenized supplier RFQ portal, MOQ reorder buffering, CTO purchase approvals, automated PO splits by brand, Goods Receipt Note (GRN) with landed cost, and 3-way invoice matching.
            </div>
          </div>
          <div class="mod-meta-row">
            <span><i class="fa-solid fa-clock"></i> 12 Weeks (3.0 Mo)</span>
            <a href="SL-POP-ERP-MS-002.html" class="mod-link-btn" target="_blank">Full Doc <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>

        <!-- Mod 3 -->
        <div class="mod-card">
          <div>
            <div class="mod-card-header">
              <span class="mod-tag">MODULE 3</span>
              <span class="mod-cost-tag">BD 5,113.636</span>
            </div>
            <div class="mod-name">Store Verification & Multi-Warehouse Stock Control</div>
            <div class="mod-desc">
              5-tier warehouse spatial layout (Zone/Aisle/Rack/Shelf/Bin), handheld Android scanner engine, blind 60/40 cycle counts, inter-branch stock transfers (GIT) with driver signatures, and FIFO inventory valuation.
            </div>
          </div>
          <div class="mod-meta-row">
            <span><i class="fa-solid fa-clock"></i> 15 Weeks (3.75 Mo)</span>
            <a href="SL-POP-ERP-MS-003.html" class="mod-link-btn" target="_blank">Full Doc <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>

        <!-- Mod 4 -->
        <div class="mod-card">
          <div>
            <div class="mod-card-header">
              <span class="mod-tag">MODULE 4</span>
              <span class="mod-cost-tag">BD 5,113.636</span>
            </div>
            <div class="mod-name">Sales Process, Mobile POS & Branch Cash Control</div>
            <div class="mod-desc">
              High-speed counter POS, mobile Android handheld floor sales, dynamic QR cart handoff, credit customer credit-risk limits, verified invoice returns with condition grading, and End-of-Day cash drawer closing locks.
            </div>
          </div>
          <div class="mod-meta-row">
            <span><i class="fa-solid fa-clock"></i> 15 Weeks (3.75 Mo)</span>
            <a href="SL-POP-ERP-MS-004.html" class="mod-link-btn" target="_blank">Full Doc <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>

        <!-- Mod 5 -->
        <div class="mod-card">
          <div>
            <div class="mod-card-header">
              <span class="mod-tag">MODULE 5</span>
              <span class="mod-cost-tag">BD 4,431.818</span>
            </div>
            <div class="mod-name">Accounting, General Ledger, AP/AR & VAT Compliance</div>
            <div class="mod-desc">
              5-group Chart of Accounts (COA), real-time double-entry GL, automated AP/AR subledgers, multi-currency treasury, automated Bank Reconciliation (BRS), PDC management, and Bahrain NBR 10% VAT return filings.
            </div>
          </div>
          <div class="mod-meta-row">
            <span><i class="fa-solid fa-clock"></i> 13 Weeks (3.25 Mo)</span>
            <a href="SL-POP-ERP-MS-005.html" class="mod-link-btn" target="_blank">Full Doc <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>

        <!-- Mod 6 -->
        <div class="mod-card">
          <div>
            <div class="mod-card-header">
              <span class="mod-tag">MODULE 6</span>
              <span class="mod-cost-tag">BD 4,090.909</span>
            </div>
            <div class="mod-name">Enterprise Administration, Fixed Assets & Fleet</div>
            <div class="mod-desc">
              Centralized branch facility ticketing, fixed asset QR tagging with automated straight-line depreciation, company vehicle fleet logs with Total Cost of Ownership (TCO), and legal document expiry alerts (CR, Leases).
            </div>
          </div>
          <div class="mod-meta-row">
            <span><i class="fa-solid fa-clock"></i> 12 Weeks (3.0 Mo)</span>
            <a href="SL-POP-ERP-MS-006.html" class="mod-link-btn" target="_blank">Full Doc <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>

        <!-- Mod 7 -->
        <div class="mod-card">
          <div>
            <div class="mod-card-header">
              <span class="mod-tag">MODULE 7</span>
              <span class="mod-cost-tag">BD 5,454.548</span>
            </div>
            <div class="mod-name">HR Management, Biometrics, Payroll & Gratuity</div>
            <div class="mod-desc">
              Employee 360 master, physical biometric clock-in & geofenced mobile attendance, Bahrain Labour Law leave rules, automated monthly payroll engine, SIO/LMRA/WPS bank export, and End-of-Service Benefit (EOSB) settlements.
            </div>
          </div>
          <div class="mod-meta-row">
            <span><i class="fa-solid fa-clock"></i> 16 Weeks (4.0 Mo)</span>
            <a href="SL-POP-ERP-MS-007.html" class="mod-link-btn" target="_blank">Full Doc <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>

        <!-- Mod 8 -->
        <div class="mod-card">
          <div>
            <div class="mod-card-header">
              <span class="mod-tag">MODULE 8</span>
              <span class="mod-cost-tag">BD 1,022.727</span>
            </div>
            <div class="mod-name">Hardware Setup, Scanners, Printers & Cloud Cluster</div>
            <div class="mod-desc">
              3-tier cloud server architecture (Dev / Staging / Prod), RabbitMQ asynchronous background queue, Android PDA scanner listeners, ESC/POS thermal receipt & barcode label printers, and biometric sync daemons.
            </div>
          </div>
          <div class="mod-meta-row">
            <span><i class="fa-solid fa-clock"></i> 3 Weeks (0.75 Mo)</span>
            <a href="SL-POP-ERP-MS-008.html" class="mod-link-btn" target="_blank">Full Doc <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>

        <!-- Mod 9 -->
        <div class="mod-card">
          <div>
            <div class="mod-card-header">
              <span class="mod-tag">MODULE 9</span>
              <span class="mod-cost-tag">BD 1,363.636</span>
            </div>
            <div class="mod-name">Executive Management Dashboard & BI Cockpit</div>
            <div class="mod-desc">
              OLAP data warehouse aggregation engine, real-time KPI metrics across all 8 modules, automated anomaly detection, daily 7:00 AM WhatsApp/Email executive digest, and secure C-Suite mobile executive reporting.
            </div>
          </div>
          <div class="mod-meta-row">
            <span><i class="fa-solid fa-clock"></i> 4 Weeks (1.0 Mo)</span>
            <a href="SL-POP-ERP-MS-009.html" class="mod-link-btn" target="_blank">Full Doc <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>
      </div>
    </div>

    <!-- SECTION 4: Comprehensive Milestone Tranches Breakdown (Phase by Phase) -->
    <div class="section-card">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-list-check"></i> Complete 35 Milestone Tranches Detailed Breakdown (BHD)</div>
          <div class="section-subtitle">Specific milestone gates, percentages, exact BHD allocations, and payment triggers for each phase</div>
        </div>
        <span class="badge-accent">35 Milestone Tranches</span>
      </div>

      <!-- Module 1 Accordion -->
      <div class="phase-module-box">
        <div class="phase-module-header" onclick="togglePhase('p1')">
          <div class="phase-title-left">
            <span class="mod-tag">MOD 1</span>
            <span class="phase-title-text">Module 1: PCode Generation & Item Master Engine (10 Weeks)</span>
          </div>
          <div class="phase-pills">
            <span class="mod-cost-tag">BD 3,409.091</span>
            <i class="fa-solid fa-chevron-down" id="p1_icon"></i>
          </div>
        </div>
        <div class="phase-grid" id="p1_content">
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 1.1 (25%)</span>
              <span class="phase-item-amt">BD 852.273</span>
            </div>
            <div class="phase-item-desc">PCode DB Schema, Data Cleansing Engine & Base Generation Algorithm.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 1–3</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 1.2 (25%)</span>
              <span class="phase-item-amt">BD 852.273</span>
            </div>
            <div class="phase-item-desc">Brand / Model / Spec Dynamic Hierarchy & Automated PCode Generator Engine.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 4–5</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 1.3 (25%)</span>
              <span class="phase-item-amt">BD 852.273</span>
            </div>
            <div class="phase-item-desc">Universal Cross-Reference / Interchange Matrix & Barcode Tagging Engine.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 6–8</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 1.4 (25%)</span>
              <span class="phase-item-amt">BD 852.273</span>
            </div>
            <div class="phase-item-desc">Real-Time Search, Legacy Migration (50,000+ SKUs) & Multi-Branch Final UAT.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 9–10</div>
          </div>
        </div>
      </div>

      <!-- Module 2 Accordion -->
      <div class="phase-module-box">
        <div class="phase-module-header" onclick="togglePhase('p2')">
          <div class="phase-title-left">
            <span class="mod-tag">MOD 2</span>
            <span class="phase-title-text">Module 2: Vendor & Purchase Management (12 Weeks)</span>
          </div>
          <div class="phase-pills">
            <span class="mod-cost-tag">BD 4,090.909</span>
            <i class="fa-solid fa-chevron-down" id="p2_icon"></i>
          </div>
        </div>
        <div class="phase-grid" id="p2_content">
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 2.1 (25%)</span>
              <span class="phase-item-amt">BD 1,022.727</span>
            </div>
            <div class="phase-item-desc">Supplier Master, Tokenized Vendor Portal & Automated RFQ Engine.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 1–3</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 2.2 (25%)</span>
              <span class="phase-item-amt">BD 1,022.727</span>
            </div>
            <div class="phase-item-desc">Multi-Vendor Quotation Evaluation Matrix & Automated PO Split Engine.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 4–6</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 2.3 (25%)</span>
              <span class="phase-item-amt">BD 1,022.727</span>
            </div>
            <div class="phase-item-desc">Goods Receipt Note (GRN), Multi-Currency Landed Cost & QC Inspection.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 7–9</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 2.4 (25%)</span>
              <span class="phase-item-amt">BD 1,022.727</span>
            </div>
            <div class="phase-item-desc">3-Way Invoice Matching, Vendor SLA Scorecards & Multi-Branch Sign-Off.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 10–12</div>
          </div>
        </div>
      </div>

      <!-- Module 3 Accordion -->
      <div class="phase-module-box">
        <div class="phase-module-header" onclick="togglePhase('p3')">
          <div class="phase-title-left">
            <span class="mod-tag">MOD 3</span>
            <span class="phase-title-text">Module 3: Store Verification & Stock Control (15 Weeks)</span>
          </div>
          <div class="phase-pills">
            <span class="mod-cost-tag">BD 5,113.636</span>
            <i class="fa-solid fa-chevron-down" id="p3_icon"></i>
          </div>
        </div>
        <div class="phase-grid" id="p3_content">
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 3.1 (25%)</span>
              <span class="phase-item-amt">BD 1,278.409</span>
            </div>
            <div class="phase-item-desc">Warehouse Spatial Hierarchy (5 Tiers), Bin Matrix & Inward PVN Setup.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 1–4</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 3.2 (25%)</span>
              <span class="phase-item-amt">BD 1,278.409</span>
            </div>
            <div class="phase-item-desc">Handheld Scanner Engine, Blind 60/40 Cycle Counts & Variance Alerts.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 5–8</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 3.3 (25%)</span>
              <span class="phase-item-amt">BD 1,278.409</span>
            </div>
            <div class="phase-item-desc">Inter-Branch Stock Transfers (GIT), Multi-Tier Discrepancy & FIFO Valuation.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 9–12</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 3.4 (25%)</span>
              <span class="phase-item-amt">BD 1,278.409</span>
            </div>
            <div class="phase-item-desc">Min/Max Safety Stock Auto-Replenishment, Aging & Final Warehouse Sign-Off.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 13–15</div>
          </div>
        </div>
      </div>

      <!-- Module 4 Accordion -->
      <div class="phase-module-box">
        <div class="phase-module-header" onclick="togglePhase('p4')">
          <div class="phase-title-left">
            <span class="mod-tag">MOD 4</span>
            <span class="phase-title-text">Module 4: Sales Process, POS & Branch Financial Control (15 Weeks)</span>
          </div>
          <div class="phase-pills">
            <span class="mod-cost-tag">BD 5,113.636</span>
            <i class="fa-solid fa-chevron-down" id="p4_icon"></i>
          </div>
        </div>
        <div class="phase-grid" id="p4_content">
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 4.1 (25%)</span>
              <span class="phase-item-amt">BD 1,278.409</span>
            </div>
            <div class="phase-item-desc">Multi-Branch POS Architecture, Offline Sync & Cash Drawer Session Control.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 1–4</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 4.2 (25%)</span>
              <span class="phase-item-amt">BD 1,278.409</span>
            </div>
            <div class="phase-item-desc">Counter & Mobile Handheld POS Billing, Multi-Price Matrix & Barcodes.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 5–8</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 4.3 (25%)</span>
              <span class="phase-item-amt">BD 1,278.409</span>
            </div>
            <div class="phase-item-desc">Credit Customer Governance, Credit Limit Locks, Delivery Notes & B2B Invoices.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 9–12</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 4.4 (25%)</span>
              <span class="phase-item-amt">BD 1,278.409</span>
            </div>
            <div class="phase-item-desc">Verified Sales Returns, End-of-Day Branch Reconciliation & Audit UAT.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 13–15</div>
          </div>
        </div>
      </div>

      <!-- Module 5 Accordion -->
      <div class="phase-module-box">
        <div class="phase-module-header" onclick="togglePhase('p5')">
          <div class="phase-title-left">
            <span class="mod-tag">MOD 5</span>
            <span class="phase-title-text">Module 5: Accounting & Financial Management (13 Weeks)</span>
          </div>
          <div class="phase-pills">
            <span class="mod-cost-tag">BD 4,431.818</span>
            <i class="fa-solid fa-chevron-down" id="p5_icon"></i>
          </div>
        </div>
        <div class="phase-grid" id="p5_content">
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 5.1 (25%)</span>
              <span class="phase-item-amt">BD 1,107.955</span>
            </div>
            <div class="phase-item-desc">Dynamic Chart of Accounts (COA), Cost Centers & Auto Journal Engine.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 1–3</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 5.2 (25%)</span>
              <span class="phase-item-amt">BD 1,107.955</span>
            </div>
            <div class="phase-item-desc">AP / AR Subledgers, Aging Analysis, Statements & Credit Lock Rules.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 4–6</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 5.3 (25%)</span>
              <span class="phase-item-amt">BD 1,107.955</span>
            </div>
            <div class="phase-item-desc">Multi-Currency Treasury, Automated Bank Reconciliation & Cashflow Engine.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 7–10</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 5.4 (25%)</span>
              <span class="phase-item-amt">BD 1,107.955</span>
            </div>
            <div class="phase-item-desc">Bahrain NBR 10% VAT Return Generator, Balance Sheet, P&L & Final Sign-Off.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 11–13</div>
          </div>
        </div>
      </div>

      <!-- Module 6 Accordion -->
      <div class="phase-module-box">
        <div class="phase-module-header" onclick="togglePhase('p6')">
          <div class="phase-title-left">
            <span class="mod-tag">MOD 6</span>
            <span class="phase-title-text">Module 6: Enterprise Administration & Fixed Assets (12 Weeks)</span>
          </div>
          <div class="phase-pills">
            <span class="mod-cost-tag">BD 4,090.909</span>
            <i class="fa-solid fa-chevron-down" id="p6_icon"></i>
          </div>
        </div>
        <div class="phase-grid" id="p6_content">
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 6.1 (25%)</span>
              <span class="phase-item-amt">BD 1,022.727</span>
            </div>
            <div class="phase-item-desc">Facility Management, Maintenance Ticketing, Utility Logs & Lease Alerts.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 1–3</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 6.2 (25%)</span>
              <span class="phase-item-amt">BD 1,022.727</span>
            </div>
            <div class="phase-item-desc">Fixed Asset Master, QR Tagging, Custodian Tracking & Depreciation Engine.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 4–6</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 6.3 (25%)</span>
              <span class="phase-item-amt">BD 1,022.727</span>
            </div>
            <div class="phase-item-desc">Fleet Logistics, Vehicle Bookings, Fuel Reconciliation & TCO Analytics.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 7–9</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 6.4 (25%)</span>
              <span class="phase-item-amt">BD 1,022.727</span>
            </div>
            <div class="phase-item-desc">Staff Locker Control, Secure Digital Document Vault & CR Renewal Alerts.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 10–12</div>
          </div>
        </div>
      </div>

      <!-- Module 7 Accordion -->
      <div class="phase-module-box">
        <div class="phase-module-header" onclick="togglePhase('p7')">
          <div class="phase-title-left">
            <span class="mod-tag">MOD 7</span>
            <span class="phase-title-text">Module 7: Human Resource Management & Payroll (16 Weeks)</span>
          </div>
          <div class="phase-pills">
            <span class="mod-cost-tag">BD 5,454.548</span>
            <i class="fa-solid fa-chevron-down" id="p7_icon"></i>
          </div>
        </div>
        <div class="phase-grid" id="p7_content">
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 7.1 (25%)</span>
              <span class="phase-item-amt">BD 1,363.637</span>
            </div>
            <div class="phase-item-desc">Org Structure, Employee Master, Document Vault & Digital Onboarding.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 1–4</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 7.2 (25%)</span>
              <span class="phase-item-amt">BD 1,363.637</span>
            </div>
            <div class="phase-item-desc">Biometric Attendance, Shift Rosters & Bahrain Labour Law Leave System.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 5–8</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 7.3 (25%)</span>
              <span class="phase-item-amt">BD 1,363.637</span>
            </div>
            <div class="phase-item-desc">Automated Payroll, SIO/LMRA Compliance, WPS/CBB Export & Loan Advances.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 9–12</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 7.4 (25%)</span>
              <span class="phase-item-amt">BD 1,363.637</span>
            </div>
            <div class="phase-item-desc">Performance KPIs, ESS Self-Service Portal, EOSB Gratuity & Production Go-Live.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Weeks 13–16</div>
          </div>
        </div>
      </div>

      <!-- Module 8 Accordion -->
      <div class="phase-module-box">
        <div class="phase-module-header" onclick="togglePhase('p8')">
          <div class="phase-title-left">
            <span class="mod-tag">MOD 8</span>
            <span class="phase-title-text">Module 8: Hardware Integration & Cloud Cluster (3 Weeks)</span>
          </div>
          <div class="phase-pills">
            <span class="mod-cost-tag">BD 1,022.727</span>
            <i class="fa-solid fa-chevron-down" id="p8_icon"></i>
          </div>
        </div>
        <div class="phase-grid" id="p8_content">
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 8.1 (33.33%)</span>
              <span class="phase-item-amt">BD 340.909</span>
            </div>
            <div class="phase-item-desc">3-Tier Server Environment (Dev/Stage/Prod), RabbitMQ & Backup Automation.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Week 1</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 8.2 (33.33%)</span>
              <span class="phase-item-amt">BD 340.909</span>
            </div>
            <div class="phase-item-desc">Handheld Android QR Scanners, ESC/POS Printers & Biometric Clocks.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Week 2</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 8.3 (33.34%)</span>
              <span class="phase-item-amt">BD 340.909</span>
            </div>
            <div class="phase-item-desc">Offline Auto-Sync Engine, Multi-Branch Stress Testing & Go-Live.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Week 3</div>
          </div>
        </div>
      </div>

      <!-- Module 9 Accordion -->
      <div class="phase-module-box">
        <div class="phase-module-header" onclick="togglePhase('p9')">
          <div class="phase-title-left">
            <span class="mod-tag">MOD 9</span>
            <span class="phase-title-text">Module 9: Executive Management Dashboard & BI Cockpit (4 Weeks)</span>
          </div>
          <div class="phase-pills">
            <span class="mod-cost-tag">BD 1,363.636</span>
            <i class="fa-solid fa-chevron-down" id="p9_icon"></i>
          </div>
        </div>
        <div class="phase-grid" id="p9_content">
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 9.1 (25%)</span>
              <span class="phase-item-amt">BD 340.909</span>
            </div>
            <div class="phase-item-desc">Data Warehouse OLAP Schema, Non-Blocking ETL Pipelines & KPI Models.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Week 1</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 9.2 (25%)</span>
              <span class="phase-item-amt">BD 340.909</span>
            </div>
            <div class="phase-item-desc">Commercial, Stock Velocity, Warehouse Verification & Vendor SLA Cockpit.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Week 2</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 9.3 (25%)</span>
              <span class="phase-item-amt">BD 340.909</span>
            </div>
            <div class="phase-item-desc">Financial Liquidity, VAT, HR Payroll, Fixed Assets & Infra Health Analytics.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Week 3</div>
          </div>
          <div class="phase-item-card">
            <div class="phase-item-header">
              <span class="phase-item-tag">Milestone 9.4 (25%)</span>
              <span class="phase-item-amt">BD 340.909</span>
            </div>
            <div class="phase-item-desc">Management Filtering, 7:00 AM WhatsApp/Email Digest & Final Sign-Off.</div>
            <div class="phase-item-time"><i class="fa-solid fa-calendar"></i> Week 4</div>
          </div>
        </div>
      </div>
    </div>

    <!-- SECTION 5: Master Resource Rate Card & Team Transparency (Pure BHD) -->
    <div class="section-card">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-users"></i> Dedicated Engineering Team & Transparent Rate Matrix</div>
          <div class="section-subtitle">Full-time dedicated 5-person engineering team rate card in Bahraini Dinars (BHD)</div>
        </div>
        <span class="badge-success">Team Monthly Rate: BD 1,363.636</span>
      </div>

      <p style="font-size: 13px; color: var(--gray-700); margin-bottom: 15px;">
        All modules are estimated strictly using the agreed dedicated team rate matrix in Bahraini Dinars (BHD). Total dedicated team capacity: 160 hours / month per engineer.
      </p>

      <div class="rate-card-grid">
        <div class="rate-box">
          <div class="role-name">Project Manager & Enterprise Solutions Architect</div>
          <div class="bhd-val">BD 545.455</div>
          <div class="bhd-sub">BD 136.364 / Wk &bull; BD 3.409 / Hr</div>
          <div class="alloc-val">100% Dedicated</div>
        </div>
        <div class="rate-box">
          <div class="role-name">Back-End Lead Engineer (PHP MVC / REST APIs)</div>
          <div class="bhd-val">BD 227.273</div>
          <div class="bhd-sub">BD 56.818 / Wk &bull; BD 1.420 / Hr</div>
          <div class="alloc-val">100% Dedicated</div>
        </div>
        <div class="rate-box">
          <div class="role-name">Front-End Lead Engineer (React / UI Design Tokens)</div>
          <div class="bhd-val">BD 227.273</div>
          <div class="bhd-sub">BD 56.818 / Wk &bull; BD 1.420 / Hr</div>
          <div class="alloc-val">100% Dedicated</div>
        </div>
        <div class="rate-box">
          <div class="role-name">Database & Cloud DevOps Specialist</div>
          <div class="bhd-val">BD 204.545</div>
          <div class="bhd-sub">BD 51.136 / Wk &bull; BD 1.278 / Hr</div>
          <div class="alloc-val">100% Dedicated</div>
        </div>
        <div class="rate-box">
          <div class="role-name">QA Automation & Multi-Branch Test Lead</div>
          <div class="bhd-val">BD 159.091</div>
          <div class="bhd-sub">BD 39.773 / Wk &bull; BD 0.994 / Hr</div>
          <div class="alloc-val">100% Dedicated</div>
        </div>
      </div>
    </div>

    <!-- SECTION 6: Total Project Cost & Milestone Schedule in Bahraini Dinars -->
    <div class="section-card">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-coins"></i> Total Project Investment & Milestone Schedule in Bahraini Dinars (BHD)</div>
          <div class="section-subtitle">Consolidated commercial breakdown and 4-milestone payment tranche distribution for Popular Auto Spare Co.</div>
        </div>
        <span class="badge-accent">Grand Total: BD 34,090.910</span>
      </div>

      <div class="table-container">
        <table class="master-table">
          <thead>
            <tr>
              <th>Module Reference</th>
              <th>Module Domain</th>
              <th>Total (BHD)</th>
              <th>Tranche 1 (BHD)</th>
              <th>Tranche 2 (BHD)</th>
              <th>Tranche 3 (BHD)</th>
              <th>Tranche 4 (BHD)</th>
              <th>Payment Milestone Trigger</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="mod-tag">MS-001</span></td>
              <td><strong>PCode Generation Module</strong></td>
              <td><span class="currency-bhd">BD 3,409.091</span></td>
              <td>BD 852.273</td>
              <td>BD 852.273</td>
              <td>BD 852.273</td>
              <td>BD 852.273</td>
              <td>Demonstration & Staging Sign-Off</td>
            </tr>
            <tr>
              <td><span class="mod-tag">MS-002</span></td>
              <td><strong>Vendor & Purchase Module</strong></td>
              <td><span class="currency-bhd">BD 4,090.909</span></td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>Supplier Portal & 3-Way Match Verification</td>
            </tr>
            <tr>
              <td><span class="mod-tag">MS-003</span></td>
              <td><strong>Store Verification Module</strong></td>
              <td><span class="currency-bhd">BD 5,113.636</span></td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>Scanner Verification & Cycle Count UAT</td>
            </tr>
            <tr>
              <td><span class="mod-tag">MS-004</span></td>
              <td><strong>Sales Process & POS Module</strong></td>
              <td><span class="currency-bhd">BD 5,113.636</span></td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>Counter POS & Cash Drawer Closing UAT</td>
            </tr>
            <tr>
              <td><span class="mod-tag">MS-005</span></td>
              <td><strong>Accounts & VAT Module</strong></td>
              <td><span class="currency-bhd">BD 4,431.818</span></td>
              <td>BD 1,107.955</td>
              <td>BD 1,107.955</td>
              <td>BD 1,107.955</td>
              <td>BD 1,107.955</td>
              <td>GL Double-Entry & 10% VAT Return Sign-Off</td>
            </tr>
            <tr>
              <td><span class="mod-tag">MS-006</span></td>
              <td><strong>Enterprise Admin & Fleet</strong></td>
              <td><span class="currency-bhd">BD 4,090.909</span></td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>Asset QR Tagging & Fleet TCO Sign-Off</td>
            </tr>
            <tr>
              <td><span class="mod-tag">MS-007</span></td>
              <td><strong>HRM & Payroll Module</strong></td>
              <td><span class="currency-bhd">BD 5,454.548</span></td>
              <td>BD 1,363.637</td>
              <td>BD 1,363.637</td>
              <td>BD 1,363.637</td>
              <td>BD 1,363.637</td>
              <td>Biometric Sync & WPS CBB Bank Export UAT</td>
            </tr>
            <tr>
              <td><span class="mod-tag">MS-008</span></td>
              <td><strong>Hardware & Cloud Setup</strong></td>
              <td><span class="currency-bhd">BD 1,022.727</span></td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>—</td>
              <td>3-Tier Cloud & Hardware Peripherals Setup</td>
            </tr>
            <tr>
              <td><span class="mod-tag">MS-009</span></td>
              <td><strong>Executive BI Dashboard</strong></td>
              <td><span class="currency-bhd">BD 1,363.636</span></td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>C-Suite Mobile Dashboard & Anomaly Alerts</td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="2"><strong>GRAND TOTAL INVESTMENT (BHD)</strong></td>
              <td><strong style="color: var(--accent-gold); font-size: 15px;">BD 34,090.910</strong></td>
              <td><strong>BD 8,707.955</strong></td>
              <td><strong>BD 8,707.955</strong></td>
              <td><strong>BD 8,707.955</strong></td>
              <td><strong>BD 7,967.045</strong></td>
              <td><strong>35 Verified Milestone Gates</strong></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>

    <!-- SECTION 7: Terms, Governance & Acceptance SLA -->
    <div class="section-card">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-scale-balanced"></i> Governance, SLA & Payment Terms</div>
          <div class="section-subtitle">Contractual milestones, UAT acceptance gates, and IP protection protocols</div>
        </div>
        <span class="badge-success">Enterprise SLA</span>
      </div>

      <div class="terms-box">
        <h4>1. Milestone-Driven Invoicing & Payment Tranches</h4>
        <ul>
          <li><strong>Zero Blind Upfront Risk:</strong> Invoices are raised strictly upon completion, demonstration, and staging sign-off of each milestone tranche (25% or 33.3% per gate).</li>
          <li><strong>15-Day Verification & UAT Grace Period:</strong> The client is entitled to a 15-calendar-day UAT review window per milestone to test all specified acceptance criteria before signing off.</li>
          <li><strong>Change Request (CR) Protocol:</strong> Any features outside the defined scope are logged via Jira/Confluence and quoted using the transparent hourly rate card (BD 8.523 / Hour).</li>
        </ul>
      </div>

      <div class="terms-box">
        <h4>2. Source Code Ownership, Security & Warranty</h4>
        <ul>
          <li><strong>100% Intellectual Property (IP) Ownership:</strong> Upon settlement of contract invoices, full proprietary source code, DB schemas, and deployment scripts belong exclusively to Popular Auto Spare Co.</li>
          <li><strong>Zero Third-Party Recurring Royalties:</strong> Built on open-standard enterprise stacks (PHP 8.3 MVC, MySQL InnoDB, React 18, RabbitMQ, SQLite) with zero vendor lock-in.</li>
          <li><strong>12-Month Post-Launch Bug Warranty:</strong> 365 days of comprehensive bug-fixing SLA and security patch support following the final production deployment of each module.</li>
        </ul>
      </div>
    </div>

    <!-- SECTION 8: Digital Multi-Party Sign-Off Console -->
    <div class="signoff-section">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-signature"></i> Executive Governance & Digital Sign-Off Console</div>
          <div class="section-subtitle">Multi-party cryptographic verification and authorization for the Master 9-Module ERP Roadmap</div>
        </div>
        <span class="badge-accent">Official Acceptance</span>
      </div>

      <p style="font-size: 13px; color: var(--gray-700); margin-bottom: 20px;">
        By affixing digital signatures below, all participating executive stakeholders ratify this Master Milestone & Budgeting Summary as the official baseline for the Popular Auto Spare ERP implementation.
      </p>

      <div class="signoff-grid">
        <!-- Signoff 1 -->
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

        <!-- Signoff 2 -->
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

        <!-- Signoff 3 -->
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
    </div>

    <!-- Footer -->
    <div class="doc-footer">
      <div>
        <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong> &bull; Kingdom of Bahrain &bull; Commercial Registration (CR) Active
      </div>
      <div>
        Engineered with &hearts; by <strong>SaNDS Lab Middle East W.L.L</strong> &copy; 2026. All Rights Reserved.
      </div>
    </div>

  </div>

  <!-- Signature Modal -->
  <div class="modal-overlay" id="sigModal">
    <div class="modal-box">
      <div class="modal-header">
        <div class="modal-title"><i class="fa-solid fa-signature"></i> Digital Signature Capture</div>
        <button class="close-modal" onclick="closeSignModal()">&times;</button>
      </div>
      <div class="form-group">
        <label>Signer Full Name</label>
        <input type="text" class="form-control" id="signerName" placeholder="Enter your full official name">
      </div>
      <div class="form-group">
        <label>Signer Title / Designation</label>
        <input type="text" class="form-control" id="signerDesignation" placeholder="e.g. Managing Director">
      </div>
      <div class="form-group">
        <label>Draw Signature on Canvas</label>
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
    // Accordion toggle
    function togglePhase(id) {{
      const content = document.getElementById(id + '_content');
      const icon = document.getElementById(id + '_icon');
      if (content.style.display === 'none') {{
        content.style.display = 'grid';
        icon.className = 'fa-solid fa-chevron-down';
      }} else {{
        content.style.display = 'none';
        icon.className = 'fa-solid fa-chevron-right';
      }}
    }}

    // Render Charts
    window.addEventListener('DOMContentLoaded', () => {{
      // 1. Budget Donut Chart
      const ctxBudget = document.getElementById('budgetChart').getContext('2d');
      new Chart(ctxBudget, {{
        type: 'doughnut',
        data: {{
          labels: [
            'M1: PCode Master',
            'M2: Vendor & Purchase',
            'M3: Store Verification',
            'M4: Sales & POS',
            'M5: Accounts & VAT',
            'M6: Admin & Fixed Assets',
            'M7: HRM & Payroll',
            'M8: Hardware Setup',
            'M9: Executive BI Dashboard'
          ],
          datasets: [{{
            data: [3409.091, 4090.909, 5113.636, 5113.636, 4431.818, 4090.909, 5454.548, 1022.727, 1363.636],
            backgroundColor: [
              '#3b82f6',
              '#06b6d4',
              '#10b981',
              '#f59e0b',
              '#8b5cf6',
              '#ec4899',
              '#6366f1',
              '#64748b',
              '#0a2540'
            ],
            borderWidth: 2,
            borderColor: '#ffffff'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'right',
              labels: {{
                boxWidth: 12,
                font: {{ size: 11, family: 'Inter' }}
              }}
            }},
            tooltip: {{
              callbacks: {{
                label: function(context) {{
                  const val = context.raw;
                  const total = 34090.910;
                  const pct = ((val / total) * 100).toFixed(1);
                  return ` BD ${{val.toLocaleString('en-US', {{minimumFractionDigits: 3}})}} (${{pct}}%)`;
                }}
              }}
            }}
          }}
        }}
      }});

      // 2. Timeline Bar Chart
      const ctxTime = document.getElementById('timelineChart').getContext('2d');
      new Chart(ctxTime, {{
        type: 'bar',
        data: {{
          labels: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'],
          datasets: [{{
            label: 'Timeline (Weeks)',
            data: [10, 12, 15, 15, 13, 12, 16, 3, 4],
            backgroundColor: '#0a2540',
            borderRadius: 6,
            hoverBackgroundColor: '#d97706'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ display: false }},
            tooltip: {{
              callbacks: {{
                label: function(context) {{
                  return ` ${{context.raw}} Working Weeks`;
                }}
              }}
            }}
          }},
          scales: {{
            y: {{
              beginAtZero: true,
              max: 18,
              ticks: {{
                stepSize: 2,
                font: {{ size: 11, family: 'Inter' }}
              }},
              title: {{
                display: true,
                text: 'Weeks',
                font: {{ size: 11, weight: 'bold' }}
              }}
            }},
            x: {{
              ticks: {{
                font: {{ size: 11, family: 'Inter' }}
              }}
            }}
          }}
        }}
      }});
    }});

    // Signature Canvas Logic
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
      return {{
        x: clientX - rect.left,
        y: clientY - rect.top
      }};
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

    function stopDrawing() {{
      isDrawing = false;
    }}

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    window.addEventListener('mouseup', stopDrawing);

    canvas.addEventListener('touchstart', startDrawing, {{ passive: false }});
    canvas.addEventListener('touchmove', draw, {{ passive: false }});
    canvas.addEventListener('touchend', stopDrawing);

    function clearCanvas() {{
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }}

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
        alert('Please enter the signer full name.');
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
          alert('Signature applied successfully to Master Executive Summary (SL-POP-ERP-SUMMARY-001)!');
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

    // Fetch existing signatures
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

# 1. Save HTML to SL-POP-ERP-SUMMARY-001.html and Executive_Master_Summary_and_Budget_Milestone.html
html_path_1 = os.path.join(BASE_DIR, 'SL-POP-ERP-SUMMARY-001.html')
html_path_2 = os.path.join(BASE_DIR, 'Executive_Master_Summary_and_Budget_Milestone.html')
with open(html_path_1, 'w', encoding='utf-8') as f:
    f.write(html_content)
with open(html_path_2, 'w', encoding='utf-8') as f:
    f.write(html_content)

# Copy to popular/ folder
popular_html_1 = os.path.join(BASE_DIR, 'popular', 'SL-POP-ERP-SUMMARY-001.html')
popular_html_2 = os.path.join(BASE_DIR, 'popular', 'Executive_Master_Summary_and_Budget_Milestone.html')
shutil.copyfile(html_path_1, popular_html_1)
shutil.copyfile(html_path_1, popular_html_2)

print('Generated and distributed HTML files.')

# 2. Render through PHP and generate PDF with Chrome Headless
rendered_html_path = os.path.join(BASE_DIR, 'rendered_summary.html')
with open(rendered_html_path, 'w', encoding='utf-8') as rf:
    rf.write(html_content)

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
pdf_output_root_1 = os.path.join(BASE_DIR, 'SL-POP-ERP-SUMMARY-001.pdf')
pdf_output_root_2 = os.path.join(BASE_DIR, 'Executive_Master_Summary_and_Budget_Milestone.pdf')

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
popular_pdf_1 = os.path.join(BASE_DIR, 'popular', 'SL-POP-ERP-SUMMARY-001.pdf')
popular_pdf_2 = os.path.join(BASE_DIR, 'popular', 'Executive_Master_Summary_and_Budget_Milestone.pdf')
shutil.copyfile(pdf_output_root_1, popular_pdf_1)
shutil.copyfile(pdf_output_root_1, popular_pdf_2)

print('Distributed PDF files successfully.')

# 3. Open PDF with PyMuPDF to check pages
doc = fitz.open(pdf_output_root_1)
print(f'Generated PDF Page Count: {len(doc)}')

# 4. Insert into SQLite .auth_portal.db
db_paths = [os.path.join(BASE_DIR, '.auth_portal.db'), os.path.join(BASE_DIR, 'popular', '.auth_portal.db')]
for db_p in db_paths:
    if os.path.exists(db_p):
        try:
            conn = sqlite3.connect(db_p)
            cur = conn.cursor()
            cur.execute("INSERT OR REPLACE INTO document_meta (doc_id, title, status) VALUES (?, ?, ?)",
                        ('SL-POP-ERP-SUMMARY-001', 'Master Executive Milestone Summary & Complete 9-Module Budgeting Roadmap', 'IN_REVIEW'))
            conn.commit()
            conn.close()
            print(f'Updated document_meta in {db_p}')
        except Exception as e:
            print(f'DB update error for {db_p}:', e)
