with open('scratch/doc004_deep_dive.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect key areas
def find_section(kw):
    import re
    pos = text.lower().find(kw.lower())
    if pos != -1:
        return text[pos:pos+1500]
    return "NOT FOUND"

print("--- 1.3 CUSTOMER MASTER ---")
print(find_section("1.3. Customer Master Management")[:600])

print("\n--- 1.5 ITEM SEARCH & PRICING ---")
print(find_section("1.5. Item Identification")[:600])

print("\n--- 1.6 HANDHELD SALES ---")
print(find_section("1.6. Sales Process with Handheld")[:600])

print("\n--- 1.8 SALES RETURN ---")
print(find_section("1.8. Sales Return Management")[:600])

print("\n--- 1.15 SALES DOCUMENTS ---")
print(find_section("1.15. Sales Document Modules")[:600])

print("\n--- 1.16 ACCOUNTING DOCUMENTS ---")
print(find_section("1.16. Other Accounting Documents")[:600])

print("\n--- 1.17 FINANCIAL CONTROL ---")
print(find_section("1.17. Accounting & Branch Financial Control")[:600])

print("\n--- 1.18 DAILY CLOSING ---")
print(find_section("1.18. Daily Closing Process")[:600])
