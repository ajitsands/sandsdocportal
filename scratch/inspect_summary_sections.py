import re

with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find all section headers or titles
titles = re.findall(r'<div class="section-title">([\s\S]*?)</div>', c)
for t in titles:
    clean = re.sub(r'<[^>]+>', '', t).strip()
    print("Summary Section Title:", clean)
