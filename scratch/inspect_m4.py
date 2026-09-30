import re

with open('SL-POP-ERP-MS-004.html', 'r', encoding='utf-8') as f:
    c = f.read()

sidebar_links = re.findall(r'<a href="([^"]+)"', c)
print("M4 sidebar links:", [l for l in sidebar_links if l.startswith('#')])

sec_matches = re.findall(r'<(?:section|div)[^>]*id="([^"]+)"[^>]*class="([^"]+)"', c)
print("M4 elements with id & class:")
for sm in sec_matches:
    print(f"  id='{sm[0]}' class='{sm[1]}'")
