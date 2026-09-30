import re

with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find header or portal bar in MS-003
start = text.find('<body')
end = text.find('</header>')
if start != -1 and end != -1:
    print("MS-003 Header HTML:")
    print(text[start:end+10])
else:
    # search for 'Back to Portal'
    pos = text.find('Back to Portal')
    if pos != -1:
        print("Found Back to Portal in MS-003:")
        print(text[pos-200:pos+300])
