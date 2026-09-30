import re

with open('SL-POP-ERP-MS-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find classes with page
print("Classes with page:")
matches = set(re.findall(r'class="([^"]*page[^"]*)"', text, re.I))
for m in matches:
    print(' ', m)

# Let's see the overall DOM structure
# Search for top-level divs inside body
body_match = re.search(r'<body[^>]*>(.*?)</body>', text, re.DOTALL)
if body_match:
    body = body_match.group(1)
    # find major divs
    divs = re.findall(r'<div class="([^"]+)"', body[:5000])
    print("\nInitial classes in body:")
    for d in divs[:15]:
        print(' -', d)
