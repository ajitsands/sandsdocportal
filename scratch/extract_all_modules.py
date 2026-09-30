import re
import os

for i in range(1, 10):
    fn = f'SL-POP-ERP-MS-{i:03d}.html'
    if not os.path.exists(fn):
        continue
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    m_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.I | re.DOTALL)
    h1 = re.sub(r'<[^>]+>', ' ', m_h1.group(1)).strip() if m_h1 else 'N/A'

    # Extract all text blocks inside hero/header
    metas = re.findall(r'<div class="meta-item"[^>]*>(.*?)</div>', content, re.I | re.DOTALL)
    meta_text = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m)).strip() for m in metas]

    print(f"\n=======================================================")
    print(f"MODULE {i} ({fn})")
    print(f"H1: {h1}")
    print(f"Meta: {meta_text}")

    # Extract tables
    tables = re.findall(r'<table[^>]*>(.*?)</table>', content, re.DOTALL | re.I)
    for t_idx, t in enumerate(tables):
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.DOTALL | re.I)
        is_relevant = False
        row_texts = []
        for r in rows:
            cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.DOTALL | re.I)
            clean = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', c)).strip() for c in cells]
            if any('milestone' in c.lower() or 'timeline' in c.lower() or 'deliverable' in c.lower() or 'cost' in c.lower() or 'bhd' in c.lower() or 'fee' in c.lower() for c in clean):
                is_relevant = True
            row_texts.append(" | ".join(clean))
        if is_relevant:
            print(f"--- Table {t_idx+1} ---")
            for rt in row_texts:
                print("  " + rt)
