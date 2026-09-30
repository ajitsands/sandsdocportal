import re

with open('scratch/doc_005_text.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pages = text.split('=== PAGE ')

# Let's inspect sections:
sections_to_check = [
    "1. ACCOUNTING & FINANCIAL MANAGEMENT",
    "1.1. System Design Philosophy",
    "1.2. Chart of Accounts (COA)",
    "1.3. General Ledger (GL)",
    "1.4. Accounts Payable (AP)",
    "1.5. Accounts Receivable (AR)",
    "2. Inventory-Integrated Accounting",
    "2.1. Inventory Accounting Logic",
    "2.2. Banking, Cash & Treasury Management",
    "2.3. Financial Budgeting & Budget Management",
    "2.4. Multi-Currency & Foreign Exchange (FX) Management",
    "2.5. Tax & Compliance Management",
    "2.6. Financial Statements, Consolidation & Management Reporting",
    "3. NEW BRANCH SETUP GUIDELINE & CHECKLIST"
]

print(f"Total length of DOC-005 text: {len(text)} characters across {len(pages)-1} pages.")

with open('scratch/doc005_summary_overview.txt', 'w', encoding='utf-8') as out:
    for idx, page in enumerate(pages[1:], 1):
        lines = [l.strip() for l in page.splitlines() if l.strip()]
        out.write(f"\n--- PAGE {idx} ---\n")
        # Filter out common running header/footer
        content_lines = []
        for l in lines:
            if any(skip in l for skip in ['SaNDS Lab Middle East W.L.L', 'Office No :', 'Page -', 'ERP Solution Business Analysis Document', 'Prepared by', 'WWW.SANDSLAB.COM', 'POPULAR', 'ERP DOCUMENT 5.0', 'DRAFT - CONFIDENTIAL', '04-July-2026', '04-JUL-2026']):
                continue
            content_lines.append(l)
        out.write('\n'.join(content_lines) + '\n')

print("Summary overview saved to scratch/doc005_summary_overview.txt")
