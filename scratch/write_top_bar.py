with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Back to Portal')
if pos != -1:
    with open('scratch/top_bar_full.html', 'w', encoding='utf-8') as out:
        out.write(text[pos-800:pos+300])
    print("Written to scratch/top_bar_full.html")
