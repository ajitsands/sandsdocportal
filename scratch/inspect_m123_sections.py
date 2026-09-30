import re
import os

def inspect_file(fn, name):
    with open(fn, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"\n============================== {name}: {fn} ==============================")
    sections = re.findall(r'<div[^>]+id="([^"]+)"[^>]*>(.*?)</div>\s*(?=<div[^>]+id=|<footer|</body>)', c, re.DOTALL | re.I)
    print(f"Found {len(sections)} top-level sections.")
    for sid, sbody in sections[:10]:
        h2 = re.search(r'<h[23][^>]*>(.*?)</h[23]>', sbody, re.I | re.DOTALL)
        h2_t = re.sub(r'<[^>]+>', '', h2.group(1)).strip() if h2 else 'No H2/H3'
        print(f"  ID: {sid:<20} | Title: {h2_t} ({len(sbody)} chars)")

inspect_file('build_documents.py', 'Module 1')
inspect_file('build_vendor_purchase_milestone.py', 'Module 2')
inspect_file('build_store_verification_milestone.py', 'Module 3')
