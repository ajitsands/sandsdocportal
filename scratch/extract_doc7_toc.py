import re

with open('scratch/doc_007_text.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

pages = text.split('=== PAGE ')

with open('scratch/doc_007_toc.txt', 'w', encoding='utf-8') as out:
    for i in range(1, min(10, len(pages))):
        out.write(f"--- PAGE {i} ---\n")
        out.write(pages[i] + "\n\n")

print("Saved first 10 pages to scratch/doc_007_toc.txt")
