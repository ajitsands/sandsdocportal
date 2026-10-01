import os, glob

files = glob.glob('*.html') + glob.glob('popular/*.html') + glob.glob('*.py') + glob.glob('popular/*.py')

for f in files:
    content = open(f, encoding='utf-8').read()
    if 'Jira/Confluence' in content or 'Jira / Confluence' in content or 'Jira' in content or 'Confluence' in content:
        content_fixed = content.replace('Jira/Confluence', 'SaNDS Lab Portal')
        content_fixed = content_fixed.replace('Jira / Confluence', 'SaNDS Lab Portal')
        with open(f, 'w', encoding='utf-8') as out:
            out.write(content_fixed)
        print(f"Replaced Jira/Confluence in {f}")

print("Completed all replacements.")
