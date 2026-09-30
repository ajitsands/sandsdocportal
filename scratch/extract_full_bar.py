with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Back to Portal')
if pos != -1:
    # Find start of tag
    start = text.rfind('<div', 0, pos)
    print("Found HTML around Back to Portal:")
    with open('scratch/portal_bar_extracted.html', 'w', encoding='utf-8') as out:
        out.write(text[start:pos+300])
    print("Saved to scratch/portal_bar_extracted.html")

# Also find CSS for the classes found
pos_css = text.find('web-action-right')
if pos_css != -1:
    print("Found CSS for web-action-right:")
    with open('scratch/portal_bar_css_extracted.css', 'w', encoding='utf-8') as out:
        out.write(text[pos_css-200:pos_css+600])
    print("Saved to scratch/portal_bar_css_extracted.css")
