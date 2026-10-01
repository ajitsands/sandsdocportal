with open('SL-POP-ERP-MS-001.html', 'r', encoding='utf-8') as f:
    text1 = f.read()

idx1 = text1.find('id="sec-signoff"')
if idx1 != -1:
    print("=== SL-POP-ERP-MS-001.html Signoff Section ===")
    print(text1[idx1:idx1+4000])

with open('SL-POP-ERP-SUMMARY-001.html', 'r', encoding='utf-8') as f:
    text_sum = f.read()

idx_sum = text_sum.find('id="sec-signoff"')
if idx_sum != -1:
    print("\n=== SL-POP-ERP-SUMMARY-001.html Signoff Section ===")
    print(text_sum[idx_sum:idx_sum+4000])
