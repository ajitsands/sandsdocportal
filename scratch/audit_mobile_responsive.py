import glob, re, os

files = sorted(glob.glob('*.html') + ['index.php'] + glob.glob('popular/*.html') + ['popular/index.php'])

print(f"{'File':<55} | {'Viewport':<8} | {'@media':<7} | {'Scrollable Tables'}")
print("-" * 90)

for f in files:
    content = open(f, encoding='utf-8').read()
    has_viewport = 'name="viewport"' in content.lower()
    media_count = len(re.findall(r'@media\s*\([^{]+?\)', content))
    has_overflow = 'overflow-x' in content or 'table-container' in content or 'table-responsive' in content
    print(f"{f:<55} | {str(has_viewport):<8} | {media_count:<7} | {str(has_overflow)}")
