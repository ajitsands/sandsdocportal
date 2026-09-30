import re

for i in range(1, 10):
    doc = f"SL-POP-ERP-MS-00{i}.html"
    with open(doc, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"=== Module {i}: {doc} ===")
    m = re.search(r'<ul class="sidebar-menu"[\s\S]*?</ul>', c)
    if m:
        links = re.findall(r'<a [^>]*href="([^"]+)"[^>]*>([\s\S]*?)</a>', m.group(0))
        for h, text in links:
            clean_text = re.sub(r'<[^>]+>', '', text).strip()
            print(f"  {h} -> {clean_text}")
    else:
        print("NO UL.SIDEBAR-MENU")
