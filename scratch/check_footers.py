import glob, os, re

files = glob.glob('SL-POP-ERP-*.html') + glob.glob('*_Milestone_and_Payment_Structure.html') + ['Executive_Master_Summary_and_Budget_Milestone.html']
files += [os.path.join('popular', f) for f in files]

for f in sorted(set(files)):
    if not os.path.exists(f): continue
    content = open(f, encoding='utf-8').read()
    
    # Find all footer-like matches
    footers = [m.start() for m in re.finditer(r'(?:<footer|class=["\']doc-footer["\'])', content)]
    # Find all signoff matches
    signoffs = [m.start() for m in re.finditer(r'(?:id=["\']sec-signoff["\']|class=["\'][^"\']*signoff-section[^"\']*["\'])', content)]
    
    print(f"{f}:")
    print(f"   Signoffs at: {signoffs}")
    print(f"   Footers at:  {footers}")
    if signoffs and footers:
        if max(signoffs) > min(footers):
            print(f"   --> WARNING: Signoff is AFTER footer in {f}!")
