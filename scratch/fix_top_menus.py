import os, glob, re

# 1. Fix index.php to ensure $is_locked is always defined
index_path = 'index.php'
if os.path.exists(index_path):
    content = open(index_path, encoding='utf-8').read()
    if '$is_locked = $is_finalized;' not in content:
        content = content.replace(
            "$is_finalized = ($doc_status === 'FINALIZED_AND_LOCKED');",
            "$is_finalized = ($doc_status === 'FINALIZED_AND_LOCKED');\n    $is_locked = $is_finalized;"
        )
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated index.php with $is_locked definition.")

# 2. Fix HTML files in root and popular/
targets = [
    ('SL-POP-ERP-MS-004.html', '4', 'DOC-004'),
    ('SL-POP-ERP-MS-005.html', '5', 'DOC-005'),
    ('SL-POP-ERP-MS-006.html', '6', 'DOC-006'),
    ('SL-POP-ERP-MS-007.html', '7', 'DOC-007'),
    ('SL-POP-ERP-MS-008.html', '8', 'ARCH-001'),
    ('SL-POP-ERP-MS-009.html', '9', 'DOC-009'),
    ('Sales_Process_Milestone_and_Payment_Structure.html', '4', 'DOC-004'),
    ('Accounts_Milestone_and_Payment_Structure.html', '5', 'DOC-005'),
    ('Administration_Milestone_and_Payment_Structure.html', '6', 'DOC-006'),
    ('Human_Resource_Management_Milestone_and_Payment_Structure.html', '7', 'DOC-007'),
    ('Hardware_and_Server_Setup_Milestone_and_Payment_Structure.html', '8', 'ARCH-001'),
    ('SL-POP-ERP-SUMMARY-001.html', 'Summary', 'EXEC-SUMMARY'),
    ('Executive_Master_Summary_and_Budget_Milestone.html', 'Summary', 'EXEC-SUMMARY')
]

directories = ['.', 'popular']

for d in directories:
    for filename, mod_num, ba_ref in targets:
        filepath = os.path.join(d, filename)
        if not os.path.exists(filepath):
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Replace the <?php if ($is_locked): ?> block in web-action-bar
        pattern_locked = r'<\?php\s+if\s*\(\$is_locked\):\s*\?>.*?<\?php\s+endif;\s*\?>'
        replacement_badge = '<span class="badge badge-accent">📝 IN ACTIVE REVIEW</span>'
        html = re.sub(pattern_locked, replacement_badge, html, flags=re.DOTALL)
        
        # Fix wrong module badges in header
        if mod_num != 'Summary':
            # Fix module number badge e.g. Module 6 / 9 -> Module 7 / 9
            html = re.sub(
                r'<span class="badge-tag badge-primary"><i class="fas fa-layer-group"></i> Module \d / 9</span>',
                f'<span class="badge-tag badge-primary"><i class="fas fa-layer-group"></i> Module {mod_num} / 9</span>',
                html
            )
            # Fix BA Ref badge
            html = re.sub(
                r'<span class="badge-tag badge-success"><i class="fas fa-check-double"></i> Verified BA Ref: [^<]+</span>',
                f'<span class="badge-tag badge-success"><i class="fas fa-check-double"></i> Verified BA Ref: {ba_ref}</span>',
                html
            )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Fixed {filepath}")

# Also check for any remaining $is_locked in any html file
all_html = glob.glob('*.html') + glob.glob('popular/*.html')
for h in all_html:
    txt = open(h, encoding='utf-8').read()
    if '<?php if ($is_locked): ?>' in txt:
        print(f"WARNING: still found $is_locked in {h}")
        txt = re.sub(r'<\?php\s+if\s*\(\$is_locked\):\s*\?>.*?<\?php\s+endif;\s*\?>', '<span class="badge badge-accent">📝 IN ACTIVE REVIEW</span>', txt, flags=re.DOTALL)
        with open(h, 'w', encoding='utf-8') as f:
            f.write(txt)
        print(f"Cleaned {h}")

print("All top menus and headers fixed successfully!")
