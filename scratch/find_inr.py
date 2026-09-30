with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
print(f"Total lines: {len(lines)}")
for idx, l in enumerate(lines):
    if any(k in l for k in ['INR', '₹', 'Rupee', 'rupee']):
        print(f"Line {idx+1}: {l}")
