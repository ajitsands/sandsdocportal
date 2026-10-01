import re

with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.findall(r'<div[^>]*class=["\'][^"\']*section-card[^"\']*["\'][^>]*>', text)
print(f'Total section-cards found: {len(sections)}')
for s in sections:
    print("CARD:", s)

headers = re.findall(r'<div class="section-title">.*?</div>', text, re.DOTALL)
print(f'Total section titles: {len(headers)}')
for h in headers[:10]:
    print("TITLE:", h.strip().replace('\n', ' '))
