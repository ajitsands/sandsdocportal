with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<div[^>]*class=["\'][^"\']*section-card[^"\']*["\'][^>]*>', text)
print("Section cards found:", len(matches))
for m in matches:
    print(m)
