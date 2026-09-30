import re

def update_portal_with_ms5(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add route entry if not present
    ms5_route = """    'SL-POP-ERP-MS-005' => array(
        'title'    => 'Module 5: Accounting & Financial Management, General Ledger, Treasury, AP/AR & VAT Compliance Milestone',
        'html'     => 'SL-POP-ERP-MS-005.html',
        'pdf'      => 'SL-POP-ERP-MS-005.pdf',
        'status'   => 'Submitted & Ready for Sign-off',
        'timeline' => '13 Working Weeks (65 Days)',
        'scope'    => 'Double-Entry GL, Treasury, AP/AR, Landed Cost & VAT Compliance',
        'ba_ref'   => 'DOC-005 (Ver 1.0)',
        'date'     => '04/07/2026',
        'desc'     => 'Comprehensive 13-week implementation roadmap for 5-Group Dynamic Chart of Accounts, Double-Entry General Ledger, 3-Way AP Matching, Landed-Cost COGS Apportionment, AR Overdue Credit Risk Locks, Multi-Bank Reconciliation (BRS), Post-Dated Cheques (PDC) Lifecycle, Multi-Currency FX Engine, GCC VAT Compliance, Consolidated Balance Sheet/P&L, and 10-Phase New Branch Setup SOP (BD 4,431.818).'
    ),"""

    if "'SL-POP-ERP-MS-005'" not in content:
        # insert before SL-POP-ERP-MS-004 route or after
        content = content.replace("'SL-POP-ERP-MS-004' => array(", ms5_route + "\n    'SL-POP-ERP-MS-004' => array(")

    # 2. Add status check variable for ms5
    if "$ms5_status" not in content:
        content = content.replace("$ms4_status = 'IN_REVIEW';", "$ms4_status = 'IN_REVIEW';\n    $ms5_status = 'IN_REVIEW';")
        content = content.replace("if ($ms4_meta_stmt) {\n            $val = $ms4_meta_stmt->fetchColumn();\n            if ($val) $ms4_status = $val;\n        }",
                                  "if ($ms4_meta_stmt) {\n            $val = $ms4_meta_stmt->fetchColumn();\n            if ($val) $ms4_status = $val;\n        }\n        $ms5_meta_stmt = $pdo->query(\"SELECT status FROM document_meta WHERE doc_id = 'SL-POP-ERP-MS-005'\");\n        if ($ms5_meta_stmt) {\n            $val = $ms5_meta_stmt->fetchColumn();\n            if ($val) $ms5_status = $val;\n        }")

    # 3. Add Document Card in Dashboard
    doc_card_ms5 = """    <!-- DOCUMENT 6: MILESTONE 5 (ACCOUNTS & FINANCIAL MANAGEMENT) -->
    <div class="doc-card" style="border-top: 4px solid #2563eb;">
      <div class="doc-header-row">
        <div>
          <span class="doc-ref-badge" style="background:#eff6ff; color:#1d4ed8;">DOC-005 (Ver 1.0)</span>
          <h2 class="doc-title">Module 5: Accounting & Financial Management, General Ledger, Treasury, AP/AR & VAT Compliance</h2>
        </div>
        <span class="doc-status-badge" style="<?php echo ($ms5_status === 'FINALIZED_AND_LOCKED') ? 'background:#dcfce7; color:#15803d; border-color:#bbf7d0;' : 'background:#eff6ff; color:#1d4ed8; border-color:#bfdbfe;'; ?>">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <?php echo ($ms5_status === 'FINALIZED_AND_LOCKED') ? '✅ Finalized & Executed' : 'Submitted & Ready for Sign-off'; ?>
        </span>
      </div>

      <div class="doc-meta-grid">
        <div>
          <div class="meta-item-label">Timeline</div>
          <div class="meta-item-val">13 Weeks (65 Days)</div>
        </div>
        <div>
          <div class="meta-item-label">Scope</div>
          <div class="meta-item-val">Double-Entry GL & Treasury</div>
        </div>
        <div>
          <div class="meta-item-label">Milestone Fee</div>
          <div class="meta-item-val">BD 4,431.818</div>
        </div>
        <div>
          <div class="meta-item-label">Date of Submission</div>
          <div class="meta-item-val">04-July-2026</div>
        </div>
      </div>

      <p class="doc-desc">
        Comprehensive 13-week implementation roadmap for 5-Group Dynamic Chart of Accounts, Double-Entry General Ledger, 3-Way AP Matching, Landed-Cost COGS Apportionment, AR Overdue Credit Risk Locks, Multi-Bank Reconciliation (BRS), Post-Dated Cheques (PDC) Lifecycle, Multi-Currency FX Engine, GCC VAT Compliance, Consolidated Balance Sheet/P&L, and 10-Phase New Branch Setup SOP (BD 4,431.818).
      </p>

      <div class="doc-actions">
        <a href="?doc=SL-POP-ERP-MS-005" class="btn btn-primary" style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
          Open Interactive Document
        </a>
        <a href="?doc=SL-POP-ERP-MS-005.pdf" target="_blank" class="btn btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
          Download Signed PDF (16 Pages)
        </a>
      </div>
    </div>
"""

    if "<!-- DOCUMENT 6: MILESTONE 5" not in content:
        target = "<!-- UPCOMING MODULES -->"
        if target in content:
            content = content.replace(target, doc_card_ms5 + "\n" + target)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")

update_portal_with_ms5('index.php')
update_portal_with_ms5('popular/index.php')
