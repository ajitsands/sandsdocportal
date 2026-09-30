import re

path = 'build_tech_architecture.py'
content = open(path, encoding='utf-8').read()

# Wrap each arch-table with arch-table-wrap div
# Find pattern: indentation + <table class="arch-table">
# and close with </table> + </div>

# First: add opening wrapper before each <table class="arch-table">
content = content.replace(
    '        <table class="arch-table">',
    '        <div class="arch-table-wrap">\n        <table class="arch-table">'
)
content = content.replace(
    '      <table class="arch-table">',
    '      <div class="arch-table-wrap">\n      <table class="arch-table">'
)

# Close: add </div> after each </table> that follows arch-table
# Since all tables are arch-table, replace all </table> with </table>\n</div>
# But we need to match context. Use a temporary marker approach.
content = content.replace('</table>', '</table>\n        </div>', 3)

# Fix the finalized cert grid - replace inline style
old_style = 'display:grid; grid-template-columns:repeat(4, 1fr); gap:6px; font-size:7px; color:#14532d; line-height:1.35;'
content = content.replace(
    f'<div style="{old_style}">',
    '<div class="finalized-cert-grid">'
)

open(path, 'w', encoding='utf-8').write(content)
print('Done! arch-table wrapping and cert grid class applied successfully.')

# Verify
count = content.count('arch-table-wrap')
cert_fixed = 'finalized-cert-grid' in content
print(f'arch-table-wrap occurrences: {count}')
print(f'finalized-cert-grid class applied: {cert_fixed}')
