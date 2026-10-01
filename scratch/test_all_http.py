import urllib.request

urls = [
    'http://localhost:8000/index.php',
    'http://localhost:8000/SL-POP-ERP-SUMMARY-001.html',
    'http://localhost:8000/SL-POP-ERP-ARCH-001.html',
    'http://localhost:8000/SL-POP-ERP-MS-001.html',
    'http://localhost:8000/SL-POP-ERP-MS-002.html',
    'http://localhost:8000/SL-POP-ERP-MS-003.html',
    'http://localhost:8000/SL-POP-ERP-MS-004.html',
    'http://localhost:8000/SL-POP-ERP-MS-005.html',
    'http://localhost:8000/SL-POP-ERP-MS-006.html',
    'http://localhost:8000/SL-POP-ERP-MS-007.html',
    'http://localhost:8000/SL-POP-ERP-MS-008.html',
    'http://localhost:8000/SL-POP-ERP-MS-009.html',
    'http://localhost:8000/Internal_Resource_Pricing_Reference.html'
]

for u in urls:
    req = urllib.request.urlopen(u)
    content = req.read().decode('utf-8', errors='ignore')
    name = u.split('/')[-1]
    has_warning = 'Warning' in content or 'Undefined variable' in content
    print(f"{name:<45}: HTTP {req.status} | Warning={has_warning} | Size={len(content):,} bytes")
