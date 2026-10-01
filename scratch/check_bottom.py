with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Find where signoff section or terms ends
terms_idx = text.find('Governance, SLA & Payment Terms')
if terms_idx != -1:
    print(text[terms_idx:terms_idx+3500])
