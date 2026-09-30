import sys

with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for idx, l in enumerate(lines):
    if any(k in l for k in ['INR', '₹', 'Rupee', 'rupee']):
        sys.stdout.buffer.write(f"Line {idx+1}: {l}\n".encode('utf-8'))
