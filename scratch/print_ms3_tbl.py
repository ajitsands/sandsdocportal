import sys

with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Engineering Role')
if pos != -1:
    sys.stdout.buffer.write(text[pos-200:pos+1500].encode('utf-8'))
