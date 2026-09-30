with open('build_documents.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find sections or comments in build_documents.py
comments = re.findall(r'(<!--.*?-->|/\*.*?\*/|###.*|##.*)', text)
for c in comments[:30]:
    print(c[:100])

# Let's see the outline of HTML in build_documents.py
print("\n--- HTML Structure Outline ---")
for line in text.split('\n'):
    if '<section' in line or '<h1' in line or '<h2' in line or 'class="section' in line or 'id="sec' in line or 'page' in line.lower() and ('<' in line and '>' in line):
        if len(line.strip()) < 120:
            print(line.strip())
