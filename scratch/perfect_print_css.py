import re
import os
import subprocess
import shutil
import fitz

# Read HTML
with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove any existing @page or @media print from inside <style>
# We will place @page and @media print at the VERY END of <style>
html = re.sub(r'@page\s*\{[^}]*\}', '', html)
html = re.sub(r'@media\s+print\s*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', '', html, flags=re.DOTALL)

# 2. Ensure section IDs are in place
sections_map = {
    "Visual Milestone & Budget Analytics": "sec-visual-analytics",
    "Master 9-Module Budgeting & Milestone Matrix (BHD)": "sec-master-table",
    "9-Module Architectural Scope & Deliverable Pillars": "sec-scope-pillars",
    "Complete 35 Milestone Tranches Detailed Breakdown (BHD)": "sec-detailed-milestones",
    "Dedicated Engineering Team & Transparent Rate Matrix": "sec-team-rate-card",
    "Total Project Investment & Milestone Schedule in Bahraini Dinars (BHD)": "sec-total-investment",
    "Governance, SLA & Payment Terms": "sec-terms-governance"
}

for title, s_id in sections_map.items():
    if f'id="{s_id}"' not in html:
        pattern = re.compile(r'(<div class="section-card")(>(\s*<div class="section-header">.*?<div class="section-title"><i[^>]*></i>\s*' + re.escape(title) + r'</div>))', re.DOTALL)
        m = pattern.search(html)
        if m:
            html = html[:m.start(1)] + f'<div class="section-card" id="{s_id}"' + html[m.end(1):]
            print(f"Added id='{s_id}'")

# In Section 4 (Detailed milestones), let's mark Module 6 with a page break class or ID so Modules 1-5 are on Page 5 and Modules 6-9 are on Page 6
# Let's search for Module 6 phase item in detailed milestones
m6_pattern = re.compile(r'(<div class="phase-module-item">\s*<div class="phase-mod-header"[^>]*>\s*<div[^>]*>\s*<span class="phase-mod-badge">MOD 6</span>)', re.DOTALL)
m6_match = m6_pattern.search(html)
if m6_match:
    # Add id="sec-milestones-part2" or class
    html = html[:m6_match.start(1)] + '<div class="phase-module-item page-break-before-print" id="sec-milestones-part2"' + html[m6_match.start(1)+len('<div class="phase-module-item"'):]
    print("Added page-break to Module 6 for clean 2-page tranche split!")

