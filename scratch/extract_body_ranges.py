with open('scratch/doc005_summary_overview.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by pages
pages = text.split('\n--- PAGE ')

print(f"Total parsed pages: {len(pages)-1}")

def get_page_range(start_p, end_p):
    res = []
    for i in range(start_p, min(end_p + 1, len(pages))):
        res.append(f"=== PAGE {i} ===\n" + pages[i])
    return '\n'.join(res)

with open('scratch/doc005_body_details.txt', 'w', encoding='utf-8') as out:
    out.write("### SECTION 1: SYSTEM PHILOSOPHY, COA, GL (Pages 5-11) ###\n")
    out.write(get_page_range(5, 11) + "\n\n")

    out.write("### SECTION 2: ACCOUNTS PAYABLE (Pages 12-14) ###\n")
    out.write(get_page_range(12, 14) + "\n\n")

    out.write("### SECTION 3: ACCOUNTS RECEIVABLE (Pages 15-20) ###\n")
    out.write(get_page_range(15, 20) + "\n\n")

    out.write("### SECTION 4: INVENTORY ACCOUNTING & BANKING/TREASURY (Pages 21-28) ###\n")
    out.write(get_page_range(21, 28) + "\n\n")

    out.write("### SECTION 5: BUDGETING, MULTI-CURRENCY, TAX & REPORTING (Pages 29-40) ###\n")
    out.write(get_page_range(29, 40) + "\n\n")

    out.write("### SECTION 6: NEW BRANCH SETUP GUIDELINE & CHECKLIST (Pages 41-51) ###\n")
    out.write(get_page_range(41, 51) + "\n\n")

print("Saved scratch/doc005_body_details.txt")
