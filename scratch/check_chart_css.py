with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
css_chart = re.findall(r'(\.[a-zA-Z0-9_-]*chart[a-zA-Z0-9_-]*\s*\{[^}]*\})', text)
for c in css_chart:
    print(c)
    print("-" * 40)
