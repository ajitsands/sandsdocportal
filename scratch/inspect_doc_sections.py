with open('scratch/store_verification_doc_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect each major section in detail
print("=== COMPLETE SECTION BREAKDOWN ===")
import re
sections = [
    "1. Introduction",
    "2. Store Verification Process",
    "3. STOCK VERIFICATION PROCESS",
    "4. Risk Score Generation",
    "5. Stock Verification Summary",
    "6. Rack, Bin, and Location Numbering System",
    "7. Stock Transfer Management",
    "8. Damaged Stock Management",
    "9. Management Review Points",
    "10. Conclusion"
]

for sec in sections:
    pos = text.find(sec)
    if pos != -1:
        print(f"\n--- Found {sec} at char {pos} ---")
        print(text[pos:pos+1500].encode('ascii', 'replace').decode('ascii'))
