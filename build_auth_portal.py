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
 * SaNDS Lab Enterprise Document Portal - Authenticated Access Engine
 * Location: /home/sandsl23/public_html/docs.sandslab.com/popular/index.php
 * Features:
 *   - Authorized Email Verification
 *   - 6-Digit OTP Email Delivery via PHP mail()
 *   - Permanent Device Authentication Cookie (Forever on this Device)
 *   - Beautiful Responsive SaNDS Lab Branded Login UI
 *   - PHP 5.6 to 8.x Compatible
 */

session_start();

// =========================================================================
// 1. AUTHORIZED USERS TABLE (Add / Edit Allowed Email Addresses Here)
// =========================================================================
$authorized_users = array(
    'ajit@sandslab.com'            => 'Ajit Kumar KV (SaNDS Lab)',
    'info@sandslab.com'            => 'SaNDS Lab Admin',
    'director@popularbahrain.com'  => 'Popular Auto Spare - Director',
    'popularpartsbh@gmail.com'     => 'Popular Auto Spare - Admin',
    'cto@popularbahrain.com'       => 'Popular Auto Spare - CTO',
    'consultant@uniglobal.com'     => 'UniGlobal Consultant',
    'uniglobalconsult@gmail.com'   => 'UniGlobal Consultant',
);

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
$auth_file = __DIR__ . '/.auth_devices.json';

function get_device_fingerprint($email) {{
    global $secret_salt;
    $ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'generic_browser';
    return hash('sha256', strtolower($email) . '|' . $secret_salt . '|' . $ua);
}}

function is_device_authenticated() {{
    global $auth_file, $authorized_users;
    
    if (isset($_SESSION['authenticated_user']) && !empty($_SESSION['authenticated_user'])) {{
        return $_SESSION['authenticated_user'];
    }}
    
    if (isset($_COOKIE['sands_auth_device']) && !empty($_COOKIE['sands_auth_device'])) {{
        $cookie_token = $_COOKIE['sands_auth_device'];
        if (file_exists($auth_file)) {{
            $tokens = json_decode(file_get_contents($auth_file), true);
            if (is_array($tokens) && isset($tokens[$cookie_token])) {{
                $saved_email = $tokens[$cookie_token];
                if (isset($authorized_users[$saved_email])) {{
                    $_SESSION['authenticated_user'] = $saved_email;
                    return $saved_email;
                }}
            }}
        }}
    }}
    return false;
}}

function register_authenticated_device($email) {{
    global $auth_file;
    $email = strtolower(trim($email));
    $token = get_device_fingerprint($email);
    
    // Set persistent cookie for 5 years (157,680,000 seconds = forever on this browser/device)
    setcookie('sands_auth_device', $token, time() + (86400 * 365 * 5), '/', '', false, true);
    
    // Save to device registry
    $tokens = array();
    if (file_exists($auth_file)) {{
        $tokens = json_decode(file_get_contents($auth_file), true);
        if (!is_array($tokens)) {{
            $tokens = array();
        }}
    }}
    $tokens[$token] = $email;
    @file_put_contents($auth_file, json_encode($tokens));
    
    $_SESSION['authenticated_user'] = $email;
    unset($_SESSION['otp_code']);
    unset($_SESSION['otp_email']);
    unset($_SESSION['otp_time']);
}}

// Handle Logout
if (isset($_GET['logout'])) {{
    if (isset($_COOKIE['sands_auth_device'])) {{
        $cookie_token = $_COOKIE['sands_auth_device'];
        if (file_exists($auth_file)) {{
            $tokens = json_decode(file_get_contents($auth_file), true);
            if (isset($tokens[$cookie_token])) {{
                unset($tokens[$cookie_token]);
                @file_put_contents($auth_file, json_encode($tokens));
            }}
        }}
        setcookie('sands_auth_device', '', time() - 3600, '/', '', false, true);
    }}
    session_destroy();
    header('Location: ' . strtok($_SERVER["REQUEST_URI"], '?'));
    exit;
}}

// =========================================================================
// 4. AJAX / POST AUTHENTICATION HANDLERS (Send OTP & Verify OTP)
// =========================================================================
$auth_error = '';
$auth_success = '';
$current_step = 'EMAIL_INPUT'; // 'EMAIL_INPUT' or 'OTP_INPUT'

