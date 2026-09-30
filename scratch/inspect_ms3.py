import re

with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    code = f.read()

nav_links = re.findall(r'<a href="#([^"]+)" class="nav-link[^"]*">\s*(?:<i[^>]*></i>\s*)?(.*?)\s*</a>', code)
print("Nav Links in MS-003:")
for n_id, n_title in nav_links:
    print(f"  #{n_id} -> {n_title}")

headers = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', code)
print("\nHeaders in MS-003:")
for h in headers[:25]:
    clean_h = re.sub(r'<[^>]+>', '', h).strip()
    print(f"  - {clean_h}")
