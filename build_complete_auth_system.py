import base64

def get_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

logo_sands_white = get_b64('logos/SaNDSLab-LogoNewUpdatedWhite.png')
logo_sands_color = get_b64('logos/SaNDSLab-LogoNewUpdated copy.png')
logo_uniglobal_color = get_b64('logos/UNIGLOBAL_CONSULTANCY_LOGO_FINAL.png')
logo_popular = get_b64('logos/logoPopular.png')

php_code = f'''<?php
/**
 * SaNDS Lab Enterprise Document Portal - Authenticated Access & User Management
 * Location: /home/sandsl23/public_html/docs.sandslab.com/popular/index.php
 * Features:
 *   - SQLite Database (Auto-creates tables on first run)
 *   - Super Admin Panel for ajit@sandslab.com (Add, Edit, Activate/Deactivate, Delete Users)
 *   - 6-Digit OTP Email Delivery via PHP mail()
 *   - Permanent Device Authentication (5-Year Cookie)
 *   - Multi-Device Security & Device Revocation
 *   - Clean Responsive UI
 */

session_start();

// =========================================================================
// 1. SQLITE DATABASE INITIALIZATION & AUTO-TABLE SETUP
// =========================================================================
$db_file = __DIR__ . '/.auth_portal.db';
$pdo = null;

try {{
    $pdo = new PDO('sqlite:' . $db_file);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    
    // Auto-create Tables
    $pdo->exec("CREATE TABLE IF NOT EXISTS authorized_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        organization TEXT NOT NULL,
        role TEXT DEFAULT 'Client',
        is_active INTEGER DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )");
    
    $pdo->exec("CREATE TABLE IF NOT EXISTS authenticated_devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        device_token TEXT UNIQUE NOT NULL,
        user_agent TEXT,
        ip_address TEXT,
        verified_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )");

    $pdo->exec("CREATE TABLE IF NOT EXISTS otp_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        otp_code TEXT NOT NULL,
        ip_address TEXT,
        status TEXT DEFAULT 'SENT',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )");

    // Seed Initial Authorized Users if table is empty
    $check_stmt = $pdo->query("SELECT COUNT(*) as count FROM authorized_users");
    $user_count = $check_stmt->fetchColumn();

    if ($user_count == 0) {{
        $initial_users = array(
            array('ajit@sandslab.com', 'Ajit Kumar KV', 'SaNDS Lab Middle East W.L.L', 'Super Admin', 1),
            array('info@sandslab.com', 'SaNDS Lab Administration', 'SaNDS Lab Middle East W.L.L', 'Admin', 1),
            array('director@popularbahrain.com', 'Managing Director', 'Popular Auto Spare & A/C Parts Co. W.L.L', 'Client Director', 1),
            array('popularpartsbh@gmail.com', 'Executive Team', 'Popular Auto Spare & A/C Parts Co. W.L.L', 'Client', 1),
            array('cto@popularbahrain.com', 'Chief Technology Officer', 'Popular Auto Spare & A/C Parts Co. W.L.L', 'Client CTO', 1),
            array('consultant@uniglobal.com', 'Lead IT Consultant', 'UniGlobal Consultancy', 'Consultant', 1),
            array('uniglobalconsult@gmail.com', 'IT Architecture Team', 'UniGlobal Consultancy', 'Consultant', 1),
        );
        $insert_stmt = $pdo->prepare("INSERT OR IGNORE INTO authorized_users (email, full_name, organization, role, is_active) VALUES (?, ?, ?, ?, ?)");
        foreach ($initial_users as $u) {{
            $insert_stmt->execute($u);
        }}
    }}
}} catch (Exception $e) {{
    // Fallback if SQLite fails
    error_log("Database Error: " . $e->getMessage());
}}

// =========================================================================
// 2. DOCUMENT ROUTING TABLE
// =========================================================================
$routes = array(
    'SL-POP-ERP-MS-001' => array(
        'title'    => 'Module 1: PCode Generation & Item Master Milestone & Payment Structure',
        'html'     => 'SL-POP-ERP-MS-001.html',
        'pdf'      => 'SL-POP-ERP-MS-001.pdf',
        'status'   => 'Submitted & Ready for Sign-off',
        'timeline' => '10 Working Weeks (50 Days)',
        'scope'    => 'Multi Branch System',
        'ba_ref'   => 'DOC-001 (Ver 1.0)',
        'date'     => '21-Sep-2026',
        'desc'     => 'Comprehensive 10-week implementation roadmap, dedicated resource allocation matrix, 5 milestone deliverables, payment schedule (BD 3,409.091 + BD 5,000 Advance), 15-day grace period SLA, Bahrain public holidays working calendar, hardware procurement policies, and Force Majeure provisions.'
    ),
);

// =========================================================================
// 3. DEVICE AUTHENTICATION TOKEN CHECK (Permanent Access on Device)
// =========================================================================
$secret_salt = 'SaNDS_Lab_Secured_Token_Key_2026_ERP_Popular';

function get_device_fingerprint($email) {{
    global $secret_salt;
    $ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'generic_browser';
    return hash('sha256', strtolower($email) . '|' . $secret_salt . '|' . $ua);
}}

function is_device_authenticated() {{
    global $pdo;
    if (isset($_SESSION['authenticated_user']) && !empty($_SESSION['authenticated_user'])) {{
        return $_SESSION['authenticated_user'];
    }}
    
    if ($pdo && isset($_COOKIE['sands_auth_device']) && !empty($_COOKIE['sands_auth_device'])) {{
        $token = $_COOKIE['sands_auth_device'];
        $stmt = $pdo->prepare("SELECT d.email, u.is_active FROM authenticated_devices d JOIN authorized_users u ON LOWER(d.email) = LOWER(u.email) WHERE d.device_token = ?");
        $stmt->execute(array($token));
        $row = $stmt->fetch();
        if ($row && $row['is_active'] == 1) {{
            $_SESSION['authenticated_user'] = $row['email'];
            return $row['email'];
        }}
    }}
    return false;
}}

function register_authenticated_device($email) {{
    global $pdo;
    $email = strtolower(trim($email));
    $token = get_device_fingerprint($email);
    $ua    = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
    $ip    = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
    
    // Set 5-year persistent cookie
    setcookie('sands_auth_device', $token, time() + (86400 * 365 * 5), '/', '', false, true);
    
    if ($pdo) {{
        $stmt = $pdo->prepare("INSERT OR REPLACE INTO authenticated_devices (email, device_token, user_agent, ip_address, verified_at) VALUES (?, ?, ?, ?, datetime('now'))");
        $stmt->execute(array($email, $token, $ua, $ip));
    }}
    
    $_SESSION['authenticated_user'] = $email;
    unset($_SESSION['otp_code']);
    unset($_SESSION['otp_email']);
    unset($_SESSION['otp_time']);
}}

// Handle Logout
if (isset($_GET['logout'])) {{
    if ($pdo && isset($_COOKIE['sands_auth_device'])) {{
        $token = $_COOKIE['sands_auth_device'];
        $stmt = $pdo->prepare("DELETE FROM authenticated_devices WHERE device_token = ?");
        $stmt->execute(array($token));
        setcookie('sands_auth_device', '', time() - 3600, '/', '', false, true);
    }}
    session_destroy();
    header('Location: ' . strtok($_SERVER["REQUEST_URI"], '?'));
    exit;
}}

// =========================================================================
// 4. SUPER ADMIN USER MANAGEMENT HANDLERS (ajit@sandslab.com)
// =========================================================================
$authenticated_user = is_device_authenticated();
$is_super_admin = ($authenticated_user && (strtolower($authenticated_user) === 'ajit@sandslab.com' || strtolower($authenticated_user) === 'info@sandslab.com'));

$admin_msg = '';
$admin_error = '';

if ($is_super_admin && $_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['admin_action'])) {{
    $action = $_POST['admin_action'];
    
    // 1. ADD NEW USER
    if ($action === 'add_user') {{
        $new_email = strtolower(trim($_POST['new_email']));
        $new_name  = trim($_POST['new_name']);
        $new_org   = trim($_POST['new_org']);
        $new_role  = trim($_POST['new_role']);
        $is_act    = isset($_POST['is_active']) ? 1 : 0;
        
        if (empty($new_email) || !filter_var($new_email, FILTER_VALIDATE_EMAIL)) {{
            $admin_error = 'Please enter a valid email address.';
        }} elseif (empty($new_name) || empty($new_org)) {{
            $admin_error = 'Please enter both Full Name and Organization.';
        }} else {{
            try {{
                $stmt = $pdo->prepare("INSERT INTO authorized_users (email, full_name, organization, role, is_active) VALUES (?, ?, ?, ?, ?)");
                $stmt->execute(array($new_email, $new_name, $new_org, $new_role, $is_act));
                $admin_msg = 'Authorized User <strong>' . htmlspecialchars($new_email) . '</strong> added successfully!';
            }} catch (Exception $e) {{
                $admin_error = 'Error adding user (Email may already exist).';
            }}
        }}
    }}
    
    // 2. UPDATE USER
    if ($action === 'edit_user') {{
        $user_id   = intval($_POST['user_id']);
        $up_name   = trim($_POST['edit_name']);
        $up_org    = trim($_POST['edit_org']);
        $up_role   = trim($_POST['edit_role']);
        $up_email  = strtolower(trim($_POST['edit_email']));
        
        try {{
            $stmt = $pdo->prepare("UPDATE authorized_users SET full_name = ?, organization = ?, role = ?, email = ? WHERE id = ?");
            $stmt->execute(array($up_name, $up_org, $up_role, $up_email, $user_id));
            $admin_msg = 'User details updated successfully!';
        }} catch (Exception $e) {{
            $admin_error = 'Error updating user details.';
        }}
    }}
    
    // 3. TOGGLE ACTIVE / DEACTIVATE STATUS
    if ($action === 'toggle_status') {{
        $user_id   = intval($_POST['user_id']);
        $curr_stat = intval($_POST['current_status']);
        $new_stat  = ($curr_stat == 1) ? 0 : 1;
        
        try {{
            $stmt = $pdo->prepare("UPDATE authorized_users SET is_active = ? WHERE id = ?");
            $stmt->execute(array($new_stat, $user_id));
            
            // If deactivating, also revoke their active device tokens
            if ($new_stat == 0) {{
                $get_mail = $pdo->prepare("SELECT email FROM authorized_users WHERE id = ?");
                $get_mail->execute(array($user_id));
                $target_mail = $get_mail->fetchColumn();
                if ($target_mail) {{
                    $del_dev = $pdo->prepare("DELETE FROM authenticated_devices WHERE LOWER(email) = LOWER(?)");
                    $del_dev->execute(array($target_mail));
                }}
            }}
            $admin_msg = 'User status changed successfully!';
        }} catch (Exception $e) {{
            $admin_error = 'Error changing user status.';
        }}
    }}
    
    // 4. REVOKE DEVICE TOKENS (FORCE RE-AUTHENTICATION)
    if ($action === 'revoke_devices') {{
        $target_email = strtolower(trim($_POST['user_email']));
        try {{
            $stmt = $pdo->prepare("DELETE FROM authenticated_devices WHERE LOWER(email) = LOWER(?)");
            $stmt->execute(array($target_email));
            $admin_msg = 'All remembered devices for <strong>' . htmlspecialchars($target_email) . '</strong> have been revoked.';
        }} catch (Exception $e) {{
            $admin_error = 'Error revoking devices.';
        }}
    }}
    
    // 5. DELETE USER
    if ($action === 'delete_user') {{
        $user_id = intval($_POST['user_id']);
        try {{
            $get_mail = $pdo->prepare("SELECT email FROM authorized_users WHERE id = ?");
            $get_mail->execute(array($user_id));
            $target_mail = $get_mail->fetchColumn();
            
            if ($target_mail && strtolower($target_mail) === 'ajit@sandslab.com') {{
                $admin_error = 'Action Prohibited: Super Admin ajit@sandslab.com cannot be deleted.';
            }} else {{
                $stmt = $pdo->prepare("DELETE FROM authorized_users WHERE id = ?");
                $stmt->execute(array($user_id));
                if ($target_mail) {{
                    $del_dev = $pdo->prepare("DELETE FROM authenticated_devices WHERE LOWER(email) = LOWER(?)");
                    $del_dev->execute(array($target_mail));
                }}
                $admin_msg = 'User deleted from authorized registry.';
            }}
        }} catch (Exception $e) {{
            $admin_error = 'Error deleting user.';
        }}
    }}
}}

// =========================================================================
// 5. AJAX / POST AUTHENTICATION HANDLERS (Send OTP & Verify OTP)
// =========================================================================
$auth_error = '';
$auth_success = '';
$current_step = 'EMAIL_INPUT';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'send_otp') {{
    $input_email = strtolower(trim($_POST['email']));
    
    if (empty($input_email) || !filter_var($input_email, FILTER_VALIDATE_EMAIL)) {{
        $auth_error = 'Please enter a valid email address.';
    }} else {{
        // Check in SQLite database table
        $user_row = null;
        if ($pdo) {{
            $stmt = $pdo->prepare("SELECT * FROM authorized_users WHERE LOWER(email) = ?");
            $stmt->execute(array($input_email));
            $user_row = $stmt->fetch();
        }}
        
        if (!$user_row) {{
            $auth_error = 'Access Denied: <strong>' . htmlspecialchars($input_email) . '</strong> is not authorized to access this portal.';
        }} elseif ($user_row['is_active'] != 1) {{
            $auth_error = 'Access Suspended: Your access has been deactivated by the Administrator (SaNDS Lab).';
        }} else {{
            // Generate 6-digit OTP
            $otp = sprintf("%06d", mt_rand(100000, 999999));
            $_SESSION['otp_code']  = $otp;
            $_SESSION['otp_email'] = $input_email;
            $_SESSION['otp_time']  = time();
            
            // Log OTP in SQLite
            if ($pdo) {{
                $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
                $log_stmt = $pdo->prepare("INSERT INTO otp_logs (email, otp_code, ip_address) VALUES (?, ?, ?)");
                $log_stmt->execute(array($input_email, $otp, $ip));
            }}
            
            // Send HTML Email
            $user_name = $user_row['full_name'];
            $subject = "Your Verification Code: $otp - SaNDS Lab Document Portal";
            
            $headers  = "MIME-Version: 1.0\\r\\n";
            $headers .= "Content-type: text/html; charset=UTF-8\\r\\n";
            $headers .= "From: SaNDS Lab Security <no-reply@sandslab.com>\\r\\n";
            $headers .= "Reply-To: support@sandslab.com\\r\\n";
            $headers .= "X-Mailer: PHP/" . phpversion();
            
            $email_body = "<!DOCTYPE html>
            <html>
            <head><meta charset='UTF-8'><title>Verification Code</title></head>
            <body style='font-family: Arial, sans-serif; background-color: #f4f7fa; margin: 0; padding: 30px;'>
              <table align='center' border='0' cellpadding='0' cellspacing='0' width='550' style='background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border-top: 5px solid #e67e22;'>
                <tr>
                  <td style='background-color: #07192c; padding: 25px 30px; text-align: center;'>
                    <h2 style='color: #ffffff; margin: 0; font-size: 20px; letter-spacing: 0.5px;'>SaNDS Lab • Enterprise Document Portal</h2>
                    <div style='color: #e67e22; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-top: 5px;'>Popular Auto Spare ERP Transformation</div>
                  </td>
                </tr>
                <tr>
                  <td style='padding: 35px 35px 25px;'>
                    <p style='font-size: 15px; color: #334155; margin-top: 0;'>Hello <strong>$user_name</strong>,</p>
                    <p style='font-size: 14px; color: #475569; line-height: 1.6;'>You requested access to the <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong> ERP Proposal & Architecture Document Repository. Use the 6-digit verification code below to authorize this device:</p>
                    
                    <div style='background-color: #f8fafc; border: 2px dashed #0a2540; border-radius: 8px; padding: 18px; text-align: center; margin: 25px 0;'>
                      <span style='font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #0a2540; font-family: monospace;'>$otp</span>
                    </div>
                    
                    <p style='font-size: 12.5px; color: #64748b; line-height: 1.5;'>This verification code is valid for <strong>15 minutes</strong>. Once verified, this device will remain permanently authenticated.</p>
                    <p style='font-size: 12.5px; color: #e11d48;'>If you did not request this verification code, please ignore this email.</p>
                  </td>
                </tr>
                <tr>
                  <td style='background-color: #f8fafc; padding: 18px 35px; border-top: 1px solid #e2e8f0; text-align: center; font-size: 11px; color: #94a3b8;'>
                    SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain • Hotline: +973 35 078 079
                  </td>
                </tr>
              </table>
            </body>
            </html>";
            
            @mail($input_email, $subject, $email_body, $headers);
            
            $current_step = 'OTP_INPUT';
            $auth_success = 'A 6-digit verification code has been dispatched to <strong>' . htmlspecialchars($input_email) . '</strong>.';
        }}
    }}
}}

// Verify OTP
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'verify_otp') {{
    $submitted_otp = trim($_POST['otp']);
    
    if (isset($_POST['otp_digits']) && is_array($_POST['otp_digits'])) {{
        $submitted_otp = implode('', $_POST['otp_digits']);
    }}
    
    $saved_otp   = isset($_SESSION['otp_code']) ? $_SESSION['otp_code'] : '';
    $saved_email = isset($_SESSION['otp_email']) ? $_SESSION['otp_email'] : '';
    $saved_time  = isset($_SESSION['otp_time']) ? $_SESSION['otp_time'] : 0;
    
    if (empty($saved_otp) || empty($saved_email)) {{
        $auth_error = 'Session expired. Please request a new verification code.';
        $current_step = 'EMAIL_INPUT';
    }} elseif ((time() - $saved_time) > 900) {{
        $auth_error = 'Verification code has expired. Please request a new one.';
        $current_step = 'EMAIL_INPUT';
    }} elseif ($submitted_otp !== $saved_otp) {{
        $auth_error = 'Invalid 6-digit verification code. Please check your email and try again.';
        $current_step = 'OTP_INPUT';
    }} else {{
        register_authenticated_device($saved_email);
        $target_url = strtok($_SERVER["REQUEST_URI"], '?');
        if (isset($_GET['doc']) && !empty($_GET['doc'])) {{
            $target_url .= '?doc=' . urlencode($_GET['doc']);
        }}
        header('Location: ' . $target_url);
        exit;
    }}
}}

if (isset($_SESSION['otp_code']) && !empty($_SESSION['otp_code']) && empty($auth_error) && $current_step === 'EMAIL_INPUT' && isset($_GET['step']) && $_GET['step'] === 'otp') {{
    $current_step = 'OTP_INPUT';
}}

// =========================================================================
// 6. IF NOT AUTHENTICATED -> RENDER AUTHENTICATION VIEW (Email / OTP)
// =========================================================================
if (!$authenticated_user) {{
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <title>Security Verification - SaNDS Lab Client Document Portal</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #0a2540;
      --accent: #e67e22;
      --accent-dark: #d35400;
      --secondary: #0e7490;
      --dark: #0f172a;
      --gray-800: #1e293b;
      --gray-700: #334155;
      --gray-600: #475569;
      --gray-500: #64748b;
      --gray-300: #cbd5e1;
      --gray-200: #e2e8f0;
      --gray-50: #f8fafc;
      --white: #ffffff;
      --danger: #e11d48;
      --danger-bg: #ffe4e6;
      --success: #10b981;
      --success-bg: #ecfdf5;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: radial-gradient(circle at top center, #153e67 0%, #0a2540 40%, #061524 100%);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 20px 16px;
      color: var(--white);
    }}
    .auth-card {{
      background: rgba(255, 255, 255, 0.98);
      color: var(--gray-800);
      width: 100%;
      max-width: 440px;
      border-radius: 16px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
      overflow: hidden;
    }}
    .auth-header {{
      background: linear-gradient(135deg, #07192c 0%, #0a2540 100%);
      padding: 35px 30px 28px;
      text-align: center;
      border-bottom: 3px solid var(--accent);
    }}
    .auth-logo-img {{
      max-height: 54px; /* Big SaNDS Logo */
      width: auto;
      margin-bottom: 12px;
      filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));
    }}
    .auth-portal-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: var(--white);
    }}
    .auth-portal-sub {{
      font-size: 11.5px;
      color: #94a3b8;
      margin-top: 4px;
    }}
    .auth-body {{
      padding: 32px 30px 30px;
    }}
    .auth-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 20px;
      font-weight: 800;
      color: var(--primary);
      margin-bottom: 6px;
      text-align: center;
    }}
    .auth-desc {{
      font-size: 13px;
      color: var(--gray-600);
      text-align: center;
      line-height: 1.5;
      margin-bottom: 24px;
    }}
    .alert {{
      padding: 12px 14px;
      border-radius: 8px;
      font-size: 12.5px;
      line-height: 1.45;
      margin-bottom: 20px;
    }}
    .alert-danger {{
      background: var(--danger-bg);
      color: #9f1239;
      border: 1px solid #fecdd3;
    }}
    .alert-success {{
      background: var(--success-bg);
      color: #065f46;
      border: 1px solid #a7f3d0;
    }}
    .form-group {{
      margin-bottom: 20px;
    }}
    .form-label {{
      display: block;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--gray-700);
      margin-bottom: 8px;
    }}
    .input-wrapper {{
      position: relative;
      display: flex;
      align-items: center;
    }}
    .input-icon {{
      position: absolute;
      left: 14px;
      color: var(--gray-400);
    }}
    .form-control {{
      width: 100%;
      height: 48px;
      padding: 10px 14px 10px 42px;
      font-size: 14px;
      font-family: 'Inter', sans-serif;
      color: var(--gray-800);
      background: var(--gray-50);
      border: 1.5px solid var(--gray-300);
      border-radius: 8px;
      outline: none;
    }}
    .form-control:focus {{
      background: var(--white);
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.18);
    }}
    .otp-inputs-grid {{
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 8px;
      margin-bottom: 22px;
    }}
    .otp-digit-box {{
      width: 100%;
      height: 52px;
      font-size: 22px;
      font-weight: 800;
      font-family: 'Outfit', monospace;
      text-align: center;
      color: var(--primary);
      background: var(--gray-50);
      border: 2px solid var(--gray-300);
      border-radius: 8px;
      outline: none;
    }}
    .otp-digit-box:focus {{
      background: var(--white);
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.25);
    }}
    .btn-submit {{
      width: 100%;
      height: 48px;
      background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
      color: var(--white);
      border: none;
      border-radius: 8px;
      font-family: 'Outfit', sans-serif;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(230, 126, 34, 0.4);
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
    }}
    .btn-submit:hover {{
      transform: translateY(-1px);
    }}
    .auth-footer-links {{
      margin-top: 20px;
      text-align: center;
      font-size: 12.5px;
      color: var(--gray-500);
    }}
    .auth-link {{
      color: var(--accent-dark);
      text-decoration: none;
      font-weight: 600;
      cursor: pointer;
    }}
    .security-badge {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      font-size: 11px;
      color: var(--gray-500);
      margin-top: 25px;
      padding-top: 15px;
      border-top: 1px solid var(--gray-200);
    }}
    .copyright {{
      margin-top: 25px;
      font-size: 11.5px;
      color: rgba(255, 255, 255, 0.6);
    }}
  </style>
</head>
<body>

  <div class="auth-card">
    <div class="auth-header">
      <img class="auth-logo-img" src="{logo_sands_white}" alt="SaNDS Lab" />
      <div class="auth-portal-title">Client Document Portal</div>
      <div class="auth-portal-sub">Popular Auto Spare & A/C Parts Co. W.L.L ERP Repository</div>
    </div>

    <div class="auth-body">
      <?php if (!empty($auth_error)): ?>
        <div class="alert alert-danger"><?php echo $auth_error; ?></div>
      <?php endif; ?>

      <?php if (!empty($auth_success)): ?>
        <div class="alert alert-success"><?php echo $auth_success; ?></div>
      <?php endif; ?>

      <?php if ($current_step === 'EMAIL_INPUT'): ?>
        <h2 class="auth-title">Authorized Sign-In</h2>
        <p class="auth-desc">Enter your registered organizational email address to receive your 6-digit verification code.</p>

        <form method="POST" action="">
          <input type="hidden" name="action" value="send_otp">
          <div class="form-group">
            <label class="form-label" for="email">Corporate Email Address</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              <input type="email" name="email" id="email" class="form-control" placeholder="name@company.com" required autofocus value="<?php echo isset($_POST['email']) ? htmlspecialchars($_POST['email']) : ''; ?>">
            </div>
          </div>
          <button type="submit" class="btn-submit">
            Send 6-Digit Code
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
          </button>
        </form>

      <?php else: ?>
        <h2 class="auth-title">Verify Your Identity</h2>
        <p class="auth-desc">We sent a 6-digit code to <strong><?php echo htmlspecialchars($_SESSION['otp_email']); ?></strong>. Enter it below to unlock this device forever.</p>

        <form method="POST" action="" id="otpForm">
          <input type="hidden" name="action" value="verify_otp">
          <input type="hidden" name="otp" id="combinedOtp" value="">
          <div class="form-group">
            <label class="form-label" style="text-align:center;">Enter 6-Digit Code</label>
            <div class="otp-inputs-grid">
              <input type="text" maxlength="1" class="otp-digit-box" inputmode="numeric" pattern="[0-9]*" autofocus required>
              <input type="text" maxlength="1" class="otp-digit-box" inputmode="numeric" pattern="[0-9]*" required>
              <input type="text" maxlength="1" class="otp-digit-box" inputmode="numeric" pattern="[0-9]*" required>
              <input type="text" maxlength="1" class="otp-digit-box" inputmode="numeric" pattern="[0-9]*" required>
              <input type="text" maxlength="1" class="otp-digit-box" inputmode="numeric" pattern="[0-9]*" required>
              <input type="text" maxlength="1" class="otp-digit-box" inputmode="numeric" pattern="[0-9]*" required>
            </div>
          </div>
          <button type="submit" class="btn-submit">
            Verify & Unlock Device
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
          </button>
        </form>

        <div class="auth-footer-links">
          Didn't receive code? 
          <form method="POST" action="" style="display:inline;">
            <input type="hidden" name="action" value="send_otp">
            <input type="hidden" name="email" value="<?php echo htmlspecialchars($_SESSION['otp_email']); ?>">
            <button type="submit" class="auth-link" style="background:none;border:none;padding:0;font-size:inherit;">Resend Code</button>
          </form>
          • <a href="<?php echo strtok($_SERVER["REQUEST_URI"], '?'); ?>?step=reset" class="auth-link">Use Different Email</a>
        </div>

        <script>
          const otpBoxes = document.querySelectorAll('.otp-digit-box');
          const combinedOtp = document.getElementById('combinedOtp');
          const otpForm = document.getElementById('otpForm');

          otpBoxes.forEach((box, index) => {{
            box.addEventListener('input', (e) => {{
              if (e.target.value.length === 1 && index < otpBoxes.length - 1) {{
                otpBoxes[index + 1].focus();
              }}
              updateCombined();
            }});
            box.addEventListener('keydown', (e) => {{
              if (e.key === 'Backspace' && !box.value && index > 0) {{
                otpBoxes[index - 1].focus();
              }}
            }});
            box.addEventListener('paste', (e) => {{
              e.preventDefault();
              const pasted = (e.clipboardData || window.clipboardData).getData('text').trim();
              if (/^\\d{{6}}$/.test(pasted)) {{
                pasted.split('').forEach((char, i) => {{
                  if (otpBoxes[i]) otpBoxes[i].value = char;
                }});
                updateCombined();
                otpForm.submit();
              }}
            }});
          }});

          function updateCombined() {{
            let code = '';
            otpBoxes.forEach(b => code += b.value);
            combinedOtp.value = code;
          }}

          otpForm.addEventListener('submit', (e) => {{
            updateCombined();
            if (combinedOtp.value.length !== 6) {{
              e.preventDefault();
              alert('Please enter all 6 digits.');
            }}
          }});
        </script>
      <?php endif; ?>

      <div class="security-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
        256-Bit Encrypted Device Verification Engine
      </div>
    </div>
  </div>

  <div class="copyright">&copy; 2026 SaNDS Lab Middle East W.L.L</div>
</body>
</html>
<?php
    exit;
}}

// =========================================================================
// 7. SUPER ADMIN USER MANAGEMENT DASHBOARD (ajit@sandslab.com only)
// =========================================================================
if ($is_super_admin && isset($_GET['view']) && $_GET['view'] === 'admin') {{
    $all_users = array();
    $all_devices = array();
    $all_logs = array();
    if ($pdo) {{
        $all_users = $pdo->query("SELECT * FROM authorized_users ORDER BY id ASC")->fetchAll();
        $all_devices = $pdo->query("SELECT d.*, u.full_name FROM authenticated_devices d LEFT JOIN authorized_users u ON LOWER(d.email)=LOWER(u.email) ORDER BY d.verified_at DESC")->fetchAll();
        $all_logs = $pdo->query("SELECT * FROM otp_logs ORDER BY created_at DESC LIMIT 15")->fetchAll();
    }}
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin User Management - SaNDS Lab</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #0a2540;
      --accent: #e67e22;
      --accent-dark: #d35400;
      --secondary: #0e7490;
      --dark: #0f172a;
      --gray-800: #1e293b;
      --gray-700: #334155;
      --gray-600: #475569;
      --gray-500: #64748b;
      --gray-300: #cbd5e1;
      --gray-200: #e2e8f0;
      --gray-100: #f1f5f9;
      --gray-50: #f8fafc;
      --white: #ffffff;
      --success: #15803d;
      --success-bg: #dcfce7;
      --danger: #b91c1c;
      --danger-bg: #fee2e2;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: #f1f5f9;
      color: var(--gray-700);
      line-height: 1.5;
    }}
    .admin-nav {{
      background: #07192c;
      border-bottom: 2px solid var(--accent);
      padding: 14px 35px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .nav-brand {{
      display: flex;
      align-items: center;
      gap: 15px;
    }}
    .nav-logo {{
      height: 32px;
      width: auto;
    }}
    .nav-title {{
      color: #ffffff;
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 15px;
    }}
    .nav-sub {{
      color: #94a3b8;
      font-size: 11px;
    }}
    .admin-container {{
      max-width: 1140px;
      margin: 30px auto;
      padding: 0 20px;
    }}
    .admin-header-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .admin-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      font-weight: 800;
      color: var(--primary);
    }}
    .admin-actions-bar {{
      display: flex;
      gap: 10px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12.5px;
      font-weight: 600;
      padding: 8px 15px;
      border-radius: 6px;
      text-decoration: none;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-primary {{
      background: var(--accent);
      color: #ffffff;
    }}
    .btn-primary:hover {{
      background: var(--accent-dark);
    }}
    .btn-outline {{
      background: #ffffff;
      border: 1px solid var(--gray-300);
      color: var(--gray-700);
    }}
    .btn-outline:hover {{
      background: var(--gray-100);
    }}
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 15px;
      margin-bottom: 25px;
    }}
    .stat-card {{
      background: #ffffff;
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      padding: 16px 20px;
    }}
    .stat-num {{
      font-family: 'Outfit', sans-serif;
      font-size: 24px;
      font-weight: 800;
      color: var(--primary);
    }}
    .stat-label {{
      font-size: 11.5px;
      color: var(--gray-500);
      text-transform: uppercase;
      font-weight: 600;
      margin-top: 2px;
    }}
    .admin-card {{
      background: #ffffff;
      border: 1px solid var(--gray-200);
      border-radius: 10px;
      padding: 24px;
      margin-bottom: 25px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }}
    .card-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--gray-200);
    }}
    .card-head h3 {{
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: var(--primary);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
    }}
    th {{
      background: var(--gray-50);
      color: var(--gray-700);
      font-weight: 700;
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid var(--gray-200);
    }}
    td {{
      padding: 12px;
      border-bottom: 1px solid var(--gray-200);
      vertical-align: middle;
    }}
    .badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .badge-success {{ background: var(--success-bg); color: var(--success); }}
    .badge-danger {{ background: var(--danger-bg); color: var(--danger); }}
    .badge-primary {{ background: #e0f2fe; color: #0369a1; }}
    
    .action-btn-group {{
      display: flex;
      gap: 6px;
    }}
    .btn-sm {{
      padding: 4px 8px;
      font-size: 11px;
      border-radius: 4px;
    }}
    .btn-toggle-on {{ background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }}
    .btn-toggle-off {{ background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }}
    .btn-del {{ background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; }}

    /* Modal Form Styling */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(4px);
      z-index: 10000;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }}
    .modal-box {{
      background: #ffffff;
      border-radius: 12px;
      max-width: 500px;
      width: 100%;
      padding: 28px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }}
    .modal-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--gray-200);
    }}
    .modal-head h3 {{
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      color: var(--primary);
    }}
    .form-row {{
      margin-bottom: 14px;
    }}
    .form-row label {{
      display: block;
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--gray-700);
      margin-bottom: 5px;
    }}
    .form-row input, .form-row select {{
      width: 100%;
      height: 40px;
      padding: 8px 12px;
      font-size: 13px;
      border: 1px solid var(--gray-300);
      border-radius: 6px;
      outline: none;
    }}

    @media (max-width: 768px) {{
      .stats-grid {{ grid-template-columns: 1fr 1fr; }}
      table {{ display: block; overflow-x: auto; }}
    }}
  </style>
</head>
<body>

  <!-- ADMIN TOP NAVIGATION -->
  <nav class="admin-nav">
    <div class="nav-brand">
      <img class="nav-logo" src="{logo_sands_white}" alt="SaNDS Lab" />
      <div>
        <div class="nav-title">SaNDS Lab • Super Admin Control Center</div>
        <div class="nav-sub">Logged in as: <strong>ajit@sandslab.com</strong></div>
      </div>
    </div>
    <div style="display:flex; gap:10px;">
      <a href="?" class="btn btn-outline" style="background:#ffffff; color:#0a2540;">&larr; Return to Document Portal</a>
      <a href="?logout=1" class="btn btn-outline" style="background:rgba(225,29,72,0.15); color:#ffffff; border-color:#e11d48;">Sign Out</a>
    </div>
  </nav>

  <div class="admin-container">

    <?php if (!empty($admin_msg)): ?>
      <div style="background:#ecfdf5; color:#065f46; border:1px solid #a7f3d0; padding:12px 16px; border-radius:8px; margin-bottom:20px; font-size:13px;">
        <?php echo $admin_msg; ?>
      </div>
    <?php endif; ?>

    <?php if (!empty($admin_error)): ?>
      <div style="background:#ffe4e6; color:#9f1239; border:1px solid #fecdd3; padding:12px 16px; border-radius:8px; margin-bottom:20px; font-size:13px;">
        <?php echo $admin_error; ?>
      </div>
    <?php endif; ?>

    <div class="admin-header-row">
      <div>
        <h1 class="admin-title">Authorized User Registry</h1>
        <p style="font-size:13px; color:var(--gray-500);">Manage authorized email access, OTP verification, and authenticated devices for Popular Auto Spare ERP documents.</p>
      </div>
      <div class="admin-actions-bar">
        <button onclick="openAddModal()" class="btn btn-primary">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          Add New User
        </button>
      </div>
    </div>

    <!-- STATS -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-num"><?php echo count($all_users); ?></div>
        <div class="stat-label">Total Users</div>
      </div>
      <div class="stat-card">
        <div class="stat-num" style="color:#15803d;">
          <?php echo count(array_filter($all_users, function($u) {{ return $u['is_active'] == 1; }})); ?>
        </div>
        <div class="stat-label">Active Users</div>
      </div>
      <div class="stat-card">
        <div class="stat-num" style="color:#b91c1c;">
          <?php echo count(array_filter($all_users, function($u) {{ return $u['is_active'] == 0; }})); ?>
        </div>
        <div class="stat-label">Deactivated</div>
      </div>
      <div class="stat-card">
        <div class="stat-num" style="color:#0369a1;"><?php echo count($all_devices); ?></div>
        <div class="stat-label">Devices Remembered</div>
      </div>
    </div>

    <!-- USERS TABLE -->
    <div class="admin-card">
      <div class="card-head">
        <h3>Authorized Email Access List (SQLite Table)</h3>
        <span style="font-size:12px; color:var(--gray-500);">Database: <code>.auth_portal.db</code></span>
      </div>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name & Organization</th>
            <th>Authorized Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Created</th>
            <th style="text-align:right;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <?php foreach ($all_users as $user): ?>
          <tr>
            <td><strong>#<?php echo $user['id']; ?></strong></td>
            <td>
              <strong><?php echo htmlspecialchars($user['full_name']); ?></strong><br>
              <span style="font-size:11.5px; color:var(--gray-500);"><?php echo htmlspecialchars($user['organization']); ?></span>
            </td>
            <td><code><?php echo htmlspecialchars($user['email']); ?></code></td>
            <td><span class="badge badge-primary"><?php echo htmlspecialchars($user['role']); ?></span></td>
            <td>
              <?php if ($user['is_active'] == 1): ?>
                <span class="badge badge-success">Active</span>
              <?php else: ?>
                <span class="badge badge-danger">Deactivated</span>
              <?php endif; ?>
            </td>
            <td style="font-size:11px; color:var(--gray-500);"><?php echo substr($user['created_at'], 0, 10); ?></td>
            <td style="text-align:right;">
              <div class="action-btn-group" style="justify-content:flex-end;">
                
                <!-- Toggle Active / Deactivate -->
                <form method="POST" action="" style="display:inline;">
                  <input type="hidden" name="admin_action" value="toggle_status">
                  <input type="hidden" name="user_id" value="<?php echo $user['id']; ?>">
                  <input type="hidden" name="current_status" value="<?php echo $user['is_active']; ?>">
                  <?php if ($user['is_active'] == 1): ?>
                    <button type="submit" class="btn btn-sm btn-toggle-on" title="Deactivate user">Deactivate</button>
                  <?php else: ?>
                    <button type="submit" class="btn btn-sm btn-toggle-off" title="Activate user">Activate</button>
                  <?php endif; ?>
                </form>

                <!-- Edit User -->
                <button onclick="openEditModal(<?php echo htmlspecialchars(json_encode($user)); ?>)" class="btn btn-sm btn-outline">Edit</button>

                <!-- Revoke Devices -->
                <form method="POST" action="" style="display:inline;" onsubmit="return confirm('Revoke all remembered devices for <?php echo htmlspecialchars($user['email']); ?>? They will be asked for OTP again.');">
                  <input type="hidden" name="admin_action" value="revoke_devices">
                  <input type="hidden" name="user_email" value="<?php echo htmlspecialchars($user['email']); ?>">
                  <button type="submit" class="btn btn-sm btn-outline" title="Revoke devices">Revoke Device</button>
                </form>

                <?php if (strtolower($user['email']) !== 'ajit@sandslab.com'): ?>
                <!-- Delete User -->
                <form method="POST" action="" style="display:inline;" onsubmit="return confirm('Delete user <?php echo htmlspecialchars($user['email']); ?>?');">
                  <input type="hidden" name="admin_action" value="delete_user">
                  <input type="hidden" name="user_id" value="<?php echo $user['id']; ?>">
                  <button type="submit" class="btn btn-sm btn-del">Delete</button>
                </form>
                <?php endif; ?>

              </div>
            </td>
          </tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>

    <!-- RECENT DEVICE ACTIVITY -->
    <div class="admin-card">
      <div class="card-head">
        <h3>Authenticated Devices (Active Forever on Device)</h3>
      </div>
      <table>
        <thead>
          <tr>
            <th>User</th>
            <th>Email</th>
            <th>IP Address</th>
            <th>Browser / Device Details</th>
            <th>Verified Date</th>
          </tr>
        </thead>
        <tbody>
          <?php if (empty($all_devices)): ?>
            <tr><td colspan="5" style="text-align:center; color:var(--gray-500); padding:20px;">No authenticated devices registered yet.</td></tr>
          <?php else: ?>
            <?php foreach ($all_devices as $dev): ?>
            <tr>
              <td><strong><?php echo htmlspecialchars($dev['full_name'] ? $dev['full_name'] : 'User'); ?></strong></td>
              <td><code><?php echo htmlspecialchars($dev['email']); ?></code></td>
              <td><?php echo htmlspecialchars($dev['ip_address'] ? $dev['ip_address'] : 'N/A'); ?></td>
              <td style="font-size:11px; color:var(--gray-600); max-width:300px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                <?php echo htmlspecialchars($dev['user_agent']); ?>
              </td>
              <td style="font-size:11.5px; color:var(--gray-500);"><?php echo $dev['verified_at']; ?></td>
            </tr>
            <?php endforeach; ?>
          <?php endif; ?>
        </tbody>
      </table>
    </div>

  </div>

  <!-- ADD USER MODAL -->
  <div class="modal-overlay" id="addModal">
    <div class="modal-box">
      <div class="modal-head">
        <h3>Add New Authorized User</h3>
        <button onclick="closeAddModal()" style="background:none; border:none; font-size:18px; cursor:pointer;">&times;</button>
      </div>
      <form method="POST" action="">
        <input type="hidden" name="admin_action" value="add_user">
        <div class="form-row">
          <label>Email Address</label>
          <input type="email" name="new_email" required placeholder="user@domain.com">
        </div>
        <div class="form-row">
          <label>Full Name</label>
          <input type="text" name="new_name" required placeholder="e.g. John Doe">
        </div>
        <div class="form-row">
          <label>Organization / Company</label>
          <input type="text" name="new_org" required placeholder="e.g. Popular Auto Spare / UniGlobal">
        </div>
        <div class="form-row">
          <label>Role</label>
          <select name="new_role">
            <option value="Client">Client</option>
            <option value="Client Director">Client Director</option>
            <option value="Client CTO">Client CTO</option>
            <option value="Consultant">Consultant</option>
            <option value="Admin">Admin</option>
          </select>
        </div>
        <div class="form-row" style="display:flex; align-items:center; gap:8px;">
          <input type="checkbox" name="is_active" id="addActive" checked style="width:auto; height:auto;">
          <label for="addActive" style="margin-bottom:0; cursor:pointer;">Active (Allowed to sign in)</label>
        </div>
        <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:20px;">
          <button type="button" onclick="closeAddModal()" class="btn btn-outline">Cancel</button>
          <button type="submit" class="btn btn-primary">Save & Authorize User</button>
        </div>
      </form>
    </div>
  </div>

  <!-- EDIT USER MODAL -->
  <div class="modal-overlay" id="editModal">
    <div class="modal-box">
      <div class="modal-head">
        <h3>Edit User Details</h3>
        <button onclick="closeEditModal()" style="background:none; border:none; font-size:18px; cursor:pointer;">&times;</button>
      </div>
      <form method="POST" action="">
        <input type="hidden" name="admin_action" value="edit_user">
        <input type="hidden" name="user_id" id="editUserId">
        <div class="form-row">
          <label>Email Address</label>
          <input type="email" name="edit_email" id="editEmail" required>
        </div>
        <div class="form-row">
          <label>Full Name</label>
          <input type="text" name="edit_name" id="editName" required>
        </div>
        <div class="form-row">
          <label>Organization / Company</label>
          <input type="text" name="edit_org" id="editOrg" required>
        </div>
        <div class="form-row">
          <label>Role</label>
          <select name="edit_role" id="editRole">
            <option value="Client">Client</option>
            <option value="Client Director">Client Director</option>
            <option value="Client CTO">Client CTO</option>
            <option value="Consultant">Consultant</option>
            <option value="Admin">Admin</option>
            <option value="Super Admin">Super Admin</option>
          </select>
        </div>
        <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:20px;">
          <button type="button" onclick="closeEditModal()" class="btn btn-outline">Cancel</button>
          <button type="submit" class="btn btn-primary">Update User</button>
        </div>
      </form>
    </div>
  </div>

  <script>
    function openAddModal() {{
      document.getElementById('addModal').style.display = 'flex';
    }}
    function closeAddModal() {{
      document.getElementById('addModal').style.display = 'none';
    }}
    function openEditModal(user) {{
      document.getElementById('editUserId').value = user.id;
      document.getElementById('editEmail').value = user.email;
      document.getElementById('editName').value = user.full_name;
      document.getElementById('editOrg').value = user.organization;
      document.getElementById('editRole').value = user.role;
      document.getElementById('editModal').style.display = 'flex';
    }}
    function closeEditModal() {{
      document.getElementById('editModal').style.display = 'none';
    }}
  </script>

</body>
</html>
<?php
    exit;
}}

// =========================================================================
// 8. AUTHENTICATED USER: SERVE REQUESTED DOCUMENT OR DOCUMENT HUB
// =========================================================================

// Extract query parameter or URL path
$doc = '';
if (isset($_GET['doc']) && !empty($_GET['doc'])) {{
    $doc = trim($_GET['doc']);
}} else {{
    $request_uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    $path_parts  = array_values(array_filter(explode('/', trim($request_uri, '/'))));
    foreach ($path_parts as $part) {{
        $upper = strtoupper($part);
        if ($upper !== 'POPULAR' && $upper !== 'INDEX.PHP') {{
            $doc = $part;
            break;
        }}
    }}
}}

$clean_id = preg_replace('/\.(HTML|PDF)$/i', '', strtoupper(trim($doc)));

// Direct PDF Download / Stream
if (!empty($doc) && substr(strtolower($doc), -4) === '.pdf') {{
    if (isset($routes[$clean_id])) {{
        $pdf_file = __DIR__ . '/' . $routes[$clean_id]['pdf'];
        if (file_exists($pdf_file)) {{
            header('Content-Type: application/pdf');
            header('Content-Disposition: inline; filename="' . basename($pdf_file) . '"');
            header('Content-Length: ' . filesize($pdf_file));
            readfile($pdf_file);
            exit;
        }}
    }}
}}

// Include Requested Document
if (!empty($clean_id) && isset($routes[$clean_id])) {{
    $html_file = __DIR__ . '/' . $routes[$clean_id]['html'];
    if (file_exists($html_file)) {{
        include $html_file;
        exit;
    }}
}}

// Otherwise Render Document Portal Hub
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Client Document Portal - Popular Auto Spare & A/C Parts Co. W.L.L | SaNDS Lab</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #0a2540;
      --accent: #e67e22;
      --accent-dark: #d35400;
      --secondary: #0e7490;
      --dark: #0f172a;
      --gray-800: #1e293b;
      --gray-700: #334155;
      --gray-600: #475569;
      --gray-500: #64748b;
      --gray-200: #e2e8f0;
      --gray-100: #f1f5f9;
      --gray-50: #f8fafc;
      --white: #ffffff;
      --success: #15803d;
      --success-bg: #dcfce7;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: #f8fafc;
      color: var(--gray-700);
      line-height: 1.5;
    }}
    .portal-nav {{
      background: #07192c;
      border-bottom: 2px solid var(--accent);
      padding: 14px 35px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .nav-brand {{
      display: flex;
      align-items: center;
      gap: 15px;
    }}
    .nav-logo {{
      height: 32px;
      width: auto;
    }}
    .nav-title-block {{
      display: flex;
      flex-direction: column;
    }}
    .nav-title {{
      color: #ffffff;
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 15px;
      letter-spacing: 0.3px;
    }}
    .nav-sub {{
      color: #94a3b8;
      font-size: 11px;
    }}
    .nav-right {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .btn-admin-manage {{
      background: #e67e22;
      color: #ffffff;
      font-size: 11.5px;
      font-weight: 700;
      padding: 5px 12px;
      border-radius: 4px;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 5px;
      box-shadow: 0 2px 8px rgba(230,126,34,0.35);
      transition: all 0.2s;
    }}
    .btn-admin-manage:hover {{
      background: #d35400;
    }}
    .user-auth-badge {{
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid #10b981;
      color: #a7f3d0;
      font-size: 11.5px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .btn-logout {{
      background: rgba(255, 255, 255, 0.1);
      color: #cbd5e1;
      border: 1px solid rgba(255, 255, 255, 0.2);
      font-size: 11.5px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 4px;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .btn-logout:hover {{
      background: rgba(225, 29, 72, 0.2);
      color: #fecdd3;
      border-color: #e11d48;
    }}
    .portal-container {{
      max-width: 1100px;
      margin: 35px auto;
      padding: 0 25px;
    }}
    .client-hero {{
      background: linear-gradient(135deg, #0a2540 0%, #153e67 100%);
      color: #ffffff;
      border-radius: 12px;
      padding: 30px 35px;
      margin-bottom: 30px;
      box-shadow: 0 10px 25px rgba(10, 37, 64, 0.12);
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
      overflow: hidden;
    }}
    .client-hero::after {{
      content: '';
      position: absolute;
      top: 0; right: 0; bottom: 0; width: 6px;
      background: var(--accent);
    }}
    .hero-info h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      font-weight: 800;
      margin-bottom: 6px;
    }}
    .hero-info p {{
      color: #cbd5e1;
      font-size: 13px;
      max-width: 620px;
      line-height: 1.5;
    }}
    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: var(--dark);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .doc-card {{
      background: #ffffff;
      border: 1px solid var(--gray-200);
      border-radius: 10px;
      padding: 24px 28px;
      margin-bottom: 20px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.03);
      transition: all 0.2s ease;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-left: 5px solid var(--accent);
    }}
    .doc-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0,0,0,0.08);
      border-color: var(--gray-300);
      border-left-color: var(--accent-dark);
    }}
    .doc-card.upcoming {{
      border-left: 5px solid #cbd5e1;
      opacity: 0.75;
    }}
    .doc-card-left {{
      flex: 1;
      padding-right: 25px;
    }}
    .doc-badge-row {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 8px;
    }}
    .badge-ref {{
      font-family: 'Outfit', sans-serif;
      font-size: 12px;
      font-weight: 800;
      color: var(--primary);
      background: #e0f2fe;
      padding: 3px 9px;
      border-radius: 4px;
    }}
    .badge-status-active {{
      font-size: 11px;
      font-weight: 700;
      color: var(--success);
      background: var(--success-bg);
      padding: 3px 9px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }}
    .badge-status-upcoming {{
      font-size: 11px;
      font-weight: 600;
      color: var(--gray-500);
      background: var(--gray-100);
      padding: 3px 9px;
      border-radius: 4px;
      text-transform: uppercase;
    }}
    .doc-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: var(--dark);
      margin-bottom: 6px;
    }}
    .doc-desc {{
      font-size: 12.5px;
      color: var(--gray-600);
      line-height: 1.5;
      margin-bottom: 12px;
    }}
    .doc-meta {{
      display: flex;
      gap: 20px;
      font-size: 11.5px;
      color: var(--gray-500);
    }}
    .doc-meta span strong {{
      color: var(--gray-700);
    }}
    .doc-actions {{
      display: flex;
      flex-direction: column;
      gap: 9px;
      min-width: 170px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 7px;
      font-size: 12.5px;
      font-weight: 600;
      padding: 9px 16px;
      border-radius: 6px;
      text-decoration: none;
      transition: all 0.2s;
      cursor: pointer;
      text-align: center;
    }}
    .btn-view {{
      background: var(--primary);
      color: #ffffff;
    }}
    .btn-view:hover {{
      background: #18446e;
    }}
    .btn-download {{
      background: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
    }}
    .btn-download:hover {{
      background: #d1fae5;
    }}
    .btn-disabled {{
      background: var(--gray-100);
      color: var(--gray-400);
      cursor: not-allowed;
      border: 1px solid var(--gray-200);
    }}
    .portal-footer {{
      margin-top: 50px;
      border-top: 1px solid var(--gray-200);
      padding: 22px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11.5px;
      color: var(--gray-500);
    }}

    @media (max-width: 768px) {{
      .portal-nav {{
        padding: 12px 18px;
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
      }}
      .nav-right {{
        width: 100%;
        justify-content: space-between;
      }}
      .portal-container {{
        margin: 20px auto;
        padding: 0 16px;
      }}
      .client-hero {{
        padding: 24px 20px;
      }}
      .client-hero h1 {{
        font-size: 20px;
      }}
      .doc-card {{
        flex-direction: column;
        align-items: stretch;
        gap: 16px;
        padding: 20px 18px;
      }}
      .doc-card-left {{
        padding-right: 0;
      }}
      .doc-meta {{
        flex-direction: column;
        gap: 6px;
      }}
      .doc-actions {{
        width: 100%;
      }}
      .btn {{
        width: 100%;
        padding: 11px 16px;
      }}
      .portal-footer {{
        flex-direction: column;
        text-align: center;
        gap: 10px;
        margin-top: 40px;
        padding: 20px 0;
      }}
    }}
  </style>
</head>
<body>

  <!-- TOP NAVIGATION -->
  <nav class="portal-nav">
    <div class="nav-brand">
      <img class="nav-logo" src="{logo_sands_white}" alt="SaNDS Lab" />
      <div class="nav-title-block">
        <span class="nav-title">SaNDS Lab • Enterprise Document Portal</span>
        <span class="nav-sub">docs.sandslab.com/popular</span>
      </div>
    </div>
    <div class="nav-right">
      <?php if ($is_super_admin): ?>
        <a href="?view=admin" class="btn-admin-manage">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          User Management
        </a>
      <?php endif; ?>
      <div class="user-auth-badge">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        <span><?php echo htmlspecialchars($authenticated_user); ?></span>
      </div>
      <a href="?logout=1" class="btn-logout">Sign Out</a>
    </div>
  </nav>

  <div class="portal-container">

    <!-- CLIENT HERO -->
    <div class="client-hero">
      <div class="hero-info">
        <h1>Popular Auto Spare & A/C Parts Co. W.L.L</h1>
        <p>Enterprise Cloud ERP Transformation Project • Official Project Documents, Milestone Delivery Plans, Architecture Specifications & Payment Schedule Repository.</p>
      </div>
    </div>

    <!-- DOCUMENT LIST -->
    <div class="section-header">
      <h2 class="section-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
        Master ERP Project Documents
      </h2>
    </div>

    <?php foreach ($routes as $route_id => $item): ?>
    <!-- ACTIVE DOCUMENT CARD -->
    <div class="doc-card">
      <div class="doc-card-left">
        <div class="doc-badge-row">
          <span class="badge-ref"><?php echo htmlspecialchars($route_id); ?></span>
          <span class="badge-status-active"><?php echo htmlspecialchars($item['status']); ?></span>
        </div>
        <h3 class="doc-title"><?php echo htmlspecialchars($item['title']); ?></h3>
        <p class="doc-desc"><?php echo htmlspecialchars($item['desc']); ?></p>
        <div class="doc-meta">
          <span>BA Ref: <strong><?php echo htmlspecialchars($item['ba_ref']); ?></strong></span>
          <span>Timeline: <strong><?php echo htmlspecialchars($item['timeline']); ?></strong></span>
          <span>Submission: <strong><?php echo htmlspecialchars($item['date']); ?></strong></span>
          <span>Scope: <strong><?php echo htmlspecialchars($item['scope']); ?></strong></span>
        </div>
      </div>
      <div class="doc-actions">
        <a href="?doc=<?php echo urlencode($route_id); ?>" class="btn btn-view">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
          View Online Document
        </a>
        <a href="?doc=<?php echo urlencode($route_id); ?>.pdf" download="<?php echo htmlspecialchars($item['pdf']); ?>" class="btn btn-download">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
          Download PDF
        </a>
      </div>
    </div>
    <?php endforeach; ?>

    <!-- UPCOMING MODULES -->
    <div class="doc-card upcoming">
      <div class="doc-card-left">
        <div class="doc-badge-row">
          <span class="badge-ref">SL-POP-ERP-TECH-001</span>
          <span class="badge-status-upcoming">In Architecture Review</span>
        </div>
        <h3 class="doc-title">ERP Technology Stack, Offline Sync Engine & Security Architecture</h3>
        <p class="doc-desc">Technical specification covering React.js Frontend, PHP MVC REST API, MySQL 8.0 Master-Replica, Offline SQLite/IndexedDB sync, JWT + AES-256 encryption, and Git CI/CD deployment.</p>
      </div>
      <div class="doc-actions">
        <button class="btn btn-disabled" disabled>Coming Soon</button>
      </div>
    </div>

    <div class="doc-card upcoming">
      <div class="doc-card-left">
        <div class="doc-badge-row">
          <span class="badge-ref">SL-POP-ERP-MS-002</span>
          <span class="badge-status-upcoming">Phase 2 Scheduled</span>
        </div>
        <h3 class="doc-title">Module 2: Vendor & Purchase Flow Milestone Proposal</h3>
        <p class="doc-desc">Centralized procurement workflows, purchase orders (PO), goods receiving note (GRN), vendor variance tracking, and CTO purchase approvals.</p>
      </div>
      <div class="doc-actions">
        <button class="btn btn-disabled" disabled>Coming Soon</button>
      </div>
    </div>

    <!-- FOOTER -->
    <footer class="portal-footer">
      <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain • Hotline: +973 35 078 079</div>
      <div>Confidential Client Portal • Popular Auto Spare & A/C Parts Co. W.L.L</div>
    </footer>

  </div>

</body>
</html>
'''

with open('index.php', 'w', encoding='utf-8') as f:
    f.write(php_code)

with open('popular/index.php', 'w', encoding='utf-8') as f:
    f.write(php_code)

print('Full SQLite Database + Admin User Management index.php generated successfully!')