// AJAX / Form Action: Send OTP
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'send_otp') {{
    $input_email = strtolower(trim($_POST['email']));
    
    if (empty($input_email) || !filter_var($input_email, FILTER_VALIDATE_EMAIL)) {{
        $auth_error = 'Please enter a valid email address.';
    }} elseif (!isset($authorized_users[$input_email])) {{
        $auth_error = 'Access Denied: <strong>' . htmlspecialchars($input_email) . '</strong> is not authorized to access this portal.';
    }} else {{
        // Generate 6-digit OTP
        $otp = sprintf("%06d", mt_rand(100000, 999999));
        $_SESSION['otp_code'] = $otp;
        $_SESSION['otp_email'] = $input_email;
        $_SESSION['otp_time'] = time();
        
        // Prepare HTML Email
        $user_name = $authorized_users[$input_email];
        $subject = "Your Verification Code: $otp - SaNDS Lab Document Portal";
        
        $headers  = "MIME-Version: 1.0\\r\\n";
        $headers .= "Content-type: text/html; charset=UTF-8\\r\\n";
        $headers .= "From: SaNDS Lab Security <no-reply@sandslab.com>\\r\\n";
        $headers .= "Reply-To: support@sandslab.com\\r\\n";
        $headers .= "X-Mailer: PHP/" . phpversion();
        
        $email_body = "<!DOCTYPE html>
        <html>
        <head>
          <meta charset='UTF-8'>
          <title>Verification Code</title>
        </head>
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
                
                <p style='font-size: 12.5px; color: #64748b; line-height: 1.5;'>This verification code is valid for <strong>15 minutes</strong>. Once entered, this device will remain permanently authenticated.</p>
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
        
        // Send email via PHP mail()
        @mail($input_email, $subject, $email_body, $headers);
        
        $current_step = 'OTP_INPUT';
        $auth_success = 'A 6-digit verification code has been dispatched to <strong>' . htmlspecialchars($input_email) . '</strong>.';
    }}
}}

// AJAX / Form Action: Verify OTP
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'verify_otp') {{
    $submitted_otp = trim($_POST['otp']);
    
    // Combine 6 inputs if passed as array
    if (isset($_POST['otp_digits']) && is_array($_POST['otp_digits'])) {{
        $submitted_otp = implode('', $_POST['otp_digits']);
    }}
    
    $saved_otp   = isset($_SESSION['otp_code']) ? $_SESSION['otp_code'] : '';
    $saved_email = isset($_SESSION['otp_email']) ? $_SESSION['otp_email'] : '';
    $saved_time  = isset($_SESSION['otp_time']) ? $_SESSION['otp_time'] : 0;
    
    if (empty($saved_otp) || empty($saved_email)) {{
        $auth_error = 'Session expired. Please request a new verification code.';
        $current_step = 'EMAIL_INPUT';
    }} elseif ((time() - $saved_time) > 900) {{ // 15 mins expiry
        $auth_error = 'Verification code has expired. Please request a new one.';
        $current_step = 'EMAIL_INPUT';
    }} elseif ($submitted_otp !== $saved_otp) {{
        $auth_error = 'Invalid 6-digit verification code. Please check your email and try again.';
        $current_step = 'OTP_INPUT';
    }} else {{
        // OTP Valid! Register Device Permanently
        register_authenticated_device($saved_email);
        
        // Redirect to clean requested page
        $target_url = strtok($_SERVER["REQUEST_URI"], '?');
        if (isset($_GET['doc']) && !empty($_GET['doc'])) {{
            $target_url .= '?doc=' . urlencode($_GET['doc']);
        }}
        header('Location: ' . $target_url);
        exit;
    }}
}}

// If user already in OTP step
if (isset($_SESSION['otp_code']) && !empty($_SESSION['otp_code']) && empty($auth_error) && $current_step === 'EMAIL_INPUT' && isset($_GET['step']) && $_GET['step'] === 'otp') {{
    $current_step = 'OTP_INPUT';
}}

