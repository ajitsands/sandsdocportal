import glob, os

builders = glob.glob('build_*.py')
print(f"Found {len(builders)} python builders: {builders}")

for b in builders:
    content = open(b, encoding='utf-8').read()
    if 'COMPREHENSIVE MOBILE RESPONSIVE' not in content:
        # Check where </style> is and inject
        if '</style>' in content:
            # We can use double curly braces in f-strings or standard replace
            content_fixed = content.replace('</style>', """    /* =========================================================================
       COMPREHENSIVE MOBILE RESPONSIVE STYLING
       ========================================================================= */
    @media (max-width: 1100px) {{
      .main-wrapper {{
        grid-template-columns: 240px minmax(0, 1fr) !important;
        gap: 20px !important;
        padding: 0 16px !important;
      }}
      .sticky-sidebar {{
        width: 240px !important;
      }}
    }}

    @media (max-width: 900px) {{
      .main-wrapper {{
        display: block !important;
        grid-template-columns: 1fr !important;
        padding: 0 12px !important;
      }}
      .sticky-sidebar {{
        position: static !important;
        width: 100% !important;
        max-height: none !important;
        margin-bottom: 24px !important;
        top: 0 !important;
      }}
      .sidebar-nav {{
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
      }}
      .sidebar-link {{
        flex: 1 1 calc(50% - 6px) !important;
        padding: 8px 10px !important;
        font-size: 11.5px !important;
      }}
      .hero-stats-grid, .stat-grid, .kpi-grid, .meta-grid {{
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 12px !important;
      }}
      .doc-top-bar-inner, .header-content {{
        flex-direction: column !important;
        text-align: center !important;
        gap: 12px !important;
        padding: 16px 12px !important;
      }}
      .logos-cluster, .header-logos {{
        justify-content: center !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
      }}
      .doc-meta-badge-group, .doc-meta-badge {{
        justify-content: center !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
      }}
      .charts-grid {{
        grid-template-columns: 1fr !important;
      }}
    }}

    @media (max-width: 600px) {{
      .web-action-bar {{
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 10px !important;
        padding: 10px 12px !important;
      }}
      .web-action-left, .web-action-right {{
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 6px !important;
        width: 100% !important;
      }}
      .web-action-bar .btn {{
        flex: 1 1 calc(50% - 6px) !important;
        text-align: center !important;
        justify-content: center !important;
        font-size: 11.5px !important;
        padding: 7px 10px !important;
      }}
      .portal-branding {{
        font-size: 12px !important;
        text-align: center !important;
        width: 100% !important;
        justify-content: center !important;
        display: flex !important;
      }}
      .hero-card, .doc-section, .section-card, .signoff-section {{
        padding: 16px 12px !important;
        border-radius: 10px !important;
        margin-bottom: 16px !important;
      }}
      .hero-title, .section-title {{
        font-size: 18px !important;
      }}
      .hero-stats-grid, .stat-grid, .kpi-grid, .meta-grid {{
        grid-template-columns: 1fr !important;
        gap: 10px !important;
      }}
      .sidebar-link {{
        flex: 1 1 100% !important;
      }}
      .table-container {{
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        width: 100% !important;
        margin: 10px 0 15px 0 !important;
        border-radius: 6px !important;
      }}
      table.milestone-table, table.master-table, table.data-table, table.rate-table {{
        min-width: 540px !important;
      }}
      .modal-box {{
        width: 95% !important;
        max-width: 95% !important;
        padding: 16px !important;
        margin: 10px !important;
      }}
      canvas.signature-pad, .sig-pad-canvas {{
        height: 140px !important;
      }}
      .total-cost-hero-box {{
        flex-direction: column !important;
        text-align: center !important;
        gap: 12px !important;
        padding: 16px !important;
      }}
      .total-cost-amt {{
        font-size: 24px !important;
      }}
    }}
  </style>""")
            with open(b, 'w', encoding='utf-8') as f:
                f.write(content_fixed)
            print(f"Updated python builder {b}")
