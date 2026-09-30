import re

for doc in ['SL-POP-ERP-MS-001.html', 'SL-POP-ERP-MS-002.html', 'SL-POP-ERP-MS-003.html', 'SL-POP-ERP-MS-004.html', 'SL-POP-ERP-MS-005.html']:
    with open(doc, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"================ {doc} ================")
    # Look for sidebar html
    sidebar_match = re.search(r'(<ul class="sidebar-menu"[\s\S]*?</ul>|<nav class="sidebar-nav"[\s\S]*?</nav>)', c)
    if sidebar_match:
        print("Sidebar nav HTML snippet:\n", sidebar_match.group(0)[:300])
    else:
        print("NO SIDEBAR UL/NAV FOUND!")
    
    # Look for sections
    sec_tags = re.findall(r'<section [^>]*>', c)
    print(f"Total <section> tags: {len(sec_tags)}")
    for st in sec_tags[:5]:
        print("  ", st)
        
    # Look for active css
    active_css = re.findall(r'(\.sidebar[^{]*\.active[^{]*\{[^}]*\})', c)
    print("Active CSS rules:", active_css)
