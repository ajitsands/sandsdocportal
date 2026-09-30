with open('scratch/doc002_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
sections = [
    "1. Vendor Master Management",
    "2. Vendor Communication Framework",
    "3. Automated Low-Stock Reporting",
    "4. Less Item List Handling",
    "5. Purchase-Review-and-Approval-Workflow",
    "5.3. Request for Quotation",
    "6. Purchase Order Module",
    "7. Purchase-Verification-Note",
    "8. Reporting Module",
    "9. Management Review",
    "10. Data Flow Process for Purchase"
]

for sec in sections:
    pos = text.find(sec[:15])
    if pos != -1:
        print(f"\n==================== {sec} ====================")
        print(text[pos:pos+1200].encode('ascii', 'replace').decode('ascii'))
