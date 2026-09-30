with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix unescaped try { in f-string
code = code.replace("try {\n        $meta_stmt", "try {{\n        $meta_stmt")
code = code.replace("if ($status_val === 'FINALIZED_AND_LOCKED') {\n            $is_locked = true;\n        }\n    } catch (Exception $e) {}",
                    "if ($status_val === 'FINALIZED_AND_LOCKED') {{\n            $is_locked = true;\n        }}\n    }} catch (Exception $e) {{}}")

# Also check any single { in the added CSS
code = code.replace(".web-action-bar {\n", ".web-action-bar {{\n")
code = code.replace(".web-action-left {\n", ".web-action-left {{\n")
code = code.replace(".portal-branding {\n", ".portal-branding {{\n")
code = code.replace(".web-action-right {\n", ".web-action-right {{\n")
code = code.replace(".badge-accent {\n", ".badge-accent {{\n")
code = code.replace(".badge-success {\n", ".badge-success {{\n")

with open('build_sales_process_milestone.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed braces in build_sales_process_milestone.py")
