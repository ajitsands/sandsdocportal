with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the web action bar CSS with enhanced button styles
old_web_bar_css = """.web-action-right {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}"""

new_web_bar_css = """.web-action-right {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .web-action-bar .btn {{
      font-family: 'Inter', sans-serif;
      font-size: 12px;
      font-weight: 600;
      padding: 7px 14px;
      border-radius: 6px;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }}

    .web-action-bar .btn-outline {{
      background: rgba(255, 255, 255, 0.12) !important;
      border: 1px solid rgba(255, 255, 255, 0.45) !important;
      color: #ffffff !important;
    }}

    .web-action-bar .btn-outline:hover {{
      background: rgba(255, 255, 255, 0.25) !important;
      border-color: #ffffff !important;
      color: #ffffff !important;
    }}

    .web-action-bar .btn-accent {{
      background: #d97706 !important;
      border: 1px solid #d97706 !important;
      color: #ffffff !important;
      font-weight: 700 !important;
    }}

    .web-action-bar .btn-accent:hover {{
      background: #b45309 !important;
      border-color: #b45309 !important;
    }}"""

code = code.replace(old_web_bar_css, new_web_bar_css)

with open('build_sales_process_milestone.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated build_sales_process_milestone.py with high-contrast button styling!")
