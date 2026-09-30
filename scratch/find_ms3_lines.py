with open('index.php', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for idx, l in enumerate(lines):
    if 'SL-POP-ERP-MS-003' in l or 'SL-POP-ERP-MS-002' in l:
        print(f"Line {idx+1}: {l}")
