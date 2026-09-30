import re

with open('scratch/doc004_deep_dive.txt', 'r', encoding='utf-8') as f:
    text = f.read()

def search_section(pattern, length=1200):
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    print(f"Pattern '{pattern}' found {len(matches)} matches:")
    for i, m in enumerate(matches):
        start = m.start()
        # Find which page this is in
        prev_page = text[:start].rfind('=== PAGE ')
        page_info = text[prev_page:start].split('\n')[0] if prev_page != -1 else 'Unknown'
        print(f"\n--- Match {i+1} ({page_info}) ---")
        print(text[start:start+length])
        print("="*60)

with open('scratch/section_details.txt', 'w', encoding='utf-8') as out:
    for s_num in ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '1.10', '1.11', '1.12', '1.13', '1.14', '1.15', '1.16', '1.17', '1.18', '1.19', '1.20', '1.21']:
        matches = list(re.finditer(rf'(?:^|\n)({s_num}\.?\s+[^\n]+)', text))
        out.write(f"\n############################################################\n")
        out.write(f"### SECTION {s_num}\n")
        out.write(f"############################################################\n\n")
        for m in matches:
            start = m.start()
            # print up to 4000 characters
            out.write(text[start:start+3500] + "\n\n--------------------------------------------\n\n")

print("Section details written to scratch/section_details.txt")
