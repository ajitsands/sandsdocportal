with open('build_documents.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Page break instances in MS-001:")
for m in re.finditer(r'class="page-break"', text):
    start = max(0, m.start() - 200)
    end = min(len(text), m.end() + 200)
    print("---")
    print(text[start:end].encode('ascii', 'replace').decode('ascii'))
