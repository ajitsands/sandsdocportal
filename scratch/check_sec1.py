with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<div class="section-card" id="sec-visual-analytics">(.*?)<div class="section-card" id="sec-master-table">', text, re.DOTALL)
if m:
    print("Content length of Section 1:", len(m.group(1)))
    print("Content preview of Section 1:\n", m.group(1)[:2000])
else:
    print("Could not find section 1 block")
