import fitz

doc = fitz.open('scratch/temp_summary.pdf')
for p in range(min(6, len(doc))):
    page = doc[p]
    print(f"\n================ PAGE {p+1} ================")
    print("PAGE RECT:", page.rect)
    text = page.get_text()
    safe_text = text[:600].encode('ascii', errors='replace').decode('ascii')
    print("TEXT:\n", safe_text)
