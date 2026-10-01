with open('SL-POP-ERP-MS-001.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Engineering Preparation & Stakeholder Verification Matrix')
if idx != -1:
    print(text[idx:idx+3500])
