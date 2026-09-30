with open('scratch/doc002_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# print TOC and all major headings
pos_toc = text.find('TABLE OF CONTENT')
if pos_toc != -1:
    print("--- TABLE OF CONTENTS ---")
    print(text[pos_toc:pos_toc+2500].encode('ascii', 'replace').decode('ascii'))

print("\n--- ALL NUMBERED SECTIONS ---")
matches = re.findall(r'(?:=== PAGE \d+ ===|\n\d+[\.\d]*\s+[A-Z].*)', text)
for m in matches[:60]:
    if m.strip():
        print(m.strip().encode('ascii', 'replace').decode('ascii'))
