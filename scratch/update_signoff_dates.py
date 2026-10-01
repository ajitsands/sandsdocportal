import os, glob, re, shutil, subprocess

# Define module verification and approval metadata
# doc_id: (doc_title, prep_date, verif_date, consultant_date, client_date)
# If date is None, it remains "In Active Review" / "Pending Approval"
modules_meta = {
    'SL-POP-ERP-MS-001': (
        'Module 1: PCode Generation & Item Master Engine',
        '10-September-2026',
        '21-September-2026',
        '15-March-2026',    # UniGlobal
        '22-February-2026'   # Popular
    ),
    'SL-POP-ERP-MS-002': (
        'Module 2: Vendor & Purchase Management',
        '15-September-2026',
        '27-September-2026',
        '15-March-2026',    # UniGlobal
        '09-March-2026'     # Popular
    ),
    'SL-POP-ERP-MS-003': (
        'Module 3: Store Verification & Stock Control',
        '18-September-2026',
        '27-September-2026',
        '19-March-2026',    # UniGlobal
        '12-April-2026'     # Popular
    ),
    'SL-POP-ERP-MS-004': (
        'Module 4: Sales Process, POS & Billing',
        '20-March-2026',
        '30-March-2026',
        '22-July-2026',     # UniGlobal
        '30-July-2026'      # Popular
    ),
    'SL-POP-ERP-MS-005': (
        'Module 5: Accounting, GL, AP/AR & VAT',
        '15-June-2026',
        '04-July-2026',
        '13-September-2026', # UniGlobal
        '13-September-2026'  # Popular
    ),
    'SL-POP-ERP-MS-006': (
        'Module 6: Enterprise Administration & Fleet',
        '20-June-2026',
        '06-July-2026',
        None,               # UniGlobal: No Dates
        '09-August-2026'    # Popular
    ),
    'SL-POP-ERP-MS-007': (
        'Module 7: Human Resource Management & Payroll',
        '22-June-2026',
        '04-July-2026',
        None,
        None
    ),
    'SL-POP-ERP-MS-008': (
        'Module 8: Hardware, QR Scanner & Cloud Setup',
        '24-September-2026',
        '30-September-2026',
        None,
        None
    ),
    'SL-POP-ERP-MS-009': (
        'Module 9: Executive Management Dashboard & BI',
        '25-September-2026',
        '30-September-2026',
        None,
        None
    ),
    'SL-POP-ERP-SUMMARY-001': (
        'Master 9-Module ERP Milestone & Budget Roadmap',
        '25-September-2026',
        '30-September-2026',
        None,
        None
    )
}

aliases_map = {
    'PCode_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-001',
    'Vendor_Purchase_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-002',
    'Store_Verification_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-003',
    'Sales_Process_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-004',
    'Accounts_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-005',
    'Administration_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-006',
    'Human_Resource_Management_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-007',
    'Hardware_and_Server_Setup_Milestone_and_Payment_Structure.html': 'SL-POP-ERP-MS-008',
    'Executive_Master_Summary_and_Budget_Milestone.html': 'SL-POP-ERP-SUMMARY-001'
}

def generate_consultant_card(consultant_date):
    if consultant_date:
        badge_html = f"""<span class="badge-tag badge-success" style="background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-check"></i> Reviewed ({consultant_date})
                </span>"""
        status_html = """<span class="signoff-status-badge status-signed" id="badge_consultant_review" style="background: #f1f5f9; color: #0f766e; border: 1px solid #ccfbf1; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">REVIEWED & ENDORSED</span>"""
    else:
        badge_html = """<span class="badge-tag badge-primary" style="background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-clock"></i> In Active Review
                </span>"""
        status_html = """<span class="signoff-status-badge status-pending" id="badge_consultant_review" style="background: #fffbeb; color: #b45309; border: 1px solid #fde68a; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">IN REVIEW</span>"""

    return f"""            <!-- Consultant Review -->
            <div class="signoff-card" style="padding: 16px; border: 1.5px dashed #cbd5e1; border-radius: 8px; background: #ffffff; text-align: center;">
              <div style="font-size: 11px; font-weight: 800; color: #0a2540; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">CONSULTANT REVIEW</div>
              <div style="font-size: 13px; font-weight: 700; color: #1e293b;">UniGlobal Business Solutions</div>
              <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">Project Management Consultant</div>
              <div style="margin-bottom: 8px;" id="sig_badge_consultant_review">
                {badge_html}
              </div>
              {status_html}
            </div>"""

