with open('index.php', 'r', encoding='utf-8') as f:
    text = f.read()

import re
lines = text.split('\n')
for idx, line in enumerate(lines):
    if 'ms1_status' in line or 'arch_status' in line or 'ms3_status' in line:
        print(f"Line {idx+1}: {line.strip()}")
