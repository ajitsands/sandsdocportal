with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace lines 46-57
for i in range(len(lines)):
    if 'if (isset($pdo) && $pdo) {' in lines[i]:
        lines[i] = 'if (isset($pdo) && $pdo) {{\n'
    if lines[i].strip() == '}':
        # check if it's closing the if (isset($pdo) && $pdo) block
        if i > 40 and i < 60:
            lines[i] = '}}\n'

with open('build_sales_process_milestone.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed lines 46-57 in build_sales_process_milestone.py")
