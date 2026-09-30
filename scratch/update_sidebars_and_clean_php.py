import os
import re
import glob

BASE_DIR = r"e:\PopularMileStones"
POPULAR_DIR = os.path.join(BASE_DIR, "popular")

# CSS to ensure exists in styles
SIDEBAR_CARD_CSS = """
    .sidebar-card {
      margin-top: 20px;
      padding: 16px;
      background: linear-gradient(135deg, var(--gray-50, #f8fafc) 0%, var(--gray-100, #f1f5f9) 100%);
      border-radius: var(--radius-md, 8px);
      border: 1px solid var(--gray-200, #e2e8f0);
      font-size: 12px;
      color: var(--gray-700, #334155);
    }

    .sidebar-card-title {
      font-weight: 700;
      color: var(--primary, #0a2540);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
    }
"""

# Cards for each module
CARDS = {
    "MS-001": """      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Module 1 At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Timeline:</strong> 10 Weeks (50 Days)</div>
          <div><strong>Total Baseline:</strong> BD 3,409.091</div>
          <div><strong>Sprints:</strong> 4 x 25% Gates</div>
          <div><strong>BA Source:</strong> DOC-001 v1.0 (42 pgs)</div>
          <div><strong>Scope:</strong> PCode & Master Item Engine</div>
        </div>
        <button class="btn btn-primary" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>""",

    "MS-002": """      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Module 2 At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Timeline:</strong> 12 Weeks (60 Days)</div>
          <div><strong>Total Baseline:</strong> BD 4,090.909</div>
          <div><strong>Sprints:</strong> 4 x 25% Gates</div>
          <div><strong>BA Source:</strong> DOC-002 v1.0 (48 pgs)</div>
          <div><strong>Scope:</strong> Vendor & Purchase Management</div>
        </div>
        <button class="btn btn-primary" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>""",

    "MS-003": """      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Module 3 At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Timeline:</strong> 15 Weeks (75 Days)</div>
          <div><strong>Total Baseline:</strong> BD 5,113.636</div>
          <div><strong>Sprints:</strong> 4 x 25% Gates</div>
          <div><strong>BA Source:</strong> DOC-003 v1.0 (54 pgs)</div>
          <div><strong>Scope:</strong> Store Verification & Stock Control</div>
        </div>
        <button class="btn btn-primary" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>""",

    "MS-004": """      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Module 4 At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Timeline:</strong> 15 Weeks (3.75 Mo)</div>
          <div><strong>Total Baseline:</strong> BD 5,113.636</div>
          <div><strong>Sprints:</strong> 5 x 20% Phases</div>
          <div><strong>BA Source:</strong> DOC-004 v1.0 (58 pgs)</div>
          <div><strong>Scope:</strong> Counter & Handheld POS Billing</div>
        </div>
        <button class="btn btn-primary" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>""",

    "MS-005": """      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Module 5 At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Timeline:</strong> 13 Weeks (3.25 Mo)</div>
          <div><strong>Total Baseline:</strong> BD 4,431.818</div>
          <div><strong>Sprints:</strong> 5 x 20% Phases</div>
          <div><strong>BA Source:</strong> DOC-005 v1.0 (51 pgs)</div>
          <div><strong>Scope:</strong> Multi-Branch ERP Accounts</div>
        </div>
        <button class="btn btn-primary" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>""",

    "MS-006": """      <div class="sidebar-card">
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
      </div>""",

    "MS-007": """      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Module 7 At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Timeline:</strong> 16 Weeks (80 Days)</div>
          <div><strong>Total Baseline:</strong> BD 5,454.548</div>
          <div><strong>Milestones:</strong> 4 x 25% Phases</div>
          <div><strong>BA Source:</strong> DOC-007 v1.0 (80 pgs)</div>
          <div><strong>Scope:</strong> HRMS, Attendance, Payroll & EOSB</div>
        </div>
        <button class="btn btn-primary" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>""",

    "MS-008": """      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Module 8 At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Timeline:</strong> 3 Working Weeks (15 Days)</div>
          <div><strong>Total Baseline:</strong> BD 1,022.727</div>
          <div><strong>Milestones:</strong> 3 Verified Gates</div>
          <div><strong>BA Source:</strong> ARCH-001 v1.0 (80 pgs)</div>
          <div><strong>Scope:</strong> QR Handhelds, Biometrics & Servers</div>
        </div>
        <button class="btn btn-primary" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>""",

    "MS-009": """      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Module 9 At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Timeline:</strong> 4 Working Weeks (20 Days)</div>
          <div><strong>Total Baseline:</strong> BD 1,363.636</div>
          <div><strong>Milestones:</strong> 4 Verified Gates</div>
          <div><strong>BA Source:</strong> DOC-009 v1.0 (30 pgs)</div>
          <div><strong>Scope:</strong> Cross-Module BI & 8-Module KPIs</div>
        </div>
        <button class="btn btn-primary" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>""",

    "SUMMARY": """      <div class="sidebar-card">
        <div class="sidebar-card-title">
          <i class="fas fa-chart-pie"></i> Master ERP At A Glance
        </div>
        <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
          <div><strong>Total Modules:</strong> 9 Integrated Process Suites</div>
          <div><strong>Total Timeline:</strong> 88 Dedicated Weeks (17.6 Mo)</div>
          <div><strong>Total Project Cost:</strong> BD 34,090.910</div>
          <div><strong>Delivery Gates:</strong> 35 Verified Sprints</div>
          <div><strong>Scope:</strong> Enterprise Multi-Branch Suite</div>
        </div>
        <button class="btn btn-accent" onclick="window.print()" style="width: 100%; margin-top: 14px; padding: 8px 12px; font-size: 12px; color: #fff;">
          <i class="fas fa-file-pdf"></i> Export / Print PDF
        </button>
      </div>"""
}

