import re
import os

files_to_check = [
    'SL-POP-ERP-SUMMARY-001.html',
    'SL-POP-ERP-MS-001.html',
    'SL-POP-ERP-MS-002.html',
    'SL-POP-ERP-MS-003.html',
    'SL-POP-ERP-MS-004.html',
    'SL-POP-ERP-MS-005.html',
    'SL-POP-ERP-MS-006.html',
    'SL-POP-ERP-MS-007.html',
    'SL-POP-ERP-MS-008.html',
    'SL-POP-ERP-MS-009.html',
    'SL-POP-ERP-ARCH-001.html',
    'index.php'
]

for fname in files_to_check:
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        matches = re.findall(r'Stakeholder Authorization|CONSULTANT REVIEW|CLIENT APPROVAL|UniGlobal|Popular', content, re.IGNORECASE)
        print(f"{fname}: matches={len(matches)}")
        
        # Check if there is a block table or module list in signoff
        if 'Stakeholder Authorization' in content:
            idx = content.find('Stakeholder Authorization')
            snippet = content[idx:idx+2500]
            print(f"--- {fname} Signoff Block Snippet ---")
            print(snippet[:600].replace('\n', ' '))
