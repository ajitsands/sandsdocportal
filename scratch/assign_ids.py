import re

with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Map section titles to IDs
title_to_id = [
    ("Visual Milestone & Budget Analytics", "sec-visual-analytics"),
    ("Master 9-Module Budgeting & Milestone Matrix (BHD)", "sec-master-table"),
    ("9-Module Architectural Scope & Deliverable Pillars", "sec-scope-pillars"),
    ("Complete 35 Milestone Tranches Detailed Breakdown (BHD)", "sec-detailed-milestones"),
    ("Dedicated Engineering Team & Transparent Rate Matrix", "sec-team-rate-card"),
    ("Total Project Investment & Milestone Schedule in Bahraini Dinars (BHD)", "sec-total-investment"),
    ("Governance, SLA & Payment Terms", "sec-terms-governance")
]

for title, sec_id in title_to_id:
    # Pattern to match <div class="section-card"> followed soon by the title
    pattern = re.compile(r'(<div class="section-card")(>(\s*<div class="section-header">.*?<div class="section-title"><i[^>]*></i>\s*' + re.escape(title) + r'</div>))', re.DOTALL)
    m = pattern.search(text)
    if m:
        text = text[:m.start(1)] + f'<div class="section-card" id="{sec_id}"' + text[m.end(1):]
        print(f"Assigned id='{sec_id}' to section '{title}'")
    else:
        print(f"WARNING: Could not find section '{title}'")

# Save updated HTML
with open('SL-POP-ERP-SUMMARY-001.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved SL-POP-ERP-SUMMARY-001.html")
