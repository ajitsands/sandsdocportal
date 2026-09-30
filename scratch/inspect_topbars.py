import re

for doc in ['SL-POP-ERP-MS-001.html', 'SL-POP-ERP-MS-002.html', 'SL-POP-ERP-MS-003.html', 'SL-POP-ERP-MS-004.html', 'SL-POP-ERP-SUMMARY-001.html']:
    with open(doc, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"================ {doc} ================")
    # Top bar
    top_bar = re.search(r'<div class="doc-top-bar"[\s\S]*?</header>|<div class="doc-top-bar"[\s\S]*?</div>\s*</div>', c)
    if top_bar:
        print("Top bar snippet:\n", top_bar.group(0)[:300])
    
    # Sidebar quick links / buttons
    sidebar_card = re.search(r'<div class="sidebar-card"[\s\S]*?</div>\s*</aside>', c)
    if sidebar_card:
        print("Sidebar card snippet:\n", sidebar_card.group(0)[:300])
