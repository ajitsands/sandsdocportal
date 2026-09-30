import re

with open('scratch/doc_005_text.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pages = text.split('=== PAGE ')

with open('scratch/doc_005_toc.txt', 'w', encoding='utf-8') as out:
    for i in range(1, min(10, len(pages))):
        out.write(f"--- PAGE {i} ---\n")
        lines = [l.strip() for l in pages[i].splitlines() if l.strip()]
        out.write('\n'.join(lines) + "\n\n")

# Find all section headers
sections = re.findall(r'(?:^|\n)(\d+\.\d*(?:\.\d+)*\s+[^\n]+)', text)
with open('scratch/doc_005_sections.txt', 'w', encoding='utf-8') as out:
    out.write("Found Sections in DOC-005 Accounts:\n")
    for s in set(sections):
        out.write(s + "\n")

print(f"Saved TOC and found {len(sections)} sections")
