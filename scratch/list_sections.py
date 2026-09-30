import re

with open('scratch/doc_004_summary.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all numbered headings like 1., 1.1, 1.1.1, 1.2, etc.
sections = re.findall(r'(?:^|\n)(1\.\d+(?:\.\d+)?\.?\s+[^\n]+)', content)
print(f"Found {len(sections)} sections:")
for s in sections:
    print(s)
