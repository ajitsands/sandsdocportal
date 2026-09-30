import fitz, os

doc = fitz.open('Docs/DOC-005_v1.0_-_Accounts.pdf')
page_count = len(doc)
print(f"Total Pages in DOC-005: {page_count}")

with open('scratch/doc_005_text.txt', 'w', encoding='utf-8') as f:
    for i, page in enumerate(doc):
        f.write(f"=== PAGE {i+1} ===\n")
        f.write(page.get_text() + "\n\n")

print("Saved scratch/doc_005_text.txt")
