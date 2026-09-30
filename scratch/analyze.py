import re
import json

with open('SL-POP-ERP-MS-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('File size:', len(text))
pages = re.findall(r'<div class="page([^"]*)" id="([^"]*)">', text)
print('Pages found:', len(pages))
for p in pages:
    print(' -', p)

headers = re.findall(r'<div class="page-title"[^>]*>(.*?)</div>', text, re.DOTALL)
print('\nPage titles:')
for h in headers:
    clean_h = re.sub(r'<[^>]+>', '', h).strip()
    print(' *', clean_h)
