with open('index.php', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('DOCUMENT 1')
if pos != -1:
    print(text[pos:pos+4000].encode('ascii', 'replace').decode('ascii'))
