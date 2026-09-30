with open('SL-POP-ERP-MS-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Master ERP Transformation Architecture')
if pos != -1:
    print(text[pos:pos+3000].encode('ascii', 'replace').decode('ascii'))
