import os

pricing_css = """
    @media (max-width: 768px) {
      body { padding: 12px !important; font-size: 12px !important; }
      .container { padding: 16px !important; }
      .table-responsive, table { overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; display: block !important; }
      .grid, .kpi-grid, .stat-grid { grid-template-columns: 1fr !important; }
    }
"""

for f in ['Internal_Resource_Pricing_Reference.html', 'popular/Internal_Resource_Pricing_Reference.html']:
    if os.path.exists(f):
        c = open(f, encoding='utf-8').read()
        if '@media (max-width: 768px)' not in c:
            c = c.replace('</style>', pricing_css + '\n  </style>')
            with open(f, 'w', encoding='utf-8') as out:
                out.write(c)
            print(f"Updated {f}")
