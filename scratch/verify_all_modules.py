import re

for i in range(1, 10):
    doc = f"SL-POP-ERP-MS-00{i}.html"
    with open(doc, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"=== Verification for {doc} ===")
    
    # 1. Check Master Budget Roadmap link
    has_roadmap_link = 'SL-POP-ERP-SUMMARY-001.html' in c
    print(f"  Master Budget Roadmap linked: {has_roadmap_link}")
    
    # 2. Check sidebar menu links and their target IDs
    nav_links = re.findall(r'<a[^>]*href="(#[^"]+)"', c)
    print(f"  Sidebar link hrefs: {nav_links}")
    missing_ids = []
    for h in nav_links:
        tid = h[1:]
        # search for id="tid" in html
        if not re.search(rf'id="{tid}"', c):
            missing_ids.append(tid)
    if missing_ids:
        print(f"  WARNING: Missing DOM elements for IDs: {missing_ids}")
    else:
        print(f"  PASS: All {len(nav_links)} sidebar target IDs found in DOM!")
        
    # 3. Check Universal ScrollSpy script presence
    has_spy = 'Universal High-Precision Scroll Spy' in c
    print(f"  Scroll Spy script installed: {has_spy}")
