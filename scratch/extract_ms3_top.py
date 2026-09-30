with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

# find from <style> to <div class="document-container">
pos_style = text.find('<style>')
pos_body = text.find('<body')
pos_container = text.find('<div class="document-container">')

with open('scratch/ms3_structure_top.html', 'w', encoding='utf-8') as out:
    out.write(text[pos_style:pos_container+500])

print("Saved structure to scratch/ms3_structure_top.html")
