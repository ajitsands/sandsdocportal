import os
import base64
import subprocess
import shutil
import fitz

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_b64(rel_path):
    full_path = os.path.join(BASE_DIR, rel_path)
    if not os.path.exists(full_path):
        return ''
    with open(full_path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

logo_sands_white = get_b64('logos/SaNDSLab-LogoNewUpdatedWhite.png')
logo_sands_color = get_b64('logos/SaNDSLab-LogoNewUpdated copy.png')
logo_uniglobal_white = get_b64('logos/UniGlobalWhite.png')
logo_uniglobal_color = get_b64('logos/UNIGLOBAL_CONSULTANCY_LOGO_FINAL.png')
logo_popular = get_b64('logos/logoPopular.png')

html_content = f"""<?php
// SaNDS Lab Enterprise Technical Architecture & Cybersecurity Specification
// Document Reference: SL-POP-ERP-ARCH-001
$session_save_dir = __DIR__ . '/.sessions';
if (session_status() === PHP_SESSION_NONE) {{
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

$doc_id = 'SL-POP-ERP-ARCH-001';

$db_candidates = array(__DIR__ . '/db.php', dirname(__DIR__) . '/db.php');
foreach ($db_candidates as $dbc) {{
    if (file_exists($dbc)) {{
        require_once $dbc;
        break;
    }}
}}

$authenticated_user = isset($_SESSION['authenticated_user']) ? $_SESSION['authenticated_user'] : (isset($_COOKIE['sands_auth_device']) ? 'authorized_user' : '');

// Handle direct AJAX POST actions
if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {{
    header('Content-Type: application/json');
    $action = trim($_POST['action']);

    if ($action === 'sign_document') {{
        $sig_data = isset($_POST['signature_data']) ? trim($_POST['signature_data']) : '';
        $s_name = isset($_POST['signer_name']) ? trim($_POST['signer_name']) : '';
        $s_org  = isset($_POST['signer_org']) ? trim($_POST['signer_org']) : '';
        $s_role = isset($_POST['signer_role']) ? trim($_POST['signer_role']) : 'Executive Sponsor';
        $post_doc_id = isset($_POST['doc_id']) ? trim($_POST['doc_id']) : $doc_id;

        if (empty($sig_data)) {{
            echo json_encode(array('success' => false, 'message' => 'Please draw your signature before submitting.'));
            exit;
        }}

        if ($pdo) {{
            $mstmt = $pdo->prepare("SELECT status FROM document_meta WHERE doc_id = ?");
            $mstmt->execute(array($post_doc_id));
            if ($mstmt->fetchColumn() === 'FINALIZED_AND_LOCKED') {{
                echo json_encode(array('success' => false, 'message' => 'This document is finalized and locked. No further signature edits are permitted.'));
                exit;
            }}
        }}

        $signer_email = !empty($_POST['signer_email']) ? strtolower(trim($_POST['signer_email'])) : (!empty($authenticated_user) ? strtolower(trim($authenticated_user)) : '');
        if (empty($signer_email) || $signer_email === 'authorized_user') {{
            $lo_org = strtolower($s_org);
            $lo_role = strtolower($s_role);
            $lo_name = strtolower($s_name);
            if (strpos($lo_org, 'popular') !== false || strpos($lo_role, 'client') !== false || strpos($lo_role, 'director') !== false || strpos($lo_role, 'sponsor') !== false) {{
                $signer_email = 'director@popularbahrain.com';
            }} elseif (strpos($lo_org, 'uniglobal') !== false || strpos($lo_role, 'consultant') !== false || strpos($lo_role, 'auditor') !== false) {{
                $signer_email = 'consultant@uniglobal.com';
            }} elseif (strpos($lo_org, 'sands') !== false || strpos($lo_name, 'ajit') !== false || strpos($lo_role, 'architect') !== false || strpos($lo_role, 'admin') !== false) {{
                $signer_email = 'ajit@sandslab.com';
            }} else {{
                $signer_email = 'director@popularbahrain.com';
            }}
        }}

        $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '127.0.0.1';
        $ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';

        if ($pdo) {{
            try {{
                $check = $pdo->prepare("SELECT id FROM document_signatures WHERE doc_id = ? AND LOWER(email) = LOWER(?)");
                $check->execute(array($post_doc_id, $signer_email));
                $existing_id = $check->fetchColumn();

                $now_str = date('Y-m-d H:i:s');
                if ($existing_id) {{
                    $up = $pdo->prepare("UPDATE document_signatures SET full_name = ?, organization = ?, role = ?, status = 'SIGNED', signature_data = ?, disagree_reason = NULL, ip_address = ?, device_name = ?, signed_at = ? WHERE id = ?");
                    $up->execute(array($s_name, $s_org, $s_role, $sig_data, $ip, $ua, $now_str, $existing_id));
                }} else {{
                    $ins = $pdo->prepare("INSERT INTO document_signatures (doc_id, email, full_name, organization, role, status, signature_data, ip_address, device_name, signed_at) VALUES (?, ?, ?, ?, ?, 'SIGNED', ?, ?, ?, ?)");
                    $ins->execute(array($post_doc_id, $signer_email, $s_name, $s_org, $s_role, $sig_data, $ip, $ua, $now_str));
                }}

                echo json_encode(array('success' => true, 'message' => 'Digital signature successfully recorded and verified!'));
                exit;
            }} catch (Exception $e) {{
                echo json_encode(array('success' => false, 'message' => 'Database Error: ' . $e->getMessage()));
                exit;
            }}
        }} else {{
            echo json_encode(array('success' => false, 'message' => 'Database connection unavailable.'));
            exit;
        }}
    }}

    if ($action === 'disagree_document') {{
        $reason = isset($_POST['disagree_reason']) ? trim($_POST['disagree_reason']) : '';
        $post_doc_id = isset($_POST['doc_id']) ? trim($_POST['doc_id']) : $doc_id;

        if (empty($reason)) {{
            echo json_encode(array('success' => false, 'message' => 'Please provide a descriptive reason for disagreement.'));
            exit;
        }}

        $signer_email = !empty($authenticated_user) ? $authenticated_user : 'director@popularbahrain.com';
        $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '127.0.0.1';
        $ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';

        if ($pdo) {{
            try {{
                $now_str = date('Y-m-d H:i:s');
                $check = $pdo->prepare("SELECT id FROM document_signatures WHERE doc_id = ? AND LOWER(email) = LOWER(?)");
                $check->execute(array($post_doc_id, $signer_email));
                $existing_id = $check->fetchColumn();

                if ($existing_id) {{
                    $up = $pdo->prepare("UPDATE document_signatures SET status = 'DISAGREED', signature_data = NULL, disagree_reason = ?, ip_address = ?, device_name = ?, signed_at = ? WHERE id = ?");
                    $up->execute(array($reason, $ip, $ua, $now_str, $existing_id));
                }} else {{
                    $ins = $pdo->prepare("INSERT INTO document_signatures (doc_id, email, full_name, organization, role, status, disagree_reason, ip_address, device_name, signed_at) VALUES (?, ?, 'Executive', 'Stakeholder', 'Stakeholder', 'DISAGREED', ?, ?, ?, ?)");
                    $ins->execute(array($post_doc_id, $signer_email, $reason, $ip, $ua, $now_str));
                }}

                echo json_encode(array('success' => true, 'message' => 'Revision request submitted and recorded.'));
                exit;
            }} catch (Exception $e) {{
                echo json_encode(array('success' => false, 'message' => 'Database Error: ' . $e->getMessage()));
                exit;
            }}
        }}
    }}

    if ($action === 'finalize_document') {{
        $final_by = !empty($authenticated_user) ? $authenticated_user : 'ajit@sandslab.com';
        $post_doc_id = isset($_POST['doc_id']) ? trim($_POST['doc_id']) : $doc_id;
        if ($pdo) {{
            $now_str = date('Y-m-d H:i:s');
            $fstmt = $pdo->prepare("UPDATE document_meta SET status = 'FINALIZED_AND_LOCKED', finalized_by = ?, finalized_at = ? WHERE doc_id = ?");
            $fstmt->execute(array($final_by, $now_str, $post_doc_id));
            echo json_encode(array('success' => true, 'message' => 'Specification finalized and locked.'));
            exit;
        }}
    }}

    if ($action === 'admin_reopen_document') {{
        $clear_sigs = isset($_POST['clear_signatures']) && ($_POST['clear_signatures'] === '1' || $_POST['clear_signatures'] === 'true');
        $post_doc_id = isset($_POST['doc_id']) ? trim($_POST['doc_id']) : $doc_id;
        if ($pdo) {{
            $rstmt = $pdo->prepare("UPDATE document_meta SET status = 'IN_REVIEW', finalized_by = NULL, finalized_at = NULL WHERE doc_id = ?");
            $rstmt->execute(array($post_doc_id));
            if ($clear_sigs) {{
                $del = $pdo->prepare("DELETE FROM document_signatures WHERE doc_id = ?");
                $del->execute(array($post_doc_id));
            }}
            echo json_encode(array('success' => true, 'message' => 'Document reopened for review.'));
            exit;
        }}
    }}

    if ($action === 'admin_clear_all_signatures') {{
        $post_doc_id = isset($_POST['doc_id']) ? trim($_POST['doc_id']) : $doc_id;
        if ($pdo) {{
            $del = $pdo->prepare("DELETE FROM document_signatures WHERE doc_id = ?");
            $del->execute(array($post_doc_id));
            echo json_encode(array('success' => true, 'message' => 'All signatures cleared successfully.'));
            exit;
        }}
    }}

    if ($action === 'admin_clear_signature') {{
        $target = isset($_POST['target_email']) ? strtolower(trim($_POST['target_email'])) : '';
        $post_doc_id = isset($_POST['doc_id']) ? trim($_POST['doc_id']) : $doc_id;
        if ($pdo && !empty($target)) {{
            $del = $pdo->prepare("DELETE FROM document_signatures WHERE doc_id = ? AND LOWER(email) = LOWER(?)");
            $del->execute(array($post_doc_id, $target));
            echo json_encode(array('success' => true, 'message' => 'Signature cleared successfully.'));
            exit;
        }}
    }}
}}

if (!isset($doc_meta) || empty($doc_meta) || !isset($all_signatures) || empty($all_signatures)) {{
    $doc_meta = null;
    $doc_status = 'IN_REVIEW';
    $all_signatures = array();
    $my_sig = null;
    $user_record = null;

    if (isset($pdo) && $pdo) {{
        try {{
            $stmt = $pdo->prepare("SELECT * FROM document_meta WHERE doc_id = ?");
            $stmt->execute(array($doc_id));
            $doc_meta = $stmt->fetch();
            if ($doc_meta && !empty($doc_meta['status'])) {{
                $doc_status = $doc_meta['status'];
            }}

            $sig_stmt = $pdo->prepare("SELECT * FROM document_signatures WHERE doc_id = ? ORDER BY signed_at ASC");
            $sig_stmt->execute(array($doc_id));
            $all_signatures = $sig_stmt->fetchAll();

            if (!empty($authenticated_user)) {{
                $u_stmt = $pdo->prepare("SELECT * FROM authorized_users WHERE LOWER(email) = LOWER(?)");
                $u_stmt->execute(array($authenticated_user));
                $user_record = $u_stmt->fetch();

                foreach ($all_signatures as $s) {{
                    if (strtolower($s['email']) === strtolower($authenticated_user)) {{
                        $my_sig = $s;
                        break;
                    }}
                }}
            }}
        }} catch (Exception $e) {{
            error_log("DB Arch Error: " . $e->getMessage());
        }}
    }}
}}

$is_finalized = ($doc_status === 'FINALIZED_AND_LOCKED');

$sands_sig = null;
$uniglobal_sig = null;
$popular_sig = null;

foreach ($all_signatures as $s) {{
    if ($s['status'] === 'SIGNED') {{
        $org = strtolower($s['organization']);
        $role = strtolower($s['role']);
        $email = strtolower($s['email']);
        $name = strtolower($s['full_name']);
        if (strpos($org, 'sands') !== false || strpos($email, 'sandslab') !== false || strpos($name, 'ajit') !== false || strpos($role, 'super admin') !== false || strpos($role, 'lead architect') !== false) {{
            $sands_sig = $s;
        }} elseif (strpos($org, 'uniglobal') !== false || strpos($email, 'uniglobal') !== false || strpos($name, 'consultant') !== false || strpos($role, 'consultant') !== false) {{
            $uniglobal_sig = $s;
        }} elseif (strpos($org, 'popular') !== false || strpos($email, 'popular') !== false || strpos($name, 'director') !== false || strpos($role, 'client') !== false || strpos($role, 'director') !== false || strpos($role, 'sponsor') !== false) {{
            $popular_sig = $s;
        }}
    }}
}}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ERP Technical Architecture Specification - Popular Auto Spare</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  <style>
    :root {{
      --primary: #0a2540;
      --primary-dark: #07192c;
      --primary-light: #18446e;
      --accent: #e67e22;
      --accent-dark: #d35400;
      --teal: #0d9488;
      --blue: #2563eb;
      --purple: #7c3aed;
      --green: #15803d;
      --red: #be123c;
      --gray-50: #f8fafc;
      --gray-100: #f1f5f9;
      --gray-200: #e2e8f0;
      --gray-300: #cbd5e1;
      --gray-500: #64748b;
      --gray-700: #334155;
      --gray-800: #1e293b;
      --gray-900: #0f172a;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Inter', sans-serif;
      font-size: 9.8px;
      line-height: 1.46;
      color: var(--gray-800);
      background-color: #e2e8f0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    .document-wrapper {{
      max-width: 850px;
      margin: 20px auto;
      background: #ffffff;
      box-shadow: 0 8px 30px rgba(0,0,0,0.12);
      border-radius: 6px;
      overflow: hidden;
    }}

    .page {{
      padding: 22px 30px;
      position: relative;
      background: #ffffff;
      min-height: 1080px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .page-break {{
      page-break-after: always;
      break-after: page;
      border-bottom: 2px dashed #cbd5e1;
    }}

    @media print {{
      body {{
        background: #ffffff;
      }}
      .no-print {{
        display: none !important;
      }}
      .document-wrapper {{
        max-width: 100%;
        margin: 0;
        box-shadow: none;
        border-radius: 0;
      }}
      .page {{
        padding: 0 0 6mm 0;
        min-height: 0;
        height: 100%;
      }}
      .page-break {{
        page-break-after: always;
        break-after: page;
        border-bottom: none;
      }}
      @page {{
        size: A4 portrait;
        margin: 12mm 14mm 12mm 14mm;
      }}
    }}

    /* Header */
    .doc-header {{
      background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 50%, var(--primary-light) 100%);
      color: #ffffff;
      padding: 15px 22px 12px;
      position: relative;
      border-radius: 6px 6px 0 0;
    }}

    .doc-header::after {{
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: linear-gradient(90deg, var(--accent) 0%, #38bdf8 50%, var(--accent) 100%);
    }}

    .header-logos {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(255,255,255,0.15);
    }}

    .header-logo-img {{
      height: 28px;
      width: auto;
      max-width: 120px;
      object-fit: contain;
    }}

    .doc-badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: rgba(230,126,34,0.2);
      border: 1px solid var(--accent);
      color: #ffedd5;
      font-size: 7.5px;
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      padding: 2px 7px;
      border-radius: 16px;
      margin-bottom: 4px;
    }}

    .doc-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 17.5px;
      font-weight: 800;
      letter-spacing: -0.4px;
      line-height: 1.2;
      margin-bottom: 3px;
      color: #ffffff;
    }}

    .doc-subtitle {{
      font-size: 9px;
      color: #cbd5e1;
      line-height: 1.38;
    }}

    .meta-bar {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      background: rgba(0,0,0,0.3);
      border-radius: 5px;
      padding: 6px 9px;
      margin-top: 8px;
    }}

    .meta-item {{
      font-size: 8px;
    }}

    .meta-label {{
      color: #94a3b8;
      text-transform: uppercase;
      font-weight: 600;
      letter-spacing: 0.5px;
      font-size: 7px;
    }}

    .meta-val {{
      color: #ffffff;
      font-weight: 600;
      margin-top: 1px;
    }}

    /* Mini Page Header */
    .mini-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--gray-200);
      padding-bottom: 5px;
      margin-bottom: 10px;
      font-size: 8px;
      color: var(--gray-500);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .mini-header-title {{
      color: var(--primary);
      font-weight: 700;
    }}

    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 7px;
      padding-bottom: 4px;
      margin: 10px 0 6px;
      border-bottom: 2px solid var(--gray-200);
    }}

    .section-title::before {{
      content: '';
      width: 4px;
      height: 13px;
      background: var(--accent);
      border-radius: 2px;
      display: inline-block;
    }}

    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 9px;
      margin: 6px 0;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin: 6px 0;
    }}

    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin: 6px 0;
    }}

    .tech-card {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-left: 3px solid var(--primary);
      border-radius: 4px;
      padding: 7px 9px;
    }}

    .tech-card-header {{
      display: flex;
      align-items: center;
      gap: 5px;
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 9.5px;
      color: var(--primary);
      margin-bottom: 3px;
    }}

    .tech-card-icon {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 17px;
      height: 17px;
      border-radius: 3px;
      background: #e0f2fe;
      color: #0369a1;
      font-size: 9px;
    }}

    .tech-card ul {{
      padding-left: 13px;
      font-size: 8px;
      color: var(--gray-700);
    }}

    .tech-card ul li {{
      margin-bottom: 1.5px;
    }}

    /* Diagrams */
    .diagram-container {{
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 5px;
      padding: 9px;
      margin: 7px 0;
      color: #f8fafc;
    }}

    .diagram-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 9.5px;
      font-weight: 700;
      color: #38bdf8;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 3px;
    }}

    .diagram-svg {{
      width: 100%;
      height: auto;
      display: block;
    }}

    /* Tables */
    .arch-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 8px;
      margin: 6px 0;
    }}

    .arch-table th {{
      background: var(--primary);
      color: #ffffff;
      padding: 4px 6px;
      text-align: left;
      font-weight: 600;
      border: 1px solid var(--primary-light);
      font-size: 7.5px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }}

    .arch-table td {{
      padding: 4px 6px;
      border: 1px solid var(--gray-200);
      vertical-align: top;
      line-height: 1.35;
    }}

    .arch-table tr:nth-child(even) td {{
      background: var(--gray-50);
    }}

    .badge-pill {{
      display: inline-block;
      padding: 1px 5px;
      border-radius: 10px;
      font-size: 7px;
      font-weight: 700;
      letter-spacing: 0.3px;
    }}

    .badge-blue {{ background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }}
    .badge-green {{ background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }}
    .badge-orange {{ background: #ffedd5; color: #9a3412; border: 1px solid #fed7aa; }}
    .badge-purple {{ background: #f3e8ff; color: #6b21a8; border: 1px solid #e9d5ff; }}
    .badge-red {{ background: #ffe4e6; color: #9f1239; border: 1px solid #fecdd3; }}

    .callout {{
      padding: 6px 9px;
      border-radius: 4px;
      font-size: 8px;
      margin: 6px 0;
      line-height: 1.38;
    }}

    .callout-security {{
      background: #fef2f2;
      border: 1px solid #fecdd3;
      border-left: 3px solid var(--red);
      color: #991b1b;
    }}

    .callout-perf {{
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-left: 3px solid var(--blue);
      color: #1e40af;
    }}

    .callout-backup {{
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-left: 3px solid var(--green);
      color: #166534;
    }}

    .callout-title {{
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 9px;
      margin-bottom: 2px;
    }}

    /* Sign-off Grid */
    .signoff-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-top: 8px;
    }}

    .signoff-card {{
      background: #ffffff;
      border: 1px solid var(--gray-300);
      border-radius: 5px;
      padding: 9px;
      text-align: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.03);
      position: relative;
    }}

    .signoff-logo-box {{
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 5px;
    }}

    .signoff-logo {{
      max-height: 26px;
      width: auto;
      max-width: 95px;
      object-fit: contain;
    }}

    .sands-approval-logo {{
      max-height: 36px !important;
      max-width: 135px !important;
    }}

    .signoff-role {{
      font-size: 6.8px;
      font-weight: 700;
      color: var(--accent-dark);
      text-transform: uppercase;
      letter-spacing: 0.6px;
      margin-bottom: 2px;
    }}

    .signoff-org {{
      font-size: 7.5px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 4px;
      min-height: 18px;
    }}

    .signoff-details {{
      font-size: 7px;
      color: var(--gray-700);
      border-top: 1px solid var(--gray-200);
      border-bottom: 1px solid var(--gray-200);
      padding: 4px 0;
      margin-bottom: 5px;
      text-align: left;
      line-height: 1.35;
    }}

    .signoff-placeholder {{
      height: 52px;
      border: 1.5px dashed var(--gray-300);
      border-radius: 4px;
      background: var(--gray-50);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 7px;
      color: var(--gray-500);
      font-style: italic;
    }}

    .signoff-caption {{
      font-size: 6.5px;
      color: var(--gray-500);
      margin-top: 3px;
    }}

    .sig-img-preview {{
      max-height: 48px;
      width: auto;
      max-width: 100%;
      object-fit: contain;
      display: block;
      margin: 0 auto 3px;
    }}

    .sig-status-badge {{
      display: inline-block;
      font-size: 6.8px;
      font-weight: 700;
      padding: 1px 4px;
      border-radius: 3px;
    }}

    .sig-status-signed {{
      background: #dcfce7;
      color: #15803d;
      border: 1px solid #86efac;
    }}

    /* Footer */
    .page-footer {{
      border-top: 1px solid var(--gray-200);
      padding-top: 6px;
      margin-top: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.5px;
      color: var(--gray-500);
    }}

    /* Web Action Bar */
    .web-action-bar {{
      position: sticky;
      top: 0;
      z-index: 1000;
      background: var(--primary);
      padding: 8px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }}

    .btn-tool {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 5px 10px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      border: 1px solid #334155;
      background: #1e293b;
      color: #f8fafc;
      transition: all 0.2s ease;
    }}

    .btn-tool:hover {{
      background: #334155;
      color: #ffffff;
    }}

    .superadmin-banner {{
      background: #1e293b;
      border-bottom: 2px solid var(--accent);
      padding: 6px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      color: #ffffff;
    }}

    /* Signature Interactive Area */
    .sign-interactive-card {{
      background: #ffffff;
      border: 2px solid var(--accent);
      border-radius: 8px;
      padding: 14px;
      margin: 15px auto 0;
      max-width: 850px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }}

    .canvas-container {{
      position: relative;
      border: 2px dashed #94a3b8;
      border-radius: 6px;
      background: #f8fafc;
      height: 110px;
      margin: 8px 0;
      touch-action: none;
    }}

    .canvas-container canvas {{
      width: 100%;
      height: 100%;
      display: block;
      cursor: crosshair;
    }}

    .canvas-placeholder-text {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: #94a3b8;
      font-size: 10.5px;
      pointer-events: none;
      font-weight: 500;
    }}

    .signer-info-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-bottom: 8px;
    }}

    .signer-input-group label {{
      display: block;
      font-size: 8.5px;
      font-weight: 700;
      text-transform: uppercase;
      color: #334155;
      margin-bottom: 2px;
    }}

    .signer-input-group input {{
      width: 100%;
      padding: 5px 8px;
      font-size: 9.5px;
      border: 1px solid #cbd5e1;
      border-radius: 4px;
      font-family: 'Inter', sans-serif;
    }}

    .finalized-cert-wrap {{
      background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
      border: 2px solid #22c55e;
      border-radius: 6px;
      padding: 10px;
      margin-top: 10px;
    }}

    .arch-table-wrap {{
      width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      margin: 6px 0;
    }}

    .finalized-cert-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      font-size: 7px;
      color: #14532d;
      line-height: 1.35;
    }}

    .inline-spinner {{
      display: inline-block;
      width: 10px;
      height: 10px;
      border: 2px solid rgba(153, 27, 27, 0.25);
      border-top-color: #991b1b;
      border-radius: 50%;
      animation: docSpin 0.75s linear infinite;
      vertical-align: middle;
      margin-right: 3px;
    }}

    @keyframes docSpin {{
      0% {{ transform: rotate(0deg); }}
      100% {{ transform: rotate(360deg); }}
    }}

    /* =========================================================================
       RESPONSIVE MOBILE STYLES (Screen View Only - Preserves Clean A4 Print)
       ========================================================================= */
    @media screen and (max-width: 768px) {{
      body {{
        font-size: 13px !important;
        line-height: 1.6 !important;
        background-color: #f1f5f9 !important;
        padding-bottom: 25px !important;
      }}

      .web-action-bar {{
        padding: 10px 12px !important;
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 8px !important;
      }}

      .web-action-bar > div {{
        display: flex !important;
        justify-content: space-between !important;
        width: 100% !important;
        gap: 6px !important;
      }}

      .btn-tool {{
        font-size: 12px !important;
        padding: 8px 12px !important;
        justify-content: center !important;
      }}

      .superadmin-banner {{
        flex-direction: column !important;
        align-items: stretch !important;
        padding: 10px 12px !important;
        gap: 8px !important;
      }}

      .superadmin-banner > div {{
        display: flex !important;
        justify-content: space-between !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
      }}

      .document-wrapper {{
        max-width: 100% !important;
        margin: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        background: transparent !important;
      }}

      .page {{
        min-height: auto !important;
        height: auto !important;
        padding: 18px 14px !important;
        margin-bottom: 16px !important;
        background: #ffffff !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
        border-radius: 6px !important;
      }}

      .page-break {{
        border-bottom: none !important;
      }}

      .doc-header {{
        padding: 16px 14px 14px !important;
        border-radius: 6px !important;
      }}

      .header-logos {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 8px !important;
      }}

      .header-logo-img {{
        height: auto !important;
        max-height: 24px !important;
        max-width: 28% !important;
      }}

      .doc-badge {{
        font-size: 9.5px !important;
        padding: 3px 8px !important;
      }}

      .doc-title {{
        font-size: 16px !important;
        line-height: 1.25 !important;
        margin-top: 4px !important;
      }}

      .doc-subtitle {{
        font-size: 11.5px !important;
        line-height: 1.5 !important;
      }}

      .meta-bar {{
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
        padding: 8px 10px !important;
      }}

      .meta-item {{
        font-size: 10.5px !important;
      }}

      .meta-label {{
        font-size: 9px !important;
      }}

      .mini-header {{
        font-size: 10px !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 3px !important;
        padding-bottom: 6px !important;
      }}

      .section-title {{
        font-size: 14.5px !important;
        line-height: 1.3 !important;
        margin: 12px 0 8px !important;
      }}

      .section-title::before {{
        height: 15px !important;
        width: 4px !important;
      }}

      p {{
        font-size: 12.5px !important;
        line-height: 1.55 !important;
      }}

      /* Grids to Single Column on Mobile */
      .grid-2, .grid-3, .grid-4 {{
        grid-template-columns: 1fr !important;
        gap: 10px !important;
        margin: 8px 0 !important;
      }}

      .tech-card {{
        padding: 10px 12px !important;
      }}

      .tech-card-header {{
        font-size: 12.5px !important;
      }}

      .tech-card-icon {{
        width: 22px !important;
        height: 22px !important;
        font-size: 12px !important;
      }}

      .tech-card ul {{
        padding-left: 16px !important;
        font-size: 11.5px !important;
        line-height: 1.5 !important;
      }}

      .tech-card p {{
        font-size: 11.5px !important;
        line-height: 1.5 !important;
      }}

      /* Diagrams: Horizontal Swipe & Pinch */
      .diagram-container {{
        padding: 10px 8px !important;
        margin: 10px 0 !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        position: relative !important;
      }}

      .diagram-title {{
        font-size: 11.5px !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 2px !important;
        padding-bottom: 5px !important;
      }}

      .diagram-title span:last-child {{
        font-size: 9.5px !important;
      }}

      .diagram-svg {{
        min-width: 650px !important;
        width: 650px !important;
        height: auto !important;
        display: block !important;
      }}

      /* Tables: Touch Scrolling */
      .arch-table-wrap {{
        width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        margin: 8px 0 !important;
        border-radius: 4px !important;
        border: 1px solid var(--gray-200) !important;
      }}

      .arch-table {{
        min-width: 540px !important;
        font-size: 11px !important;
        margin: 0 !important;
      }}

      .arch-table th {{
        font-size: 10px !important;
        padding: 6px 8px !important;
      }}

      .arch-table td {{
        font-size: 11px !important;
        padding: 6px 8px !important;
        line-height: 1.45 !important;
      }}

      .badge-pill {{
        font-size: 9px !important;
        padding: 2px 6px !important;
      }}

      .callout {{
        padding: 10px 12px !important;
        font-size: 11.5px !important;
        line-height: 1.5 !important;
        margin: 8px 0 !important;
      }}

      .callout-title {{
        font-size: 12.5px !important;
      }}

      .callout ul {{
        font-size: 11px !important;
        line-height: 1.45 !important;
      }}

      /* Sign-off Cards - Full Width Single Column on Mobile */
      .signoff-grid {{
        grid-template-columns: 1fr !important;
        gap: 14px !important;
        margin-top: 12px !important;
      }}

      .signoff-card {{
        padding: 14px 12px !important;
        border-radius: 6px !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }}

      .signoff-logo-box {{
        height: 38px !important;
        margin-bottom: 6px !important;
      }}

      .signoff-logo {{
        max-height: 32px !important;
        max-width: 130px !important;
      }}

      .sands-approval-logo {{
        max-height: 42px !important;
        max-width: 165px !important;
      }}

      .signoff-role {{
        font-size: 9px !important;
        margin-bottom: 3px !important;
      }}

      .signoff-org {{
        font-size: 11px !important;
        min-height: auto !important;
        margin-bottom: 6px !important;
      }}

      .signoff-details {{
        font-size: 10.5px !important;
        padding: 6px 0 !important;
        margin-bottom: 8px !important;
        line-height: 1.45 !important;
      }}

      .signoff-placeholder {{
        height: 65px !important;
        font-size: 10px !important;
      }}

      .signoff-caption {{
        font-size: 9.5px !important;
        margin-top: 4px !important;
      }}

      .sig-img-preview {{
        max-height: 60px !important;
        margin-bottom: 6px !important;
      }}

      .sig-status-badge {{
        font-size: 9px !important;
        padding: 3px 7px !important;
      }}

      /* Certificate */
      .finalized-cert-wrap {{
        padding: 12px !important;
        margin-top: 12px !important;
      }}

      .finalized-cert-wrap > div:first-child {{
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 6px !important;
      }}

      .finalized-cert-grid {{
        grid-template-columns: 1fr 1fr !important;
        gap: 8px !important;
        font-size: 10px !important;
      }}

      /* Interactive Signature Card */
      .sign-interactive-card {{
        margin: 12px 6px !important;
        padding: 14px 12px !important;
        border-radius: 6px !important;
      }}

      .sign-interactive-card > div:first-child {{
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 4px !important;
      }}

      .signer-info-grid {{
        grid-template-columns: 1fr !important;
        gap: 8px !important;
      }}

      .signer-input-group label {{
        font-size: 10px !important;
      }}

      .signer-input-group input {{
        padding: 8px 10px !important;
        font-size: 12px !important;
      }}

      .canvas-container {{
        height: 140px !important;
        margin: 10px 0 !important;
      }}

      .canvas-placeholder-text {{
        font-size: 11.5px !important;
        width: 85% !important;
        text-align: center !important;
      }}

      .page-footer {{
        flex-direction: column !important;
        gap: 4px !important;
        align-items: flex-start !important;
        font-size: 9.5px !important;
        padding-top: 8px !important;
        margin-top: 12px !important;
      }}
    }}

    @media screen and (max-width: 480px) {{
      .meta-bar {{
        grid-template-columns: 1fr !important;
      }}
      .finalized-cert-grid {{
        grid-template-columns: 1fr !important;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Floating Controls (No Print) -->
  <div class="web-action-bar no-print">
    <a href="?" class="btn-tool">
      &larr; Return to Client Document Hub
    </a>
    <div style="display:flex; gap:8px; align-items:center;">
      <?php if ($is_finalized): ?>
        <span style="background:#dcfce7; color:#15803d; border:1px solid #86efac; font-size:10px; font-weight:700; padding:4px 8px; border-radius:4px;">🔒 Document Finalized & Locked</span>
      <?php else: ?>
        <span style="background:#fef3c7; color:#b45309; border:1px solid #fde68a; font-size:10px; font-weight:700; padding:4px 8px; border-radius:4px;">⏳ In Stakeholder Review</span>
      <?php endif; ?>
      <button onclick="window.print()" class="btn-tool" style="background:#0a2540; color:#ffffff; border-color:#0a2540;">
        🖨️ Print / Save as PDF
      </button>
    </div>
  </div>

  <?php if (!empty($authenticated_user) && (strtolower($authenticated_user) === 'ajit@sandslab.com' || strtolower($authenticated_user) === 'info@sandslab.com')): ?>
    <!-- Super Admin Controls Banner (No Print) -->
    <div class="superadmin-banner no-print">
      <div style="display:flex; align-items:center; gap:8px;">
        <span style="background:#e67e22; color:#ffffff; font-size:9px; font-weight:700; padding:2px 6px; border-radius:3px; text-transform:uppercase;">👑 Super Admin</span>
        <span style="font-size:10.5px; font-weight:600;">
          Status: <?php echo $is_finalized ? '<strong style="color:#4ade80;">🔒 Finalized & Locked</strong>' : '<strong style="color:#facc15;">⏳ In Stakeholder Review</strong>'; ?>
        </span>
      </div>
      <div style="display:flex; align-items:center; gap:6px;">
        <?php if ($is_finalized): ?>
          <button type="button" onclick="adminPromptReopenDoc()" class="btn-tool" style="background:#b45309; color:#ffffff; border-color:#d97706; font-size:10px; padding:4px 8px;">
            🔓 Re-Open Document
          </button>
          <button type="button" onclick="adminConfirmClearAllSigs()" class="btn-tool" style="background:#be123c; color:#ffffff; border-color:#e11d48; font-size:10px; padding:4px 8px;">
            🧹 Clear All Signatures
          </button>
        <?php else: ?>
          <button type="button" onclick="adminConfirmFinalizeDoc()" class="btn-tool" style="background:#15803d; color:#ffffff; border-color:#16a34a; font-size:10px; padding:4px 8px;">
            🔒 Finalize & Lock Specification
          </button>
          <button type="button" onclick="adminConfirmClearAllSigs()" class="btn-tool" style="background:#be123c; color:#ffffff; border-color:#e11d48; font-size:10px; padding:4px 8px;">
            🧹 Clear All Signatures
          </button>
        <?php endif; ?>
      </div>
    </div>
  <?php endif; ?>

<div class="document-wrapper">

  <!-- =========================================================================
       PAGE 1: COVER & SECTION 1 (EXECUTIVE ARCHITECTURAL BLUEPRINT)
       ========================================================================= -->
  <div class="page page-break">
    <div>
      <header class="doc-header">
        <div class="header-logos">
          <img class="header-logo-img" src="{logo_sands_white}" alt="SaNDS Lab Middle East" />
          <img class="header-logo-img" src="{logo_popular}" alt="Popular Auto Spare" />
          <img class="header-logo-img" src="{logo_uniglobal_white}" alt="UniGlobal Consultancy" />
        </div>
        <div class="doc-badge">🛡️ Enterprise Technical Architecture Specification</div>
        <h1 class="doc-title">ERP SOLUTION ARCHITECTURE & CYBERSECURITY DESIGN</h1>
        <p class="doc-subtitle">
          High-Availability Multi-Tier Enterprise Resource Planning (ERP) System featuring React.js Custom Controls, Clean PHP MVC Backend, RabbitMQ Request Queueing, Offline SQLite/IndexedDB Storage Engine, Git Version Governance, and JetBackup 5 Incremental Disaster Recovery.
        </p>

        <div class="meta-bar">
          <div class="meta-item">
            <div class="meta-label">Document Reference</div>
            <div class="meta-val">SL-POP-ERP-ARCH-001</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">System Release</div>
            <div class="meta-val">Version 1.0 (Enterprise)</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Target Infrastructure</div>
            <div class="meta-val">3-Tier Virtualized Server</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Security & Backup Tier</div>
            <div class="meta-val">Zero-Trust / JetBackup 5 Incremental</div>
          </div>
        </div>
      </header>

      <section style="margin-top:12px;">
        <h2 class="section-title">1. Executive Summary & Core Architectural Principles</h2>
        <p>
          The Popular Auto Spare ERP Solution is engineered as an ultra-reliable, high-throughput, mission-critical enterprise system. It unifies multi-branch automotive spare parts cataloging, counter POS billing, warehouse inventory ledgering, and financial accounting across the Kingdom of Bahrain. The architectural philosophy prioritizes:
        </p>

        <div class="grid-4">
          <div class="tech-card">
            <div class="tech-card-header">
              <span class="tech-card-icon">⚡</span>
              <span>Sub-Second Latency</span>
            </div>
            <ul>
              <li>Optimistic React.js UI state</li>
              <li>Redis distributed query caching</li>
              <li>Bespoke lightweight UI controls</li>
            </ul>
          </div>
          <div class="tech-card">
            <div class="tech-card-header">
              <span class="tech-card-icon">📶</span>
              <span>Offline Resilience</span>
            </div>
            <ul>
              <li>IndexedDB local transaction log</li>
              <li>Native POS terminal SQLite DB</li>
              <li>Bi-directional delta auto-sync</li>
            </ul>
          </div>
          <div class="tech-card">
            <div class="tech-card-header">
              <span class="tech-card-icon">📬</span>
              <span>Async Queueing</span>
            </div>
            <ul>
              <li>RabbitMQ message broker</li>
              <li>Background ledger reconciliation</li>
              <li>Zero thread blocking on POS writes</li>
            </ul>
          </div>
          <div class="tech-card">
            <div class="tech-card-header">
              <span class="tech-card-icon">🛡️</span>
              <span>Git & JetBackup DR</span>
            </div>
            <ul>
              <li>3-Tier Git branching governance</li>
              <li>JetBackup 5 incremental snapshots</li>
              <li>Point-in-Time Recovery (PITR)</li>
            </ul>
          </div>
        </div>

        <div class="arch-table-wrap">
        <div class="arch-table-wrap">
      <table class="arch-table">
          <thead>
            <tr>
              <th style="width:20%;">Layer / Tier</th>
              <th style="width:25%;">Core Technology</th>
              <th style="width:30%;">Key Libraries & Drivers</th>
              <th style="width:25%;">Architectural Purpose</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Client Presentation</strong></td>
              <td>React.js 18.2+ (SPA & PWA)</td>
              <td>Custom Virtual DOM Controls, Lucide Icons, Canvas API</td>
              <td>Reactive, touch-optimized POS & Admin portal.</td>
            </tr>
            <tr>
              <td><strong>Local Offline Store</strong></td>
              <td>IndexedDB (PWA) / SQLite (Native)</td>
              <td>Dexie.js 3.2+ Wrapper, SQLite3 Embedded C-Engine</td>
              <td>Zero-latency offline billing & mutation outbox.</td>
            </tr>
            <tr>
              <td><strong>Edge & Gateway</strong></td>
              <td>Nginx 1.24+ Reverse Proxy</td>
              <td>ModSecurity WAF, Let's Encrypt TLS 1.3, Brotli</td>
              <td>SSL termination, DDoS mitigation, virtual host routing.</td>
            </tr>
            <tr>
              <td><strong>Application Backend</strong></td>
              <td>PHP 8.2+ Clean MVC Core</td>
              <td>FastRoute, PHP-DI, Respect/Validation, PDO MySQL</td>
              <td>Stateless REST APIs, domain business logic rules.</td>
            </tr>
            <tr>
              <td><strong>Message Queue Broker</strong></td>
              <td>RabbitMQ 3.12+ (Erlang OTP 26)</td>
              <td>AMQP 0-9-1 Protocol, RabbitMQ Management Plugin</td>
              <td>Async batch ingestion, sync payload processing.</td>
            </tr>
            <tr>
              <td><strong>Persistence & Cache</strong></td>
              <td>MySQL 8.0+ & Redis 7.0+</td>
              <td>InnoDB ACID Engine, Redis In-Memory KV Cache</td>
              <td>Master financial ledgers, token store & rate limits.</td>
            </tr>
            <tr>
              <td><strong>Backup & Recovery</strong></td>
              <td>JetBackup 5 + MySQL PITR</td>
              <td>Dedicated NVMe Backup Volume, AES-256 S3 Sync</td>
              <td>Incremental snapshots, RPO &lt; 1h, RTO &lt; 30m.</td>
            </tr>
          </tbody>
        </table>
        </div>
      </section>
    </div>

    <div class="page-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain</div>
      <div>Document Reference: SL-POP-ERP-ARCH-001 • Page 1 of 9</div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 2: SECTION 2 (END-TO-END ARCHITECTURE SCHEMATIC)
       ========================================================================= -->
  <div class="page page-break">
    <div>
      <div class="mini-header">
        <span class="mini-header-title">Technical Architecture Specification</span>
        <span>Section 2: End-to-End System Schematic</span>
      </div>

      <h2 class="section-title">2. End-to-End System Architecture Schematic</h2>
      <p>
        The system is organized into a clean decoupled 5-tier architecture. High-frequency write requests from branch POS terminals and administrative web consoles pass through the Nginx Edge Gateway directly to the PHP MVC micro-kernel. Heavy reconciliation tasks and offline delta synchronizations are queued into RabbitMQ to guarantee maximum responsiveness.
      </p>

      <div class="diagram-container">
        <div class="diagram-title">
          <span>Enterprise Layered Architecture Schematic</span>
          <span style="color:#94a3b8; font-size:8px;">Figure 1: Decoupled Multi-Tier System Blueprint</span>
        </div>

        <svg class="diagram-svg" viewBox="0 0 820 395" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="820" height="395" rx="6" fill="#0f172a" />
          
          <!-- Layer 1: Client Tier -->
          <rect x="20" y="15" width="780" height="58" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" />
          <text x="35" y="34" fill="#38bdf8" font-family="'Outfit', sans-serif" font-size="10" font-weight="700">PRESENTATION & OFFLINE CLIENT LAYER (React.js SPA / PWA)</text>
          
          <rect x="35" y="42" width="230" height="22" rx="3" fill="#0284c7" />
          <text x="45" y="57" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8.5" font-weight="600">🖥️ Web Admin ERP (React.js SPA)</text>
          
          <rect x="280" y="42" width="250" height="22" rx="3" fill="#0d9488" />
          <text x="290" y="57" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8.5" font-weight="600">📱 Mobile / PWA POS (Service Worker)</text>
          
          <rect x="545" y="42" width="240" height="22" rx="3" fill="#4f46e5" />
          <text x="555" y="57" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8.5" font-weight="600">💾 Offline Store (IndexedDB / SQLite)</text>

          <!-- Flow Arrow 1 to 2 -->
          <path d="M410 73 L410 96" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 2" />
          <polygon points="407,96 413,96 410,102" fill="#38bdf8" />
          <text x="420" y="88" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7.5">HTTPS / TLS 1.3 (JWT Bearer)</text>

          <!-- Layer 2: Edge & Security Gateway -->
          <rect x="20" y="104" width="780" height="50" rx="5" fill="#1e293b" stroke="#e11d48" stroke-width="1.5" />
          <text x="35" y="122" fill="#f43f5e" font-family="'Outfit', sans-serif" font-size="10" font-weight="700">EDGE GATEWAY & CYBERSECURITY SHIELD (Nginx + ModSecurity WAF)</text>
          
          <rect x="35" y="128" width="175" height="19" rx="3" fill="#9f1239" />
          <text x="45" y="141" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🛡️ TLS 1.3 Termination</text>
          
          <rect x="225" y="128" width="175" height="19" rx="3" fill="#881337" />
          <text x="235" y="141" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🛑 Rate Limiter & IP Shield</text>
          
          <rect x="415" y="128" width="185" height="19" rx="3" fill="#9f1239" />
          <text x="425" y="141" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🌐 3-Domain Proxy Router</text>
          
          <rect x="615" y="128" width="170" height="19" rx="3" fill="#be123c" />
          <text x="625" y="141" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🔑 JWT Validator Filter</text>

          <!-- Flow Arrow 2 to 3 -->
          <path d="M410 154 L410 176" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4 2" />
          <polygon points="407,176 413,176 410,182" fill="#f43f5e" />

          <!-- Layer 3: Backend Application Layer -->
          <rect x="20" y="184" width="780" height="58" rx="5" fill="#1e293b" stroke="#e67e22" stroke-width="1.5" />
          <text x="35" y="202" fill="#fb923c" font-family="'Outfit', sans-serif" font-size="10" font-weight="700">CORE APPLICATION LOGIC TIER (PHP 8.2+ Clean MVC Architecture)</text>
          
          <rect x="35" y="210" width="175" height="22" rx="3" fill="#b45309" />
          <text x="45" y="225" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🎮 Controllers & Routing</text>
          
          <rect x="225" y="210" width="175" height="22" rx="3" fill="#c2410c" />
          <text x="235" y="225" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">⚙️ Domain Service Engines</text>
          
          <rect x="415" y="210" width="185" height="22" rx="3" fill="#d97706" />
          <text x="425" y="225" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🗄️ Repositories & Data Mappers</text>
          
          <rect x="615" y="210" width="170" height="22" rx="3" fill="#ea580c" />
          <text x="625" y="225" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🔒 AES-256 Crypto Provider</text>

          <!-- Split Flows from 3 to 4 & 5 -->
          <path d="M250 242 L250 272" stroke="#fb923c" stroke-width="2" stroke-dasharray="4 2" />
          <polygon points="247,272 253,272 250,278" fill="#fb923c" />
          
          <path d="M570 242 L570 272" stroke="#fb923c" stroke-width="2" stroke-dasharray="4 2" />
          <polygon points="567,272 573,272 570,278" fill="#fb923c" />

          <!-- Layer 4: Asynchronous Queue Broker (RabbitMQ) -->
          <rect x="20" y="280" width="375" height="98" rx="5" fill="#1e293b" stroke="#f97316" stroke-width="1.5" />
          <text x="35" y="298" fill="#fb923c" font-family="'Outfit', sans-serif" font-size="9.5" font-weight="700">MESSAGE QUEUE BROKER (RabbitMQ 3.12+)</text>
          
          <rect x="35" y="306" width="165" height="20" rx="3" fill="#7c2d12" />
          <text x="42" y="320" fill="#fed7aa" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">📥 queue.offline.sync</text>
          
          <rect x="215" y="306" width="165" height="20" rx="3" fill="#7c2d12" />
          <text x="222" y="320" fill="#fed7aa" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">📊 queue.ledger.reconcile</text>
          
          <rect x="35" y="332" width="165" height="20" rx="3" fill="#7c2d12" />
          <text x="42" y="346" fill="#fed7aa" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">📧 queue.notifications</text>
          
          <rect x="215" y="332" width="165" height="20" rx="3" fill="#7c2d12" />
          <text x="222" y="346" fill="#fed7aa" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">📑 queue.audit.stream</text>
          
          <text x="35" y="368" fill="#fdba74" font-family="'Inter', sans-serif" font-size="7.5">Supervised PHP CLI Daemons with Dead-Letter Handling</text>

          <!-- Layer 5: Data Persistence Tier -->
          <rect x="425" y="280" width="375" height="98" rx="5" fill="#1e293b" stroke="#22c55e" stroke-width="1.5" />
          <text x="440" y="298" fill="#4ade80" font-family="'Outfit', sans-serif" font-size="9.5" font-weight="700">PERSISTENCE & CACHING (MySQL & Redis)</text>
          
          <rect x="440" y="306" width="165" height="44" rx="3" fill="#14532d" />
          <text x="450" y="323" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="700">🗄️ MySQL 8.0 Primary</text>
          <text x="450" y="339" fill="#86efac" font-family="'Inter', sans-serif" font-size="7">ACID Ledgers & Fulltext</text>
          
          <rect x="620" y="306" width="165" height="44" rx="3" fill="#831843" />
          <text x="630" y="323" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="700">⚡ Redis 7.0 In-Memory</text>
          <text x="630" y="339" fill="#fbcfe8" font-family="'Inter', sans-serif" font-size="7">Token Store & Rate Limits</text>

          <text x="440" y="368" fill="#86efac" font-family="'Inter', sans-serif" font-size="7.5">JetBackup 5 Incremental Snapshots + Continuous Binary Logs</text>
        </svg>
      </div>

      <div class="callout callout-perf">
        <div class="callout-title">⚡ Zero-Blocking Asynchronous Transaction Flow</div>
        Counter cashiers receive invoice confirmation in under 45ms. Database write locks, VAT tax ledgering, customer statement updates, and SMS receipts run completely in the background via RabbitMQ worker pools.
      </div>
    </div>

    <div class="page-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain</div>
      <div>Document Reference: SL-POP-ERP-ARCH-001 • Page 2 of 9</div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 3: SECTION 3 & 4 (FRONTEND & BACKEND ARCHITECTURE)
       ========================================================================= -->
  <div class="page page-break">
    <div>
      <div class="mini-header">
        <span class="mini-header-title">Technical Architecture Specification</span>
        <span>Section 3 & 4: Frontend & Backend Engine</span>
      </div>

      <section>
        <h2 class="section-title">3. Frontend Architecture (React.js Bespoke Custom Controls)</h2>
        <p>
          The user interface is constructed using <strong>custom-engineered high-performance React.js components</strong> without bloated dependencies, ensuring high frame rates during counter checkout and instantaneous search over 100,000+ spare parts cross-references.
        </p>

        <div class="grid-2">
          <div class="tech-card">
            <div class="tech-card-header">
              <span class="tech-card-icon">⚡</span>
              <span>Virtual DOM High-Speed DataGrid</span>
            </div>
            <p style="font-size:8px;">
              Renders 50,000+ automotive spare part SKUs using window virtualization (only rendering visible rows). Sub-16ms frame times, multi-column search by OEM Part #, brand, and vehicle chassis compatibility.
            </p>
          </div>
          <div class="tech-card" style="border-left-color:var(--accent);">
            <div class="tech-card-header">
              <span class="tech-card-icon" style="background:#ffedd5; color:#9a3412;">🛒</span>
              <span>POS Fast-Checkout Engine & Scanner</span>
            </div>
            <p style="font-size:8px;">
              Keyboard-first counter billing with <strong>Automatic 1D/2D Barcode & QR Code Listener</strong>. Intercepts hardware HID scanners globally with focus-bypass, decodes live camera streams via WebRTC frame analyzers, handles split payments, and outputs direct ESC/POS thermal receipts.
            </p>
          </div>
          <div class="tech-card">
            <div class="tech-card-header">
              <span class="tech-card-icon">✍️</span>
              <span>Vector Digital Signature Canvas</span>
            </div>
            <p style="font-size:8px;">
              Bezier curve smoothing signature pad with embedded SHA-256 integrity watermark, capturing pressure and hardware timestamps for delivery notes, credit approvals, and milestone sign-offs.
            </p>
          </div>
          <div class="tech-card">
            <div class="tech-card-header">
              <span class="tech-card-icon">📦</span>
              <span>Offline Service Worker Cache</span>
            </div>
            <p style="font-size:8px;">
              Progressive Web App (PWA) cache engine storing application bundles and catalog master data. Emits network availability heartbeats and initiates transactional background synchronization queues.
            </p>
          </div>
        </div>
      </section>

      <section style="margin-top:8px;">
        <h2 class="section-title">4. Backend Architecture (PHP 8.2+ Clean MVC Core)</h2>
        <p>
          The backend enforces strict separation between HTTP transport, domain business logic, and database access. Controllers remain strictly thin, delegating all processing to transactional Domain Services.
        </p>

        <div class="arch-table-wrap">
        <div class="arch-table-wrap">
      <table class="arch-table">
          <thead>
            <tr>
              <th style="width:20%;">Layer</th>
              <th style="width:28%;">Component Name</th>
              <th style="width:32%;">Core Responsibilities</th>
              <th style="width:20%;">Enforcement</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>1. HTTP Gateway</strong></td>
              <td>Nginx & Global Middleware</td>
              <td>Request parsing, IP filtering, rate-limiting, CORS, Brotli compression.</td>
              <td>WAF & TLS 1.3 Termination</td>
            </tr>
            <tr>
              <td><strong>2. Middleware</strong></td>
              <td>Auth & Schema Handlers</td>
              <td>JWT token verification, permission bitmask checks, input payload sanitization.</td>
              <td>Replay token rejection</td>
            </tr>
            <tr>
              <td><strong>3. Controllers</strong></td>
              <td>Thin MVC Controllers</td>
              <td>Input mapping, Service delegation, JSON:API structured output formatting.</td>
              <td>Zero raw SQL allowed</td>
            </tr>
            <tr>
              <td><strong>4. Domain Services</strong></td>
              <td>Pure Business Engines</td>
              <td>VAT calculation, double-entry inventory ledger updates, discount validation.</td>
              <td>Atomic DB transactions</td>
            </tr>
            <tr>
              <td><strong>5. Repositories</strong></td>
              <td>Data Access Layer</td>
              <td>Abstracting SQL data access via strict PDO Prepared Statements, Redis cache.</td>
              <td>100% SQLi immunity</td>
            </tr>
            <tr>
              <td><strong>6. Message Queue</strong></td>
              <td>AMQP RabbitMQ Client</td>
              <td>Publishing async events (Sync, Ledger Rollup, SMS, Audit Stream) to broker.</td>
              <td>Persistent delivery mode</td>
            </tr>
          </tbody>
        </table>
        </div>
      </section>
    </div>

    <div class="page-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain</div>
      <div>Document Reference: SL-POP-ERP-ARCH-001 • Page 3 of 9</div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 4: SECTION 5 (RABBITMQ ASYNC QUEUEING ENGINE)
       ========================================================================= -->
  <div class="page page-break">
    <div>
      <div class="mini-header">
        <span class="mini-header-title">Technical Architecture Specification</span>
        <span>Section 5: Asynchronous Request Queueing</span>
      </div>

      <h2 class="section-title">5. Asynchronous Request Queueing & RabbitMQ Integration</h2>
      <p>
        To prevent server lock contention and eliminate checkout lag during peak store hours, the ERP implements <strong>RabbitMQ (AMQP 0-9-1)</strong> as a high-throughput message broker. Time-consuming operations are offloaded from HTTP request cycles into dedicated background worker queues.
      </p>

      <div class="diagram-container">
        <div class="diagram-title">
          <span>RabbitMQ Asynchronous Processing Pipeline</span>
          <span style="color:#94a3b8; font-size:8px;">Figure 2: Message Exchange & Worker Routing Architecture</span>
        </div>

        <svg class="diagram-svg" viewBox="0 0 820 220" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="820" height="220" rx="6" fill="#0f172a" />
          
          <!-- Producer -->
          <rect x="25" y="35" width="160" height="150" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" />
          <text x="40" y="58" fill="#38bdf8" font-family="'Outfit', sans-serif" font-size="10.5" font-weight="700">HTTP PRODUCER</text>
          <text x="40" y="78" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8.5" font-weight="600">PHP FastCGI Engine</text>
          <text x="40" y="98" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7.5">• REST API Requests</text>
          <text x="40" y="113" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7.5">• Offline Sync Batches</text>
          <text x="40" y="128" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7.5">• POS Invoice Creation</text>
          <rect x="38" y="145" width="134" height="22" rx="3" fill="#0284c7" />
          <text x="48" y="159" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8" font-weight="700">Publish AMQP Event</text>

          <!-- Producer to Exchange Arrow -->
          <path d="M185 110 L230 110" stroke="#38bdf8" stroke-width="2" />
          <polygon points="230,106 238,110 230,114" fill="#38bdf8" />
          <text x="190" y="103" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7">Publish</text>

          <!-- Exchange -->
          <rect x="240" y="35" width="140" height="150" rx="5" fill="#1e293b" stroke="#f97316" stroke-width="1.5" />
          <text x="250" y="58" fill="#f97316" font-family="'Outfit', sans-serif" font-size="10.5" font-weight="700">TOPIC EXCHANGE</text>
          <text x="250" y="78" fill="#fed7aa" font-family="'Inter', sans-serif" font-size="8" font-weight="600">erp.events.topic</text>
          <text x="250" y="102" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7.5">• sync.batch.*</text>
          <text x="250" y="117" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7.5">• ledger.post.*</text>
          <text x="250" y="132" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7.5">• notify.sms.*</text>
          <text x="250" y="147" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7.5">• audit.record.*</text>

          <!-- Routing Arrows -->
          <path d="M380 65 L435 48" stroke="#f97316" stroke-width="1.5" />
          <polygon points="433,45 441,47 436,51" fill="#f97316" />
          
          <path d="M380 95 L435 88" stroke="#f97316" stroke-width="1.5" />
          <polygon points="434,85 441,87 436,91" fill="#f97316" />

          <path d="M380 125 L435 128" stroke="#f97316" stroke-width="1.5" />
          <polygon points="436,125 441,129 434,131" fill="#f97316" />

          <path d="M380 155 L435 168" stroke="#f97316" stroke-width="1.5" />
          <polygon points="436,165 441,170 433,171" fill="#f97316" />

          <!-- Queues -->
          <rect x="445" y="35" width="160" height="28" rx="3" fill="#7c2d12" stroke="#ea580c" />
          <text x="455" y="52" fill="#ffedd5" font-family="'Inter', sans-serif" font-size="8" font-weight="600">📥 queue.sync.payload</text>

          <rect x="445" y="75" width="160" height="28" rx="3" fill="#7c2d12" stroke="#ea580c" />
          <text x="455" y="92" fill="#ffedd5" font-family="'Inter', sans-serif" font-size="8" font-weight="600">📊 queue.ledger.reconcile</text>

          <rect x="445" y="115" width="160" height="28" rx="3" fill="#7c2d12" stroke="#ea580c" />
          <text x="455" y="132" fill="#ffedd5" font-family="'Inter', sans-serif" font-size="8" font-weight="600">📧 queue.notifications</text>

          <rect x="445" y="155" width="160" height="28" rx="3" fill="#7c2d12" stroke="#ea580c" />
          <text x="455" y="172" fill="#ffedd5" font-family="'Inter', sans-serif" font-size="8" font-weight="600">📑 queue.audit.stream</text>

          <!-- Queue to Consumer Arrows -->
          <path d="M605 48 L650 48" stroke="#22c55e" stroke-width="1.5" />
          <polygon points="650,45 656,48 650,51" fill="#22c55e" />

          <path d="M605 88 L650 88" stroke="#22c55e" stroke-width="1.5" />
          <polygon points="650,85 656,88 650,91" fill="#22c55e" />

          <path d="M605 128 L650 128" stroke="#22c55e" stroke-width="1.5" />
          <polygon points="650,125 656,128 650,131" fill="#22c55e" />

          <path d="M605 168 L650 168" stroke="#22c55e" stroke-width="1.5" />
          <polygon points="650,165 656,168 650,171" fill="#22c55e" />

          <!-- Consumers -->
          <rect x="660" y="35" width="140" height="150" rx="5" fill="#1e293b" stroke="#22c55e" stroke-width="1.5" />
          <text x="670" y="58" fill="#4ade80" font-family="'Outfit', sans-serif" font-size="10.5" font-weight="700">CLI DAEMON POOL</text>
          <text x="670" y="78" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8" font-weight="600">PHP Supervisor Pool</text>
          <text x="670" y="100" fill="#86efac" font-family="'Inter', sans-serif" font-size="7.5">• Sync Consumer (x4)</text>
          <text x="670" y="115" fill="#86efac" font-family="'Inter', sans-serif" font-size="7.5">• Ledger Worker (x2)</text>
          <text x="670" y="130" fill="#86efac" font-family="'Inter', sans-serif" font-size="7.5">• SMS/Email Worker (x2)</text>
          <text x="670" y="145" fill="#86efac" font-family="'Inter', sans-serif" font-size="7.5">• Dead-Letter DLX Queue</text>
        </svg>
      </div>

      <div class="grid-3">
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">1</span>
            <span>Zero-Blocking Ingestion</span>
          </div>
          <p style="font-size:8px;">
            POS checkout responses return in <strong>&lt; 45ms</strong> to the cashier. Complex multi-table inventory ledger updates and cost calculations are published to `queue.ledger.reconcile` and executed asynchronously.
          </p>
        </div>
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">2</span>
            <span>Backpressure & Throttling</span>
          </div>
          <p style="font-size:8px;">
            If multiple branches upload large offline transaction batches simultaneously upon internet reconnection, RabbitMQ buffers messages smoothly, preventing database lock exhaustion or CPU spikes.
          </p>
        </div>
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">3</span>
            <span>Dead Letter Exchange (DLX)</span>
          </div>
          <p style="font-size:8px;">
            Failed tasks undergo exponential retry (3 attempts). Persistent anomalies are safely routed to a Dead Letter Queue (`dlq.failed.events`) with real-time alerts to the Super Admin.
          </p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain</div>
      <div>Document Reference: SL-POP-ERP-ARCH-001 • Page 4 of 9</div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 5: SECTION 6 (OFFLINE-FIRST STORAGE & AUTO-SYNC ENGINE)
       ========================================================================= -->
  <div class="page page-break">
    <div>
      <div class="mini-header">
        <span class="mini-header-title">Technical Architecture Specification</span>
        <span>Section 6: Offline Storage & Auto-Sync Engine</span>
      </div>

      <h2 class="section-title">6. Offline-First Architecture & Bi-Directional Auto-Sync Engine</h2>
      <p>
        Automotive spare parts sales counters must operate continuously without interruption, even during telecom outages, fiber cuts, or local Wi-Fi disruptions. The ERP implements an <strong>Autonomous Offline Storage & Transaction Queue</strong> that seamlessly transitions between offline and online states.
      </p>

      <div class="grid-2">
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">💾</span>
            <span>Client Storage Engine</span>
          </div>
          <p style="font-size:8px;">
            <strong>IndexedDB (Dexie.js):</strong> Stores complete branch stock catalogs, customer accounts, and pending invoice outbox locally in browser memory.<br>
            <strong>SQLite Engine (Native Electron):</strong> Standalone POS counters maintain a local relational SQLite database with full ACID transactions.
          </p>
        </div>
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">🔄</span>
            <span>Auto-Sync Coordinator</span>
          </div>
          <p style="font-size:8px;">
            <strong>Heartbeat Monitor:</strong> Pings `/api/health` every 5 seconds.<br>
            <strong>Delta Replay Engine:</strong> Packages pending mutations into encrypted JSON batches and flushes sequentially to RabbitMQ upon reconnection with deterministic conflict resolution.
          </p>
        </div>
      </div>

      <div class="diagram-container">
        <div class="diagram-title">
          <span>Offline-to-Online Transaction Sync Pipeline</span>
          <span style="color:#94a3b8; font-size:8px;">Figure 3: Autonomous Queue Replay & Master Reconciliation</span>
        </div>

        <svg class="diagram-svg" viewBox="0 0 820 185" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="820" height="185" rx="6" fill="#0f172a" />
          
          <!-- Box 1: Offline POS -->
          <rect x="25" y="22" width="220" height="140" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" />
          <text x="35" y="44" fill="#38bdf8" font-family="'Outfit', sans-serif" font-size="10" font-weight="700">1. OFFLINE POS TERMINAL</text>
          <rect x="35" y="54" width="200" height="24" rx="3" fill="#0369a1" />
          <text x="45" y="70" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8" font-weight="600">🛒 Cashier Generates Bill / Barcode Scan</text>
          
          <rect x="35" y="86" width="200" height="24" rx="3" fill="#0d9488" />
          <text x="45" y="102" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8" font-weight="600">💾 Writes to Local IndexedDB / SQLite</text>

          <rect x="35" y="118" width="200" height="24" rx="3" fill="#475569" />
          <text x="45" y="134" fill="#f1f5f9" font-family="'Inter', sans-serif" font-size="7.5">📴 Outbox Status: PENDING_SYNC</text>

          <!-- Arrow 1 to 2 -->
          <path d="M245 92 L300 92" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4 2" />
          <polygon points="300,88 308,92 300,96" fill="#f59e0b" />
          <text x="252" y="85" fill="#fcd34d" font-family="'Inter', sans-serif" font-size="7.5">Online Detected</text>

          <!-- Box 2: Sync Engine -->
          <rect x="310" y="22" width="220" height="140" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5" />
          <text x="320" y="44" fill="#f59e0b" font-family="'Outfit', sans-serif" font-size="10" font-weight="700">2. SECURE SYNC INGESTION</text>
          <rect x="320" y="54" width="200" height="24" rx="3" fill="#b45309" />
          <text x="330" y="70" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8" font-weight="600">🔐 Encrypted Batch Payload (GZIP)</text>
          
          <rect x="320" y="86" width="200" height="24" rx="3" fill="#c2410c" />
          <text x="330" y="102" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8" font-weight="600">📬 Publish to RabbitMQ Topic</text>

          <rect x="320" y="118" width="200" height="24" rx="3" fill="#7c2d12" />
          <text x="330" y="134" fill="#fed7aa" font-family="'Inter', sans-serif" font-size="7.5">⚡ HTTP 202 Accepted (&lt; 20ms)</text>

          <!-- Arrow 2 to 3 -->
          <path d="M530 92 L585 92" stroke="#22c55e" stroke-width="2" />
          <polygon points="585,88 593,92 585,96" fill="#22c55e" />
          <text x="536" y="85" fill="#86efac" font-family="'Inter', sans-serif" font-size="7.5">Async Consume</text>

          <!-- Box 3: Master Reconciliation -->
          <rect x="595" y="22" width="200" height="140" rx="5" fill="#1e293b" stroke="#22c55e" stroke-width="1.5" />
          <text x="605" y="44" fill="#4ade80" font-family="'Outfit', sans-serif" font-size="10" font-weight="700">3. MASTER RECONCILE</text>
          <rect x="605" y="54" width="180" height="24" rx="3" fill="#14532d" />
          <text x="615" y="70" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8" font-weight="600">🗄️ MySQL Master Ledgers</text>
          
          <rect x="605" y="86" width="180" height="24" rx="3" fill="#166534" />
          <text x="615" y="102" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8" font-weight="600">⚖️ Lamport Timestamp Order</text>

          <rect x="605" y="118" width="180" height="24" rx="3" fill="#15803d" />
          <text x="615" y="134" fill="#dcfce7" font-family="'Inter', sans-serif" font-size="7.5">✅ ACK & Stock Vector Update</text>
        </svg>
      </div>

      <div class="callout callout-perf">
        <div class="callout-title">⚖️ Conflict-Free Deterministic Merge Rule</div>
        If two sales branches sell the final unit of the same spare part simultaneously while both are offline, transactions are ordered by <strong>Cryptographic Millisecond Lamport Timestamps</strong>. The secondary order generates an automated Backorder Stock Requisition with instant cashier notification.
      </div>
    </div>

    <div class="page-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain</div>
      <div>Document Reference: SL-POP-ERP-ARCH-001 • Page 5 of 9</div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 6: SECTION 7 (CYBERSECURITY, ZERO-TRUST & JWT REPLAY DEFENSE)
       ========================================================================= -->
  <div class="page page-break">
    <div>
      <div class="mini-header">
        <span class="mini-header-title">Technical Architecture Specification</span>
        <span>Section 7: Cybersecurity & Cryptography</span>
      </div>

      <h2 class="section-title">7. Cybersecurity Architecture, Zero-Trust Model & Cryptography</h2>
      <p>
        The Popular Auto Spare ERP follows a strict <strong>Zero-Trust Security Architecture</strong>. Every single API request is authenticated, cryptographically signed, rate-limited, and audited against replay attacks.
      </p>

      <div class="grid-3">
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">🔑</span>
            <span>Rotating JWT Authentication</span>
          </div>
          <ul style="font-size:7.8px;">
            <li><strong>Access Token (15m):</strong> Short-lived RS256 signed.</li>
            <li><strong>Refresh Token (30d):</strong> Stored in `HttpOnly` Secure cookie.</li>
            <li><strong>Sliding JTI Whitelist:</strong> Redis revokes stolen tokens immediately.</li>
          </ul>
        </div>
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">🔒</span>
            <span>Data-at-Rest Field Crypto</span>
          </div>
          <ul style="font-size:7.8px;">
            <li><strong>AES-256-GCM:</strong> Encrypts CPR, commercial records, BenefitPay tokens.</li>
            <li><strong>Argon2id Hashing:</strong> 64MB memory cost for employee credentials.</li>
            <li><strong>Per-Tenant Salts:</strong> Isolated encryption vectors.</li>
          </ul>
        </div>
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">🛡️</span>
            <span>Tamper-Proof Audit Trail</span>
          </div>
          <ul style="font-size:7.8px;">
            <li><strong>SHA-256 Block Chaining:</strong> Financial ledger lines form a hash chain.</li>
            <li><strong>IP & Geo-Fencing:</strong> Captures device fingerprints and login IPs.</li>
            <li><strong>Immutable Logs:</strong> Write-once audit tables preventing edits.</li>
          </ul>
        </div>
      </div>

      <div class="diagram-container">
        <div class="diagram-title">
          <span>Zero-Trust Request Verification & Cryptographic Flow</span>
          <span style="color:#94a3b8; font-size:8px;">Figure 4: Multi-Stage Shield Pipeline</span>
        </div>

        <svg class="diagram-svg" viewBox="0 0 820 85" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="820" height="85" rx="6" fill="#0f172a" />
          
          <rect x="15" y="15" width="140" height="52" rx="4" fill="#1e293b" stroke="#38bdf8" />
          <text x="25" y="32" fill="#38bdf8" font-family="'Outfit', sans-serif" font-size="8.5" font-weight="700">1. TLS 1.3 INGRESS</text>
          <text x="25" y="46" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5">Strict HSTS (2 Years)</text>
          <text x="25" y="58" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7">ECDHE-ECDSA Ciphers</text>

          <path d="M155 41 L180 41" stroke="#38bdf8" stroke-width="1.5" />
          <polygon points="180,38 185,41 180,44" fill="#38bdf8" />

          <rect x="185" y="15" width="150" height="52" rx="4" fill="#1e293b" stroke="#e11d48" />
          <text x="195" y="32" fill="#f43f5e" font-family="'Outfit', sans-serif" font-size="8.5" font-weight="700">2. WAF & RATE SHIELD</text>
          <text x="195" y="46" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5">ModSecurity OWASP Core</text>
          <text x="195" y="58" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7">Token Bucket Rate Limits</text>

          <path d="M335 41 L360 41" stroke="#e11d48" stroke-width="1.5" />
          <polygon points="360,38 365,41 360,44" fill="#e11d48" />

          <rect x="365" y="15" width="130" height="52" rx="4" fill="#1e293b" stroke="#a855f7" />
          <text x="375" y="32" fill="#c084fc" font-family="'Outfit', sans-serif" font-size="8.5" font-weight="700">3. JWT REPLAY FILTER</text>
          <text x="375" y="46" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5">Redis JTI Nonce Check</text>
          <text x="375" y="58" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7">Bitmask Permissions</text>

          <path d="M495 41 L520 41" stroke="#a855f7" stroke-width="1.5" />
          <polygon points="520,38 525,41 520,44" fill="#a855f7" />

          <rect x="525" y="15" width="140" height="52" rx="4" fill="#1e293b" stroke="#ea580c" />
          <text x="535" y="32" fill="#fb923c" font-family="'Outfit', sans-serif" font-size="8.5" font-weight="700">4. FIELD CRYPTO</text>
          <text x="535" y="46" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5">AES-256-GCM Encryption</text>
          <text x="535" y="58" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7">CPR/CR & Card Token Tagged</text>

          <path d="M665 41 L690 41" stroke="#ea580c" stroke-width="1.5" />
          <polygon points="690,38 695,41 690,44" fill="#ea580c" />

          <rect x="695" y="15" width="110" height="52" rx="4" fill="#1e293b" stroke="#22c55e" />
          <text x="705" y="32" fill="#4ade80" font-family="'Outfit', sans-serif" font-size="8.5" font-weight="700">5. AUDIT LOG</text>
          <text x="705" y="46" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5">Immutable Stream</text>
          <text x="705" y="58" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7">SHA-256 Row Hash</text>
        </svg>
      </div>

      <div class="callout callout-security">
        <div class="callout-title">🛡️ Comprehensive OWASP Top 10 Mitigation Matrix</div>
        <ul style="padding-left:12px; margin-top:2px; font-size:7.8px; line-height:1.32;">
          <li><strong>Injection Attacks (SQLi/Command):</strong> 100% strictly parameterized PDO prepared statements; zero string concatenation in queries.</li>
          <li><strong>Cross-Site Scripting (XSS):</strong> Automatic HTML entity encoding via Twig/React JSX, strict `Content-Security-Policy` headers, and input DOMPurify sanitization.</li>
          <li><strong>Cross-Site Request Forgery (CSRF):</strong> Anti-CSRF cryptographic token validation on state-changing non-GET endpoints combined with `SameSite=Strict` cookies.</li>
          <li><strong>Cryptographic Failures:</strong> Passwords hashed using Argon2id / Bcrypt (cost factor 12); TLS 1.3 encryption for all data in transit with forward secrecy.</li>
          <li><strong>Brute Force Protection:</strong> Redis-backed sliding-window token bucket algorithm enforcing maximum 5 failed attempts per 15 minutes per IP/User.</li>
        </ul>
      </div>
    </div>

    <div class="page-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain</div>
      <div>Document Reference: SL-POP-ERP-ARCH-001 • Page 6 of 9</div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 7: SECTION 8 (3-DOMAIN SERVER TOPOLOGY & GIT CONTROLS GOVERNANCE)
       ========================================================================= -->
  <div class="page page-break">
    <div>
      <div class="mini-header">
        <span class="mini-header-title">Technical Architecture Specification</span>
        <span>Section 8: 3-Domain Topology & Git Version Control</span>
      </div>

      <h2 class="section-title">8. 3-Domain Multi-Environment Topology & Git Version Governance</h2>
      <p>
        To ensure zero downtime, complete isolation of experimental engineering, and rigorous client User Acceptance Testing (UAT), the ERP infrastructure implements <strong>strict Git branching governance</strong> mapped directly to <strong>three isolated domain environments</strong>:
      </p>

      <div class="diagram-container">
        <div class="diagram-title">
          <span>Git Branching Strategy & Multi-Domain Virtual Host Routing</span>
          <span style="color:#94a3b8; font-size:8px;">Figure 5: 3-Tier Environment Isolation & Release Automation Pipeline</span>
        </div>

        <svg class="diagram-svg" viewBox="0 0 820 180" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="820" height="180" rx="6" fill="#0f172a" />
          
          <!-- Git Control Hub -->
          <rect x="20" y="16" width="155" height="148" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" />
          <text x="32" y="38" fill="#38bdf8" font-family="'Outfit', sans-serif" font-size="10" font-weight="700">GIT REPOSITORY</text>
          <text x="32" y="54" fill="#ffffff" font-family="'Inter', sans-serif" font-size="8" font-weight="600">Enterprise CI/CD Hub</text>
          <text x="32" y="72" fill="#c084fc" font-family="'Inter', sans-serif" font-size="7.5">🌿 develop (Active Sprint)</text>
          <text x="32" y="88" fill="#fde047" font-family="'Inter', sans-serif" font-size="7.5">📦 release/* (UAT Tags)</text>
          <text x="32" y="104" fill="#86efac" font-family="'Inter', sans-serif" font-size="7.5">🛡️ main (Protected / v1.x)</text>
          <rect x="28" y="122" width="138" height="24" rx="3" fill="#0284c7" />
          <text x="36" y="138" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="700">🔒 Signed Commits / PR Gates</text>

          <!-- Routing Arrows -->
          <path d="M175 42 L220 38" stroke="#a855f7" stroke-width="1.5" />
          <polygon points="220,35 226,38 220,41" fill="#a855f7" />

          <path d="M175 88 L220 88" stroke="#eab308" stroke-width="1.5" />
          <polygon points="220,85 226,88 220,91" fill="#eab308" />

          <path d="M175 134 L220 138" stroke="#22c55e" stroke-width="1.5" />
          <polygon points="220,135 226,138 220,141" fill="#22c55e" />

          <!-- Tier 1: Dev -->
          <rect x="230" y="16" width="570" height="44" rx="4" fill="#1e293b" stroke="#a855f7" stroke-width="1.5" />
          <rect x="238" y="22" width="135" height="32" rx="3" fill="#581c87" />
          <text x="246" y="36" fill="#f3e8ff" font-family="'Outfit', sans-serif" font-size="8.5" font-weight="700">1. DEVELOPMENT</text>
          <text x="246" y="48" fill="#d8b4fe" font-family="'Inter', sans-serif" font-size="7">dev.popularbahrain.com</text>

          <text x="382" y="34" fill="#e2e8f0" font-family="'Inter', sans-serif" font-size="7.5">Sprint features, active debug mode, mock BenefitPay sandbox, rapid developer merge.</text>
          <text x="382" y="48" fill="#c084fc" font-family="'Inter', sans-serif" font-size="7">DB: popular_erp_dev  |  Branch: develop  |  CI: Auto-Build & Static Analysis</text>

          <!-- Tier 2: Staging -->
          <rect x="230" y="68" width="570" height="44" rx="4" fill="#1e293b" stroke="#eab308" stroke-width="1.5" />
          <rect x="238" y="74" width="135" height="32" rx="3" fill="#713f12" />
          <text x="246" y="88" fill="#fef9c3" font-family="'Outfit', sans-serif" font-size="8.5" font-weight="700">2. STAGING / UAT</text>
          <text x="246" y="100" fill="#fde047" font-family="'Inter', sans-serif" font-size="7">staging.popularbahrain.com</text>

          <text x="382" y="86" fill="#e2e8f0" font-family="'Inter', sans-serif" font-size="7.5">Client acceptance testing (UAT), pre-release verification, consultant audit & sign-off.</text>
          <text x="382" y="100" fill="#fde047" font-family="'Inter', sans-serif" font-size="7">DB: popular_erp_staging  |  Branch: release/*  |  Gate: Client UAT Sign-off</text>

          <!-- Tier 3: Production -->
          <rect x="230" y="120" width="570" height="44" rx="4" fill="#1e293b" stroke="#22c55e" stroke-width="1.5" />
          <rect x="238" y="126" width="135" height="32" rx="3" fill="#14532d" />
          <text x="246" y="140" fill="#dcfce7" font-family="'Outfit', sans-serif" font-size="8.5" font-weight="700">3. LIVE PRODUCTION</text>
          <text x="246" y="152" fill="#86efac" font-family="'Inter', sans-serif" font-size="7">erp.popularbahrain.com</text>

          <text x="382" y="138" fill="#e2e8f0" font-family="'Inter', sans-serif" font-size="7.5">Live operational billing, inventory ledgers, strict audit trail, zero debug exposure.</text>
          <text x="382" y="152" fill="#86efac" font-family="'Inter', sans-serif" font-size="7">DB: popular_erp_prod  |  Branch: main (Protected)  |  Release: Tagged v1.x (GPG Signed)</text>
        </svg>
      </div>

      <div class="grid-3">
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">🌿</span>
            <span>Branch Protection Controls</span>
          </div>
          <p style="font-size:7.8px;">
            `main` and `staging` branches are <strong>strictly protected</strong>. Direct commits and force pushes (`git push --force`) are completely prohibited. All code merges require mandatory Pull Request (PR) peer review and approval.
          </p>
        </div>
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">🔍</span>
            <span>Automated CI Quality Gates</span>
          </div>
          <p style="font-size:7.8px;">
            Every pull request triggers automated CI pipelines: PHPStan Level 8 static analysis, ESLint syntax validations, security dependency audit (composer/npm audit), and zero-breaking-change database migration dry-runs.
          </p>
        </div>
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">⏪</span>
            <span>Instant Rollback Tags</span>
          </div>
          <p style="font-size:7.8px;">
            Every production deployment creates an immutable Git semantic release tag (`v1.0.1`, `v1.0.2`). In the event of an unforeseen regression, the release pipeline performs an automated rollback in <strong>&lt; 60 seconds</strong>.
          </p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain</div>
      <div>Document Reference: SL-POP-ERP-ARCH-001 • Page 7 of 9</div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 8: SECTION 9 (DATA BACKUP & JETBACKUP 5 DISASTER RECOVERY)
       ========================================================================= -->
  <div class="page page-break">
    <div>
      <div class="mini-header">
        <span class="mini-header-title">Technical Architecture Specification</span>
        <span>Section 9: Backup & Disaster Recovery</span>
      </div>

      <h2 class="section-title">9. Enterprise Data Backup Architecture & JetBackup 5 Incremental Engine</h2>
      <p>
        To ensure enterprise business continuity, complete protection against data corruption, hardware failure, or ransomware, the server infrastructure is provisioned with <strong>dedicated backup storage partitions</strong> and the industry-standard <strong>JetBackup 5 Incremental Backup Utility</strong>.
      </p>

      <div class="grid-3">
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">💽</span>
            <span>Dedicated Disk Partition</span>
          </div>
          <p style="font-size:7.8px;">
            <strong>Quota-Isolated Storage:</strong> A high-performance secondary NVMe mount (`/backup/jetbackup`) is isolated from the root OS and database storage. This guarantees that backup processing never starves ERP application disk space.
          </p>
        </div>
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">⚡</span>
            <span>JetBackup Incremental Process</span>
          </div>
          <p style="font-size:7.8px;">
            <strong>Block-Level Change Tracking:</strong> Only modified disk blocks and incremental database logs are captured after initial seeding. This reduces CPU/IO load by <strong>&gt;85%</strong> and completely eliminates table locking during business hours.
          </p>
        </div>
        <div class="tech-card">
          <div class="tech-card-header">
            <span class="tech-card-icon">⏱️</span>
            <span>MySQL Point-in-Time Recovery</span>
          </div>
          <p style="font-size:7.8px;">
            <strong>Continuous Binary Logs (PITR):</strong> MySQL binary logging (`binlog`) runs continuously, enabling database restoration to the <strong>exact second</strong> prior to any accidental deletion or corruption event.
          </p>
        </div>
      </div>

      <div class="diagram-container">
        <div class="diagram-title">
          <span>JetBackup 5 Incremental Backup & Offsite Disaster Recovery Pipeline</span>
          <span style="color:#94a3b8; font-size:8px;">Figure 6: High-Availability Storage Tiering & Single-Click Restoration Workflow</span>
        </div>

        <svg class="diagram-svg" viewBox="0 0 820 170" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect width="820" height="170" rx="6" fill="#0f172a" />
          
          <!-- Source Tier -->
          <rect x="20" y="18" width="180" height="135" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" />
          <text x="32" y="38" fill="#38bdf8" font-family="'Outfit', sans-serif" font-size="9.5" font-weight="700">1. PRIMARY SERVER DATA</text>
          
          <rect x="30" y="48" width="160" height="24" rx="3" fill="#0369a1" />
          <text x="38" y="64" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🗄️ MySQL 8.0 Master Databases</text>
          
          <rect x="30" y="78" width="160" height="24" rx="3" fill="#0d9488" />
          <text x="38" y="94" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">📁 ERP Application & Storage Assets</text>
          
          <rect x="30" y="108" width="160" height="24" rx="3" fill="#475569" />
          <text x="38" y="124" fill="#f1f5f9" font-family="'Inter', sans-serif" font-size="7.5">📜 Continuous MySQL Binlogs (PITR)</text>

          <!-- Arrow 1 to 2 -->
          <path d="M200 85 L250 85" stroke="#38bdf8" stroke-width="2" />
          <polygon points="250,81 258,85 250,89" fill="#38bdf8" />
          <text x="205" y="78" fill="#94a3b8" font-family="'Inter', sans-serif" font-size="7">Block Diffs</text>

          <!-- JetBackup Engine -->
          <rect x="260" y="18" width="260" height="135" rx="5" fill="#1e293b" stroke="#22c55e" stroke-width="1.5" />
          <text x="272" y="38" fill="#4ade80" font-family="'Outfit', sans-serif" font-size="9.5" font-weight="700">2. JETBACKUP 5 ENGINE (Dedicated Partition)</text>
          
          <rect x="270" y="48" width="240" height="24" rx="3" fill="#14532d" />
          <text x="278" y="64" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">⚡ Hourly Incremental DB Snapshots (No Lock)</text>
          
          <rect x="270" y="78" width="240" height="24" rx="3" fill="#166534" />
          <text x="278" y="94" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">📅 Daily System State Images (/backup/jetbackup)</text>
          
          <rect x="270" y="108" width="240" height="24" rx="3" fill="#15803d" />
          <text x="278" y="124" fill="#dcfce7" font-family="'Inter', sans-serif" font-size="7.5">🔐 AES-256 GCM Snapshot Encryption</text>

          <!-- Arrow 2 to 3 -->
          <path d="M520 85 L570 85" stroke="#22c55e" stroke-width="2" stroke-dasharray="4 2" />
          <polygon points="570,81 578,85 570,89" fill="#22c55e" />
          <text x="526" y="78" fill="#86efac" font-family="'Inter', sans-serif" font-size="7">Encrypted Sync</text>

          <!-- Offsite & Restore Target -->
          <rect x="580" y="18" width="220" height="135" rx="5" fill="#1e293b" stroke="#ea580c" stroke-width="1.5" />
          <text x="592" y="38" fill="#fb923c" font-family="'Outfit', sans-serif" font-size="9.5" font-weight="700">3. OFFSITE CLOUD & DISASTER RECOVERY</text>
          
          <rect x="590" y="48" width="200" height="24" rx="3" fill="#7c2d12" />
          <text x="598" y="64" fill="#ffedd5" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">☁️ Remote Encrypted Cloud Vault (S3)</text>
          
          <rect x="590" y="78" width="200" height="24" rx="3" fill="#9a3412" />
          <text x="598" y="94" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🖱️ 1-Click Single Table / Database Restore</text>
          
          <rect x="590" y="108" width="200" height="24" rx="3" fill="#b45309" />
          <text x="598" y="124" fill="#ffffff" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600">🚨 Full Bare-Metal Rebuild (&lt; 30 Mins)</text>
        </svg>
      </div>

      <div class="arch-table-wrap">
      <table class="arch-table">
        <thead>
          <tr>
            <th style="width:20%;">Metric / Objective</th>
            <th style="width:25%;">Architectural Target</th>
            <th style="width:35%;">Implementation Mechanism</th>
            <th style="width:20%;">Verification Schedule</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>RPO (Recovery Point)</strong></td>
            <td><strong>&lt; 1 Hour</strong> (Incremental)<br><strong>&lt; 1 Min</strong> (with PITR)</td>
            <td>JetBackup hourly delta snapshots + continuous MySQL binary log streaming.</td>
            <td>Continuous automated check</td>
          </tr>
          <tr>
            <td><strong>RTO (Recovery Time)</strong></td>
            <td><strong>&lt; 30 Minutes</strong> (Full Server)<br><strong>&lt; 5 Minutes</strong> (Database)</td>
            <td>Direct JetBackup 1-click snapshot restore without manual file extraction.</td>
            <td>Quarterly simulated drill</td>
          </tr>
          <tr>
            <td><strong>Retention Policy</strong></td>
            <td>24h Hourly • 30d Daily • 12m Monthly</td>
            <td>Automated rolling grandfather-father-son backup rotation with auto-pruning.</td>
            <td>Daily automated audit</td>
          </tr>
          <tr>
            <td><strong>Disaster Offsite Vault</strong></td>
            <td>100% Offsite Mirroring</td>
            <td>Automated secondary sync to encrypted cloud object storage (AWS S3 / Wasabi).</td>
            <td>Nightly offsite checksum check</td>
          </tr>
        </tbody>
      </table>
        </div>

      <div class="callout callout-backup">
        <div class="callout-title">🛡️ Step-by-Step Disaster Recovery Runbook</div>
        In the event of total server hardware failure or data corruption: <strong>(1)</strong> Provision replacement VM instance &rarr; <strong>(2)</strong> Mount JetBackup storage partition &rarr; <strong>(3)</strong> Trigger 1-Click JetBackup snapshot restoration &rarr; <strong>(4)</strong> Replay continuous MySQL binary logs to exact point of failure &rarr; <strong>(5)</strong> Run automated ledger SHA-256 integrity hash verification &rarr; <strong>(6)</strong> Switch DNS / Nginx traffic back online.
      </div>
    </div>

    <div class="page-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain</div>
      <div>Document Reference: SL-POP-ERP-ARCH-001 • Page 8 of 9</div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 9: SECTION 10 (ARCHITECTURAL GOVERNANCE & SIGN-OFF)
       ========================================================================= -->
  <div class="page">
    <div>
      <div class="mini-header">
        <span class="mini-header-title">Technical Architecture Specification</span>
        <span>Section 10: Governance & Technical Sign-off</span>
      </div>

      <h2 class="section-title">10. Architectural Governance & Technical Sign-off</h2>
      <p>
        This Technical Architecture Specification serves as the foundational engineering baseline for the Popular Auto Spare ERP Solution. It formalizes all performance benchmarks, queueing pipelines, offline auto-sync engines, cybersecurity layers, Git version controls, and JetBackup disaster recovery procedures across the Kingdom of Bahrain.
      </p>

      <div class="signoff-grid">
        <!-- 1. SaNDS Lab (Left) -->
        <div class="signoff-card">
          <div class="signoff-logo-box">
            <img class="signoff-logo sands-approval-logo" src="{logo_sands_color}" alt="SaNDS Lab Middle East" />
          </div>
          <div class="signoff-role">SERVICE PROVIDER & LEAD ARCHITECT</div>
          <div class="signoff-org"><?php echo htmlspecialchars($sands_sig && !empty($sands_sig['organization']) ? $sands_sig['organization'] : 'SaNDS Lab Middle East W.L.L'); ?></div>
          <div class="signoff-details">
            <div><strong>Lead Architect:</strong> <?php echo htmlspecialchars($sands_sig && !empty($sands_sig['full_name']) ? $sands_sig['full_name'] : 'Ajit Kumar KV'); ?></div>
            <div><strong>Role:</strong> <?php echo htmlspecialchars($sands_sig && !empty($sands_sig['role']) ? $sands_sig['role'] : 'Super Admin & Director'); ?></div>
            <div><strong>Date:</strong> <?php echo htmlspecialchars($sands_sig && !empty($sands_sig['signed_at']) ? date('d/m/Y', strtotime($sands_sig['signed_at'])) : '—'); ?></div>
          </div>
          <?php if ($sands_sig && !empty($sands_sig['signature_data'])): ?>
            <div style="text-align:center; padding:3px 0;">
              <img class="sig-img-preview" src="<?php echo $sands_sig['signature_data']; ?>" alt="Signature" />
              <div style="display:flex; justify-content:center; align-items:center; gap:4px;">
                <span class="sig-status-badge sig-status-signed">✅ Digitally Signed</span>
                <?php if (!empty($authenticated_user) && (strtolower($authenticated_user) === 'ajit@sandslab.com' || strtolower($authenticated_user) === 'info@sandslab.com')): ?>
                  <button type="button" onclick="adminClearSingleSig(this, '<?php echo htmlspecialchars(!empty($sands_sig['email']) ? $sands_sig['email'] : 'ajit@sandslab.com', ENT_QUOTES); ?>', 'SaNDS Lab')" class="no-print" style="background:#fee2e2; border:1px solid #fca5a5; color:#991b1b; font-size:8px; font-weight:700; border-radius:3px; padding:1px 4px; cursor:pointer;" title="Clear signature">🗑️ Clear</button>
                <?php endif; ?>
              </div>
            </div>
          <?php else: ?>
            <div class="signoff-placeholder"></div>
            <div class="signoff-caption">Authorized Technical Signature & Seal</div>
          <?php endif; ?>
        </div>

        <!-- 2. Popular Auto Spare (ALWAYS CENTER) -->
        <div class="signoff-card">
          <div class="signoff-logo-box">
            <img class="signoff-logo" src="{logo_popular}" alt="Popular Auto Spare" />
          </div>
          <div class="signoff-role">CLIENT REPRESENTATIVE & OWNER</div>
          <div class="signoff-org"><?php echo htmlspecialchars($popular_sig && !empty($popular_sig['organization']) ? $popular_sig['organization'] : 'Popular Auto Spare & A/C Parts Co. W.L.L'); ?></div>
          <div class="signoff-details">
            <div><strong>Client Director:</strong> <?php echo htmlspecialchars($popular_sig && !empty($popular_sig['full_name']) ? $popular_sig['full_name'] : 'Managing Director'); ?></div>
            <div><strong>Role:</strong> <?php echo htmlspecialchars($popular_sig && !empty($popular_sig['role']) ? $popular_sig['role'] : 'Executive Sponsor'); ?></div>
            <div><strong>Date:</strong> <?php echo htmlspecialchars($popular_sig && !empty($popular_sig['signed_at']) ? date('d/m/Y', strtotime($popular_sig['signed_at'])) : '—'); ?></div>
          </div>
          <?php if ($popular_sig && !empty($popular_sig['signature_data'])): ?>
            <div style="text-align:center; padding:3px 0;">
              <img class="sig-img-preview" src="<?php echo $popular_sig['signature_data']; ?>" alt="Signature" />
              <div style="display:flex; justify-content:center; align-items:center; gap:4px;">
                <span class="sig-status-badge sig-status-signed">✅ Digitally Signed</span>
                <?php if (!empty($authenticated_user) && (strtolower($authenticated_user) === 'ajit@sandslab.com' || strtolower($authenticated_user) === 'info@sandslab.com')): ?>
                  <button type="button" onclick="adminClearSingleSig(this, '<?php echo htmlspecialchars(!empty($popular_sig['email']) ? $popular_sig['email'] : 'director@popularbahrain.com', ENT_QUOTES); ?>', 'Popular Auto Spare')" class="no-print" style="background:#fee2e2; border:1px solid #fca5a5; color:#991b1b; font-size:8px; font-weight:700; border-radius:3px; padding:1px 4px; cursor:pointer;" title="Clear signature">🗑️ Clear</button>
                <?php endif; ?>
              </div>
            </div>
          <?php else: ?>
            <div class="signoff-placeholder"></div>
            <div class="signoff-caption">Client Technical Approval & Acceptance</div>
          <?php endif; ?>
        </div>

        <!-- 3. UniGlobal Consultancy (Right) -->
        <div class="signoff-card">
          <div class="signoff-logo-box">
            <img class="signoff-logo" src="{logo_uniglobal_color}" alt="UniGlobal Consultancy" />
          </div>
          <div class="signoff-role">INDEPENDENT CONSULTANT & AUDITOR</div>
          <div class="signoff-org"><?php echo htmlspecialchars($uniglobal_sig && !empty($uniglobal_sig['organization']) ? $uniglobal_sig['organization'] : 'UniGlobal Consultancy'); ?></div>
          <div class="signoff-details">
            <div><strong>Lead Consultant:</strong> <?php echo htmlspecialchars($uniglobal_sig && !empty($uniglobal_sig['full_name']) ? $uniglobal_sig['full_name'] : 'Lead IT Consultant'); ?></div>
            <div><strong>Role:</strong> <?php echo htmlspecialchars($uniglobal_sig && !empty($uniglobal_sig['role']) ? $uniglobal_sig['role'] : 'Architecture Reviewer'); ?></div>
            <div><strong>Date:</strong> <?php echo htmlspecialchars($uniglobal_sig && !empty($uniglobal_sig['signed_at']) ? date('d/m/Y', strtotime($uniglobal_sig['signed_at'])) : '—'); ?></div>
          </div>
          <?php if ($uniglobal_sig && !empty($uniglobal_sig['signature_data'])): ?>
            <div style="text-align:center; padding:3px 0;">
              <img class="sig-img-preview" src="<?php echo $uniglobal_sig['signature_data']; ?>" alt="Signature" />
              <div style="display:flex; justify-content:center; align-items:center; gap:4px;">
                <span class="sig-status-badge sig-status-signed">✅ Digitally Signed</span>
                <?php if (!empty($authenticated_user) && (strtolower($authenticated_user) === 'ajit@sandslab.com' || strtolower($authenticated_user) === 'info@sandslab.com')): ?>
                  <button type="button" onclick="adminClearSingleSig(this, '<?php echo htmlspecialchars(!empty($uniglobal_sig['email']) ? $uniglobal_sig['email'] : 'consultant@uniglobal.com', ENT_QUOTES); ?>', 'UniGlobal Consultancy')" class="no-print" style="background:#fee2e2; border:1px solid #fca5a5; color:#991b1b; font-size:8px; font-weight:700; border-radius:3px; padding:1px 4px; cursor:pointer;" title="Clear signature">🗑️ Clear</button>
                <?php endif; ?>
              </div>
            </div>
          <?php else: ?>
            <div class="signoff-placeholder"></div>
            <div class="signoff-caption">Independent Review & Recommendation</div>
          <?php endif; ?>
        </div>
      </div>

      <?php if ($is_finalized): ?>
        <!-- Official Digital Execution Certificate -->
        <div class="finalized-cert-wrap">
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #86efac; padding-bottom:6px; margin-bottom:6px;">
            <div style="display:flex; align-items:center; gap:6px;">
              <span style="font-size:15px;">🛡️</span>
              <div>
                <div style="font-family:'Outfit',sans-serif; font-size:10.5px; font-weight:800; color:#14532d;">OFFICIAL DIGITAL EXECUTION CERTIFICATE & CRYPTOGRAPHIC SEAL</div>
                <div style="font-size:7px; color:#15803d;">Doc Ref: SL-POP-ERP-ARCH-001 • Legally Binding Technical Baseline • Kingdom of Bahrain</div>
              </div>
            </div>
            <div style="background:#15803d; color:#ffffff; font-size:7.5px; font-weight:700; padding:2px 6px; border-radius:3px;">
              SEALED & LOCKED
            </div>
          </div>
          <div class="finalized-cert-grid">
            <div><strong>Finalized By:</strong><br><?php echo htmlspecialchars(!empty($doc_meta['finalized_by']) ? $doc_meta['finalized_by'] : 'ajit@sandslab.com'); ?></div>
            <div><strong>Finalized At:</strong><br><?php echo htmlspecialchars(!empty($doc_meta['finalized_at']) ? date('d/m/Y H:i:s', strtotime($doc_meta['finalized_at'])) : date('d/m/Y H:i:s')); ?></div>
            <div><strong>Integrity Check:</strong><br>SHA-256 Validated</div>
            <div><strong>Jurisdiction:</strong><br>Kingdom of Bahrain</div>
          </div>
        </div>
      <?php endif; ?>

    </div>

    <div class="page-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain</div>
      <div>Document Reference: SL-POP-ERP-ARCH-001 • Page 9 of 9 (End of Specification)</div>
    </div>
  </div>

</div>

<!-- Interactive Digital Signature Modal (No Print) -->
<?php if (!$is_finalized): ?>
  <div class="sign-interactive-card no-print">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
      <div>
        <h3 style="font-family:'Outfit',sans-serif; font-size:12.5px; color:var(--primary); font-weight:700;">🖋️ Stakeholder Digital Signature Authorization</h3>
        <p style="font-size:9px; color:var(--gray-500); margin:0;">Draw your signature below using mouse or touchscreen.</p>
      </div>
      <div style="font-size:9px; color:var(--primary); font-weight:700;">
        Active User: <code><?php echo htmlspecialchars($authenticated_user ? $authenticated_user : 'Client'); ?></code>
      </div>
    </div>

    <form id="docSignForm" onsubmit="submitDigitalSignature(event)">
      <div class="signer-info-grid">
        <div class="signer-input-group">
          <label>Signer Full Name</label>
          <input type="text" id="signerName" required value="<?php echo htmlspecialchars($user_record ? $user_record['full_name'] : ($my_sig ? $my_sig['full_name'] : '')); ?>" placeholder="e.g. John Doe">
        </div>
        <div class="signer-input-group">
          <label>Organization / Company</label>
          <input type="text" id="signerOrg" required value="<?php echo htmlspecialchars($user_record ? $user_record['organization'] : ($my_sig ? $my_sig['organization'] : 'Popular Auto Spare & A/C Parts Co. W.L.L')); ?>" placeholder="e.g. Popular Auto Spare">
        </div>
        <div class="signer-input-group">
          <label>Designation / Role</label>
          <input type="text" id="signerRole" required value="<?php echo htmlspecialchars($user_record ? $user_record['role'] : ($my_sig ? $my_sig['role'] : 'Executive Sponsor')); ?>" placeholder="e.g. Managing Director">
        </div>
      </div>

      <div class="canvas-container">
        <canvas id="sigCanvas"></canvas>
        <div id="canvasPlaceholder" class="canvas-placeholder-text">
          ✍️ Draw signature here using finger (touch) or mouse pointer
        </div>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <div style="display:flex; gap:6px;">
          <button type="button" onclick="clearSignatureCanvas()" class="btn-tool" style="font-size:9px; padding:3px 8px;">Clear Pad</button>
          <button type="button" onclick="undoSignatureStroke()" class="btn-tool" style="font-size:9px; padding:3px 8px;">Undo Stroke</button>
        </div>
        <div style="font-size:8.5px; color:var(--gray-500);">
          High-Resolution Encrypted Electronic Signature
        </div>
      </div>

      <div style="display:flex; align-items:flex-start; gap:8px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; padding:7px; margin-bottom:8px;">
        <input type="checkbox" id="signConsent" required style="width:13px; height:13px; margin-top:1px; cursor:pointer;">
        <label for="signConsent" style="font-size:9px; color:var(--gray-700); cursor:pointer; line-height:1.35;">
          I confirm that I have reviewed the ERP Technical Architecture, Cybersecurity Specification, RabbitMQ pipeline, offline storage engine, 3-domain topology, Git branching controls, and JetBackup incremental disaster recovery baseline, and formally authorize this technical specification.
        </label>
      </div>

      <div style="display:flex; justify-content:flex-end; gap:8px;">
        <button type="submit" id="btnSubmitSign" class="btn-tool" style="background:#15803d; color:#ffffff; border-color:#16a34a; font-weight:700; padding:7px 14px; font-size:10.5px;">
          Submit & Authorize Technical Architecture
        </button>
      </div>
    </form>
  </div>
<?php endif; ?>

<!-- Client Signature Pad Script -->
<script class="no-print">
  var canvas = document.getElementById('sigCanvas');
  var ctx = canvas ? canvas.getContext('2d') : null;
  var isDrawing = false;
  var hasDrawn = false;
  var strokes = [];
  var currentStroke = [];

  function initSignaturePad() {{
    if (!canvas) return;
    var rect = canvas.getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    ctx.strokeStyle = '#0a2540';
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing);

    canvas.addEventListener('touchstart', function(e) {{
      e.preventDefault();
      var touch = e.touches[0];
      var mouseEvent = new MouseEvent('mousedown', {{
        clientX: touch.clientX,
        clientY: touch.clientY
      }});
      canvas.dispatchEvent(mouseEvent);
    }}, {{ passive: false }});

    canvas.addEventListener('touchmove', function(e) {{
      e.preventDefault();
      var touch = e.touches[0];
      var mouseEvent = new MouseEvent('mousemove', {{
        clientX: touch.clientX,
        clientY: touch.clientY
      }});
      canvas.dispatchEvent(mouseEvent);
    }}, {{ passive: false }});

    canvas.addEventListener('touchend', function(e) {{
      e.preventDefault();
      var mouseEvent = new MouseEvent('mouseup', {{}});
      canvas.dispatchEvent(mouseEvent);
    }}, {{ passive: false }});
  }}

  function getCanvasPos(e) {{
    var rect = canvas.getBoundingClientRect();
    return {{
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    }};
  }}

  function startDrawing(e) {{
    isDrawing = true;
    hasDrawn = true;
    var placeholder = document.getElementById('canvasPlaceholder');
    if (placeholder) placeholder.style.display = 'none';
    var pos = getCanvasPos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
    currentStroke = [pos];
  }}

  function draw(e) {{
    if (!isDrawing) return;
    var pos = getCanvasPos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    currentStroke.push(pos);
  }}

  function stopDrawing() {{
    if (isDrawing) {{
      isDrawing = false;
      strokes.push(currentStroke);
      currentStroke = [];
    }}
  }}

  function clearSignatureCanvas() {{
    if (!canvas || !ctx) return;
    var rect = canvas.getBoundingClientRect();
    ctx.clearRect(0, 0, rect.width, rect.height);
    strokes = [];
    hasDrawn = false;
    var placeholder = document.getElementById('canvasPlaceholder');
    if (placeholder) placeholder.style.display = 'block';
  }}

  function undoSignatureStroke() {{
    if (!canvas || !ctx || strokes.length === 0) return;
    strokes.pop();
    var rect = canvas.getBoundingClientRect();
    ctx.clearRect(0, 0, rect.width, rect.height);
    if (strokes.length === 0) {{
      hasDrawn = false;
      var placeholder = document.getElementById('canvasPlaceholder');
      if (placeholder) placeholder.style.display = 'block';
      return;
    }}
    for (var i = 0; i < strokes.length; i++) {{
      var s = strokes[i];
      if (s.length > 0) {{
        ctx.beginPath();
        ctx.moveTo(s[0].x, s[0].y);
        for (var j = 1; j < s.length; j++) {{
          ctx.lineTo(s[j].x, s[j].y);
        }}
        ctx.stroke();
      }}
    }}
  }}

  function showLoadingModal(title, text) {{
    Swal.fire({{
      title: title || 'Processing Request...',
      html: '<div style=\"display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px; margin:16px 0 6px 0;\">' +
            '  <div style=\"width:42px; height:42px; border:4px solid #fecdd3; border-top-color:#e11d48; border-radius:50%; animation:docSpin 0.75s linear infinite;\"></div>' +
            '  <div style=\"font-size:13px; color:#475569; font-weight:500;\">' + (text || 'Please wait while we update documents & synchronize PDF...') + '</div>' +
            '</div>',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showConfirmButton: false,
      didOpen: () => {{
        Swal.showLoading();
      }}
    }});
  }}

  function submitDigitalSignature(e) {{
    e.preventDefault();
    if (!hasDrawn || strokes.length === 0) {{
      Swal.fire({{
        icon: 'warning',
        title: 'Signature Required',
        text: 'Please draw your signature in the designated pad before submitting.',
        confirmButtonColor: '#0a2540'
      }});
      return;
    }}

    var sigData = canvas.toDataURL('image/png');
    var name = document.getElementById('signerName').value.trim();
    var org = document.getElementById('signerOrg').value.trim();
    var role = document.getElementById('signerRole').value.trim();
    var btn = document.getElementById('btnSubmitSign');
    btn.disabled = true;
    btn.innerText = 'Recording Signature...';

    var fd = new FormData();
    fd.append('action', 'sign_document');
    fd.append('doc_id', 'SL-POP-ERP-ARCH-001');
    fd.append('signer_email', '<?php echo !empty($authenticated_user) ? htmlspecialchars($authenticated_user, ENT_QUOTES) : ""; ?>');
    fd.append('signature_data', sigData);
    fd.append('signer_name', name);
    fd.append('signer_org', org);
    fd.append('signer_role', role);

    fetch(window.location.href, {{ method: 'POST', body: fd }})
    .then(function(r) {{
      if (!r.ok) {{
        throw new Error('Server returned HTTP ' + r.status);
      }}
      return r.json();
    }})
    .then(function(data) {{
      if (data && data.success) {{
        Swal.fire({{
          icon: 'success',
          title: 'Signature Recorded!',
          text: data.message || 'Technical Architecture document signed successfully!',
          confirmButtonColor: '#15803d'
        }}).then(function() {{ window.location.reload(); }});
      }} else {{
        btn.disabled = false;
        btn.innerText = 'Submit & Authorize Technical Architecture';
        Swal.fire({{ icon: 'error', title: 'Signature Failed', text: (data && data.message) ? data.message : 'Could not record signature.', confirmButtonColor: '#be123c' }});
      }}
    }})
    .catch(function(err) {{
      btn.disabled = false;
      btn.innerText = 'Submit & Authorize Technical Architecture';
      Swal.fire({{ icon: 'error', title: 'Submission Error', text: 'Operation failed: ' + (err.message || 'Network error'), confirmButtonColor: '#be123c' }});
    }});
  }}

  function adminConfirmFinalizeDoc() {{
    Swal.fire({{
      title: 'Finalize & Lock Specification?',
      text: 'This will lock the technical design baseline and activate the Digital Execution Certificate.',
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#15803d',
      cancelButtonColor: '#64748b',
      confirmButtonText: 'Yes, Finalize & Lock',
      cancelButtonText: 'Cancel'
    }}).then(function(result) {{
      if (result.isConfirmed) {{
        showLoadingModal('Finalizing & Sealing Document...', 'Generating official locked PDF & Digital Execution Certificates...');
        var fd = new FormData();
        fd.append('action', 'finalize_document');
        fd.append('admin_action', 'finalize_document');
        fd.append('doc_id', 'SL-POP-ERP-ARCH-001');

        fetch(window.location.href, {{ method: 'POST', body: fd }})
        .then(function(r) {{ return r.json(); }})
        .then(function(d) {{
          Swal.close();
          if (d && d.success) {{
            Swal.fire({{ icon: 'success', title: 'Document Finalized', text: d.message || 'Specification locked successfully.', confirmButtonColor: '#15803d' }})
            .then(function() {{ window.location.reload(); }});
          }} else {{
            Swal.fire({{ icon: 'error', title: 'Error', text: (d && d.message) ? d.message : 'Could not finalize document.', confirmButtonColor: '#be123c' }});
          }}
        }})
        .catch(function(err) {{
          Swal.close();
          Swal.fire({{ icon: 'error', title: 'Network Error', text: 'Operation failed: ' + (err.message || 'Network error'), confirmButtonColor: '#be123c' }});
        }});
      }}
    }});
  }}

  function adminPromptReopenDoc() {{
    Swal.fire({{
      title: 'Re-Open Specification?',
      html: 'Choose whether you want to re-open for revisions preserving signatures, or clear all signatures.',
      icon: 'warning',
      showCancelButton: true,
      showDenyButton: true,
      confirmButtonColor: '#b45309',
      denyButtonColor: '#be123c',
      cancelButtonColor: '#64748b',
      confirmButtonText: '🔓 Re-Open (Keep Signatures)',
      denyButtonText: '🧹 Re-Open & Clear All Signatures',
      cancelButtonText: 'Cancel'
    }}).then(function(result) {{
      if (result.isConfirmed) {{
        adminExecuteReopen(false);
      }} else if (result.isDenied) {{
        adminExecuteReopen(true);
      }}
    }});
  }}

  function adminExecuteReopen(clearSigs) {{
    showLoadingModal('Re-opening Document...', 'Updating lifecycle status...');
    var fd = new FormData();
    fd.append('action', 'admin_reopen_document');
    fd.append('doc_id', 'SL-POP-ERP-ARCH-001');
    fd.append('clear_signatures', clearSigs ? '1' : '0');

    fetch(window.location.href, {{ method: 'POST', body: fd }})
    .then(function(r) {{ return r.json(); }})
    .then(function(d) {{
      Swal.close();
      if (d && d.success) {{
        Swal.fire({{ icon: 'success', title: 'Document Reopened', text: d.message || 'Document reopened.', confirmButtonColor: '#15803d' }})
        .then(function() {{ window.location.reload(); }});
      }} else {{
        Swal.fire({{ icon: 'error', title: 'Error', text: (d && d.message) ? d.message : 'Failed to reopen document.', confirmButtonColor: '#be123c' }});
      }}
    }})
    .catch(function(err) {{
      Swal.close();
      Swal.fire({{ icon: 'error', title: 'Network Error', text: 'Operation failed: ' + (err.message || 'Network error'), confirmButtonColor: '#be123c' }});
    }});
  }}

  function adminConfirmClearAllSigs() {{
    Swal.fire({{
      title: 'Clear All Recorded Signatures?',
      text: 'Are you sure you want to delete all signatures for this specification?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#be123c',
      cancelButtonColor: '#64748b',
      confirmButtonText: 'Yes, Clear All',
      cancelButtonText: 'Cancel'
    }}).then(function(result) {{
      if (result.isConfirmed) {{
        showLoadingModal('Clearing All Signatures...', 'Deleting ink signatures...');
        var fd = new FormData();
        fd.append('action', 'admin_clear_all_signatures');
        fd.append('doc_id', 'SL-POP-ERP-ARCH-001');

        fetch(window.location.href, {{ method: 'POST', body: fd }})
        .then(function(r) {{ return r.json(); }})
        .then(function(d) {{
          Swal.close();
          if (d && d.success) {{
            Swal.fire({{ icon: 'success', title: 'Signatures Cleared', text: d.message || 'All signatures cleared.', confirmButtonColor: '#15803d' }})
            .then(function() {{ window.location.reload(); }});
          }} else {{
            Swal.fire({{ icon: 'error', title: 'Error', text: (d && d.message) ? d.message : 'Could not clear signatures.', confirmButtonColor: '#be123c' }});
          }}
        }})
        .catch(function(err) {{
          Swal.close();
          Swal.fire({{ icon: 'error', title: 'Network Error', text: 'Operation failed: ' + (err.message || 'Network error'), confirmButtonColor: '#be123c' }});
        }});
      }}
    }});
  }}

  function adminClearSingleSig(btn, email, name) {{
    Swal.fire({{
      title: 'Clear Stakeholder Signature?',
      html: 'Are you sure you want to clear the signature for <strong>' + name + '</strong> (' + email + ')?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#be123c',
      cancelButtonColor: '#64748b',
      confirmButtonText: 'Yes, Clear',
      cancelButtonText: 'Cancel'
    }}).then(function(result) {{
      if (result.isConfirmed) {{
        if (btn && btn.tagName === 'BUTTON') {{
          btn.innerHTML = '<span class=\"inline-spinner\"></span> Clearing...';
          btn.disabled = true;
        }}
        showLoadingModal('Clearing Signature...', 'Removing signature for ' + name + '...');
        var fd = new FormData();
        fd.append('action', 'admin_clear_signature');
        fd.append('doc_id', 'SL-POP-ERP-ARCH-001');
        fd.append('target_email', email);

        fetch(window.location.href, {{ method: 'POST', body: fd }})
        .then(function(r) {{ return r.json(); }})
        .then(function(d) {{
          Swal.close();
          if (d && d.success) {{
            Swal.fire({{ icon: 'success', title: 'Signature Cleared', text: d.message || 'Signature cleared successfully.', confirmButtonColor: '#15803d' }})
            .then(function() {{ window.location.reload(); }});
          }} else {{
            if (btn && btn.tagName === 'BUTTON') {{
              btn.innerHTML = '🗑️ Clear';
              btn.disabled = false;
            }}
            Swal.fire({{ icon: 'error', title: 'Error', text: (d && d.message) ? d.message : 'Could not clear signature.', confirmButtonColor: '#be123c' }});
          }}
        }})
        .catch(function(err) {{
          Swal.close();
          if (btn && btn.tagName === 'BUTTON') {{
            btn.innerHTML = '🗑️ Clear';
            btn.disabled = false;
          }}
          Swal.fire({{ icon: 'error', title: 'Network Error', text: 'Operation failed: ' + (err.message || 'Network error'), confirmButtonColor: '#be123c' }});
        }});
      }}
    }});
  }}

  window.addEventListener('load', function() {{
    initSignaturePad();
  }});
  window.addEventListener('resize', function() {{
    initSignaturePad();
  }});
</script>

</body>
</html>
"""

# Save HTML across all root and popular directories
html_outputs = [
    os.path.join(BASE_DIR, 'Technical_Architecture_Document.html'),
    os.path.join(BASE_DIR, 'SL-POP-ERP-ARCH-001.html'),
    os.path.join(BASE_DIR, 'popular', 'Technical_Architecture_Document.html'),
    os.path.join(BASE_DIR, 'popular', 'SL-POP-ERP-ARCH-001.html'),
]

for hp in html_outputs:
    os.makedirs(os.path.dirname(hp), exist_ok=True)
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(html_content)

print('Technical_Architecture_Document.html and SL-POP-ERP-ARCH-001.html distributed successfully.')

# Render through PHP first so dynamic variables and signatures from DB are evaluated
rendered_html_path = os.path.join(BASE_DIR, 'rendered_arch_for_pdf.html')
with open(rendered_html_path, 'w', encoding='utf-8') as rf:
    subprocess.run(['php', '-f', os.path.join(BASE_DIR, 'SL-POP-ERP-ARCH-001.html')], stdout=rf, check=True, cwd=BASE_DIR)

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
pdf_output_root_1 = os.path.join(BASE_DIR, 'Technical_Architecture_Document.pdf')
pdf_output_root_2 = os.path.join(BASE_DIR, 'SL-POP-ERP-ARCH-001.pdf')

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

# Distribute PDFs to popular/ directories
for dst_dir in [
    os.path.join(BASE_DIR, 'popular')
]:
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copyfile(pdf_output_root_1, os.path.join(dst_dir, 'Technical_Architecture_Document.pdf'))
    shutil.copyfile(pdf_output_root_2, os.path.join(dst_dir, 'SL-POP-ERP-ARCH-001.pdf'))

print('Generated and distributed SL-POP-ERP-ARCH-001.pdf and Technical_Architecture_Document.pdf')

if os.path.exists(pdf_output_root_1):
    doc = fitz.open(pdf_output_root_1)
    print(f"Generated Technical Architecture PDF Page Count: {len(doc)}")
    for i in range(len(doc)):
        page = doc[i]
        print(f"Page {i+1} rect: {page.rect}, text length: {len(page.get_text())}")
        pix = page.get_pixmap(dpi=150)
        preview_p = os.path.join(BASE_DIR, f'arch_page_{i+1}_preview.png')
        pix.save(preview_p)
        print(f"Saved preview: {preview_p}")

print("Technical Architecture compilation completed.")
