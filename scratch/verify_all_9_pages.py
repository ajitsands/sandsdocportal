import fitz

doc = fitz.open('SL-POP-ERP-SUMMARY-001.pdf')
print(f"Total pages: {len(doc)}")
for i, page in enumerate(doc):
    print(f"\n================ PAGE {i+1} ================")
    text = page.get_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    safe_lines = [l.encode('ascii', errors='replace').decode('ascii') for l in lines]
    print(f"Lines count: {len(lines)}, Total characters: {len(text)}")
    print("Header lines:", safe_lines[:3])
    print("Footer/bottom lines:", safe_lines[-3:])
