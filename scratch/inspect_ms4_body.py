with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos_body = text.find('<body>')
print("After <body>:")
print(text[pos_body:pos_body+600])