# Define the Master Print CSS
master_print_css = """
    /* =========================================================================
       MASTER PRINT CSS: PRECISION MULTI-PAGE LANDSCAPE ARCHITECTURE (8 PAGES)
       ========================================================================= */
    @page {
      size: A4 landscape;
      margin: 6mm 8mm;
    }

    @media print {
      *, *:before, *:after {
        box-shadow: none !important;
        text-shadow: none !important;
      }
      
      /* Hide web navigation, action bars, and modal controls */
      .web-action-bar, .modal-overlay, .btn-sign, .mod-link-btn, #sigModal, .interactive-badge, .fa-arrow-left {
        display: none !important;
      }
      
      body {
        background: #ffffff !important;
        font-size: 8.5pt !important;
        color: #0f172a !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        margin: 0 !important;
        padding: 0 !important;
      }

      .container {
        max-width: 100% !important;
        width: 100% !important;
        margin: 0 auto !important;
        padding: 0 4px !important;
      }

      .doc-top-bar {
        padding: 6px 14px !important;
        border-bottom: 2px solid #d97706 !important;
        margin-bottom: 8px !important;
        background: #07192c !important;
        color: #ffffff !important;
      }
      .header-logos img {
        height: 26px !important;
      }
      .doc-meta-badge {
        padding: 3px 8px !important;
      }
      .doc-meta-badge .doc-ref {
        font-size: 10px !important;
      }
      .doc-meta-badge .doc-date {
        font-size: 8.5px !important;
      }

      h1, h2, h3, h4, .section-header, .section-title, .chart-box-title {
        page-break-after: avoid !important;
        break-after: avoid !important;
      }

      .section-card {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        padding: 10px 14px !important;
        margin-bottom: 10px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .section-header {
        margin-bottom: 10px !important;
        padding-bottom: 6px !important;
        border-bottom: 1.5px solid #e2e8f0 !important;
      }
      .section-title {
        font-size: 14px !important;
      }
      .section-subtitle {
        font-size: 9.5px !important;
        margin-top: 2px !important;
      }

      /* ---------------- PAGE 1: COVER / EXECUTIVE OVERVIEW & KPIS ---------------- */
      .hero-card {
        padding: 10px 14px !important;
        margin-bottom: 8px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border-radius: 6px !important;
      }
      .hero-badge-pill {
        font-size: 8.5px !important;
        padding: 2px 6px !important;
        margin-bottom: 4px !important;
      }
      .hero-title {
        font-size: 16px !important;
        margin-bottom: 3px !important;
      }
      .hero-subtitle {
        font-size: 9.5px !important;
        margin-bottom: 8px !important;
        line-height: 1.35 !important;
      }
      .hero-grid {
        margin-top: 6px !important;
        padding-top: 6px !important;
        gap: 6px !important;
      }
      .hero-stat-box {
        padding: 5px 8px !important;
      }
      .hero-stat-box .label {
        font-size: 8.5px !important;
      }
      .hero-stat-box .value {
        font-size: 13px !important;
      }
      .hero-stat-box .subvalue {
        font-size: 8.5px !important;
      }

      .stat-row {
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 8px !important;
        margin-bottom: 8px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .stat-card {
        padding: 8px 10px !important;
        gap: 8px !important;
        border-radius: 6px !important;
      }
      .stat-icon {
        width: 32px !important;
        height: 32px !important;
        font-size: 14px !important;
        border-radius: 6px !important;
      }
      .stat-info .stat-num {
        font-size: 14px !important;
      }
      .stat-info .stat-title {
        font-size: 9.5px !important;
      }
      .stat-info .stat-desc {
        font-size: 8px !important;
      }

      /* ---------------- PAGE 2: VISUAL ANALYTICS & CHARTS ---------------- */
      #sec-visual-analytics {
        page-break-before: always !important;
        break-before: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 0 !important;
      }
      .charts-grid {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 14px !important;
        margin-bottom: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .chart-box {
        padding: 8px 12px !important;
        border-radius: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        background: #f8fafc !important;
      }
      .chart-box-title {
        font-size: 12px !important;
        margin-bottom: 6px !important;
      }
      .chart-wrapper {
        height: 230px !important;
        position: relative !important;
      }

      /* ---------------- PAGE 3: MASTER 9-MODULE BUDGET MATRIX ---------------- */
      #sec-master-table {
        page-break-before: always !important;
        break-before: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 0 !important;
      }
      .table-container {
        overflow: visible !important;
        width: 100% !important;
        margin: 2px 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      table.master-table {
        width: 100% !important;
        min-width: 100% !important;
        font-size: 8pt !important;
        table-layout: auto !important;
        border-collapse: collapse !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      table.master-table th {
        padding: 4px 6px !important;
        font-size: 8pt !important;
        background: #0f172a !important;
        color: #ffffff !important;
      }
      table.master-table td {
        padding: 3.5px 5px !important;
        font-size: 7.5pt !important;
      }
      table.master-table tr {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }

      /* ---------------- PAGE 4: 9-MODULE ARCHITECTURAL SCOPE PILLARS ---------------- */
      #sec-scope-pillars {
        page-break-before: always !important;
        break-before: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 0 !important;
      }
      .modules-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .mod-card {
        padding: 6px 8px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border-radius: 6px !important;
      }
      .mod-card-top {
        margin-bottom: 3px !important;
      }
      .mod-badge {
        font-size: 8px !important;
        padding: 1px 4px !important;
      }
      .mod-cost {
        font-size: 10px !important;
      }
      .mod-title {
        font-size: 10px !important;
        margin-bottom: 2px !important;
      }
      .mod-desc {
        font-size: 7.5pt !important;
        line-height: 1.25 !important;
        margin-bottom: 4px !important;
      }
      .mod-features {
        gap: 2px !important;
      }
      .mod-features li {
        font-size: 7.5pt !important;
        line-height: 1.2 !important;
      }

      /* ---------------- PAGES 5 & 6: COMPLETE 35 MILESTONE TRANCHES ---------------- */
      #sec-detailed-milestones {
        page-break-before: always !important;
        break-before: page !important;
        page-break-inside: auto !important;
        break-inside: auto !important;
        margin-top: 0 !important;
      }
      #sec-milestones-part2 {
        page-break-before: always !important;
        break-before: page !important;
      }
      .phase-module-item {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-bottom: 6px !important;
        border-radius: 6px !important;
      }
      .phase-mod-header {
        padding: 5px 8px !important;
      }
      .phase-mod-title {
        font-size: 10px !important;
      }
      .phase-grid {
        padding: 5px 8px !important;
        gap: 6px !important;
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
      }
      .phase-item-box {
        padding: 4px 6px !important;
        border-radius: 4px !important;
      }
      .phase-item-top {
        margin-bottom: 2px !important;
      }
      .phase-item-tag {
        font-size: 7.5pt !important;
      }
      .phase-item-amt {
        font-size: 8.5pt !important;
      }
      .phase-item-desc {
        font-size: 7.5pt !important;
        line-height: 1.2 !important;
        margin-bottom: 3px !important;
      }
      .phase-item-time {
        font-size: 7pt !important;
      }

      /* ---------------- PAGE 7: TEAM RATE CARD & TOTAL INVESTMENT ---------------- */
      #sec-team-rate-card {
        page-break-before: always !important;
        break-before: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 0 !important;
      }
      .rate-card-grid {
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 8px !important;
        margin: 6px 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .rate-box {
        padding: 6px 8px !important;
        border-radius: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .rate-box .role-name {
        font-size: 10px !important;
        margin-bottom: 2px !important;
      }
      .rate-box .bhd-val {
        font-size: 13px !important;
      }
      .rate-box .bhd-sub {
        font-size: 8.5px !important;
      }

      #sec-total-investment {
        page-break-before: auto !important;
        break-before: auto !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 8px !important;
      }
      .total-cost-hero-box {
        padding: 8px 12px !important;
        margin: 6px 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border-radius: 6px !important;
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
      }
      .total-cost-title {
        font-size: 13px !important;
        margin-bottom: 2px !important;
      }
      .total-cost-desc {
        font-size: 9px !important;
        line-height: 1.3 !important;
      }
      .total-cost-amt {
        font-size: 20px !important;
      }
      .total-cost-words {
        font-size: 8.5px !important;
      }

      /* Terms & Governance */
      #sec-terms-governance {
        page-break-before: auto !important;
        break-before: auto !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 8px !important;
      }
      .terms-box {
        padding: 8px 12px !important;
        margin: 6px 0 !important;
        border-radius: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .terms-box h4 {
        font-size: 11px !important;
        margin-bottom: 3px !important;
      }
      .terms-box ul {
        font-size: 8.5pt !important;
        line-height: 1.35 !important;
        padding-left: 14px !important;
      }

      /* ---------------- PAGE 8: STAKEHOLDER SIGN-OFF CONSOLE ---------------- */
      #sec-signoff {
        page-break-before: always !important;
        break-before: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 0 !important;
        padding: 14px 18px !important;
      }
      .signoff-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 10px !important;
        margin-top: 10px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .signoff-card {
        padding: 10px 12px !important;
        border-radius: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .signoff-card-title {
        font-size: 11px !important;
      }
      .signoff-box-area {
        height: 65px !important;
        margin-bottom: 6px !important;
      }
      .signoff-status-badge {
        font-size: 8.5px !important;
        padding: 2px 5px !important;
        margin-bottom: 4px !important;
      }

      .doc-footer {
        margin-top: 10px !important;
        padding-top: 6px !important;
        font-size: 8pt !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
    }
"""

# Insert master_print_css right before </style>
style_close_idx = html.rfind('</style>')
if style_close_idx != -1:
    html = html[:style_close_idx] + master_print_css + "\n" + html[style_close_idx:]
    print("Inserted master_print_css at the end of <style>!")

with open('SL-POP-ERP-SUMMARY-001.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated SL-POP-ERP-SUMMARY-001.html")
