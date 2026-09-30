import re

with open('scratch/doc_006_text.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pages = text.split('=== PAGE ')

with open('scratch/doc_006_toc.txt', 'w', encoding='utf-8') as out:
    for i in range(1, min(10, len(pages))):
        out.write(f"--- PAGE {i} ---\n")
        lines = [l.strip() for l in pages[i].splitlines() if l.strip()]
        out.write('\n'.join(lines) + "\n\n")

print("Saved scratch/doc_006_toc.txt")
