with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace any single } in the added web-action CSS block
old_block = """.web-action-bar {{
      background: #0f172a;
      color: #ffffff;
      padding: 12px 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    .web-action-left {{
      display: flex;
      align-items: center;
      gap: 15px;
    }

    .portal-branding {{
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 14px;
      color: #ffffff;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .web-action-right {{
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .badge-accent {{
      background: #fef3c7;
      color: #b45309;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }

    .badge-success {{
      background: #dcfce7;
      color: #15803d;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }"""

new_block = """.web-action-bar {{
      background: #0f172a;
      color: #ffffff;
      padding: 12px 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}

    .web-action-left {{
      display: flex;
      align-items: center;
      gap: 15px;
    }}

    .portal-branding {{
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 14px;
      color: #ffffff;
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .web-action-right {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .badge-accent {{
      background: #fef3c7;
      color: #b45309;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}

    .badge-success {{
      background: #dcfce7;
      color: #15803d;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}"""

code = code.replace(old_block, new_block)

with open('build_sales_process_milestone.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Double braces applied properly.")
