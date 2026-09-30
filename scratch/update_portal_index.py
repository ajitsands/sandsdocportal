import re

def update_portal_index(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add route entry if not present
    ms4_route = """    'SL-POP-ERP-MS-004' => array(
        'title'    => 'Module 4: Sales Process, POS, Multi-Branch Billing, Sales Return & Branch Financial Control Milestone',
        'html'     => 'SL-POP-ERP-MS-004.html',
        'pdf'      => 'SL-POP-ERP-MS-004.pdf',
        'status'   => 'Submitted & Ready for Sign-off',
        'timeline' => '15 Working Weeks (75 Days)',
        'scope'    => 'Counter & Mobile POS, Multi-Branch Billing & GL Accounting',
        'ba_ref'   => 'DOC-004 (Ver 1.0)',
        'date'     => '30/03/2026',
        'desc'     => 'End-to-end 15-week implementation roadmap for Centralized Customer Master & Credit Matrix, Mobile Android Handheld Floor POS, 1-Scan Dynamic QR Cart Handoff, Multi-Salesperson Commission Split, Quotations/Delivery Notes/VAT Tax Invoices/Cash Memos, Unified Sales Returns & Condition Grading, Branch Vouchers Suite (CRV/CPV/JV/Contra/Petty Cash), and End-of-Day (EOD) Physical Cash Drawer Count with hard Day-Closing lock (BD 5,113.636).'
    ),"""

    if "'SL-POP-ERP-MS-004'" not in content:
        # insert after SL-POP-ERP-MS-003 route
        content = content.replace("'SL-POP-ERP-MS-003' => array(", ms4_route + "\n    'SL-POP-ERP-MS-003' => array(")

    # 2. Add status check variable for ms4
    ms4_status_code = """    $ms4_status = 'IN_REVIEW';
    if ($pdo) {
        $ms4_meta_stmt = $pdo->query("SELECT status FROM document_meta WHERE doc_id = 'SL-POP-ERP-MS-004'");
        if ($ms4_meta_stmt) {
            $val = $ms4_meta_stmt->fetchColumn();
            if ($val) $ms4_status = $val;
        }
    }"""

    if "$ms4_status" not in content:
        content = content.replace("$ms3_status = 'IN_REVIEW';", "$ms3_status = 'IN_REVIEW';\n    $ms4_status = 'IN_REVIEW';")
        content = content.replace("if ($ms3_meta_stmt) {\n            $val = $ms3_meta_stmt->fetchColumn();\n            if ($val) $ms3_status = $val;\n        }",
                                  "if ($ms3_meta_stmt) {\n            $val = $ms3_meta_stmt->fetchColumn();\n            if ($val) $ms3_status = $val;\n        }\n        $ms4_meta_stmt = $pdo->query(\"SELECT status FROM document_meta WHERE doc_id = 'SL-POP-ERP-MS-004'\");\n        if ($ms4_meta_stmt) {\n            $val = $ms4_meta_stmt->fetchColumn();\n            if ($val) $ms4_status = $val;\n        }")

    # 3. Add Document Card in Dashboard
    doc_card_ms4 = """    <!-- DOCUMENT 5: MILESTONE 4 (SALES PROCESS & BRANCH FINANCIAL CONTROL) -->
    <div class="doc-card" style="border-top: 4px solid #059669;">
      <div class="doc-header-row">
        <div>
          <span class="doc-ref-badge" style="background:#ecfdf5; color:#047857;">DOC-004 (Ver 1.0)</span>
          <h2 class="doc-title">Module 4: Sales Process, POS, Multi-Branch Billing, Sales Return & Branch Financial Control</h2>
        </div>
        <span class="doc-status-badge" style="<?php echo ($ms4_status === 'FINALIZED_AND_LOCKED') ? 'background:#dcfce7; color:#15803d; border-color:#bbf7d0;' : 'background:#ecfdf5; color:#047857; border-color:#a7f3d0;'; ?>">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <?php echo ($ms4_status === 'FINALIZED_AND_LOCKED') ? '✅ Finalized & Executed' : 'Submitted & Ready for Sign-off'; ?>
        </span>
      </div>

      <div class="doc-meta-grid">
        <div>
          <div class="meta-item-label">Timeline</div>
          <div class="meta-item-val">15 Weeks (75 Days)</div>
        </div>
        <div>
          <div class="meta-item-label">Scope</div>
          <div class="meta-item-val">Counter POS, Mobile & GL</div>
        </div>
        <div>
          <div class="meta-item-label">Milestone Fee</div>
          <div class="meta-item-val">BD 5,113.636</div>
        </div>
        <div>
          <div class="meta-item-label">Date of Submission</div>
          <div class="meta-item-val">30-Mar-2026</div>
        </div>
      </div>

      <p class="doc-desc">
        Comprehensive 15-week implementation roadmap for Centralized Customer Master & Credit Matrix, Mobile Android Handheld Floor POS, 1-Scan Dynamic QR Cart Handoff, Multi-Salesperson Commission Split, Quotations/Delivery Notes/VAT Tax Invoices/Cash Memos, Unified Sales Returns & Condition Grading, Branch Vouchers Suite (CRV/CPV/JV/Contra/Petty Cash), and End-of-Day (EOD) Physical Cash Drawer Count with hard Day-Closing lock (BD 5,113.636).
      </p>

      <div class="doc-actions">
        <a href="?doc=SL-POP-ERP-MS-004" class="btn btn-primary" style="background: linear-gradient(135deg, #059669 0%, #047857 100%);">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
          Open Interactive Document
        </a>
        <a href="?doc=SL-POP-ERP-MS-004.pdf" target="_blank" class="btn btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
          Download Signed PDF (15 Pages)
        </a>
      </div>
    </div>
"""

    if "<!-- DOCUMENT 5: MILESTONE 4" not in content:
        # Insert after DOCUMENT 4 (MS-003)
        target = "<!-- UPCOMING MODULES -->"
        if target in content:
            content = content.replace(target, doc_card_ms4 + "\n" + target)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")

update_portal_index('index.php')
update_portal_index('popular/index.php')
