import re

for doc in ['SL-POP-ERP-MS-001.html', 'SL-POP-ERP-MS-002.html', 'SL-POP-ERP-MS-003.html', 'SL-POP-ERP-MS-004.html', 'SL-POP-ERP-MS-005.html', 'SL-POP-ERP-SUMMARY-001.html']:
    try:
        with open(doc, 'r', encoding='utf-8') as fp:
            c = fp.read()
        print(f"================ {doc} ================")
        sidebar_links = re.findall(r'<a href="([^"]+)"[^>]*class="[^"]*nav-item', c) or re.findall(r'<li[^>]*><a href="([^"]+)"', c)
        print("Sidebar hrefs:", sidebar_links)
        
        # Check what elements have IDs matching those hrefs
        for href in sidebar_links:
            if href.startswith('#'):
                target_id = href[1:]
                found_tag = re.findall(rf'<([a-zA-Z0-9]+)[^>]*id="{target_id}"', c)
                found_class = re.findall(rf'<[a-zA-Z0-9]+[^>]*id="{target_id}"[^>]*class="([^"]+)"', c)
                print(f"  Href {href} -> Tag: {found_tag}, Class: {found_class}")
        
        # Check script
        script_match = re.search(r'// Smooth Scroll Spy[\s\S]*?(?=// Signature Pad|\Z)', c)
        if script_match:
            print("Scroll Spy Script:")
            print(script_match.group(0).strip())
        else:
            print("NO SCROLL SPY SCRIPT FOUND!")
    except Exception as e:
        print(f"Error checking {doc}: {e}")
