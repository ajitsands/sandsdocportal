with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    ms3_code = f.read()

import re

# Extract milestone table or payment table
tables = re.findall(r'<table[^>]*>(.*?)</table>', ms3_code, re.DOTALL)
print(f"MS-003 has {len(tables)} tables.")
for idx, tbl in enumerate(tables):
    # Print first few rows
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbl, re.DOTALL)
    print(f"\nTable {idx+1} ({len(rows)} rows):")
    for r in rows[:4]:
        cells = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.DOTALL)]
        print(" | ".join(cells))
