import sys

with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('Section 3.0')
if start != -1:
    sys.stdout.buffer.write(text[start:start+2200].encode('utf-8'))
