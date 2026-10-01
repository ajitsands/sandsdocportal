import os, re, subprocess, shutil

summary_builder = 'build_master_summary.py'
with open(summary_builder, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add CSS styles
old_css_anchor = """.currency-bhd {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--primary);
    }"""

new_css = """.currency-bhd {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--primary);
      white-space: nowrap;
    }

    .mod-doc-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: #0a2540;
      color: #38bdf8;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      white-space: nowrap;
      letter-spacing: 0.3px;
      box-shadow: 0 1px 2px rgba(10,37,64,0.15);
    }

    .mod-ba-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: #f1f5f9;
      color: #475569;
      font-size: 10.5px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 4px;
      border: 1px solid #e2e8f0;
      white-space: nowrap;
    }

    .mod-domain-title {
      font-size: 13.5px;
      font-weight: 700;
      color: #0a2540;
      line-height: 1.35;
      margin-top: 2px;
    }

    .gate-pill {
      display: inline-block;
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 11.5px;
      font-weight: 600;
      color: #334155;
      white-space: nowrap;
    }

    .share-badge {
      display: inline-block;
      background: #eff6ff;
      color: #1d4ed8;
      font-weight: 700;
      font-size: 11.5px;
      padding: 2px 8px;
      border-radius: 12px;
      border: 1px solid #dbeafe;
      white-space: nowrap;
    }"""

if old_css_anchor in code:
    code = code.replace(old_css_anchor, new_css)
    print("Updated CSS in build_master_summary.py")

# 2. Replace Section 2 Table
old_sec2_pattern = r'<!-- SECTION 2: Master Consolidated Milestone & Budget Table -->.*?<!-- SECTION 3:'
new_sec2 = """<!-- SECTION 2: Master Consolidated Milestone & Budget Table -->
    <div class="section-card">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-table-list"></i> Master 9-Module Budgeting & Milestone Matrix (BHD)</div>
          <div class="section-subtitle">At-a-glance comparative overview of all 9 modules, timelines, effort, deliverables, and total fees in Bahraini Dinars</div>
        </div>
        <span class="badge-success">All Amounts in Bahraini Dinars (BHD)</span>
      </div>

      <div class="table-container">
        <table class="master-table">
          <thead>
            <tr>
              <th style="width: 35px; text-align: center;">#</th>
              <th>Module Scope & Implementation Domain</th>
              <th>Timeline</th>
              <th>Effort</th>
              <th>Milestone Gates</th>
              <th>Total Cost (BHD)</th>
              <th>Weekly Burn</th>
              <th>Share (%)</th>
              <th style="text-align: center;">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">1</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-001</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-001 v1.0</span>
                </div>
                <div class="mod-domain-title">PCode Generation, Cataloguing & Item Master Engine</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">10 Weeks</span></td>
              <td>2.50 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 3,409.091</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">10.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-001.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">2</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-002</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-002 v1.0</span>
                </div>
                <div class="mod-domain-title">Vendor & Purchase Management, Supplier Portal & 3-Way Match</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">12 Weeks</span></td>
              <td>3.00 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 4,090.909</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">12.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-002.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">3</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-003</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-003 v1.0</span>
                </div>
                <div class="mod-domain-title">Store Verification, Multi-Warehouse Stock & Location Matrix</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">15 Weeks</span></td>
              <td>3.75 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 5,113.636</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">15.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-003.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">4</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-004</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-004 v1.0</span>
                </div>
                <div class="mod-domain-title">Sales Process, Mobile POS, Multi-Branch Billing & Return Control</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">15 Weeks</span></td>
              <td>3.75 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 5,113.636</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">15.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-004.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">5</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-005</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-005 v1.0</span>
                </div>
                <div class="mod-domain-title">Accounting & Financial Management, General Ledger, AP/AR & VAT</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">13 Weeks</span></td>
              <td>3.25 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 4,431.818</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">13.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-005.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">6</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-006</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-006 v1.0</span>
                </div>
                <div class="mod-domain-title">Enterprise Administration, Facility, Fixed Assets, Fleet & Vault</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">12 Weeks</span></td>
              <td>3.00 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 4,090.909</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">12.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-006.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">7</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-007</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-007 v1.0</span>
                </div>
                <div class="mod-domain-title">Human Resource Management, Biometrics, Leave, Payroll & Gratuity</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">16 Weeks</span></td>
              <td>4.00 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 5,454.548</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">16.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-007.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">8</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-008</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: ARCH-001 v1.0</span>
                </div>
                <div class="mod-domain-title">Hardware Setup, Handheld QR Devices, ESC/POS & Cloud Cluster</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">3 Weeks</span></td>
              <td>0.75 Mo</td>
              <td><span class="gate-pill">3 Gates (33%)</span></td>
              <td><span class="currency-bhd">BD 1,022.727</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">3.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-008.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
            <tr>
              <td style="text-align: center; font-weight: 800; color: #0a2540;">9</td>
              <td>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-009</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> BA Ref: DOC-009 v1.0</span>
                </div>
                <div class="mod-domain-title">Executive Management Dashboard, 8-Module BI & Mobile Cockpit</div>
              </td>
              <td><span style="font-weight: 600; color: #1e293b;">4 Weeks</span></td>
              <td>1.00 Mo</td>
              <td><span class="gate-pill">4 Gates (25%)</span></td>
              <td><span class="currency-bhd">BD 1,363.636</span></td>
              <td>BD 340.909</td>
              <td><span class="share-badge">4.00%</span></td>
              <td style="text-align: center;"><a href="SL-POP-ERP-MS-009.html" class="mod-link-btn" target="_blank">View <i class="fa-solid fa-arrow-up-right-from-square"></i></a></td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="2"><strong>GRAND TOTAL: COMPLETE 9-MODULE AUTOMOTIVE ERP PORTFOLIO</strong></td>
              <td><strong>88 Weeks</strong></td>
              <td><strong>17.60 Mo</strong></td>
              <td><strong>35 Gates</strong></td>
              <td><span class="currency-bhd" style="font-size: 15px; color: var(--accent-gold);">BD 34,090.910</span></td>
              <td><strong>BD 387.397</strong></td>
              <td><strong>100.00%</strong></td>
              <td style="text-align: center;"><strong>Full Suite</strong></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>

    <!-- SECTION 3:"""

code = re.sub(old_sec2_pattern, new_sec2, code, flags=re.DOTALL)
print("Updated Section 2 Table in build_master_summary.py")

# 3. Replace Section 4 Table
old_sec4_pattern = r'<!-- SECTION 4: Multi-Tier Payment Schedule Table -->.*?<!-- SECTION 5:'
new_sec4 = """<!-- SECTION 4: Multi-Tier Payment Schedule Table -->
    <div class="section-card">
      <div class="section-header">
        <div>
          <div class="section-title"><i class="fa-solid fa-receipt"></i> 4-Tranche Milestone Cash-Flow Disbursement Plan (BHD)</div>
          <div class="section-subtitle">25% Advance &bull; 25% Sprint Midpoint &bull; 25% Staging Demo &bull; 25% Production UAT Go-Live</div>
        </div>
        <span class="badge-accent">Grand Total: BD 34,090.910</span>
      </div>

      <div class="table-container">
        <table class="master-table">
          <thead>
            <tr>
              <th>Module Scope & Implementation Domain</th>
              <th>Total (BHD)</th>
              <th>Tranche 1 (BHD)</th>
              <th>Tranche 2 (BHD)</th>
              <th>Tranche 3 (BHD)</th>
              <th>Tranche 4 (BHD)</th>
              <th>Payment Milestone Trigger</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-001</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> DOC-001</span>
                </div>
                <div class="mod-domain-title" style="font-size: 12.5px;">PCode Generation Module</div>
              </td>
              <td><span class="currency-bhd">BD 3,409.091</span></td>
              <td>BD 852.273</td>
              <td>BD 852.273</td>
              <td>BD 852.273</td>
              <td>BD 852.273</td>
              <td>Demonstration & Staging Sign-Off</td>
            </tr>
            <tr>
              <td>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-002</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> DOC-002</span>
                </div>
                <div class="mod-domain-title" style="font-size: 12.5px;">Vendor & Purchase Module</div>
              </td>
              <td><span class="currency-bhd">BD 4,090.909</span></td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>Supplier Portal & 3-Way Match Verification</td>
            </tr>
            <tr>
              <td>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-003</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> DOC-003</span>
                </div>
                <div class="mod-domain-title" style="font-size: 12.5px;">Store Verification Module</div>
              </td>
              <td><span class="currency-bhd">BD 5,113.636</span></td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>Scanner Verification & Cycle Count UAT</td>
            </tr>
            <tr>
              <td>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-004</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> DOC-004</span>
                </div>
                <div class="mod-domain-title" style="font-size: 12.5px;">Sales Process & POS Module</div>
              </td>
              <td><span class="currency-bhd">BD 5,113.636</span></td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>BD 1,278.409</td>
              <td>Counter POS & Cash Drawer Closing UAT</td>
            </tr>
            <tr>
              <td>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-005</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> DOC-005</span>
                </div>
                <div class="mod-domain-title" style="font-size: 12.5px;">Accounts & VAT Module</div>
              </td>
              <td><span class="currency-bhd">BD 4,431.818</span></td>
              <td>BD 1,107.955</td>
              <td>BD 1,107.955</td>
              <td>BD 1,107.955</td>
              <td>BD 1,107.955</td>
              <td>GL Double-Entry & 10% VAT Return Sign-Off</td>
            </tr>
            <tr>
              <td>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-006</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> DOC-006</span>
                </div>
                <div class="mod-domain-title" style="font-size: 12.5px;">Enterprise Admin & Fleet</div>
              </td>
              <td><span class="currency-bhd">BD 4,090.909</span></td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>BD 1,022.727</td>
              <td>Asset QR Tagging & Fleet TCO Sign-Off</td>
            </tr>
            <tr>
              <td>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-007</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> DOC-007</span>
                </div>
                <div class="mod-domain-title" style="font-size: 12.5px;">HRM & Payroll Module</div>
              </td>
              <td><span class="currency-bhd">BD 5,454.548</span></td>
              <td>BD 1,363.637</td>
              <td>BD 1,363.637</td>
              <td>BD 1,363.637</td>
              <td>BD 1,363.637</td>
              <td>Biometric Sync & WPS CBB Bank Export UAT</td>
            </tr>
            <tr>
              <td>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-008</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> ARCH-001</span>
                </div>
                <div class="mod-domain-title" style="font-size: 12.5px;">Hardware & Cloud Setup</div>
              </td>
              <td><span class="currency-bhd">BD 1,022.727</span></td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>—</td>
              <td>3-Tier Cloud & Hardware Peripherals Setup</td>
            </tr>
            <tr>
              <td>
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; flex-wrap: wrap;">
                  <span class="mod-doc-badge">SL-POP-ERP-MS-009</span>
                  <span class="mod-ba-badge"><i class="fa-solid fa-file-contract"></i> DOC-009</span>
                </div>
                <div class="mod-domain-title" style="font-size: 12.5px;">Executive BI Dashboard</div>
              </td>
              <td><span class="currency-bhd">BD 1,363.636</span></td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>BD 340.909</td>
              <td>Cross-Module OLAP & Executive KPI Go-Live</td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td><strong>TOTAL TRANCHE COMMITMENTS</strong></td>
              <td><span class="currency-bhd" style="font-size: 14px;">BD 34,090.910</span></td>
              <td><strong>BD 8,522.728</strong></td>
              <td><strong>BD 8,522.728</strong></td>
              <td><strong>BD 8,522.728</strong></td>
              <td><strong>BD 8,522.726</strong></td>
              <td><strong>100% Verified Delivery</strong></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>

    <!-- SECTION 5:"""

code = re.sub(old_sec4_pattern, new_sec4, code, flags=re.DOTALL)
print("Updated Section 4 Table in build_master_summary.py")

with open(summary_builder, 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved updated build_master_summary.py successfully.")
