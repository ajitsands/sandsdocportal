import re

with open('scratch/doc005_body_details.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see all subheadings
subheadings = re.findall(r'(?:^|\n)(\d+\.\d+(?:\.\d+)?\s+[^\n]+)', text)
print(f"Total subheadings found: {len(subheadings)}")
for sh in subheadings:
    print(sh)
