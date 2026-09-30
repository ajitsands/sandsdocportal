with open('SL-POP-ERP-MS-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'Module \d+:[^<]+', text)
for m in matches[:15]:
    print(m)
