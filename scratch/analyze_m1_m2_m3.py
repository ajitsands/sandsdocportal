import re
import os

for fn, name in [('build_documents.py', 'Module 1'), 
                 ('build_vendor_purchase_milestone.py', 'Module 2'), 
                 ('build_store_verification_milestone.py', 'Module 3')]:
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"\n==================== {name}: {fn} ====================")
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.I | re.DOTALL)
    for idx, h in enumerate(h2s):
        clean_h = re.sub(r'<[^>]+>', ' ', h).strip()
        print(f"  Section {idx+1}: {clean_h}")

