import shutil
import subprocess
import os
import fitz

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

# 2. Render PDF using Chrome headless to scratch/temp_summary.pdf
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

url = "http://localhost:8000/SL-POP-ERP-SUMMARY-001.html"
temp_pdf = os.path.abspath("scratch/temp_summary.pdf")

if os.path.exists(temp_pdf):
    try:
        os.remove(temp_pdf)
    except Exception as e:
        print("Could not remove temp PDF:", e)

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=6000",
    f"--print-to-pdf={temp_pdf}",
    url
]

print("Rendering PDF with command:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome return code:", res.returncode)

if not os.path.exists(temp_pdf):
    print("ERROR: temp_pdf was not created!")
else:
    print(f"Temp PDF created successfully, size: {os.path.getsize(temp_pdf)} bytes")

    # Copy to target PDFs
    pdf_destinations = [
        'SL-POP-ERP-SUMMARY-001.pdf',
        'Executive_Master_Summary_and_Budget_Milestone.pdf',
        'popular/SL-POP-ERP-SUMMARY-001.pdf',
        'popular/Executive_Master_Summary_and_Budget_Milestone.pdf'
    ]
    for pd in pdf_destinations:
        try:
            shutil.copyfile(temp_pdf, pd)
            print(f"Copied {temp_pdf} -> {pd}")
        except Exception as e:
            print(f"Error copying to {pd}: {e}")

    # Inspect pages
    doc = fitz.open(temp_pdf)
    print(f"\n================ TOTAL PAGES: {len(doc)} ================")
    for i, page in enumerate(doc):
        text = page.get_text()
        first_lines = [l.strip() for l in text.split('\n') if l.strip()][:4]
        # Clean unicode for safe printing
        safe_lines = [l.encode('ascii', errors='replace').decode('ascii') for l in first_lines]
        print(f"\n--- PAGE {i+1} (Size: {page.rect.width:.1f} x {page.rect.height:.1f}) ---")
        print("First few lines:", safe_lines)
        print(f"Text length: {len(text)} chars")
        
        pix = page.get_pixmap(dpi=150)
        pix.save(f"scratch/summary_page_{i+1}_preview.png")
        print(f"Saved preview: scratch/summary_page_{i+1}_preview.png")

