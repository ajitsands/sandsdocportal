import base64
import subprocess
import os
import fitz

def get_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

logo_sands_white = get_b64('logos/SaNDSLab-LogoNewUpdatedWhite.png')
logo_sands_color = get_b64('logos/SaNDSLab-LogoNewUpdated copy.png')
logo_uniglobal_white = get_b64('logos/UniGlobalWhite.png')
logo_uniglobal_color = get_b64('logos/UNIGLOBAL_CONSULTANCY_LOGO_FINAL.png')
logo_popular = get_b64('logos/logoPopular.png')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Project Milestone & Payment Structure - PCode Generation Module</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #0a2540;
      --primary-light: #18446e;
      --accent: #e67e22;
      --accent-dark: #d35400;
      --secondary: #0e7490;
      --dark: #0f172a;
      --gray-900: #1e293b;
      --gray-700: #334155;
      --gray-600: #475569;
      --gray-500: #64748b;
      --gray-300: #cbd5e1;
      --gray-200: #e2e8f0;
      --gray-100: #f1f5f9;
      --gray-50: #f8fafc;
      --white: #ffffff;
      --success: #15803d;
      --success-bg: #dcfce7;
      --danger: #b91c1c;
      --danger-bg: #fef2f2;
      --info: #0369a1;
      --info-bg: #e0f2fe;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #f1f5f9;
      color: var(--gray-700);
      line-height: 1.55;
      font-size: 13px;
      -webkit-font-smoothing: antialiased;
    }}

    .document-container {{
      max-width: 1040px;
      margin: 25px auto;
      background: var(--white);
      box-shadow: 0 10px 30px rgba(0,0,0,0.08);
      border-radius: 8px;
      overflow: hidden;
    }}

    /* Cover / Header Banner */
    .doc-header {{
      background: linear-gradient(135deg, #07192c 0%, #0a2540 50%, #153e67 100%);
      color: var(--white);
      padding: 30px 45px 25px;
      position: relative;
      border-bottom: 4px solid var(--accent);
    }}

    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      border-bottom: 1px solid rgba(255,255,255,0.15);
      padding-bottom: 18px;
    }}

    .org-brand {{
      display: flex;
      flex-direction: column;
      max-width: 360px;
    }}

    .header-logo-img {{
      max-height: 48px;
      width: auto;
      object-fit: contain;
      display: block;
      margin-bottom: 6px;
    }}

    .org-tagline {{
      font-size: 10px;
      color: rgba(255,255,255,0.75);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      line-height: 1.3;
    }}

    .header-partners {{
      display: flex;
      align-items: center;
      gap: 15px;
    }}

    .partner-badge-box {{
      background: rgba(255,255,255,0.08);
      padding: 8px 14px;
      border-radius: 6px;
      border: 1px solid rgba(255,255,255,0.14);
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 140px;
    }}

    .partner-label {{
      font-size: 9px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #f39c12;
      font-weight: 700;
      margin-bottom: 4px;
    }}

    .partner-logo-img {{
      max-height: 32px;
      max-width: 130px;
      width: auto;
      object-fit: contain;
    }}

    .partner-logo-white-box {{
      background: #ffffff;
      padding: 3px 8px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .doc-title-section {{
      margin-top: 10px;
    }}

    .doc-badge {{
      display: inline-block;
      background: var(--accent);
      color: #ffffff;
      font-size: 10.5px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 15px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 10px;
    }}

    .doc-main-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 26px;
      font-weight: 800;
      line-height: 1.25;
      color: #ffffff;
      margin-bottom: 6px;
    }}

    .doc-subtitle {{
      font-size: 13.5px;
      color: rgba(255,255,255,0.88);
      font-weight: 400;
      max-width: 850px;
    }}

    .doc-meta-bar {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 15px;
      margin-top: 20px;
      background: rgba(0,0,0,0.3);
      padding: 10px 18px;
      border-radius: 6px;
      font-size: 11px;
    }}

    .meta-item {{
      display: flex;
      flex-direction: column;
    }}

    .meta-title {{
      color: rgba(255,255,255,0.6);
      font-size: 9.5px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 700;
    }}

    .meta-val {{
      color: #ffffff;
      font-weight: 600;
      margin-top: 2px;
    }}

    /* Document Body Content */
    .doc-content {{
      padding: 35px 45px 45px;
    }}

    .section-block {{
      margin-bottom: 32px;
    }}

    .section-title-wrap {{
      display: flex;
      align-items: center;
      margin-bottom: 14px;
      border-bottom: 2px solid var(--gray-200);
      padding-bottom: 8px;
    }}

    .section-num {{
      background: var(--primary);
      color: var(--white);
      font-family: 'Outfit', sans-serif;
      font-size: 12px;
      font-weight: 700;
      width: 26px;
      height: 26px;
      border-radius: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 10px;
      flex-shrink: 0;
    }}

    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 17px;
      font-weight: 700;
      color: var(--primary);
      letter-spacing: -0.2px;
    }}

    p {{
      margin-bottom: 10px;
      color: var(--gray-700);
      text-align: justify;
    }}

    /* Grids */
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
      margin-top: 12px;
    }}

    .grid-3 {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-top: 12px;
    }}

    .card {{
      background: var(--gray-50);
      border: 1px solid var(--gray-200);
      border-radius: 6px;
      padding: 14px 16px;
    }}

    .card-primary {{
      border-left: 3.5px solid var(--primary);
    }}

    .card-accent {{
      border-left: 3.5px solid var(--accent);
    }}

    .card-secondary {{
      border-left: 3.5px solid var(--secondary);
    }}

    .card-danger {{
      border-left: 3.5px solid var(--danger);
      background: #fffafa;
    }}

    .card-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 13px;
      font-weight: 700;
      color: var(--dark);
      margin-bottom: 5px;
    }}

    .card-text {{
      font-size: 11.5px;
      color: var(--gray-600);
      line-height: 1.45;
    }}

    /* Roadmap Box */
    .roadmap-container {{
      background: linear-gradient(to right, #f8fafc, #f1f5f9);
      border: 1px solid var(--gray-200);
      border-radius: 6px;
      padding: 16px;
      margin-top: 12px;
    }}

    .roadmap-list {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-top: 10px;
    }}

    .roadmap-item {{
      background: var(--white);
      border: 1px solid var(--gray-200);
      border-radius: 5px;
      padding: 8px 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .roadmap-item.active {{
      border: 1.5px solid var(--accent);
      background: #fffbeb;
    }}

    .rm-badge {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      background: var(--gray-200);
      color: var(--gray-700);
    }}

    .roadmap-item.active .rm-badge {{
      background: var(--accent);
      color: var(--white);
    }}

    .rm-name {{
      font-size: 11.5px;
      font-weight: 600;
      color: var(--dark);
    }}

    /* Tables */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      margin-bottom: 15px;
      font-size: 11.5px;
    }}

    th {{
      background: var(--primary);
      color: var(--white);
      font-family: 'Outfit', sans-serif;
      font-weight: 600;
      text-align: left;
      padding: 9px 12px;
      letter-spacing: 0.3px;
    }}

    td {{
      padding: 8px 12px;
      border-bottom: 1px solid var(--gray-200);
      color: var(--gray-700);
      vertical-align: top;
    }}

    tr:nth-child(even) td {{
      background-color: #fafbfc;
    }}

    .table-subheading {{
      background: #e2e8f0 !important;
      font-weight: 700;
      color: var(--dark);
    }}

    /* Badges */
    .badge {{
      display: inline-block;
      padding: 2px 7px;
      border-radius: 3px;
      font-size: 10px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}

    .badge-primary {{ background: #e0f2fe; color: #0369a1; }}
    .badge-success {{ background: #dcfce7; color: #15803d; }}
    .badge-warning {{ background: #fef3c7; color: #b45309; }}
    .badge-purple {{ background: #f3e8ff; color: #7e22ce; }}
    .badge-accent {{ background: #ffedd5; color: #c2410c; }}
    .badge-danger {{ background: #fee2e2; color: #b91c1c; }}

    /* Milestone Detailed Box */
    .milestone-card {{
      border: 1px solid var(--gray-200);
      border-radius: 6px;
      margin-bottom: 18px;
      overflow: hidden;
    }}

    .milestone-header {{
      background: #f8fafc;
      border-bottom: 1px solid var(--gray-200);
      padding: 10px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .milestone-left {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .ms-tag {{
      background: var(--primary);
      color: var(--white);
      font-family: 'Outfit', sans-serif;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
    }}

    .ms-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 13.5px;
      font-weight: 700;
      color: var(--dark);
    }}

    .milestone-right {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .ms-duration {{
      font-size: 11px;
      font-weight: 600;
      color: var(--gray-600);
      background: var(--white);
      border: 1px solid var(--gray-200);
      padding: 3px 8px;
      border-radius: 4px;
    }}

    .ms-payment-badge {{
      background: #ecfdf5;
      color: #047857;
      border: 1px solid #a7f3d0;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 4px;
    }}

    .milestone-body {{
      padding: 14px 16px;
      background: var(--white);
    }}

    .ms-detail-grid {{
      display: grid;
      grid-template-columns: 1.8fr 1fr;
      gap: 16px;
    }}

    .ms-subheading {{
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      font-weight: 700;
      color: var(--gray-500);
      margin-bottom: 6px;
    }}

    .feature-list {{
      list-style-type: none;
    }}

    .feature-list li {{
      position: relative;
      padding-left: 14px;
      margin-bottom: 5px;
      font-size: 11.5px;
      color: var(--gray-700);
    }}

    .feature-list li::before {{
      content: "-";
      position: absolute;
      left: 0;
      color: var(--accent);
      font-weight: bold;
    }}

    .team-badge-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-top: 4px;
    }}

    .team-pill {{
      font-size: 10.5px;
      background: var(--gray-100);
      border: 1px solid var(--gray-200);
      padding: 2px 7px;
      border-radius: 3px;
      color: var(--gray-700);
      font-weight: 500;
    }}

    .signoff-box {{
      background: #f8fafc;
      border-left: 3px solid var(--secondary);
      padding: 8px 12px;
      margin-top: 10px;
      border-radius: 0 4px 4px 0;
      font-size: 11px;
    }}

    .signoff-title {{
      font-weight: 700;
      color: var(--secondary);
      margin-bottom: 2px;
    }}

    .payment-total-row {{
      background: #0a2540 !important;
      color: #ffffff !important;
      font-weight: 700;
      font-size: 12px;
    }}

    .payment-total-row td {{
      color: #ffffff !important;
      border-bottom: none;
    }}

    .contract-grand-total-row {{
      background: #1e3a5f !important;
      color: #ffffff !important;
      font-weight: 700;
      font-size: 12px;
    }}

    .contract-grand-total-row td {{
      color: #ffffff !important;
      border-bottom: none;
    }}

    .advance-summary-row {{
      background: #fffbeb !important;
      color: #b45309 !important;
      font-weight: 700;
    }}

    /* Litigation Clause Box */
    .litigation-box {{
      background: #fffbfb;
      border: 1.5px solid #fca5a5;
      border-radius: 6px;
      padding: 16px 18px;
      margin-top: 15px;
    }}

    /* Approval Grid */
    .approval-container {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 15px;
      margin-top: 20px;
    }}

    .approval-box {{
      background: var(--white);
      border: 1px solid var(--gray-200);
      border-radius: 6px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .approval-header {{
      border-bottom: 1px solid var(--gray-200);
      padding-bottom: 10px;
      margin-bottom: 10px;
    }}

    .approval-logo-wrap {{
      min-height: 40px;
      display: flex;
      align-items: center;
      margin-bottom: 8px;
    }}

    .approval-logo-img {{
      max-height: 36px;
      max-width: 140px;
      width: auto;
      object-fit: contain;
    }}

    .approval-role {{
      font-size: 9.5px;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.8px;
      color: var(--accent-dark);
    }}

    .approval-org {{
      font-family: 'Outfit', sans-serif;
      font-size: 12px;
      font-weight: 700;
      color: var(--dark);
      margin-top: 2px;
    }}

    .sig-line {{
      margin-top: 30px;
      border-top: 1px dashed var(--gray-300);
      padding-top: 6px;
      font-size: 10.5px;
      color: var(--gray-500);
    }}

    .sig-field {{
      margin-bottom: 5px;
      font-size: 11px;
    }}

    .sig-field span {{
      font-weight: 600;
      color: var(--dark);
    }}

    /* Numeric tabular styling */
    .num-col {{
      text-align: right;
      font-variant-numeric: tabular-nums;
      white-space: nowrap;
    }}

    /* Footer */
    .doc-footer {{
      background: var(--gray-50);
      border-top: 1px solid var(--gray-200);
      padding: 16px 45px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10.5px;
      color: var(--gray-500);
    }}

    /* Web Action Header (Visible on Web, Hidden on Print) */
    .web-action-bar {{
      position: sticky;
      top: 0;
      z-index: 9999;
      background: #07192c;
      border-bottom: 2px solid var(--accent);
      padding: 10px 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}

    .web-action-left {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .portal-branding {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .portal-logo {{
      height: 24px;
      width: auto;
    }}

    .portal-tag {{
      font-size: 11px;
      font-weight: 700;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .doc-ref-pill {{
      background: rgba(230, 126, 34, 0.2);
      border: 1px solid #e67e22;
      color: #ffedd5;
      font-size: 11.5px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 4px;
      font-family: 'Outfit', sans-serif;
    }}

    .web-action-right {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .btn-web-action {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: 'Inter', sans-serif;
      font-size: 12px;
      font-weight: 600;
      padding: 7px 14px;
      border-radius: 5px;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      border: none;
    }}

    .btn-pdf-download {{
      background: #e67e22;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(230,126,34,0.35);
    }}

    .btn-pdf-download:hover {{
      background: #d35400;
      transform: translateY(-1px);
    }}

    .btn-print {{
      background: rgba(255,255,255,0.12);
      color: #ffffff;
      border: 1px solid rgba(255,255,255,0.2);
    }}

    .btn-print:hover {{
      background: rgba(255,255,255,0.2);
    }}

    .btn-hub {{
      background: transparent;
      color: #cbd5e1;
      border: 1px solid rgba(255,255,255,0.15);
    }}

    /* ==================== MOBILE RESPONSIVE DESIGN ==================== */
    @media screen and (max-width: 900px) {{
      body {{
        padding: 0;
        margin: 0;
      }}

      .document-container {{
        margin: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        max-width: 100% !important;
        width: 100% !important;
      }}

      .doc-header {{
        padding: 24px 20px 20px;
      }}

      .header-top {{
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
      }}

      .header-partners {{
        width: 100%;
        justify-content: flex-start;
        flex-wrap: wrap;
        gap: 10px;
      }}

      .doc-meta-bar {{
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
      }}

      .roadmap-list {{
        grid-template-columns: 1fr 1fr;
        gap: 8px;
      }}

      .doc-content {{
        padding: 24px 18px;
      }}

      .grid-3 {{
        grid-template-columns: 1fr !important;
        gap: 12px !important;
      }}

      .grid-2 {{
        grid-template-columns: 1fr !important;
        gap: 12px !important;
      }}

      .ms-detail-grid {{
        grid-template-columns: 1fr !important;
        gap: 14px !important;
      }}

      .approval-container {{
        grid-template-columns: 1fr !important;
        gap: 15px !important;
      }}

      .web-action-bar {{
        padding: 10px 16px;
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
      }}

      .web-action-left {{
        justify-content: space-between;
      }}

      .web-action-right {{
        display: grid;
        grid-template-columns: 1fr auto auto;
        gap: 8px;
      }}

      .btn-web-action {{
        justify-content: center;
        padding: 10px 12px;
        font-size: 12px;
        min-height: 40px;
      }}
    }}

    @media screen and (max-width: 600px) {{
      .doc-main-title {{
        font-size: 20px;
        line-height: 1.3;
      }}

      .doc-subtitle {{
        font-size: 12.5px;
        line-height: 1.5;
      }}

      .doc-meta-bar {{
        grid-template-columns: 1fr;
        gap: 8px;
        padding: 10px 14px;
      }}

      .roadmap-list {{
        grid-template-columns: 1fr;
        gap: 6px;
      }}

      .milestone-header {{
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
      }}

      .milestone-right {{
        width: 100%;
        justify-content: space-between;
      }}

      .web-action-right {{
        grid-template-columns: 1fr 1fr;
      }}

      .btn-pdf-download {{
        grid-column: span 2;
        min-height: 44px;
        font-size: 13px;
      }}

      table {{
        font-size: 11px;
        display: block;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        width: 100%;
      }}

      th, td {{
        padding: 6px 8px;
        white-space: normal;
      }}

      .num-col {{
        white-space: nowrap;
      }}

      .doc-footer {{
        flex-direction: column;
        text-align: center;
        gap: 8px;
        padding: 18px 15px;
      }}
    }}

    /* Print Formatting */
    @media print {{
      .web-action-bar {{
        display: none !important;
      }}

      body {{
        background-color: #ffffff;
      }}

      .document-container {{
        max-width: 100%;
        margin: 0;
        box-shadow: none;
        border-radius: 0;
      }}

      .doc-header {{
        padding: 20px 25px 15px;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }}

      .doc-content {{
        padding: 20px 25px;
      }}

      .page-break {{
        page-break-before: always;
      }}

      .avoid-break {{
        page-break-inside: avoid;
      }}

      th, .ms-tag, .badge, .partner-badge-box, .roadmap-item.active, .card-primary, .card-accent, .card-secondary, .card-danger, .payment-total-row, .contract-grand-total-row, .advance-summary-row {{
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }}
    }}

    @page {{
      size: A4 portrait;
      margin: 10mm 10mm 10mm 10mm;
    }}
  </style>
</head>
<body>

<!-- ==================== WEB PORTAL TOP ACTION BAR ==================== -->
<div class="web-action-bar">
  <div class="web-action-left">
    <div class="portal-branding">
      <img class="portal-logo" src="{logo_sands_white}" alt="SaNDS Lab" />
      <span class="portal-tag">Client Document Portal</span>
    </div>
    <span class="doc-ref-pill">Ref: SL-POP-ERP-MS-001</span>
  </div>
  <div class="web-action-right">
    <a href="SL-POP-ERP-MS-001.pdf" download="SL-POP-ERP-MS-001_PCode_Milestone_Structure.pdf" class="btn-web-action btn-pdf-download" id="downloadPdfBtn">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
      Download Official PDF
    </a>
    <button onclick="window.print()" class="btn-web-action btn-print">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
      Print
    </button>
    <a href="/popular" class="btn-web-action btn-hub">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
      Document Hub
    </a>
  </div>
</div>

<div class="document-container">

  <!-- ==================== HEADER BANNER WITH EMBEDDED LOGOS ==================== -->
  <header class="doc-header">
    <div class="header-top">
      <div class="org-brand">
        <img class="header-logo-img" src="{logo_sands_white}" alt="SaNDS Lab Middle East W.L.L" />
        <div class="org-tagline">Software & Network Development Solutions Lab Middle East W.L.L</div>
      </div>
      <div class="header-partners">
        <!-- Consultant Badge -->
        <div class="partner-badge-box">
          <div class="partner-label">Consultant & Architect</div>
          <img class="partner-logo-img" src="{logo_uniglobal_white}" alt="UniGlobal Consultancy" />
        </div>
        <!-- Client Badge -->
        <div class="partner-badge-box">
          <div class="partner-label">Client Representative</div>
          <div class="partner-logo-white-box">
            <img class="partner-logo-img" src="{logo_popular}" alt="Popular Auto Spare & A/C Parts Co. W.L.L" />
          </div>
        </div>
      </div>
    </div>

    <div class="doc-title-section">
      <div class="doc-badge">Technical & Commercial Proposal • Milestone Delivery Plan</div>
      <h1 class="doc-main-title">Project Milestone & Payment Structure</h1>
      <p class="doc-subtitle">
        Implementation Roadmap for <strong>Module 1: PCode Generation & Centralized Inventory Management Framework</strong> — The Operational Backbone of the Enterprise Cloud ERP System.
      </p>
    </div>

    <div class="doc-meta-bar">
      <div class="meta-item">
        <span class="meta-title">Document Reference</span>
        <span class="meta-val">SL-POP-ERP-MS-001</span>
      </div>
      <div class="meta-item">
        <span class="meta-title">BA Document Ref</span>
        <span class="meta-val">DOC-001 (Ver 1.0)</span>
      </div>
      <div class="meta-item">
        <span class="meta-title">Date of Submission</span>
        <span class="meta-val">21-September-2026</span>
      </div>
      <div class="meta-item">
        <span class="meta-title">Execution Timeline</span>
        <span class="meta-val">10 Working Weeks (50 Working Days)</span>
      </div>
    </div>
  </header>

  <!-- ==================== MAIN CONTENT ==================== -->
  <main class="doc-content">

    <!-- SECTION 1: EXECUTIVE SUMMARY & MASTER ROADMAP -->
    <section class="section-block">
      <div class="section-title-wrap">
        <div class="section-num">01</div>
        <h2 class="section-title">Executive Summary & Master ERP Context</h2>
      </div>
      
      <p>
        Following the formal submission and review of the Business Analysis Document (<strong>DOC-001 Ver 1.0</strong>), <strong>SaNDS Lab Middle East W.L.L</strong> is pleased to submit this comprehensive Project Milestone and Payment Structure Document.
      </p>
      <p>
        Popular Auto Spare & A/C Parts Co. W.L.L operates a distributed multi-branch footprint across the Kingdom of Bahrain (6 branches) and UAE (Dubai wholesale hub). The transition from fragmented spreadsheets and legacy BUSY ERP to a unified, multi-company Cloud ERP requires a phased, transparent delivery strategy.
      </p>

      <div class="roadmap-container">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <h4 style="font-family:'Outfit',sans-serif; color:var(--dark); font-size:13px;">Master ERP Transformation Architecture (9 Core Process Modules)</h4>
          <span class="badge badge-accent">Current Scope: Module 01</span>
        </div>
        <div class="roadmap-list">
          <div class="roadmap-item active">
            <span class="rm-badge">01</span>
            <span class="rm-name">PCode Gen & Item Master</span>
          </div>
          <div class="roadmap-item">
            <span class="rm-badge">02</span>
            <span class="rm-name">Vendor & Purchase Flow</span>
          </div>
          <div class="roadmap-item">
            <span class="rm-badge">03</span>
            <span class="rm-name">Stock Transfer & Verification</span>
          </div>
          <div class="roadmap-item">
            <span class="rm-badge">04</span>
            <span class="rm-name">Sales</span>
          </div>
          <div class="roadmap-item">
            <span class="rm-badge">05</span>
            <span class="rm-name">Finance, Tax & VAT Accounting</span>
          </div>
          <div class="roadmap-item">
            <span class="rm-badge">06</span>
            <span class="rm-name">Administration</span>
          </div>
          <div class="roadmap-item">
            <span class="rm-badge">07</span>
            <span class="rm-name">HRMS & Payroll Management</span>
          </div>
          <div class="roadmap-item">
            <span class="rm-badge">08</span>
            <span class="rm-name">Hardware Integration & Server Setup</span>
          </div>
          <div class="roadmap-item">
            <span class="rm-badge">09</span>
            <span class="rm-name">Executive BI & Mobile Analytics</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 2: SCOPE OF WORK (MODULE 1) -->
    <section class="section-block avoid-break">
      <div class="section-title-wrap">
        <div class="section-num">02</div>
        <h2 class="section-title">Module 1: Functional Scope & Architecture Breakdown</h2>
      </div>

      <p>
        The <strong>PCode Generation & Inventory Master Module</strong> serves as the technological core of the entire ERP suite. It governs how parts are onboarded, verified, secured, priced, and substituted across all branches.
      </p>

      <div class="grid-3">
        <div class="card card-primary">
          <div class="card-title">1. Multi-Company & Branch Matrix</div>
          <div class="card-text">Creation of company entities, country assignments (Bahrain/Dubai), base currency configs (BHD/AED), VAT parameters, and branch categorization (Stores vs Outlets).</div>
        </div>
        <div class="card card-primary">
          <div class="card-title">2. Sequential PCode FIFO Engine</div>
          <div class="card-text">Automated, collision-proof sequence generation, real-time uniqueness validation, item-wise save states (Red=Unsaved, Green=Saved), and permanent lock upon CTO approval.</div>
        </div>
        <div class="card card-primary">
          <div class="card-title">3. Comprehensive Item Master</div>
          <div class="card-text">20+ core attributes including multi-OEM cross-indexing, manufacturer part numbers, vehicle compatibility, engine CC/specs, multi-image assets, and tax-inclusive pricing.</div>
        </div>

        <div class="card card-accent">
          <div class="card-title">4. Dual Approval Workflows</div>
          <div class="card-text">Structured approval pipelines for: (a) Sales Counter Request via Branch Purchase Manager (BPM) &rarr; CTO; and (b) Vendor Receiving variance via Store Purchase Manager (SPM) &rarr; CTO.</div>
        </div>
        <div class="card card-accent">
          <div class="card-title">5. Non-PCode Exception Holding</div>
          <div class="card-text">Dedicated holding buffer for emergency customer orders, linked to pending CTO review dashboard with automated sequential migration upon formal approval.</div>
        </div>
        <div class="card card-accent">
          <div class="card-title">6. Centralized Pricing Hub</div>
          <div class="card-text">Single-window country-wise price updates, automated exchange rate calculations, bulk updating, role-based modification locks, and audit history versioning.</div>
        </div>

        <div class="card card-secondary">
          <div class="card-title">7. Minimum Order Level & Alerts</div>
          <div class="card-text">Branch/store-specific safety stock thresholds, automatic low-stock trigger engine, and consolidated executive review portal for Purchase Team and CTO.</div>
        </div>
        <div class="card card-secondary">
          <div class="card-title">8. Substitute & Mapping Intelligence</div>
          <div class="card-text">Automated OEM compatibility engine, multi-brand alternative suggestions, cross-tier price recommendations, and confidential trade-secret protection.</div>
        </div>
        <div class="card card-secondary">
          <div class="card-title">9. Catalog Sync & Sales Alerts</div>
          <div class="card-text">PartSouq catalogue integration (API/Sandbox), item handling precautionary sales pop-ups (sticker/box removal), legacy PCode archiving, and CTO analytics audit screen.</div>
        </div>
      </div>
    </section>

    <div class="page-break"></div>

    <!-- SECTION 3: PROJECT TEAM STRUCTURE & RESOURCE ALLOCATION -->
    <section class="section-block avoid-break">
      <div class="section-title-wrap">
        <div class="section-num">03</div>
        <h2 class="section-title">Project Team Structure & Resource Allocation Matrix</h2>
      </div>

      <p>
        To guarantee timely execution, highest engineering quality, and seamless business alignment, SaNDS Lab Middle East W.L.L will deploy a dedicated multi-disciplinary delivery team consisting of experienced Project Managers, Software Architects, Senior Developers, and Quality Assurance Specialists.
      </p>

      <table>
        <thead>
          <tr>
            <th style="width: 24%;">Role</th>
            <th style="width: 30%;">Key Responsibilities</th>
            <th style="width: 16%;">Allocated Team</th>
            <th style="width: 15%;">Total Effort</th>
            <th style="width: 15%;">Focus Area</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Project Manager (PM) & BA</strong></td>
            <td>Sprint governance, milestone tracking, client communication, UAT coordination, requirement sign-off.</td>
            <td><span class="badge badge-primary">1 Lead PM</span></td>
            <td>160 Hours (10 Wks)</td>
            <td>Governance & Delivery Control</td>
          </tr>
          <tr>
            <td><strong>Back end Lead Eng</strong></td>
            <td>REST API development, database schemas, PCode sequential engine, approval workflows, caching, audit trails.</td>
            <td><span class="badge badge-purple">1 Senior Backend Dev</span></td>
            <td>280 Hours (10 Wks)</td>
            <td>Core Business Logic & APIs</td>
          </tr>
          <tr>
            <td><strong>Front End Lead Eng</strong></td>
            <td>Responsive UI/UX design, real-time validation grids, Item Master interface, CTO approval dashboard, sales alerts.</td>
            <td><span class="badge badge-purple">1 Senior Frontend Dev</span></td>
            <td>240 Hours (10 Wks)</td>
            <td>User Experience & Rapid Entry</td>
          </tr>
          <tr>
            <td><strong>Database and Cloud (DevOps)</strong></td>
            <td>Multi-tenant DB clustering, backup automation, PartSouq API connector, CI/CD pipelines, security hardening.</td>
            <td><span class="badge badge-accent">1 DevOps Specialist</span></td>
            <td>120 Hours (10 Wks)</td>
            <td>Cloud Infra & Data Security</td>
          </tr>
          <tr>
            <td><strong>QA (Testing & Verification)</strong></td>
            <td>Functional test suite, edge-case validation, concurrency tests on PCode generation, security audit, UAT scripts.</td>
            <td><span class="badge badge-success">1 QA Lead / Tester</span></td>
            <td>180 Hours (10 Wks)</td>
            <td>Defect Zero & Rigorous QA</td>
          </tr>
          <tr class="table-subheading">
            <td colspan="3"><strong>Total Dedicated Engineering & Governance Effort</strong></td>
            <td colspan="2"><strong>980 Person-Hours (10 Calendar Weeks)</strong></td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- SECTION 4: DETAILED MILESTONES -->
    <section class="section-block">
      <div class="section-title-wrap">
        <div class="section-num">04</div>
        <h2 class="section-title">Detailed Milestone Breakdown & Deliverables</h2>
      </div>

      <p>
        The implementation of Module 1 is structured into <strong>six (6) clear, verifiable milestones</strong> spanning 10 working weeks (50 active business working days, excluding Bahrain weekends and official public holidays). Each milestone culminates in demonstrable software artifacts, client reviews, and formalized sign-off criteria.
      </p>

      <!-- MILESTONE 1 -->
      <div class="milestone-card avoid-break">
        <div class="milestone-header">
          <div class="milestone-left">
            <span class="ms-tag">MILESTONE 01</span>
            <span class="ms-title">Architecture, Multi-Company Setup & Core Security Framework</span>
          </div>
          <div class="milestone-right">
            <span class="ms-duration">Weeks 1 – 2 (10 Working Days)</span>
            <span class="ms-payment-badge">20% • BD 681.818</span>
          </div>
        </div>
        <div class="milestone-body">
          <div class="ms-detail-grid">
            <div>
              <div class="ms-subheading">Technical Deliverables & Key Tasks</div>
              <ul class="feature-list">
                <li>Cloud infrastructure provisioning (AWS/Azure) with high-availability database cluster and staging environment.</li>
                <li>Database Schema Design for Multi-Company (Bahrain HO, Dubai branch) and Branch Outlets/Stores.</li>
                <li>Base currency (BHD, AED, USD) exchange matrix and country-specific VAT/tax structure definition.</li>
                <li>Role-Based Access Control (RBAC) engine establishing permissions for CTO, BPM, SPM, Sales, and Accounts.</li>
                <li>Comprehensive Master Data dictionary & API Swagger documentation baseline.</li>
              </ul>
            </div>
            <div>
              <div class="ms-subheading">Assigned Team</div>
              <div class="team-badge-list">
                <span class="team-pill">Project Manager</span>
                <span class="team-pill">Lead Backend Dev</span>
                <span class="team-pill">DevOps Specialist</span>
                <span class="team-pill">QA Engineer</span>
              </div>
              <div class="signoff-box">
                <div class="signoff-title">Milestone Sign-off Criteria</div>
                Working cloud staging environment, verified multi-branch database hierarchy, authenticated login with role permissions demonstrated to client.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- MILESTONE 2 -->
      <div class="milestone-card avoid-break">
        <div class="milestone-header">
          <div class="milestone-left">
            <span class="ms-tag">MILESTONE 02</span>
            <span class="ms-title">PCode Sequential Engine, Item Master & Non-PCode Holding System</span>
          </div>
          <div class="milestone-right">
            <span class="ms-duration">Weeks 3 – 4 (10 Working Days)</span>
            <span class="ms-payment-badge">20% • BD 681.818</span>
          </div>
        </div>
        <div class="milestone-body">
          <div class="ms-detail-grid">
            <div>
              <div class="ms-subheading">Technical Deliverables & Key Tasks</div>
              <ul class="feature-list">
                <li>Automated Sequential FIFO PCode Generator with zero collision risk and instant uniqueness verification.</li>
                <li>Interactive Item Master UI with 20+ fields (OEMs, Part Numbers, Brand, Vehicle Model, CC, Fitment, Units, Tax).</li>
                <li>Real-time visual entry indicators: Unsaved row (Red) vs. Saved row (Green) to prevent operational data loss.</li>
                <li>PCode Permanent Lock mechanism triggering post-creation to ensure immutable audit integrity.</li>
                <li>Non-PCode Item Master holding area for emergency counter sales, tracking unregistered items with transaction links.</li>
              </ul>
            </div>
            <div>
              <div class="ms-subheading">Assigned Team</div>
              <div class="team-badge-list">
                <span class="team-pill">Lead Frontend Dev</span>
                <span class="team-pill">Lead Backend Dev</span>
                <span class="team-pill">QA Engineer</span>
              </div>
              <div class="signoff-box">
                <div class="signoff-title">Milestone Sign-off Criteria</div>
                Live test showing automated PCode sequential generation, Item Master creation with images, Red/Green save indicators, and Non-PCode emergency booking.
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="page-break"></div>

      <!-- MILESTONE 3 -->
      <div class="milestone-card avoid-break">
        <div class="milestone-header">
          <div class="milestone-left">
            <span class="ms-tag">MILESTONE 03</span>
            <span class="ms-title">Dual Approval Workflows, Centralized Pricing & Stock Alert Engine</span>
          </div>
          <div class="milestone-right">
            <span class="ms-duration">Weeks 5 – 6 (10 Working Days)</span>
            <span class="ms-payment-badge">20% • BD 681.818</span>
          </div>
        </div>
        <div class="milestone-body">
          <div class="ms-detail-grid">
            <div>
              <div class="ms-subheading">Technical Deliverables & Key Tasks</div>
              <ul class="feature-list">
                <li><strong>Workflow Case 1 (Sales Counter):</strong> Sales Request &rarr; Branch Purchase Manager (BPM) duplicate verification &rarr; CTO technical validation & PCode creation.</li>
                <li><strong>Workflow Case 2 (Vendor Receiving):</strong> Store Purchase Manager (SPM) PO vs. physical variance &rarr; Brand divergence notification &rarr; CTO review & generation.</li>
                <li>Centralized Multi-Country Price Management single-screen interface with automated currency conversion and country overrides.</li>
                <li>Minimum Order Level (MOL) configuration by Store/Branch with automated dashboard triggers and Purchase/CTO review console.</li>
                <li>Full audit trail logging every price modification, date, user ID, and justification notes.</li>
              </ul>
            </div>
            <div>
              <div class="ms-subheading">Assigned Team</div>
              <div class="team-badge-list">
                <span class="team-pill">Project Manager</span>
                <span class="team-pill">Lead Backend Dev</span>
                <span class="team-pill">Lead Frontend Dev</span>
                <span class="team-pill">QA Tester</span>
              </div>
              <div class="signoff-box">
                <div class="signoff-title">Milestone Sign-off Criteria</div>
                End-to-end execution of both approval workflows across roles, successful centralized price update reflecting in Bahrain and Dubai stores, low-stock alerts firing.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- MILESTONE 4 -->
      <div class="milestone-card avoid-break">
        <div class="milestone-header">
          <div class="milestone-left">
            <span class="ms-tag">MILESTONE 04</span>
            <span class="ms-title">Item Mapping, Substitutes & PartSouq Integration</span>
          </div>
          <div class="milestone-right">
            <span class="ms-duration">Weeks 7 – 8 (10 Working Days)</span>
            <span class="ms-payment-badge">20% • BD 681.818</span>
          </div>
        </div>
        <div class="milestone-body">
          <div class="ms-detail-grid">
            <div>
              <div class="ms-subheading">Technical Deliverables & Key Tasks</div>
              <ul class="feature-list">
                <li>Dedicated Item Mapping Window replacing legacy text comments with structured multi-OEM relational records.</li>
                <li>Advanced Substitute Suggestion Engine offering sales staff compatible parts across brands and pricing tiers.</li>
                <li>External Catalog Reference Integration: PartSouq.com connector (API / Embedded browser sandbox) preserving in-ERP workflow.</li>
                <li>Item Handling Precautionary Sales Warning pop-ups (e.g., "Remove sticker", "Check fitment") with mandatory salesperson acknowledgement.</li>
                <li>Trade secret confidentiality enforcement: Masking internal supplier OEM data on commercial counter documents.</li>
              </ul>
            </div>
            <div>
              <div class="ms-subheading">Assigned Team</div>
              <div class="team-badge-list">
                <span class="team-pill">Lead Frontend Dev</span>
                <span class="team-pill">Lead Backend Dev</span>
                <span class="team-pill">DevOps Specialist</span>
                <span class="team-pill">QA Tester</span>
              </div>
              <div class="signoff-box">
                <div class="signoff-title">Milestone Sign-off Criteria</div>
                Working substitute engine suggesting alternate parts during search, successful PartSouq catalog lookup within ERP, sales alert confirmation modal verified.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- MILESTONE 5 -->
      <div class="milestone-card avoid-break">
        <div class="milestone-header">
          <div class="milestone-left">
            <span class="ms-tag">MILESTONE 05</span>
            <span class="ms-title">Legacy Data Migration, Governance & CTO Executive Dashboard</span>
          </div>
          <div class="milestone-right">
            <span class="ms-duration">Week 9 (5 Working Days)</span>
            <span class="ms-payment-badge">10% • BD 340.909</span>
          </div>
        </div>
        <div class="milestone-body">
          <div class="ms-detail-grid">
            <div>
              <div class="ms-subheading">Technical Deliverables & Key Tasks</div>
              <ul class="feature-list">
                <li>Legacy PCode data cleansing and migration utility from existing BUSY ERP and Excel spreadsheets.</li>
                <li>Archiving and inactive PCode hiding logic (excluding obsolete parts from active searches while preserving audit trails).</li>
                <li>Executive CTO Audit & Analytics Dashboard: Branch-wise stock visibility, price movements, purchase velocity, and demand analytics.</li>
                <li>System-wide performance indexing and query optimization for 100,000+ automotive spare part records.</li>
              </ul>
            </div>
            <div>
              <div class="ms-subheading">Assigned Team</div>
              <div class="team-badge-list">
                <span class="team-pill">Project Manager</span>
                <span class="team-pill">Lead Backend Dev</span>
                <span class="team-pill">Database Admin</span>
                <span class="team-pill">Lead Frontend Dev</span>
              </div>
              <div class="signoff-box">
                <div class="signoff-title">Milestone Sign-off Criteria</div>
                Sample legacy dataset migrated and verified, inactive PCodes successfully hidden from search, CTO dashboard presenting live analytical charts.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- MILESTONE 6 -->
      <div class="milestone-card avoid-break">
        <div class="milestone-header">
          <div class="milestone-left">
            <span class="ms-tag">MILESTONE 06</span>
            <span class="ms-title">Comprehensive QA, Client UAT, Staff Training & Go-Live Deployment</span>
          </div>
          <div class="milestone-right">
            <span class="ms-duration">Week 10 (5 Working Days)</span>
            <span class="ms-payment-badge">10% • BD 340.909</span>
          </div>
        </div>
        <div class="milestone-body">
          <div class="ms-detail-grid">
            <div>
              <div class="ms-subheading">Technical Deliverables & Key Tasks</div>
              <ul class="feature-list">
                <li>End-to-end Integration and Concurrency Testing across Bahrain & Dubai simulated branch network.</li>
                <li>Formal User Acceptance Testing (UAT) execution with Popular Auto Spare management, CTO, and Branch Managers.</li>
                <li>Comprehensive User Manuals, Video Walkthroughs, and role-based training sessions for Store Supervisors and Sales staff.</li>
                <li>Production cutover, final live cloud deployment, SSL certificate hardening, and automated daily backup routines.</li>
                <li>30-Day dedicated Post-Go-Live Hypercare and warranty support.</li>
              </ul>
            </div>
            <div>
              <div class="ms-subheading">Assigned Team</div>
              <div class="team-badge-list">
                <span class="team-pill">Full Project Team (PM, Developers, DevOps, QA Lead)</span>
              </div>
              <div class="signoff-box">
                <div class="signoff-title">Milestone Sign-off Criteria</div>
                Formal UAT Sign-off certificate signed by Client & Consultant, system deployed to live production URL, training completed for all branches.
              </div>
            </div>
          </div>
        </div>
      </div>

    </section>

    <div class="page-break"></div>

    <!-- SECTION 5: COMMERCIALS & PAYMENT SCHEDULE -->
    <section class="section-block avoid-break">
      <div class="section-title-wrap">
        <div class="section-num">05</div>
        <h2 class="section-title">Milestone Payment Structure & Invoicing Schedule</h2>
      </div>

      <p>
        To ensure total financial transparency and accountability, project billing is directly tethered to verifiable milestone completions and client sign-offs.
      </p>

      <table>
        <thead>
          <tr>
            <th style="width: 14%;">Billing Stage</th>
            <th style="width: 36%;">Deliverable Focus / Invoicing Trigger</th>
            <th style="width: 14%;">Timeline</th>
            <th style="width: 14%; text-align: center;">Payment Share</th>
            <th style="width: 22%; text-align: right;">Amount (BHD)</th>
          </tr>
        </thead>
        <tbody>
          <tr class="advance-summary-row">
            <td><strong>ADVANCE TOKEN</strong></td>
            <td><strong>Whole Project Kickoff Advance (Master ERP Contract Signing)</strong></td>
            <td>At Signing</td>
            <td style="text-align: center;"><span class="badge badge-warning">Master Advance</span></td>
            <td class="num-col"><strong>BD 5,000.000</strong></td>
          </tr>
          <tr>
            <td><strong>MS-01</strong></td>
            <td>Architecture, Multi-Company DB & Security Setup</td>
            <td>Weeks 1 – 2</td>
            <td style="text-align: center;"><span class="badge badge-primary">20%</span></td>
            <td class="num-col"><strong>BD 681.818</strong></td>
          </tr>
          <tr>
            <td><strong>MS-02</strong></td>
            <td>PCode Sequence Engine & Item Master UI</td>
            <td>Weeks 3 – 4</td>
            <td style="text-align: center;"><span class="badge badge-purple">20%</span></td>
            <td class="num-col"><strong>BD 681.818</strong></td>
          </tr>
          <tr>
            <td><strong>MS-03</strong></td>
            <td>Dual Approval Workflows & Centralized Pricing</td>
            <td>Weeks 5 – 6</td>
            <td style="text-align: center;"><span class="badge badge-purple">20%</span></td>
            <td class="num-col"><strong>BD 681.818</strong></td>
          </tr>
          <tr>
            <td><strong>MS-04</strong></td>
            <td>Item Mapping, Substitutes & PartSouq Integration</td>
            <td>Weeks 7 – 8</td>
            <td style="text-align: center;"><span class="badge badge-purple">20%</span></td>
            <td class="num-col"><strong>BD 681.818</strong></td>
          </tr>
          <tr>
            <td><strong>MS-05</strong></td>
            <td>Legacy Data Migration & CTO Analytics Dashboard</td>
            <td>Week 9</td>
            <td style="text-align: center;"><span class="badge badge-accent">10%</span></td>
            <td class="num-col"><strong>BD 340.909</strong></td>
          </tr>
          <tr>
            <td><strong>MS-06</strong></td>
            <td>QA Testing, Staff Training & Live Go-Live</td>
            <td>Week 10</td>
            <td style="text-align: center;"><span class="badge badge-success">10%</span></td>
            <td class="num-col"><strong>BD 340.910</strong></td>
          </tr>
          <!-- Subtotal / Development Cost -->
          <tr class="payment-total-row">
            <td colspan="3"><strong>TOTAL MODULE 1 DEVELOPMENT COST (Excl. Advance)</strong></td>
            <td style="text-align: center;"><strong>100%</strong></td>
            <td class="num-col"><strong>BD 3,409.091</strong></td>
          </tr>
          <!-- Overall Initial Agreement Total -->
          <tr class="contract-grand-total-row">
            <td colspan="3"><strong>TOTAL INITIAL AGREEMENT VALUE (Advance Token + Module 1)</strong></td>
            <td style="text-align: center;">—</td>
            <td class="num-col"><strong>BD 8,409.091</strong></td>
          </tr>
        </tbody>
      </table>

      <!-- Commercial, Hardware & Warranty Policy Grid -->
      <div class="grid-3" style="margin-top: 15px;">
        <div class="card card-primary">
          <div class="card-title">Commercial & Billing Terms</div>
          <div class="card-text">
            <ul style="padding-left: 14px; margin-top: 4px;">
              <li><strong>Master Project Token:</strong> BD 5,000.000 advance is due upon contract execution for whole ERP mobilization.</li>
              <li>Module milestone invoices are issued upon formal deliverable sign-off.</li>
              <li>Standard payment term: Within 10 business days from invoice presentation.</li>
              <li>All quoted prices are exclusive of statutory VAT (applied as per Bahrain tax regulations).</li>
            </ul>
          </div>
        </div>

        <div class="card card-accent">
          <div class="card-title" style="color: var(--accent-dark);">Server & Hardware Policy</div>
          <div class="card-text">
            <ul style="padding-left: 14px; margin-top: 4px;">
              <li><strong>Client Provisioning:</strong> All server hosting (cloud/on-premise), POS hardware, barcode scanners, and store terminals must be provided directly by the Client.</li>
              <li><strong>Advance for Purchasing:</strong> If SaNDS Lab is requested to procure hardware or cloud subscriptions, the <strong>Client must provide 100% of the hardware cost in advance</strong>.</li>
            </ul>
          </div>
        </div>

        <div class="card card-secondary">
          <div class="card-title">Warranty & Hypercare Support</div>
          <div class="card-text">
            <ul style="padding-left: 14px; margin-top: 4px;">
              <li>Includes <strong>30 calendar days of free post-launch Hypercare support</strong> covering bug fixes and minor operational adjustments.</li>
              <li>Dedicated on-site & remote support team based in Salmabad, Bahrain.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 6: SLA, LATE DELIVERY, CALENDAR, FORCE MAJEURE & LITIGATION -->
    <section class="section-block avoid-break">
      <div class="section-title-wrap">
        <div class="section-num">06</div>
        <h2 class="section-title">Working Calendar, SLA, Force Majeure & Legal Litigation</h2>
      </div>

      <p>
        To safeguard the commercial, operational, and legal interests of both <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong> (Client) and <strong>SaNDS Lab Middle East W.L.L</strong> (Service Provider), the following legally binding provisions govern working hours, delivery schedules, unforeseen events, and dispute resolution:
      </p>

      <div class="grid-2">
        
        <!-- Working Calendar & Bahrain Holidays -->
        <div class="card card-primary">
          <div class="card-title">1. Working Calendar & Official Bahrain Public Holidays</div>
          <div class="card-text">
            <ul style="padding-left: 14px; margin-top: 5px;">
              <li><strong>Standard Work Week:</strong> Sunday through Thursday (5 business days/week). All <strong>Fridays and Saturdays are considered official non-working corporate weekend holidays</strong>.</li>
              <li><strong>Government Public Holidays:</strong> All official public and national holidays declared/published by the <strong>Government of the Kingdom of Bahrain for the corporate/private sector</strong> (e.g., National Day, Eid Al-Fitr, Eid Al-Adha, Islamic New Year, Ashura, Labour Day, Prophet's Birthday) shall be observed as non-working holidays.</li>
              <li><strong>Schedule Adjustment:</strong> The 10-week timeline is computed based on <strong>50 actual working days</strong>. Target milestone delivery dates will automatically adjust and extend based on the official Bahrain national holiday calendar.</li>
            </ul>
          </div>
        </div>

        <!-- Force Majeure & Unforeseen Events -->
        <div class="card card-accent">
          <div class="card-title" style="color: var(--accent-dark);">2. Force Majeure & Unforeseen Events</div>
          <div class="card-text">
            <ul style="padding-left: 14px; margin-top: 5px;">
              <li><strong>Excused Delay Events:</strong> Neither party shall be held liable or penalized for delays caused by extraordinary events beyond reasonable human control, including <strong>Natural Calamities / Disasters (floods, earthquakes, severe weather), Acts of God, Wars, Armed Regional Conflicts, Civil Unrest, Government-mandated Curfews/Lockdowns, or Nationwide Telecommunication / Undersea Cable Disruptions</strong>.</li>
              <li><strong>Automatic Extension:</strong> In any Force Majeure event, the affected project milestone timeline shall automatically receive a <strong>day-for-day extension</strong> without financial penalties or liquidated damages.</li>
            </ul>
          </div>
        </div>

      </div>

      <div class="grid-2" style="margin-top: 15px;">
        
        <!-- Delay / Non-Delivery Clause -->
        <div class="card card-danger">
          <div class="card-title" style="color: var(--danger);">3. Late Delivery & Liquidated Damages (SLA Penalty)</div>
          <div class="card-text">
            <ul style="padding-left: 14px; margin-top: 5px;">
              <li><strong>On-Time Delivery Guarantee:</strong> SaNDS Lab guarantees milestone delivery within the agreed schedule (subject to timely client reviews, data inputs, and working day calendar).</li>
              <li><strong>Delay Penalty (Liquidated Damages):</strong> In the event of an unexcused delay caused solely by the Service Provider exceeding a <strong>15-calendar-day grace period</strong>, a penalty of <strong>0.5% per week of delay</strong> (calculated on the affected milestone value) will be credited to the Client, capped at a maximum of <strong>5% of that specific milestone value</strong>.</li>
              <li><strong>Hardware & Vendor Delay Exclusion:</strong> Any delay in the procurement, dispatch, international shipment, customs clearance, or vendor delivery of servers, cloud subscriptions, or physical hardware (e.g., POS terminals, barcode scanners) shall <strong>NOT be considered a project delay or breach of SLA by SaNDS Lab</strong>. An automatic day-for-day timeline extension will apply.</li>
              <li><strong>Other Exclusions:</strong> Delays resulting from client-side approvals, third-party API dependencies (e.g., PartSouq downtime), client infrastructure delays, or approved Change Requests (CR) shall grant an automatic schedule extension without penalty.</li>
            </ul>
          </div>
        </div>

        <!-- Non-Payment / Default Clause -->
        <div class="card card-accent">
          <div class="card-title" style="color: var(--accent-dark);">4. Non-Payment, Default & Work Suspension</div>
          <div class="card-text">
            <ul style="padding-left: 14px; margin-top: 5px;">
              <li><strong>Payment Window:</strong> Invoices must be settled within <strong>10 business days</strong> of formal milestone acceptance.</li>
              <li><strong>Right to Suspend Work:</strong> If any milestone invoice remains unpaid past <strong>15 calendar days</strong> following written notice, SaNDS Lab reserves the legal right to pause subsequent milestone development and staging access without liability for project timeline slippage.</li>
              <li><strong>Reactivation:</strong> Development sprints will resume within 3 business days following complete settlement of outstanding invoices.</li>
            </ul>
          </div>
        </div>

      </div>

      <!-- Legal Litigation & Dispute Resolution Box -->
      <div class="litigation-box avoid-break">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <h4 style="font-family:'Outfit',sans-serif; color:var(--danger); font-size:13.5px; font-weight:700;">
            5. Dispute Resolution, Governing Law & Legal Litigation Jurisdiction
          </h4>
          <span class="badge badge-danger">Kingdom of Bahrain Jurisdiction</span>
        </div>
        <div class="card-text" style="font-size:12px; color:var(--gray-700);">
          <p style="margin-bottom:6px;">
            <strong>Step 1 (Amicable Resolution):</strong> In the event of any technical, operational, or commercial dispute arising from or related to this contract, senior executive representatives (CEO of SaNDS Lab and Managing Director/CTO of Popular Auto Spare) shall meet within <strong>14 calendar days</strong> of written notification to reach an amicable resolution in good faith.
          </p>
          <p style="margin-bottom:6px;">
            <strong>Step 2 (Mediation & Expert Determination):</strong> If unresolved, the dispute may be referred to an independent IT Consultant (e.g. UniGlobal Consultants) for binding technical determination.
          </p>
          <p style="margin-bottom:0;">
            <strong>Step 3 (Legal Litigation & Court Jurisdiction):</strong> In the event of legal proceedings, this agreement shall be governed, construed, and enforced in accordance with the commercial and civil laws of the <strong>Kingdom of Bahrain</strong>. Both parties irrevocably submit to the exclusive jurisdiction of the <strong>Courts of the Kingdom of Bahrain</strong> / <strong>Bahrain Chamber for Dispute Resolution (BCDR)</strong> for any litigation, claim, or enforcement.
          </p>
        </div>
      </div>

    </section>

    <!-- SECTION 7: FORMAL APPROVAL & SIGN-OFF WITH LOGOS -->
    <section class="section-block avoid-break">
      <div class="section-title-wrap">
        <div class="section-num">07</div>
        <h2 class="section-title">Stakeholder Authorization & Sign-Off</h2>
      </div>

      <p>
        By signing below, the authorized representatives of <strong>SaNDS Lab Middle East W.L.L</strong>, <strong>UniGlobal Consultant</strong>, and <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong> agree to the milestone schedule, resource commitments, payment structure, SLA delivery guarantees, working calendar & holiday rules, Force Majeure provisions, and legal terms specified in this document.
      </p>

      <div class="approval-container">
        
        <!-- Service Provider -->
        <div class="approval-box">
          <div class="approval-header">
            <div class="approval-logo-wrap">
              <img class="approval-logo-img" src="{logo_sands_color}" alt="SaNDS Lab" />
            </div>
            <div class="approval-role">SERVICE PROVIDER</div>
            <div class="approval-org">SaNDS Lab Middle East W.L.L</div>
          </div>
          <div>
            <div class="sig-field">Name: <span>Ajit Kumar KV</span></div>
            <div class="sig-field">Title: <span>CEO & Managing Director</span></div>
            <div class="sig-field">Date: <span>21-Sep-2026</span></div>
          </div>
          <div class="sig-line">Authorized Signature & Seal</div>
        </div>

        <!-- Consultant -->
        <div class="approval-box">
          <div class="approval-header">
            <div class="approval-logo-wrap">
              <img class="approval-logo-img" src="{logo_uniglobal_color}" alt="UniGlobal Consultancy" />
            </div>
            <div class="approval-role">CONSULTANT & ARCHITECT</div>
            <div class="approval-org">UniGlobal Consultants</div>
          </div>
          <div>
            <div class="sig-field">Name: <span>Lead ERP Consultant</span></div>
            <div class="sig-field">Title: <span>Principal Business Analyst</span></div>
            <div class="sig-field">Date: <span>___-___-2026</span></div>
          </div>
          <div class="sig-line">Review & Recommendation Signature</div>
        </div>

        <!-- Client -->
        <div class="approval-box">
          <div class="approval-header">
            <div class="approval-logo-wrap">
              <img class="approval-logo-img" src="{logo_popular}" alt="Popular Auto Spare" />
            </div>
            <div class="approval-role">CLIENT REPRESENTATIVE</div>
            <div class="approval-org">Popular Auto Spare & A/C Parts Co.</div>
          </div>
          <div>
            <div class="sig-field">Name: <span>Managing Director / CTO</span></div>
            <div class="sig-field">Title: <span>Executive Director</span></div>
            <div class="sig-field">Date: <span>___-___-2026</span></div>
          </div>
          <div class="sig-line">Client Acceptance & Approval Signature</div>
        </div>

      </div>
    </section>

  </main>

  <!-- ==================== FOOTER ==================== -->
  <footer class="doc-footer">
    <div>SaNDS Lab Middle East W.L.L • Salmabad, Kingdom of Bahrain • Office: +973 35 078 079 • www.sandslab.com</div>
    <div>Confidential • Prepared for Popular Auto Spare & A/C Parts Co. W.L.L</div>
  </footer>

</div>

</body>
</html>"""

with open('PCode_Milestone_and_Payment_Structure.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('SL-POP-ERP-MS-001.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('PCode_Milestone_and_Payment_Structure.html and SL-POP-ERP-MS-001.html generated successfully.')

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
html_path = os.path.abspath('SL-POP-ERP-MS-001.html')
pdf_path_1 = os.path.abspath('PCode_Milestone_and_Payment_Structure.pdf')
pdf_path_2 = os.path.abspath('SL-POP-ERP-MS-001.pdf')

cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={pdf_path_2}',
    '--no-pdf-header-footer',
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
print('PDF conversion exit code:', res.returncode)

import shutil
shutil.copyfile(pdf_path_2, pdf_path_1)
print('Generated SL-POP-ERP-MS-001.pdf and PCode_Milestone_and_Payment_Structure.pdf')

doc = fitz.open(pdf_path_2)
print('Generated PDF Page Count:', len(doc))
for i in range(len(doc)):
    page = doc[i]
    print(f'Page {i+1} rect: {page.rect}, text length: {len(page.get_text())}')