// =========================================================================
// 5. CHECK AUTHENTICATION: IF NOT AUTHENTICATED -> SHOW BEAUTIFUL LOGIN SCREEN
// =========================================================================
$authenticated_user = is_device_authenticated();

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
      --primary-dark: #07192c;
      --accent: #e67e22;
      --accent-dark: #d35400;
      --secondary: #0e7490;
      --dark: #0f172a;
      --gray-900: #0f172a;
      --gray-800: #1e293b;
      --gray-700: #334155;
      --gray-600: #475569;
      --gray-500: #64748b;
      --gray-300: #cbd5e1;
      --gray-200: #e2e8f0;
      --gray-100: #f1f5f9;
      --white: #ffffff;
      --danger: #e11d48;
      --danger-bg: #ffe4e6;
      --success: #10b981;
      --success-bg: #ecfdf5;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
      overflow: hidden;
      animation: fadeIn 0.4s ease-out;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(15px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .auth-header {{
      background: linear-gradient(135deg, #07192c 0%, #0a2540 100%);
      padding: 35px 30px 28px;
      text-align: center;
      position: relative;
      border-bottom: 3px solid var(--accent);
    }}

    .auth-logo-img {{
      max-height: 52px; /* Bigger SaNDS Lab Logo as requested */
      width: auto;
      margin-bottom: 12px;
      filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));
    }}

    .auth-portal-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: var(--white);
      letter-spacing: 0.3px;
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
      pointer-events: none;
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
      transition: all 0.2s ease;
      outline: none;
    }}

    .form-control:focus {{
      background: var(--white);
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.18);
    }}

    /* 6-Digit OTP Box Grid */
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
      transition: all 0.2s;
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
      letter-spacing: 0.3px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(230, 126, 34, 0.4);
      transition: all 0.2s;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
    }}

    .btn-submit:hover {{
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(230, 126, 34, 0.5);
    }}

    .btn-submit:active {{
      transform: translateY(0);
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

    .auth-link:hover {{
      text-decoration: underline;
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
      text-align: center;
    }}

    @media (max-width: 480px) {{
      .auth-card {{
        border-radius: 12px;
      }}
      .auth-header {{
        padding: 28px 20px 22px;
      }}
      .auth-body {{
        padding: 24px 20px 20px;
      }}
      .auth-logo-img {{
        max-height: 46px;
      }}
      .otp-digit-box {{
        height: 46px;
        font-size: 18px;
      }}
    }}
  </style>
</head>
<body>

  <div class="auth-card">
    
    <!-- HEADER WITH BIGGER SANDS LAB LOGO -->
    <div class="auth-header">
      <img class="auth-logo-img" src="{logo_sands_white}" alt="SaNDS Lab Middle East W.L.L" />
      <div class="auth-portal-title">Client Document Portal</div>
      <div class="auth-portal-sub">Popular Auto Spare & A/C Parts Co. W.L.L ERP Repository</div>
    </div>

    <div class="auth-body">

      <?php if (!empty($auth_error)): ?>
        <div class="alert alert-danger">
          <?php echo $auth_error; ?>
        </div>
      <?php endif; ?>

      <?php if (!empty($auth_success)): ?>
        <div class="alert alert-success">
          <?php echo $auth_success; ?>
        </div>
      <?php endif; ?>

      <?php if ($current_step === 'EMAIL_INPUT'): ?>
        <!-- ==================== STEP 1: EMAIL ADDRESS INPUT ==================== -->
        <h2 class="auth-title">Authorized Sign-In</h2>
        <p class="auth-desc">Enter your registered organizational email address to receive your 6-digit verification code.</p>

        <form method="POST" action="">
          <input type="hidden" name="action" value="send_otp">
          
          <div class="form-group">
            <label class="form-label" for="email">Corporate Email Address</label>
            <div class="input-wrapper">
              <svg class="input-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              <input type="email" name="email" id="email" class="form-control" placeholder="name@company.com" required autofocus value="<?php echo isset($_POST['email']) ? htmlspecialchars($_POST['email']) : ''; ?>">
            </div>
          </div>

          <button type="submit" class="btn-submit">
            Send 6-Digit Code
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
          </button>
        </form>

      <?php else: ?>
        <!-- ==================== STEP 2: 6-DIGIT OTP VERIFICATION ==================== -->
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
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
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
          // Automatic 6-box OTP focusing and backspace navigation
          const otpBoxes = document.querySelectorAll('.otp-digit-box');
          const combinedOtp = document.getElementById('combinedOtp');
          const otpForm = document.getElementById('otpForm');

          otpBoxes.forEach((box, index) => {{
            box.addEventListener('input', (e) => {{
              const val = e.target.value;
              if (val.length === 1 && index < otpBoxes.length - 1) {{
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
              if (/^\d{{6}}$/.test(pasted)) {{
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
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
        256-Bit Encrypted Device Verification Engine
      </div>

    </div>
  </div>

  <div class="copyright">
    &copy; 2026 SaNDS Lab Middle East W.L.L • All Rights Reserved
  </div>

</body>
</html>
<?php
    exit;
}}

// =========================================================================
// 6. AUTHENTICATED USER: SERVE REQUESTED DOCUMENT OR DOCUMENT HUB
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
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
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
      gap: 12px;
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

    /* Mobile Responsive */
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
        <!-- View Online Document -->
        <a href="?doc=<?php echo urlencode($route_id); ?>" class="btn btn-view">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
          View Online Document
        </a>
        <!-- Download PDF -->
        <a href="?doc=<?php echo urlencode($route_id); ?>.pdf" download="<?php echo htmlspecialchars($item['pdf']); ?>" class="btn btn-download">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
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

print('Authenticated index.php generated successfully!')
