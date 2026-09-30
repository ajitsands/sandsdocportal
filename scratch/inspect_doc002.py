with open('scratch/doc002_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pages = text.split('=== PAGE ')
print(f"Total pages: {len(pages)-1}")

# Print initial pages to see title, TOC, executive summary
for p in pages[1:8]:
    p_num = p.split(' ===')[0]
    content = p.split(' ===\n', 1)[1] if ' ===\n' in p else p
    print(f"\n================ PAGE {p_num} ================")
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    for l in lines[:15]:
        print(l.encode('ascii', 'replace').decode('ascii'))