def generate_client_card(client_date):
    if client_date:
        badge_html = f"""<span class="badge-tag badge-success" style="background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-check"></i> Approved ({client_date})
                </span>"""
        status_html = """<span class="signoff-status-badge status-signed" id="badge_client_review" style="background: #f1f5f9; color: #0f766e; border: 1px solid #ccfbf1; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">APPROVED & SIGNED</span>"""
    else:
        badge_html = """<span class="badge-tag badge-primary" style="background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-clock"></i> Pending Approval
                </span>"""
        status_html = """<span class="signoff-status-badge status-pending" id="badge_client_review" style="background: #fffbeb; color: #b45309; border: 1px solid #fde68a; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">PENDING SIGNATURE</span>"""

    return f"""            <!-- Client Approval -->
            <div class="signoff-card" style="padding: 16px; border: 1.5px dashed #cbd5e1; border-radius: 8px; background: #ffffff; text-align: center;">
              <div style="font-size: 11px; font-weight: 800; color: #0a2540; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">CLIENT APPROVAL</div>
              <div style="font-size: 13px; font-weight: 700; color: #1e293b;">Popular Auto Spare & A/C Parts</div>
              <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">Authorized Executive Signatory</div>
              <div style="margin-bottom: 8px;" id="sig_badge_client_review">
                {badge_html}
              </div>
              {status_html}
            </div>"""

def update_file_signoff(filepath, doc_id):
    if doc_id not in modules_meta:
        return
    doc_title, prep_date, verif_date, consultant_date, client_date = modules_meta[doc_id]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Block 1 section inside content
    block1_pattern = re.compile(r'(<!-- Block 1: Engineering Preparation.*?)(<!-- Block 2: 3-Party Executive Governance|<div>\s*<h3[^>]*>\s*<i class="fa-solid fa-signature")', re.DOTALL)
    m = block1_pattern.search(content)
    
    consultant_card = generate_consultant_card(consultant_date)
    client_card = generate_client_card(client_date)
    
    new_block1 = f"""<!-- Block 1: Engineering Preparation & Multi-Tier Verification Matrix -->
        <div style="margin-bottom: 28px;">
          <h3 style="font-size: 14.5px; font-weight: 700; color: #0a2540; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
            <i class="fa-solid fa-code-branch" style="color: #d97706;"></i> 1. Engineering Preparation & Stakeholder Verification Matrix
          </h3>
          <div class="signoff-box-container" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px;">
            <!-- Prepared By Developer / Architect -->
            <div class="signoff-card" style="padding: 16px; border: 1.5px dashed #cbd5e1; border-radius: 8px; background: #ffffff; text-align: center;">
              <div style="font-size: 11px; font-weight: 800; color: #0a2540; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">DEVELOPER / ARCHITECT</div>
              <div style="font-size: 13px; font-weight: 700; color: #1e293b;">Ancy Varghese Thekkan</div>
              <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">Software Architect, SaNDS Lab</div>
              <div style="margin-bottom: 8px;">
                <span class="badge-tag badge-success" style="background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-check"></i> Prepared ({prep_date})
                </span>
              </div>
              <span class="signoff-status-badge status-signed" style="background: #f1f5f9; color: #0f766e; border: 1px solid #ccfbf1; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">COMPLETED</span>
            </div>

            <!-- Verified By CEO / Managing Director -->
            <div class="signoff-card" style="padding: 16px; border: 1.5px dashed #cbd5e1; border-radius: 8px; background: #ffffff; text-align: center;">
              <div style="font-size: 11px; font-weight: 800; color: #0a2540; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">VERIFIED BY (DEVELOPER)</div>
              <div style="font-size: 13px; font-weight: 700; color: #1e293b;">Ajit Kumar KV</div>
              <div style="font-size: 11px; color: #64748b; margin-bottom: 10px;">CEO & Managing Director, SaNDS Lab</div>
              <div style="margin-bottom: 8px;">
                <span class="badge-tag badge-success" style="background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 4px; font-size: 10.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px;">
                  <i class="fas fa-check"></i> Verified ({verif_date})
                </span>
              </div>
              <span class="signoff-status-badge status-signed" style="background: #f1f5f9; color: #0f766e; border: 1px solid #ccfbf1; padding: 3px 10px; border-radius: 12px; font-size: 10.5px; font-weight: 700;">CHECKED & VERIFIED</span>
            </div>

{consultant_card}

{client_card}
          </div>
        </div>

        """
    if m:
        content = content[:m.start(1)] + new_block1 + content[m.start(2):]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated Block 1 in {filepath} (Doc: {doc_id})")
    else:
        print(f"WARNING: Could not find Block 1 in {filepath}")

# Process all files
for doc_id in modules_meta:
    # 1. Main file SL-POP-ERP-MS-xxx.html
    main_file = f"{doc_id}.html"
    if os.path.exists(main_file):
        update_file_signoff(main_file, doc_id)
    
    pop_main = os.path.join('popular', main_file)
    if os.path.exists(pop_main):
        update_file_signoff(pop_main, doc_id)

for alias, doc_id in aliases_map.items():
    if os.path.exists(alias):
        update_file_signoff(alias, doc_id)
    pop_alias = os.path.join('popular', alias)
    if os.path.exists(pop_alias):
        update_file_signoff(pop_alias, doc_id)

print("\nAll HTML files updated with updated verification & approval dates!")
