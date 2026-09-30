import re, glob

for i in range(1, 10):
    doc = f"SL-POP-ERP-MS-00{i}.html"
    with open(doc, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"=== Module {i}: {doc} ===")
    nav_links = re.findall(r'<div class="sidebar[^"]*"[\s\S]*?</div>\s*</div>', c)
    # find sidebar links classes and hrefs
    links = re.findall(r'<a\s+[^>]*href="([^"]+)"[^>]*>', c)
    print("Links in doc:", [l for l in links if l.startswith('#')])
    # find sections and classes
    secs = re.findall(r'<(?:section|div)\s+[^>]*id="([^"]+)"[^>]*class="([^"]+)"', c)
    print("Sections with IDs & Classes:", [(s[0], s[1]) for s in secs if s[0].startswith('sec-') or s[0] in ['executive-summary', 'module-scope', 'pricing-matrix', 'detailed-milestones', 'payment-schedule', 'governance-sla', 'digital-signoff']])
    # Check script
    scr = re.search(r'// Smooth Scroll Spy[\s\S]*?(?=// Signature Pad|\Z)', c)
    print("Has script:", bool(scr))
