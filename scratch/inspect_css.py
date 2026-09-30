with open('build_documents.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect the CSS and layout structure in build_documents.py
import re
css_match = re.search(r'<style>(.*?)</style>', text, re.DOTALL)
if css_match:
    print("CSS length:", len(css_match.group(1)))
    print("First 1500 chars of CSS:")
    print(css_match.group(1)[:1500].encode('ascii', 'replace').decode('ascii'))
