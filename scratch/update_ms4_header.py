import re

with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add PHP is_locked check
php_check = """$is_locked = false;
if (isset($pdo) && $pdo) {
    try {
        $meta_stmt = $pdo->prepare("SELECT status FROM document_meta WHERE doc_id = ?");
        $meta_stmt->execute(array($doc_id));
        $status_val = $meta_stmt->fetchColumn();
        if ($status_val === 'FINALIZED_AND_LOCKED') {
            $is_locked = true;
        }
    } catch (Exception $e) {}
}"""

if "$is_locked =" not in code:
    code = code.replace("$authenticated_user = isset($_SESSION['authenticated_user'])", php_check + "\n\n$authenticated_user = isset($_SESSION['authenticated_user'])")

# 2. Add CSS for web-action-bar if not already present
web_bar_css = """    /* Web Action Header */
    .web-action-bar {
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
    }

    .web-action-left {
      display: flex;
      align-items: center;
      gap: 15px;
    }

    .portal-branding {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 14px;
      color: #ffffff;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .web-action-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .badge-accent {
      background: #fef3c7;
      color: #b45309;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }

    .badge-success {
      background: #dcfce7;
      color: #15803d;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }
"""

if ".web-action-bar {" not in code:
    code = code.replace("/* Global Header Banner */", web_bar_css + "\n    /* Global Header Banner */")

# 3. Add HTML for web-action-bar right after <body>
web_bar_html = """<body>

  <!-- ==================== WEB PORTAL TOP ACTION BAR ==================== -->
  <div class="web-action-bar">
    <div class="web-action-left">
      <a href="index.php" class="portal-branding">
        <span style="background:#0284c7; color:#fff; border-radius:4px; padding:2px 6px; font-size:11px;">PORTAL</span>
        SaNDS Lab • Popular ERP Governance
      </a>
      <span style="color:#64748b;">|</span>
      <span style="font-family:'JetBrains Mono', monospace; font-size:12px; color:#38bdf8;">DOC: SL-POP-ERP-MS-004</span>
      <?php if ($is_locked): ?>
        <span class="badge badge-success">🔒 FINALIZED & LOCKED</span>
      <?php else: ?>
        <span class="badge badge-accent">📝 IN ACTIVE REVIEW</span>
      <?php endif; ?>
    </div>
    <div class="web-action-right">
      <a href="index.php" class="btn btn-outline">← Back to Portal</a>
      <button onclick="window.print();" class="btn btn-outline">🖨️ Print Document</button>
      <a href="SL-POP-ERP-MS-004.pdf" download class="btn btn-accent">📥 Download Signed PDF</a>
    </div>
  </div>
"""

if "<!-- ==================== WEB PORTAL TOP ACTION BAR ==================== -->" not in code:
    code = code.replace("<body>", web_bar_html)

# 4. Make sure @media print hides .web-action-bar
if ".web-action-bar" not in code.split("@media print")[1]:
    code = code.replace("@media print {\n      body {", "@media print {\n      .web-action-bar { display: none !important; }\n      body {")

with open('build_sales_process_milestone.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated build_sales_process_milestone.py with web-action-bar!")
