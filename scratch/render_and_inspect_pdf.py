import shutil
import subprocess
import os
import fitz # PyMuPDF

# 1. Sync HTML files
html_src = 'SL-POP-ERP-SUMMARY-001.html'
destinations = [
    'Executive_Master_Summary_and_Budget_Milestone.html',
    'popular/SL-POP-ERP-SUMMARY-001.html',
    'popular/Executive_Master_Summary_and_Budget_Milestone.html'
]

for d in destinations:
    shutil.copyfile(html_src, d)
    print(f"Copied {html_src} -> {d}")

# 2. Render PDF using Chrome headless
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

url = "http://localhost:8000/SL-POP-ERP-SUMMARY-001.html"
pdf_out = "SL-POP-ERP-SUMMARY-001.pdf"

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=5000",
    f"--print-to-pdf={pdf_out}",
    url
]

print("Rendering PDF with command:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome return code:", res.returncode)
if res.stderr:
    print("Chrome stderr:", res.stderr)

# Copy PDF to aliases
pdf_destinations = [
    'Executive_Master_Summary_and_Budget_Milestone.pdf',
    'popular/SL-POP-ERP-SUMMARY-001.pdf',
    'popular/Executive_Master_Summary_and_Budget_Milestone.pdf'
]
for pd in pdf_destinations:
    shutil.copyfile(pdf_out, pd)
    print(f"Copied {pdf_out} -> {pd}")

# 3. Inspect PDF pages with PyMuPDF
doc = fitz.open(pdf_out)
print(f"\n================ TOTAL PAGES: {len(doc)} ================")
for i, page in enumerate(doc):
    text = page.get_text()
    first_lines = [l.strip() for l in text.split('\n') if l.strip()][:4]
    print(f"\n--- PAGE {i+1} (Size: {page.rect.width:.1f} x {page.rect.height:.1f}) ---")
    print("First few lines:", first_lines)
    print(f"Text length: {len(text)} chars")
    
    # Render preview image
    pix = page.get_pixmap(dpi=150)
    pix.save(f"scratch/summary_page_{i+1}_preview.png")
    print(f"Saved preview: scratch/summary_page_{i+1}_preview.png")

