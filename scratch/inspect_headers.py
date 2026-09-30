import glob, re, sys

sys.stdout.reconfigure(encoding='utf-8')

for f in sorted(glob.glob('SL-POP-ERP-MS-*.html')):
    content = open(f, encoding='utf-8').read()
    m_bar = re.search(r'<div class="web-action-bar">.*?</div>\s*</div>', content, re.DOTALL)
    print(f"=== {f} ===")
    if m_bar:
        print("ACTION BAR:")
        print(m_bar.group(0))
    
    m_hdr = re.search(r'<header class="doc-top-bar">.*?</header>', content, re.DOTALL)
    if not m_hdr:
        m_hdr = re.search(r'<div class="doc-top-bar">.*?</div>\s*</div>', content, re.DOTALL)
    if m_hdr:
        clean_hdr = re.sub(r'data:image/[^"]+', '...', m_hdr.group(0))
        print("HEADER:")
        print(clean_hdr)
    print("-" * 50)
