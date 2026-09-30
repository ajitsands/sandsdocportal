with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re

php_part = code[:code.find('<!DOCTYPE html>')]
print(f"PHP Backend lines: {len(php_part.splitlines())}")

# Check CSS classes
css_classes = re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{', code)
print(f"Total CSS classes: {len(set(css_classes))}")

# Check interactive scripts
scripts = re.findall(r'<script>(.*?)</script>', code, re.DOTALL)
print(f"Total script tags: {len(scripts)}")
