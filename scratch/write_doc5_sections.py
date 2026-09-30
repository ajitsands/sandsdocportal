import sys

with open('scratch/doc005_summary_overview.txt', 'r', encoding='utf-8') as f:
    text = f.read()

def get_section(title, length=1800):
    pos = text.find(title)
    if pos != -1:
        return text[pos:pos+length]
    return f"NOT FOUND: {title}"

with open('scratch/doc005_sections_view.txt', 'w', encoding='utf-8') as out:
    out.write("=== AP & AR ===\n")
    out.write(get_section("1.4.") + "\n\n" + "="*50 + "\n\n")
    out.write(get_section("1.5.") + "\n\n" + "="*50 + "\n\n")

    out.write("=== INVENTORY & BANKING ===\n")
    out.write(get_section("2.1.") + "\n\n" + "="*50 + "\n\n")
    out.write(get_section("2.2.") + "\n\n" + "="*50 + "\n\n")

    out.write("=== BUDGETING, TAX & FX ===\n")
    out.write(get_section("2.3.") + "\n\n" + "="*50 + "\n\n")
    out.write(get_section("2.4.") + "\n\n" + "="*50 + "\n\n")
    out.write(get_section("2.5.") + "\n\n" + "="*50 + "\n\n")

    out.write("=== FINANCIAL STATEMENTS & NEW BRANCH ===\n")
    out.write(get_section("2.6.") + "\n\n" + "="*50 + "\n\n")
    out.write(get_section("3.") + "\n\n" + "="*50 + "\n\n")

print("Saved scratch/doc005_sections_view.txt")
