with open('build_documents.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos_m = text.find('/* Milestone Detailed Box */')
pos_end_m = text.find('/* Litigation Clause Box */', pos_m)
if pos_m != -1 and pos_end_m != -1:
    print(text[pos_m:pos_end_m].encode('ascii', 'replace').decode('ascii'))
else:
    pos_m = text.find('.milestone-card')
    print(text[pos_m:pos_m+2000].encode('ascii', 'replace').decode('ascii'))
