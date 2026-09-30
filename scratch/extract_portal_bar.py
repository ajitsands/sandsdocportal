with open('build_store_verification_milestone.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos_bar = text.find('.web-portal-bar')
if pos_bar != -1:
    with open('scratch/ms3_portal_bar_css.txt', 'w', encoding='utf-8') as out:
        out.write(text[pos_bar-50:pos_bar+1500])
    print("Dumped portal bar CSS")

pos_html = text.find('class="web-portal-bar"')
if pos_html != -1:
    with open('scratch/ms3_portal_bar_html.txt', 'w', encoding='utf-8') as out:
        out.write(text[pos_html-50:pos_html+800])
    print("Dumped portal bar HTML")
