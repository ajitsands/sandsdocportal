import os, re, glob, subprocess, sqlite3, shutil

BASE_DIR = r'e:\PopularMileStones'

UNIVERSAL_SCROLLSPY_SCRIPT = """
  <script>
    // Universal High-Precision Scroll Spy for Navigation
    function initScrollSpy() {
      const navLinks = document.querySelectorAll('.sidebar-menu li a, .sidebar-menu a');
      if (!navLinks || navLinks.length === 0) return;

      const targetSections = [];
      navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('#') && href.length > 1) {
          try {
            const targetEl = document.querySelector(href);
            if (targetEl) {
              targetSections.push({ link: link, el: targetEl });
            }
          } catch(e) {}
        }
      });

      if (targetSections.length === 0) return;

      function onScroll() {
        const scrollY = window.pageYOffset || document.documentElement.scrollTop || window.scrollY || 0;
        let activeLink = null;

        for (let i = 0; i < targetSections.length; i++) {
          const item = targetSections[i];
          const rect = item.el.getBoundingClientRect();
          const topOffset = rect.top + scrollY;
          if (scrollY >= topOffset - 180) {
            activeLink = item.link;
          }
        }

        if (!activeLink && targetSections.length > 0) {
          activeLink = targetSections[0].link;
        }

        if ((window.innerHeight + scrollY) >= (document.documentElement.scrollHeight - 60) && targetSections.length > 0) {
          activeLink = targetSections[targetSections.length - 1].link;
        }

        navLinks.forEach(l => l.classList.remove('active'));
        if (activeLink) {
          activeLink.classList.add('active');
        }
      }

      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll, { passive: true });
      setTimeout(onScroll, 100);
      onScroll();
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initScrollSpy);
    } else {
      initScrollSpy();
    }
"""

def update_module_1_to_3(filepath, mod_num, mod_code, mod_title):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update web-action-bar right side to include Master Budget Roadmap button
    if 'Master Budget Roadmap' not in content:
        old_action_right = re.search(r'<div class="web-action-right">([\s\S]*?)</div>', content)
        if old_action_right:
            new_btn = """<div class="web-action-right">
      <a href="SL-POP-ERP-SUMMARY-001.html" class="btn btn-accent" style="margin-right: 6px; font-weight: 700;">
        <i class="fa-solid fa-layer-group"></i> Master Budget Roadmap
      </a>"""
            content = content.replace(old_action_right.group(0), new_btn + old_action_right.group(1).strip() + "\n    </div>")

    # 2. Add Master Portfolio Box inside sidebar if not present
    if 'sidebar-portal-box' not in content:
        sidebar_menu_end = re.search(r'</ul>\s*</aside>', content)
        if sidebar_menu_end:
            portal_box = """</ul>

      <div class="sidebar-portal-box" style="margin-top: 20px; padding: 14px; background: #f8fafc; border: 1px solid var(--gray-200); border-radius: var(--radius-md); display: flex; flex-direction: column; gap: 8px;">
        <div style="font-size: 11px; font-weight: 700; color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.5px;">
          <i class="fa-solid fa-layer-group"></i> Master Portfolio
        </div>
        <a href="SL-POP-ERP-SUMMARY-001.html" class="btn btn-accent" style="font-size: 11.5px; padding: 7px 10px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 6px; width: 100%;">
          <i class="fa-solid fa-chart-pie"></i> Master Budget Roadmap
        </a>
        <a href="index.php" class="btn btn-outline" style="font-size: 11px; padding: 6px 10px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 6px; width: 100%; color: var(--gray-700);">
          <i class="fa-solid fa-arrow-left"></i> Return to Portal
        </a>
      </div>
    </aside>"""
            content = content.replace(sidebar_menu_end.group(0), portal_box)

    # 3. Add universal scroll spy script before closing </script>
    if 'Universal High-Precision Scroll Spy' not in content:
        content = content.replace('<script>', UNIVERSAL_SCROLLSPY_SCRIPT)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated M{mod_num}: {filepath}")

