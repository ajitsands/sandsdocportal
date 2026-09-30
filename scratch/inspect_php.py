with open('build_documents.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect the PHP backend part at the start of html_content
pos_php = text.find('<?php')
pos_end_php = text.find('?>', pos_php)
print("PHP backend:")
print(text[pos_php:pos_end_php+2].encode('ascii', 'replace').decode('ascii'))
