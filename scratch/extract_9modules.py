with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Master ERP Transformation Architecture')
if pos != -1:
    print("Found Master ERP Transformation Architecture in MS-003:")
    print(text[pos-200:pos+1500])
else:
    print("Not found by exact title")
