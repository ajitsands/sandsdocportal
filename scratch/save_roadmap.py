with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Master ERP Transformation Architecture')
end = text.find('</div>', pos + 1000)

with open('scratch/roadmap_full.html', 'w', encoding='utf-8') as out:
    out.write(text[pos-100:pos+1500])

print("Saved to scratch/roadmap_full.html")
