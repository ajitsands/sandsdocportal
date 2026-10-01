import re

docs = [
    'SL-POP-ERP-MS-001.html',
    'SL-POP-ERP-MS-002.html',
    'SL-POP-ERP-MS-003.html',
    'SL-POP-ERP-MS-004.html',
    'SL-POP-ERP-MS-005.html',
    'SL-POP-ERP-MS-006.html'
]

for d in docs:
    with open(d, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"\n==================== {d} ====================")
    cards = re.findall(r'<div style="font-size: 11px; font-weight: 800; color: #0a2540; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">(.*?)</div>.*?<div style="margin-bottom: 8px;"[^>]*>\s*<span[^>]*>(.*?)</span>\s*</div>.*?<span class="signoff-status-badge[^"]*"[^>]*>(.*?)</span>', text, re.DOTALL)
    for role, badge, status in cards:
        # clean html inside badge
        badge_clean = re.sub(r'<[^>]+>', '', badge).strip()
        status_clean = re.sub(r'<[^>]+>', '', status).strip()
        print(f"  [{role.strip()}]: {badge_clean} | Status: {status_clean}")