def clean_and_update_html(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean raw PHP opening block if present
    # Look for <?php ... ?> before <!DOCTYPE html>
    if content.strip().startswith('<?php'):
        doctype_pos = content.find('<!DOCTYPE html>')
        if doctype_pos != -1:
            content = content[doctype_pos:]
        else:
            doctype_pos_lower = content.find('<!doctype html>')
            if doctype_pos_lower != -1:
                content = content[doctype_pos_lower:]

    # 2. Determine document type
    doc_type = None
    for key in ["MS-001", "MS-002", "MS-003", "MS-004", "MS-005", "MS-006", "MS-007", "MS-008", "MS-009", "SUMMARY"]:
        if key in filepath.upper() or (key == "MS-001" and "PCODE" in filepath.upper()) or \
           (key == "MS-002" and "VENDOR" in filepath.upper()) or \
           (key == "MS-003" and "STORE" in filepath.upper()) or \
           (key == "MS-004" and "SALES" in filepath.upper()) or \
           (key == "MS-005" and "ACCOUNTS" in filepath.upper()) or \
           (key == "MS-006" and "ADMINISTRATION" in filepath.upper()) or \
           (key == "MS-007" and "HUMAN_RESOURCE" in filepath.upper()) or \
           (key == "MS-008" and "HARDWARE" in filepath.upper()) or \
           (key == "MS-009" and "EXECUTIVE_MANAGEMENT" in filepath.upper()) or \
           (key == "SUMMARY" and "EXECUTIVE_MASTER_SUMMARY" in filepath.upper()):
            doc_type = key
            break

    if not doc_type:
        # Save cleaned file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return

    # Ensure CSS .sidebar-card is in <style>
    if '.sidebar-card' not in content:
        content = content.replace('</style>', SIDEBAR_CARD_CSS + '\n  </style>')

    # 3. Replace any old sidebar-portal-box or existing sidebar-card in <aside class="sticky-sidebar">
    target_card = CARDS[doc_type]
    
    # Check if sidebar-portal-box exists
    if 'sidebar-portal-box' in content:
        # Regex replace <div class="sidebar-portal-box".*?</div>\s*</aside>
        pattern = re.compile(r'<div class="sidebar-portal-box"[^>]*>[\s\S]*?</div>\s*</aside>', re.IGNORECASE)
        content = pattern.sub(target_card + '\n    </aside>', content)

    # Check if sidebar-card already exists in <aside> but might have wrong content (like Module 6 instead of Module 7)
    elif '<div class="sidebar-card">' in content:
        pattern = re.compile(r'<div class="sidebar-card"[^>]*>[\s\S]*?</div>\s*</aside>', re.IGNORECASE)
        content = pattern.sub(target_card + '\n    </aside>', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath} -> {doc_type}")

# Target file list
html_files = glob.glob(os.path.join(BASE_DIR, "*.html"))
for hf in html_files:
    clean_and_update_html(hf)

popular_html_files = glob.glob(os.path.join(POPULAR_DIR, "*.html"))
for phf in popular_html_files:
    clean_and_update_html(phf)

print("All HTML files processed successfully!")
