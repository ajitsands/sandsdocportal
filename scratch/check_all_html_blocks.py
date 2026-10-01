import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
popular_files = [os.path.join('popular', f) for f in os.listdir('popular') if f.endswith('.html')] if os.path.exists('popular') else []

all_files = html_files + popular_files

print(f"Total HTML files to inspect: {len(all_files)}")

for fpath in sorted(all_files):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    has_block1 = 'Engineering Preparation & Stakeholder Verification Matrix' in content
    has_consultant = 'CONSULTANT REVIEW' in content
    has_client = 'CLIENT APPROVAL' in content
    print(f"{fpath:60s} | Block1: {str(has_block1):5s} | Consultant: {str(has_consultant):5s} | Client: {str(has_client):5s}")
