with open('index.php', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\$documents\s*=\s*array\(.*?\);)', text, re.DOTALL)
if matches:
    print("Found $documents definition:")
    print(matches[0][:800])
else:
    # Look for doc IDs in index.php
    print("Doc occurrences in index.php:")
    for l in text.splitlines():
        if 'SL-POP-ERP' in l:
            print(l)
