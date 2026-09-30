with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Back to Portal')
if pos != -1:
    print(text[pos-800:pos+200])
