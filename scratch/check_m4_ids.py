import re

with open('SL-POP-ERP-MS-004.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's search for each sidebar link ID in M4:
links = ['executive-summary', 'module-scope', 'pricing-matrix', 'detailed-milestones', 'payment-schedule', 'governance-sla', 'digital-signoff']
for l in links:
    found = re.findall(rf'<[^>]+id="{l}"[^>]*>', c)
    print(f"Target '{l}': {found}")
