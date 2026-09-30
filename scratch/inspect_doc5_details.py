with open('scratch/doc005_summary_overview.txt', 'r', encoding='utf-8') as f:
    text = f.read()

def get_section(title, length=1800):
    pos = text.find(title)
    if pos != -1:
        return text[pos:pos+length]
    return f"NOT FOUND: {title}"

print("=== AP & AR ===")
print(get_section("1.4.")[:800])
print("\n" + "="*50 + "\n")
print(get_section("1.5.")[:800])
print("\n" + "="*50 + "\n")

print("=== INVENTORY & BANKING ===")
print(get_section("2.1.")[:800])
print("\n" + "="*50 + "\n")
print(get_section("2.2.")[:800])
print("\n" + "="*50 + "\n")

print("=== BUDGETING, TAX & FX ===")
print(get_section("2.3.")[:800])
print("\n" + "="*50 + "\n")
print(get_section("2.4.")[:800])
print("\n" + "="*50 + "\n")
print(get_section("2.5.")[:800])
print("\n" + "="*50 + "\n")

print("=== FINANCIAL STATEMENTS & NEW BRANCH ===")
print(get_section("2.6.")[:800])
print("\n" + "="*50 + "\n")
print(get_section("3. NEW BRANCH SETUP")[:800])
