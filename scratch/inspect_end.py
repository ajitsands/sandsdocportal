import sys

with open('build_documents.py', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
for line in lines[-80:]:
    print(line.encode('ascii', 'replace').decode('ascii'))
