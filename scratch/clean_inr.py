import re

with open('build_sales_process_milestone.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Replace sidebar card
code = code.replace("<div><strong>INR Value:</strong> ₹ 1,125,000.00</div>", "<div><strong>Scope:</strong> Multi-Branch ERP</div>")

# 2. Replace hero card meta
code = code.replace("BD 5,113.636 (₹ 1,125,000)", "BD 5,113.636")

# 3. Replace Section 3 intro
old_sec3_intro = "In strict accordance with the <strong>SaNDS Lab Master Employee Rate Card</strong> (Conversion: 1 BHD = 220.00 INR), the dedicated engineering team allocated for the 15-week delivery of Module 4 is structured as follows:"
new_sec3_intro = "In strict accordance with the <strong>SaNDS Lab Dedicated Engineering Rate Card</strong>, the resource allocation and cost breakdown for the 15-week (3.75 months / 75 working days) delivery of Module 4 is structured as follows (all figures in Bahraini Dinars - BHD):"
code = code.replace(old_sec3_intro, new_sec3_intro)

# 4. Replace table headers & rows in Section 3
old_table = """          <table class="custom-table">
            <thead>
              <tr>
                <th>Engineering Role</th>
                <th>Monthly Rate (INR)</th>
                <th>Monthly Rate (BHD)</th>
                <th>Weekly Rate (BHD)</th>
                <th>Effort Allocation</th>
                <th>Total Cost (BHD)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Project Manager & Solution Architect</strong></td>
                <td>₹ 120,000</td>
                <td><strong>BD 545.455</strong></td>
                <td>BD 136.364</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 2,045.456</strong></td>
              </tr>
              <tr>
                <td><strong>Back-End Lead Engineer (PHP MVC / REST APIs)</strong></td>
                <td>₹ 50,000</td>
                <td><strong>BD 227.273</strong></td>
                <td>BD 56.818</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 852.274</strong></td>
              </tr>
              <tr>
                <td><strong>Front-End Lead Engineer (Mobile POS / React UI)</strong></td>
                <td>₹ 50,000</td>
                <td><strong>BD 227.273</strong></td>
                <td>BD 56.818</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 852.274</strong></td>
              </tr>
              <tr>
                <td><strong>Database & Cloud Infrastructure Architect</strong></td>
                <td>₹ 45,000</td>
                <td><strong>BD 204.545</strong></td>
                <td>BD 51.136</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 767.044</strong></td>
              </tr>
              <tr>
                <td><strong>QA & Test Automation Lead Engineer</strong></td>
                <td>₹ 35,000</td>
                <td><strong>BD 159.091</strong></td>
                <td>BD 39.773</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 596.591</strong></td>
              </tr>
              <tr class="total-row">
                <td><strong>Total Dedicated Engineering Team</strong></td>
                <td><strong>₹ 300,000 / mo</strong></td>
                <td><strong>BD 1,363.636 / mo</strong></td>
                <td><strong>BD 340.909 / wk</strong></td>
                <td><strong>15 Weeks (3.75 Mo)</strong></td>
                <td><strong>BD 5,113.636</strong></td>
              </tr>
            </tbody>
          </table>"""

new_table = """          <table class="custom-table">
            <thead>
              <tr>
                <th>Engineering Role</th>
                <th>Monthly Rate (BHD)</th>
                <th>Weekly Rate (BHD)</th>
                <th>Hourly Rate (160h/mo)</th>
                <th>Effort Allocation</th>
                <th>Total Cost (BHD)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Project Manager & Solution Architect</strong></td>
                <td><strong>BD 545.455</strong></td>
                <td>BD 136.364</td>
                <td>BD 3.409</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 2,045.456</strong></td>
              </tr>
              <tr>
                <td><strong>Back-End Lead Engineer (PHP MVC / REST APIs)</strong></td>
                <td><strong>BD 227.273</strong></td>
                <td>BD 56.818</td>
                <td>BD 1.420</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 852.274</strong></td>
              </tr>
              <tr>
                <td><strong>Front-End Lead Engineer (Mobile POS / React UI)</strong></td>
                <td><strong>BD 227.273</strong></td>
                <td>BD 56.818</td>
                <td>BD 1.420</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 852.274</strong></td>
              </tr>
              <tr>
                <td><strong>Database & Cloud Infrastructure Architect</strong></td>
                <td><strong>BD 204.545</strong></td>
                <td>BD 51.136</td>
                <td>BD 1.278</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 767.044</strong></td>
              </tr>
              <tr>
                <td><strong>QA & Test Automation Lead Engineer</strong></td>
                <td><strong>BD 159.091</strong></td>
                <td>BD 39.773</td>
                <td>BD 0.994</td>
                <td>3.75 Months (15 Wks)</td>
                <td><strong>BD 596.591</strong></td>
              </tr>
              <tr class="total-row">
                <td><strong>Total Dedicated Engineering Team</strong></td>
                <td><strong>BD 1,363.636 / mo</strong></td>
                <td><strong>BD 340.909 / wk</strong></td>
                <td><strong>BD 8.523 / hr</strong></td>
                <td><strong>15 Weeks (3.75 Mo)</strong></td>
                <td><strong>BD 5,113.636</strong></td>
              </tr>
            </tbody>
          </table>"""

code = code.replace(old_table, new_table)

# 5. Replace Fixed Price Guarantee Callout
old_callout = "Total project investment for Module 4 is fixed at <strong>BD 5,113.636</strong> (equivalent to <strong>INR 1,125,000.00</strong>). No hidden deployment or hourly surcharges apply within the agreed functional scope."
new_callout = "Total project investment for Module 4 is fixed at <strong>BD 5,113.636</strong>. No hidden deployment, integration, or hourly surcharges apply within the agreed functional scope."
code = code.replace(old_callout, new_callout)

# 6. Replace payment table total row
code = code.replace("<td><strong>₹ 1,125,000.00 Fixed Price</strong></td>", "<td><strong>Formal Acceptance & Sign-off</strong></td>")

with open('build_sales_process_milestone.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated build_sales_process_milestone.py successfully.")
