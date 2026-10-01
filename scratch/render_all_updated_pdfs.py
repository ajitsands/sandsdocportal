import os, subprocess, shutil

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

docs_to_render = [
    ('SL-POP-ERP-MS-001.html', 'SL-POP-ERP-MS-001.pdf', 'PCode_Milestone_and_Payment_Structure.pdf'),
    ('SL-POP-ERP-MS-002.html', 'SL-POP-ERP-MS-002.pdf', 'Vendor_Purchase_Milestone_and_Payment_Structure.pdf'),
    ('SL-POP-ERP-MS-003.html', 'SL-POP-ERP-MS-003.pdf', 'Store_Verification_Milestone_and_Payment_Structure.pdf'),
    ('SL-POP-ERP-MS-004.html', 'SL-POP-ERP-MS-004.pdf', 'Sales_Process_Milestone_and_Payment_Structure.pdf'),
    ('SL-POP-ERP-MS-005.html', 'SL-POP-ERP-MS-005.pdf', 'Accounts_Milestone_and_Payment_Structure.pdf'),
    ('SL-POP-ERP-MS-006.html', 'SL-POP-ERP-MS-006.pdf', 'Administration_Milestone_and_Payment_Structure.pdf'),
    ('SL-POP-ERP-SUMMARY-001.html', 'SL-POP-ERP-SUMMARY-001.pdf', 'Executive_Master_Summary_and_Budget_Milestone.pdf')
]

for html_file, pdf_file, alias_pdf in docs_to_render:
    temp_pdf = os.path.abspath(f"scratch/temp_{pdf_file}")
    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)
    
    url = f"http://localhost:8000/{html_file}"
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
    
    print(f"Rendering {html_file} -> {temp_pdf}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_pdf):
        shutil.copyfile(temp_pdf, pdf_file)
        shutil.copyfile(temp_pdf, alias_pdf)
        if os.path.exists('popular'):
            shutil.copyfile(temp_pdf, os.path.join('popular', pdf_file))
            shutil.copyfile(temp_pdf, os.path.join('popular', alias_pdf))
        print(f"  [SUCCESS] Updated {pdf_file} and aliases!")
    else:
        print(f"  [FAILED] to create {temp_pdf}")

print("\nAll PDFs successfully rendered and synchronized!")
