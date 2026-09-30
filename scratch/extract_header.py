with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Back to Portal')
if pos != -1:
    # find enclosing element or top bar
    start_tag = text.rfind('<div', 0, pos)
    if start_tag == -1:
        start_tag = text.rfind('<header', 0, pos)
    
    with open('scratch/ms3_header_sample.html', 'w', encoding='utf-8') as out:
        out.write(text[start_tag-300:pos+800])
    print("Dumped to scratch/ms3_header_sample.html")
