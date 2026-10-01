import os
import re

for root, dirs, files in os.walk('.'):
    if '.git' in root or '.sessions' in root:
        continue
    for f in files:
        if f.endswith('.py') or f.endswith('.php') or f.endswith('.sql'):
            fpath = os.path.join(root, f)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
            if 'sig_badge_consultant_review' in c or 'UniGlobal' in c or 'fix_all_footers' in f:
                print(f"Found reference in {fpath}")
