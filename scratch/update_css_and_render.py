import re
import os
import subprocess
import shutil
import fitz

# 1. Update SL-POP-ERP-SUMMARY-001.html with perfected landscape print CSS
with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure all section IDs are present
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

# Replace print CSS block with precision landscape pagination rules
print_css_start = html.find('@page {')
if print_css_start != -1:
    print_css_end = html.find('/* =========================================================================\n       COMPREHENSIVE MOBILE RESPONSIVE STYLING', print_css_start)
    if print_css_end == -1:
        print_css_end = html.find('/* =========================================================================', print_css_start)
    
    if print_css_end != -1:
        new_print_css = """@page {
      size: A4 landscape;
      margin: 6mm 8mm;
    }

    @media print {
      *, *:before, *:after {
        box-shadow: none !important;
        text-shadow: none !important;
      }
      .web-action-bar, .modal-overlay, .btn-sign, .mod-link-btn, #sigModal {
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
      .doc-top-bar {
        padding: 8px 16px !important;
        border-bottom: 2.5px solid #d97706 !important;
        margin-bottom: 8px !important;
      }
      .header-logos img {
        height: 28px !important;
      }
      .doc-meta-badge {
        padding: 4px 10px !important;
      }
      .doc-meta-badge .doc-ref {
        font-size: 11px !important;
      }
      .doc-meta-badge .doc-date {
        font-size: 9px !important;
      }
      .container {
        max-width: 100% !important;
        width: 100% !important;
        margin: 0 auto !important;
        padding: 0 4px !important;
      }
      
      h1, h2, h3, h4, .section-header, .section-title, .chart-box-title {
        page-break-after: avoid !important;
        break-after: avoid !important;
      }

      .section-card {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
        padding: 12px 14px !important;
        margin-bottom: 12px !important;
        page-break-inside: auto !important;
        break-inside: auto !important;
      }
      .section-header {
        margin-bottom: 12px !important;
        padding-bottom: 8px !important;
      }
      .section-title {
        font-size: 15px !important;
      }
      .section-subtitle {
        font-size: 10px !important;
        margin-top: 2px !important;
      }

      /* PAGE 1: Cover / Executive Overview & Stat Cards */
      .hero-card {
        padding: 12px 16px !important;
        margin-bottom: 10px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border-radius: 8px !important;
      }
      .hero-badge-pill {
        font-size: 9px !important;
        padding: 2px 8px !important;
        margin-bottom: 6px !important;
      }
      .hero-title {
        font-size: 17px !important;
        margin-bottom: 4px !important;
      }
      .hero-subtitle {
        font-size: 10px !important;
        margin-bottom: 10px !important;
        line-height: 1.4 !important;
      }
      .hero-grid {
        margin-top: 8px !important;
        padding-top: 8px !important;
        gap: 8px !important;
      }
      .hero-stat-box {
        padding: 6px 10px !important;
      }
      .hero-stat-box .label {
        font-size: 9px !important;
      }
      .hero-stat-box .value {
        font-size: 14px !important;
      }
      .hero-stat-box .subvalue {
        font-size: 9px !important;
      }
      .stat-row {
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 8px !important;
        margin-bottom: 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .stat-card {
        padding: 8px 10px !important;
        gap: 10px !important;
        border-radius: 6px !important;
      }
      .stat-icon {
        width: 36px !important;
        height: 36px !important;
        font-size: 15px !important;
        border-radius: 8px !important;
      }
      .stat-info .stat-num {
        font-size: 15px !important;
      }
      .stat-info .stat-title {
        font-size: 10px !important;
      }
      .stat-info .stat-desc {
        font-size: 8.5px !important;
      }

      /* PAGE 2: Visual Milestone & Budget Analytics */
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
        margin-bottom: 10px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .chart-box {
        padding: 10px 14px !important;
        border-radius: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .chart-box-title {
        font-size: 13px !important;
        margin-bottom: 8px !important;
      }
      .chart-wrapper {
        height: 270px !important;
        position: relative !important;
      }

      /* PAGE 3: Master 9-Module Budgeting Matrix Table */
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
        margin: 4px 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      table.master-table {
        width: 100% !important;
        min-width: 100% !important;
        font-size: 8.5pt !important;
        table-layout: auto !important;
        border-collapse: collapse !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      table.master-table th {
        padding: 5px 6px !important;
        font-size: 8.5pt !important;
      }
      table.master-table td {
        padding: 4px 6px !important;
        font-size: 8pt !important;
      }
      table.master-table tr {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }

      /* PAGE 4: 9-Module Architectural Scope & Deliverable Pillars */
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
        gap: 8px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .mod-card {
        padding: 8px 10px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border-radius: 6px !important;
      }
      .mod-card-top {
        margin-bottom: 4px !important;
      }
      .mod-badge {
        font-size: 8.5px !important;
        padding: 1px 5px !important;
      }
      .mod-cost {
        font-size: 11px !important;
      }
      .mod-title {
        font-size: 11px !important;
        margin-bottom: 4px !important;
      }
      .mod-desc {
        font-size: 8.5px !important;
        line-height: 1.3 !important;
        margin-bottom: 6px !important;
      }
      .mod-features {
        gap: 3px !important;
      }
      .mod-features li {
        font-size: 8px !important;
        line-height: 1.25 !important;
      }

      /* Detailed 35 Milestone Tranches */
      #sec-detailed-milestones {
        page-break-before: always !important;
        break-before: page !important;
        margin-top: 0 !important;
      }
      .phase-module-item {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-bottom: 8px !important;
        border-radius: 6px !important;
      }
      .phase-mod-header {
        padding: 6px 10px !important;
      }
      .phase-grid {
        padding: 6px 10px !important;
        gap: 8px !important;
      }
      .phase-item-box {
        padding: 6px 8px !important;
      }
      .phase-item-top {
        margin-bottom: 3px !important;
      }
      .phase-item-tag {
        font-size: 8.5px !important;
      }
      .phase-item-amt {
        font-size: 9.5px !important;
      }
      .phase-item-desc {
        font-size: 8.5px !important;
        line-height: 1.25 !important;
        margin-bottom: 4px !important;
      }
      .phase-item-time {
        font-size: 8px !important;
      }

      /* Engineering Rate Matrix & Total Cost */
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
        margin: 8px 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .rate-box {
        padding: 8px 10px !important;
        border-radius: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .rate-box .role-name {
        font-size: 11px !important;
        margin-bottom: 4px !important;
      }
      .rate-box .bhd-val {
        font-size: 14px !important;
      }
      .rate-box .bhd-sub {
        font-size: 9px !important;
      }

      #sec-total-investment {
        page-break-before: auto !important;
        break-before: auto !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 10px !important;
      }
      .total-cost-hero-box {
        padding: 10px 14px !important;
        margin: 8px 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        border-radius: 8px !important;
      }
      .total-cost-title {
        font-size: 14px !important;
        margin-bottom: 3px !important;
      }
      .total-cost-desc {
        font-size: 10px !important;
        line-height: 1.35 !important;
      }
      .total-cost-amt {
        font-size: 24px !important;
      }
      .total-cost-words {
        font-size: 9px !important;
      }

      /* Terms & Governance */
      #sec-terms-governance {
        page-break-before: always !important;
        break-before: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 0 !important;
      }
      .terms-box {
        padding: 10px 14px !important;
        margin: 8px 0 !important;
        border-radius: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .terms-box h4 {
        font-size: 12px !important;
        margin-bottom: 4px !important;
      }
      .terms-box ul {
        font-size: 9.5px !important;
        line-height: 1.45 !important;
        padding-left: 16px !important;
      }

      /* Sign-Off Console */
      #sec-signoff {
        page-break-before: always !important;
        break-before: page !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        margin-top: 0 !important;
        padding: 16px 20px !important;
      }
      .signoff-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 12px !important;
        margin-top: 12px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .signoff-card {
        padding: 12px 14px !important;
        border-radius: 6px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .signoff-card-title {
        font-size: 12px !important;
      }
      .signoff-box-area {
        height: 70px !important;
        margin-bottom: 8px !important;
      }
      .signoff-status-badge {
        font-size: 9px !important;
        padding: 2px 6px !important;
        margin-bottom: 6px !important;
      }

      .doc-footer {
        margin-top: 14px !important;
        padding-top: 8px !important;
        font-size: 8.5px !important;
      }
    }
    """
        html = html[:print_css_start] + new_print_css + html[print_css_end:]
        print("Updated print CSS successfully!")

with open('SL-POP-ERP-SUMMARY-001.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved SL-POP-ERP-SUMMARY-001.html")
