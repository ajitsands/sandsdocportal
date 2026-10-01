import os, glob, re

# =========================================================================
# 1. FIX INDEX.PHP & POPULAR/INDEX.PHP
# =========================================================================
portal_css_responsive = """
    /* =========================================================================
       COMPREHENSIVE MOBILE RESPONSIVE STYLING FOR PORTAL HUB & ADMIN CONSOLE
       ========================================================================= */
    @media (max-width: 1024px) {
      .portal-header {
        padding: 16px 20px !important;
      }
      .portal-container {
        padding: 0 16px !important;
      }
      .stats-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 14px !important;
      }
      .doc-meta-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 12px !important;
      }
    }

    @media (max-width: 768px) {
      .portal-header {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 12px !important;
        padding: 14px 16px !important;
      }
      .portal-nav-left, .portal-nav-right {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
      }
      .portal-user-badge {
        font-size: 11px !important;
        padding: 4px 8px !important;
      }
      .admin-header {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 12px !important;
      }
      .admin-title {
        font-size: 20px !important;
      }
      .admin-tabs-nav {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        white-space: nowrap !important;
        padding: 6px 8px !important;
        gap: 6px !important;
      }
      .admin-tab-btn {
        padding: 8px 12px !important;
        font-size: 12px !important;
      }
      .doc-card {
        padding: 18px 16px !important;
      }
      .doc-header-row {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 10px !important;
      }
      .doc-title {
        font-size: 16px !important;
      }
      .doc-actions {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 8px !important;
      }
      .doc-actions .btn {
        width: 100% !important;
        justify-content: center !important;
        text-align: center !important;
      }
      .dataTables_wrapper .dataTables_length,
      .dataTables_wrapper .dataTables_filter,
      .dataTables_wrapper .dataTables_info,
      .dataTables_wrapper .dataTables_paginate {
        float: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        margin-bottom: 10px !important;
        width: 100% !important;
      }
      .dataTables_wrapper .dataTables_filter input {
        width: 100% !important;
        margin-left: 0 !important;
        margin-top: 6px !important;
      }
      .table-responsive, .dataTables_wrapper {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
      }
    }

    @media (max-width: 480px) {
      .stats-grid {
        grid-template-columns: 1fr !important;
        gap: 10px !important;
      }
      .doc-meta-grid {
        grid-template-columns: 1fr !important;
        gap: 8px !important;
      }
      .btn {
        font-size: 11.5px !important;
        padding: 7px 12px !important;
      }
      .portal-footer {
        font-size: 10px !important;
        padding: 20px 10px !important;
      }
    }
"""

for p_file in ['index.php', 'popular/index.php']:
    if os.path.exists(p_file):
        with open(p_file, 'r', encoding='utf-8') as f:
            p_code = f.read()
        
        # Replace broken CSS lines
        p_code = re.sub(r'\.stats-grid\s*\{\s*grid-template-columns:\s*1fr\s*1fr;\s*\}\s*table\s*\{\s*display:\s*block;\s*overflow-x:\s*auto;\s*\}\s*\}', '', p_code)
        
        if 'COMPREHENSIVE MOBILE RESPONSIVE STYLING FOR PORTAL HUB' not in p_code:
            p_code = p_code.replace('</style>', portal_css_responsive + '\n  </style>')
            with open(p_file, 'w', encoding='utf-8') as f:
                f.write(p_code)
            print(f"Injected responsive CSS into {p_file}")

# =========================================================================
# 2. ARCHITECTURE DOCUMENTS (SL-POP-ERP-ARCH-001.html & Technical_Architecture_Document.html)
# =========================================================================
arch_css_responsive = """
    /* Mobile Responsive Optimizations for Architecture Document */
    @media (max-width: 900px) {
      body {
        background-color: #ffffff !important;
        font-size: 11px !important;
      }
      .document-wrapper {
        margin: 0 !important;
        max-width: 100% !important;
        border-radius: 0 !important;
        box-shadow: none !important;
      }
      .page {
        padding: 16px 14px !important;
        min-height: auto !important;
      }
      .page-break {
        border-bottom: 2px dashed #cbd5e1 !important;
        margin-bottom: 25px !important;
        padding-bottom: 25px !important;
      }
      .header-container, .footer-container {
        flex-direction: column !important;
        text-align: center !important;
        gap: 8px !important;
      }
      .grid-2, .grid-3, .grid-4, .stats-row, .kpi-row {
        grid-template-columns: 1fr !important;
        gap: 12px !important;
      }
      .table-container, table {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        display: block !important;
        width: 100% !important;
      }
      .card {
        padding: 14px !important;
        margin-bottom: 14px !important;
      }
    }
"""

for a_file in ['SL-POP-ERP-ARCH-001.html', 'Technical_Architecture_Document.html', 'popular/SL-POP-ERP-ARCH-001.html', 'popular/Technical_Architecture_Document.html']:
    if os.path.exists(a_file):
        with open(a_file, 'r', encoding='utf-8') as f:
            a_code = f.read()
        if 'Mobile Responsive Optimizations for Architecture Document' not in a_code:
            a_code = a_code.replace('</style>', arch_css_responsive + '\n  </style>')
            with open(a_file, 'w', encoding='utf-8') as f:
                f.write(a_code)
            print(f"Injected responsive CSS into {a_file}")