def update_modules_4_to_9(filepath, mod_num, mod_code):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update top bar or action bar to link Master Budget Roadmap
    if 'Master Budget Roadmap' not in content:
        # Check for web-action-bar or doc-top-bar buttons
        top_btn = """<a href="SL-POP-ERP-SUMMARY-001.html" class="btn btn-accent" style="margin-right: 6px; font-weight: 700;">
        <i class="fas fa-layer-group"></i> Master Budget Roadmap
      </a>"""
        if '<div class="web-action-right">' in content:
            content = content.replace('<div class="web-action-right">', '<div class="web-action-right">\n      ' + top_btn)
        elif '<div class="doc-top-bar-right"' in content or '<div class="top-bar-actions"' in content:
            content = re.sub(r'(<div class="(?:doc-top-bar-right|top-bar-actions)"[^>]*>)', r'\1\n      ' + top_btn, content)

    # 2. Update sidebar-card or sidebar to include Master Budget Roadmap link
    if 'sidebar-card' in content and 'SL-POP-ERP-SUMMARY-001.html' not in content:
        summary_link = """<a href="SL-POP-ERP-SUMMARY-001.html" class="btn btn-accent" style="width: 100%; margin-top: 10px; padding: 8px 12px; font-size: 11.5px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 6px;">
          <i class="fas fa-layer-group"></i> Master Budget Roadmap
        </a>"""
        content = re.sub(r'(<button class="btn btn-primary"[^>]*onclick="window\.print\(\)"[^>]*>)', summary_link + '\n        \\1', content)

    # 3. Replace old scroll spy with universal scroll spy
    old_scroll_pattern = re.search(r'// Smooth Scroll Spy for Navigation[\s\S]*?(?=// Signature Pad|\Z)', content)
    if old_scroll_pattern:
        content = content.replace(old_scroll_pattern.group(0), UNIVERSAL_SCROLLSPY_SCRIPT.replace('<script>', ''))
    elif 'Universal High-Precision Scroll Spy' not in content:
        content = content.replace('<script>', UNIVERSAL_SCROLLSPY_SCRIPT)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated M{mod_num}: {filepath}")

# Update M1-M3
update_module_1_to_3(os.path.join(BASE_DIR, 'SL-POP-ERP-MS-001.html'), 1, 'SL-POP-ERP-MS-001', 'PCode Generation')
update_module_1_to_3(os.path.join(BASE_DIR, 'PCode_Milestone_and_Payment_Structure.html'), 1, 'SL-POP-ERP-MS-001', 'PCode Generation')

update_module_1_to_3(os.path.join(BASE_DIR, 'SL-POP-ERP-MS-002.html'), 2, 'SL-POP-ERP-MS-002', 'Vendor & Purchase')
update_module_1_to_3(os.path.join(BASE_DIR, 'Vendor_Purchase_Milestone_and_Payment_Structure.html'), 2, 'SL-POP-ERP-MS-002', 'Vendor & Purchase')

update_module_1_to_3(os.path.join(BASE_DIR, 'SL-POP-ERP-MS-003.html'), 3, 'SL-POP-ERP-MS-003', 'Store Verification')
update_module_1_to_3(os.path.join(BASE_DIR, 'Store_Verification_Milestone_and_Payment_Structure.html'), 3, 'SL-POP-ERP-MS-003', 'Store Verification')

# Update M4-M9
for i in range(4, 10):
    doc_code = f"SL-POP-ERP-MS-00{i}"
    doc_path = os.path.join(BASE_DIR, f"{doc_code}.html")
    if os.path.exists(doc_path):
        update_modules_4_to_9(doc_path, i, doc_code)

for alias in ['Sales_Process_Milestone_and_Payment_Structure.html',
              'Accounts_Milestone_and_Payment_Structure.html',
              'Administration_Milestone_and_Payment_Structure.html',
              'Human_Resource_Management_Milestone_and_Payment_Structure.html',
              'Hardware_and_Server_Setup_Milestone_and_Payment_Structure.html']:
    alias_path = os.path.join(BASE_DIR, alias)
    if os.path.exists(alias_path):
        update_modules_4_to_9(alias_path, 0, alias)

# Sync all to popular/
for f in glob.glob(os.path.join(BASE_DIR, 'SL-POP-ERP-MS-*.html')) + glob.glob(os.path.join(BASE_DIR, '*_Milestone_and_Payment_Structure.html')):
    fname = os.path.basename(f)
    shutil.copyfile(f, os.path.join(BASE_DIR, 'popular', fname))

print("All HTML files updated and synced.")
