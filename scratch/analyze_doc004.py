import re

with open('scratch/doc_004_text.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pages = text.split('=== PAGE ')

with open('scratch/doc_004_summary.txt', 'w', encoding='utf-8') as out:
    out.write("=== DOC-004 DETAILED SUMMARY & STRUCTURE ===\n\n")
    for idx, page in enumerate(pages[1:], 1):
        lines = [l.strip() for l in page.splitlines() if l.strip()]
        out.write(f"--- PAGE {idx} ---\n")
        # Filter out common running header/footer
        content_lines = []
        for l in lines:
            if any(skip in l for skip in ['SaNDS Lab Middle East W.L.L', 'Office No :', 'Page -', 'ERP Solution Business Analysis Document', 'Prepared by', 'WWW.SANDSLAB.COM', 'POPULAR', 'ERP DOCUMENT 4.0', 'DRAFT - CONFIDENTIAL', '27-Mar-2026', '30-Mar-2026', '30-MAR-2026']):
                continue
            content_lines.append(l)
        out.write('\n'.join(content_lines) + '\n\n')

print("Summary written to scratch/doc_004_summary.txt")