# =========================================================================
# 3. MILESTONE MODULE DOCUMENTS (SL-POP-ERP-MS-001 to 009 & aliases)
# =========================================================================
milestone_css_responsive = """
    /* =========================================================================
       COMPREHENSIVE MOBILE RESPONSIVE STYLING FOR MILESTONE SUITE
       ========================================================================= */
    @media (max-width: 1100px) {
      .main-wrapper {
        grid-template-columns: 240px minmax(0, 1fr) !important;
        gap: 20px !important;
        padding: 0 16px !important;
      }
      .sticky-sidebar {
        width: 240px !important;
      }
    }

    @media (max-width: 900px) {
      .main-wrapper {
        display: block !important;
        grid-template-columns: 1fr !important;
        padding: 0 12px !important;
      }
      .sticky-sidebar {
        position: static !important;
        width: 100% !important;
        max-height: none !important;
        margin-bottom: 24px !important;
        top: 0 !important;
      }
      .sidebar-nav {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
      }
      .sidebar-link {
        flex: 1 1 calc(50% - 6px) !important;
        padding: 8px 10px !important;
        font-size: 11.5px !important;
      }
      .hero-stats-grid, .stat-grid, .kpi-grid, .meta-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 12px !important;
      }
      .doc-top-bar-inner, .header-content {
        flex-direction: column !important;
        text-align: center !important;
        gap: 12px !important;
        padding: 16px 12px !important;
      }
      .logos-cluster, .header-logos {
        justify-content: center !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
      }
      .doc-meta-badge-group, .doc-meta-badge {
        justify-content: center !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
      }
      .charts-grid {
        grid-template-columns: 1fr !important;
      }
    }

    @media (max-width: 600px) {
      .web-action-bar {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 10px !important;
        padding: 10px 12px !important;
      }
      .web-action-left, .web-action-right {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 6px !important;
        width: 100% !important;
      }
      .web-action-bar .btn {
        flex: 1 1 calc(50% - 6px) !important;
        text-align: center !important;
        justify-content: center !important;
        font-size: 11.5px !important;
        padding: 7px 10px !important;
      }
      .portal-branding {
        font-size: 12px !important;
        text-align: center !important;
        width: 100% !important;
        justify-content: center !important;
        display: flex !important;
      }
      .hero-card, .doc-section, .section-card, .signoff-section {
        padding: 16px 12px !important;
        border-radius: 10px !important;
        margin-bottom: 16px !important;
      }
      .hero-title, .section-title {
        font-size: 18px !important;
      }
      .hero-stats-grid, .stat-grid, .kpi-grid, .meta-grid {
        grid-template-columns: 1fr !important;
        gap: 10px !important;
      }
      .sidebar-link {
        flex: 1 1 100% !important;
      }
      .table-container {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        width: 100% !important;
        margin: 10px 0 15px 0 !important;
        border-radius: 6px !important;
      }
      table.milestone-table, table.master-table, table.data-table, table.rate-table {
        min-width: 540px !important;
      }
      .modal-box {
        width: 95% !important;
        max-width: 95% !important;
        padding: 16px !important;
        margin: 10px !important;
      }
      canvas.signature-pad, .sig-pad-canvas {
        height: 140px !important;
      }
      .total-cost-hero-box {
        flex-direction: column !important;
        text-align: center !important;
        gap: 12px !important;
        padding: 16px !important;
      }
      .total-cost-amt {
        font-size: 24px !important;
      }
    }
"""

all_ms_files = glob.glob('SL-POP-ERP-MS-*.html') + glob.glob('*_Milestone_and_Payment_Structure.html') + glob.glob('popular/SL-POP-ERP-MS-*.html') + glob.glob('popular/*_Milestone_and_Payment_Structure.html')
for ms in set(all_ms_files):
    if os.path.exists(ms):
        with open(ms, 'r', encoding='utf-8') as f:
            code = f.read()
        if 'COMPREHENSIVE MOBILE RESPONSIVE STYLING FOR MILESTONE SUITE' not in code:
            code = code.replace('</style>', milestone_css_responsive + '\n  </style>')
            with open(ms, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"Injected responsive CSS into {ms}")

# =========================================================================
# 4. MASTER SUMMARY DOCUMENTS
# =========================================================================
for sum_f in ['SL-POP-ERP-SUMMARY-001.html', 'Executive_Master_Summary_and_Budget_Milestone.html', 'popular/SL-POP-ERP-SUMMARY-001.html', 'popular/Executive_Master_Summary_and_Budget_Milestone.html']:
    if os.path.exists(sum_f):
        with open(sum_f, 'r', encoding='utf-8') as f:
            s_code = f.read()
        if 'COMPREHENSIVE MOBILE RESPONSIVE STYLING FOR MILESTONE SUITE' not in s_code:
            s_code = s_code.replace('</style>', milestone_css_responsive + '\n  </style>')
            with open(sum_f, 'w', encoding='utf-8') as f:
                f.write(s_code)
            print(f"Injected responsive CSS into {sum_f}")

print("All mobile responsive CSS rules injected successfully!")
