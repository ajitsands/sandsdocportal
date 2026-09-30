import os

BASE_DIR = r'e:\PopularMileStones'

master_card = """    <!-- MASTER DOCUMENT 0: MASTER ERP SUMMARY & BUDGET ROADMAP -->
    <div class="doc-card" style="border-top: 4px solid #d97706; background: linear-gradient(180deg, #fffbf0 0%, #ffffff 100px);">
      <div class="doc-header-row">
        <div>
          <span class="doc-ref-badge" style="background:#fef3c7; color:#b45309; font-weight:800;">★ MASTER ROADMAP (Ver 1.0)</span>
          <h2 class="doc-title" style="color: #0a2540;">Executive Master Summary: Complete 9-Module ERP Milestone & Commercial Budget Roadmap</h2>
        </div>
        <span class="doc-status-badge" style="background:#fef3c7; color:#b45309; border-color:#fde68a;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
          Submitted & Ready for Sign-off
        </span>
      </div>

      <div class="doc-meta-grid">
        <div>
          <div class="meta-item-label">Total Portfolio Effort</div>
          <div class="meta-item-val">88 Weeks (17.6 Mo)</div>
        </div>
        <div>
          <div class="meta-item-label">Scope Coverage</div>
          <div class="meta-item-val">9 Integrated Modules</div>
        </div>
        <div>
          <div class="meta-item-label">Total Project Investment</div>
          <div class="meta-item-val" style="color:#d97706; font-size:16px;">BD 34,090.910</div>
        </div>
        <div>
          <div class="meta-item-label">Milestone Tranches</div>
          <div class="meta-item-val">35 Verified Delivery Gates</div>
        </div>
      </div>

      <p class="doc-desc">
        Comprehensive master executive summary and budgeting roadmap covering all 9 ERP modules for Popular Auto Spare & A/C Parts Co. W.L.L. Includes visual analytics, milestone payment schedules (Total Contract Value: BD 34,090.910), 35 verified milestone delivery gates, dedicated engineering resource allocation rate cards, and multi-party cryptographic digital sign-off console.
      </p>

      <div class="doc-actions">
        <a href="?doc=SL-POP-ERP-SUMMARY-001" class="btn btn-primary" style="background: linear-gradient(135deg, #d97706 0%, #b45309 100%); font-weight: 700;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
          Open Master Budget Roadmap
        </a>
        <a href="?doc=SL-POP-ERP-SUMMARY-001.pdf" target="_blank" class="btn btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
          Download Master PDF (15 Pages)
        </a>
      </div>
    </div>
"""

for target in [os.path.join(BASE_DIR, 'index.php'), os.path.join(BASE_DIR, 'popular', 'index.php')]:
    with open(target, 'r', encoding='utf-8') as f:
        content = f.read()

    target_anchor = '<div class="portal-container">'
    if 'MASTER DOCUMENT 0: MASTER ERP SUMMARY' not in content:
        content = content.replace(target_anchor, target_anchor + "\n\n" + master_card)
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {target} with Master Summary Card.")
    else:
        print(f"Master Summary Card already present in {target}.")
