import re

with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's check signoff section
signoff = re.findall(r'<div[^>]*class=["\'][^"\']*signoff[^\'"]*["\'][^>]*>', text)
print("Signoff tags:", signoff)

# Let's locate each section card and its title
pattern = re.compile(r'(<div class="section-card">)(\s*<div class="section-header">\s*<div>\s*<div class="section-title"><i[^>]*></i>\s*([^<]+)</div>)', re.DOTALL)

matches = pattern.findall(text)
print("Matches count:", len(matches))
for m in matches:
    print("Found section with title:", m[2].strip())
