import re

with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add CSS for roadmap-box
roadmap_css = """    /* Roadmap Box */
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
"""

if ".roadmap-box {" not in code and ".roadmap-box {{" not in code:
    code = code.replace("/* Grid & Cards inside sections */", roadmap_css + "\n    /* Grid & Cards inside sections */")

# 2. Add Roadmap HTML inside Section 1.0 (Executive Summary) right after the Callout Box
roadmap_html = """        <!-- Master ERP Transformation Architecture (9 Core Modules) -->
        <div class="roadmap-box">
          <div class="roadmap-header">
            <h4>Master ERP Transformation Architecture (9 Core Process Modules)</h4>
            <span class="badge-tag badge-primary" style="font-size: 10.5px; padding: 4px 12px; letter-spacing: 0.5px;">CURRENT SCOPE: MODULE 04 ACTIVE</span>
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
            <div class="roadmap-item active">
              <span class="rm-badge">04</span>
              <span class="rm-name">Sales & POS Checkout</span>
            </div>
            <div class="roadmap-item">
              <span class="rm-badge">05</span>
              <span class="rm-name">Finance, Tax & VAT Accounting</span>
            </div>
            <div class="roadmap-item">
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
"""

target_pos = "          </div>\n        </div>\n\n        <div class=\"grid-3\">"
if target_pos in code and "Master ERP Transformation Architecture (9 Core Process Modules)" not in code:
    code = code.replace(target_pos, "          </div>\n        </div>\n\n" + roadmap_html + "\n        <div class=\"grid-3\">")

with open('build_sales_process_milestone.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Added Roadmap component to build_sales_process_milestone.py successfully!")
