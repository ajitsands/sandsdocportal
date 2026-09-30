import re

with open('scratch/doc_004_summary.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's write out detailed section analyses to scratch/doc004_deep_dive.txt
pages = text.split('--- PAGE ')
with open('scratch/doc004_deep_dive.txt', 'w', encoding='utf-8') as out:
    for p in pages[1:]:
        lines = [l for l in p.splitlines() if l.strip()]
        if not lines:
            continue
        page_num = lines[0].replace('---', '').strip()
        body = '\n'.join(lines[1:])
        out.write(f"=== PAGE {page_num} ===\n{body}\n\n")

print("Deep dive written to scratch/doc004_deep_dive.txt")
