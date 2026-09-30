import os
import re
import subprocess
import fitz
import sqlite3

# Read SL-POP-ERP-MS-008.html as base
with open('SL-POP-ERP-MS-008.html', 'r', encoding='utf-8') as f:
    template = f.read()

content = template

# Replace PHP doc_id and Titles
content = content.replace("$doc_id = 'SL-POP-ERP-MS-008';", "$doc_id = 'SL-POP-ERP-MS-009';")
content = content.replace("'Module 8: Hardware Integration, QR Handheld Devices, Thermal Printers & Server Setup Infrastructure Milestone'",
                          "'Module 9: Executive Management Dashboard, Cross-Module BI Analytics, 8-Module KPI Engine & Mobile Reporting Milestone'")

content = content.replace("SL-POP-ERP-MS-008: Hardware Integration, QR Code Handheld Devices, Thermal Printers & Server Setup Milestone Agreement",
                          "SL-POP-ERP-MS-009: Executive Management Dashboard, Cross-Module BI Analytics, 8-Module KPI Engine & Mobile Reporting Milestone Agreement")

content = content.replace("SL-POP-ERP-MS-008", "SL-POP-ERP-MS-009")
content = content.replace("ARCH-001 (Ver 1.0)", "DOC-009 (Ver 1.0)")
content = content.replace("ARCH-001 / MS-008", "DOC-009 / MS-009")

# Hero Section
content = content.replace("Module 8: Hardware Integration, QR Code Handheld Device Integration, Biometric Clocks, ESC/POS Printers & Server Infrastructure Setup",
                          "Module 9: Executive Management Dashboard, Cross-Module BI Analytics, 8-Module KPI Engine & Mobile Executive Reporting")

old_hero_desc = """Comprehensive 3-week milestone agreement, dedicated infrastructure engineering team breakdown, 3-tier server cluster deployment (Dev / Staging / Prod), QR handheld scanner listeners, ESC/POS thermal printing daemons, and biometric clock integrations based on the verified Technical Architecture Blueprint <strong>ARCH-001 v1.0</strong> for <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong>."""

new_hero_desc = """Comprehensive 4-week milestone agreement, dedicated BI & analytics engineering team breakdown, cross-module data warehousing, real-time KPI cockpit synthesizing all 8 core ERP operational domains (Sales, Stock, Finance, Procurement, HR, Assets & Hardware), automated WhatsApp/Email executive digests, and role-based mobile management cockpits for <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong>."""

content = content.replace(old_hero_desc, new_hero_desc)

content = content.replace("3 Working Weeks (0.75 Months / 15 Days)", "4 Working Weeks (1.0 Month / 20 Days)")
content = content.replace("3 Working Weeks (0.75 Mo / 15 Days)", "4 Working Weeks (1.0 Mo / 20 Days)")
content = content.replace("3 Working Weeks (15 Days)", "4 Working Weeks (20 Days)")
content = content.replace("BD 1,022.727", "BD 1,363.636")
content = content.replace("BD 340.909 (33.33%)", "BD 340.909 (25.00%)")
content = content.replace("BD 340.909 (33.34%)", "BD 340.909 (25.00%)")
content = content.replace("3-Tier Server Cluster, QR Handhelds, Thermal Printers & Biometrics", "Cross-Module BI Dashboard, 8-Module KPIs & Mobile Executive Reporting")
content = content.replace("Server Setup, QR Handhelds & Hardware", "Executive BI, 8-Module Management KPIs & Reporting")
content = content.replace("ARCH-001 v1.0 (Architecture)", "DOC-009 v1.0 (Cross-Module BI)")

# Replace Executive Summary text
old_exec = """Hardware Integration & Server Infrastructure (Module 8) establishes the foundational compute, networking, cybersecurity, hardware device connectivity, and offline synchronization topology powering the entire ERP transformation for <strong>Popular Auto Spare & A/C Parts Co. W.L.L.</strong> Derived from the master <strong>ERP Technical Architecture & Cybersecurity Specification (ARCH-001 v1.0)</strong>, this module delivers high-availability 3-tier domain isolation (Development, Staging/Sandbox, Production), RabbitMQ asynchronous messaging daemons, offline-first SQLite bi-directional synchronization, Android handheld QR code barcode scanner integration, ESC/POS thermal receipt and label printing daemons, RJ11 cash drawer triggers, and ZKTeco/Hikvision biometric time-clock listeners across all branch showrooms and warehouses."""

new_exec = """Executive Management Dashboard & Business Intelligence (Module 9) represents the strategic decision-support pinnacle of the ERP ecosystem for <strong>Popular Auto Spare & A/C Parts Co. W.L.L.</strong> Operating as a real-time data aggregation and business intelligence engine, this module synthesizes live operational feeds from all eight foundational ERP modules (PCode Item Master, Procurement & Purchase Flow, Warehouse Verification & Stock Control, Multi-Branch POS Sales, Double-Entry Accounting & VAT, Enterprise Administration & Fixed Assets, Human Resources & Biometric Payroll, and Hardware/Server Infrastructure). It empowers executive leadership, General Management, and Branch Heads with instant drill-down visibility into revenue margins, cash liquidity, inventory velocity, supplier fulfillment SLAs, labor productivity, and automated anomaly alerts via responsive desktop and mobile dashboards."""

content = content.replace(old_exec, new_exec)

# Replace Core Objective
old_core_obj = """To commission a resilient enterprise infrastructure and hardware integration suite: 3-Tier Isolated Cloud Server Environments (Dev/Staging/Prod), RabbitMQ Message Queue Service, JetBackup 5 Daily Backups, Handheld Android 1D/2D QR Barcode Scanner Listeners, ESC/POS Thermal Receipt & Barcode Printers, RJ11 Cash Drawer Electronic Triggers, Biometric Attendance Hardware Daemons, and Zero-Trust AES-256 Encrypted Networks."""

new_core_obj = """To deploy a unified, high-performance Executive Management Dashboard and BI KPI Engine: Cross-Module Data Warehouse OLAP Aggregation, Real-Time Executive KPI Metric Calculations across all 8 ERP Modules (Commercial, Stock Turnover, Financial Liquidity, Vendor SLAs, Payroll Ratios & Infrastructure Health), Anomaly Detection Alerts, Automated 7:00 AM WhatsApp/Email Executive Digests, and Role-Based Mobile Executive Access."""

content = content.replace(old_core_obj, new_core_obj)

# Roadmap Box in Section 1.0 (All 8 done, 09 Active)
old_roadmap = """        <!-- Master ERP Transformation Architecture (9 Core Modules) -->
        <div class="roadmap-box">
          <div class="roadmap-header">
            <h4>Master ERP Transformation Architecture (9 Core Process Modules)</h4>
            <span class="badge-tag badge-accent" style="font-size: 10.5px; padding: 4px 12px; letter-spacing: 0.5px;">CURRENT SCOPE: MODULE 08 ACTIVE</span>
          </div>
          <div class="roadmap-list">
            <div class="roadmap-item done">
              <span class="rm-badge">01</span>
              <span class="rm-name">PCode Gen & Item Master</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">02</span>
              <span class="rm-name">Vendor & Purchase Flow</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">03</span>
              <span class="rm-name">Stock Verification & Location</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">04</span>
              <span class="rm-name">Sales & POS Checkout</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">05</span>
              <span class="rm-name">Finance, Tax & VAT Accounting</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">06</span>
              <span class="rm-name">Administration & Security</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">07</span>
              <span class="rm-name">HRMS & Biometric Payroll</span>
            </div>
            <div class="roadmap-item active">
              <span class="rm-badge">08</span>
              <span class="rm-name">Hardware & Barcode Infrastructure</span>
            </div>
            <div class="roadmap-item">
              <span class="rm-badge">09</span>
              <span class="rm-name">Executive BI & Mobile Analytics</span>
            </div>
          </div>
        </div>"""

new_roadmap = """        <!-- Master ERP Transformation Architecture (9 Core Modules) -->
        <div class="roadmap-box">
          <div class="roadmap-header">
            <h4>Master ERP Transformation Architecture (9 Core Process Modules)</h4>
            <span class="badge-tag badge-accent" style="font-size: 10.5px; padding: 4px 12px; letter-spacing: 0.5px;">CURRENT SCOPE: MODULE 09 ACTIVE (EXECUTIVE BI & KPIS)</span>
          </div>
          <div class="roadmap-list">
            <div class="roadmap-item done">
              <span class="rm-badge">01</span>
              <span class="rm-name">PCode Gen & Item Master</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">02</span>
              <span class="rm-name">Vendor & Purchase Flow</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">03</span>
              <span class="rm-name">Stock Verification & Location</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">04</span>
              <span class="rm-name">Sales & POS Checkout</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">05</span>
              <span class="rm-name">Finance, Tax & VAT Accounting</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">06</span>
              <span class="rm-name">Administration & Security</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">07</span>
              <span class="rm-name">HRMS & Biometric Payroll</span>
            </div>
            <div class="roadmap-item done">
              <span class="rm-badge">08</span>
              <span class="rm-name">Hardware & Barcode Infrastructure</span>
            </div>
            <div class="roadmap-item active">
              <span class="rm-badge">09</span>
              <span class="rm-name">Executive BI & Management KPIs</span>
            </div>
          </div>
        </div>"""

content = content.replace(old_roadmap, new_roadmap)

# Section 2.0 Scope Replacement
scope_sec_pattern = re.compile(r'<section class="doc-section" id="module-scope">.*?</section>', re.DOTALL)
new_scope_sec = """<section class="doc-section" id="module-scope">
      <div class="section-header">
        <div class="section-title-wrap">
          <span class="section-num">02. Scope</span>
          <h2 class="section-title">Module 9: Cross-Module Executive BI & KPI Architecture Breakdown</h2>
        </div>
        <span class="section-badge">Full Specification Mapping</span>
      </div>

      <p style="font-size: 13.5px; color: var(--gray-700); line-height: 1.7; margin-bottom: 24px;">
        Module 9 extracts operational feeds from all 8 upstream modules, structuring them into high-impact management KPI categories designed specifically for the executive leadership of <strong>Popular Auto Spare & A/C Parts Co. W.L.L.</strong>
      </p>

      <div class="grid-2">
        <div class="feature-card">
          <div class="feature-icon blue"><i class="fas fa-chart-pie"></i></div>
          <h3 class="feature-title">Commercial & Branch POS Performance (Module 4)</h3>
          <p class="feature-desc">
            Real-time branch revenue breakdown, gross margin realization %, Average Transaction Value (ATV), top-performing PCodes, salesperson commission splits, hourly showroom footfall traffic, and physical cash drawer variance index.
          </p>
          <div class="feature-tags">
            <span class="feature-tag">Revenue & Gross Margin</span>
            <span class="feature-tag">Branch Comparison</span>
            <span class="feature-tag">Commission Radar</span>
          </div>
        </div>

        <div class="feature-card">
          <div class="feature-icon gold"><i class="fas fa-boxes"></i></div>
          <h3 class="feature-title">Inventory Health & Valuation Velocity (Modules 1 & 3)</h3>
          <p class="feature-desc">
            Fast / Slow / Non-Moving (Dead) stock classification, Stock Holding Cost, Inventory Turnover Ratio (ITR), 60/40 daily verification accuracy %, damaged goods scrapping losses, and real-time inter-branch Goods-in-Transit (GIT) valuation.
          </p>
          <div class="feature-tags">
            <span class="feature-tag">Dead Stock Alerts</span>
            <span class="feature-tag">60/40 Audit Accuracy</span>
            <span class="feature-tag">GIT Valuation</span>
          </div>
        </div>

        <div class="feature-card">
          <div class="feature-icon emerald"><i class="fas fa-hand-holding-usd"></i></div>
          <h3 class="feature-title">Financial Liquidity & GCC VAT Cockpit (Module 5)</h3>
          <p class="feature-desc">
            Consolidated double-entry P&L, operating cash flow liquidity, Days Sales Outstanding (DSO) customer aging risk, Days Payable Outstanding (DPO), GCC VAT 10% net tax position, and multi-bank reconciliation (BRS) real-time balances.
          </p>
          <div class="feature-tags">
            <span class="feature-tag">Real-Time P&L</span>
            <span class="feature-tag">DSO Risk Aging</span>
            <span class="feature-tag">GCC VAT Net Position</span>
          </div>
        </div>

        <div class="feature-card">
          <div class="feature-icon blue"><i class="fas fa-truck-loading"></i></div>
          <h3 class="feature-title">Vendor Fulfillment & Procurement SLAs (Module 2)</h3>
          <p class="feature-desc">
            Supplier On-Time In-Full (OTIF) scorecards, Purchase Price Variance (PPV), MOQ buffer stockout prevention rate, CTO strategic requisition approval velocity, and multi-vendor RFQ cost savings analytics.
          </p>
          <div class="feature-tags">
            <span class="feature-tag">Supplier OTIF</span>
            <span class="feature-tag">Price Variance</span>
            <span class="feature-tag">CTO Requisition SLA</span>
          </div>
        </div>

        <div class="feature-card">
          <div class="feature-icon gold"><i class="fas fa-user-clock"></i></div>
          <h3 class="feature-title">HR Productivity, Labor Cost & Payroll (Module 7)</h3>
          <p class="feature-desc">
            Total labor cost-to-revenue ratio, monthly overtime spikes %, biometric attendance punctuality & absenteeism rate, LMRA/SIO regulatory compliance audit, and Bahrain End-of-Service (EOSB / Gratuity) liability accrual.
          </p>
          <div class="feature-tags">
            <span class="feature-tag">Labor Cost %</span>
            <span class="feature-tag">Biometric Punctuality</span>
            <span class="feature-tag">EOSB Accrual</span>
          </div>
        </div>

        <div class="feature-card">
          <div class="feature-icon emerald"><i class="fas fa-server"></i></div>
          <h3 class="feature-title">Assets, Fleet & Infrastructure Health (Modules 6 & 8)</h3>
          <p class="feature-desc">
            Fixed asset book value vs. monthly depreciation curves, vehicle fleet fuel & maintenance cost per kilometer, lease & legal document expiry radar, cloud server uptime SLA (99.95%), and handheld QR scanner sync throughput.
          </p>
          <div class="feature-tags">
            <span class="feature-tag">Depreciation ROI</span>
            <span class="feature-tag">Fleet Cost/KM</span>
            <span class="feature-tag">99.95% Server Uptime</span>
          </div>
        </div>
      </div>
    </section>"""

content = scope_sec_pattern.sub(new_scope_sec, content)

# Section 3.0 Pricing Matrix Replacement
pricing_sec_pattern = re.compile(r'<section class="doc-section" id="pricing-matrix">.*?</section>', re.DOTALL)
new_pricing_sec = """<section class="doc-section" id="pricing-matrix">
      <div class="section-header">
        <div class="section-title-wrap">
          <span class="section-num">03. Pricing</span>
          <h2 class="section-title">Dedicated BI Engineering Resource Allocation (4 Weeks / 1.0 Month)</h2>
        </div>
        <span class="section-badge">Standard Rate Card</span>
      </div>

      <p style="font-size: 13.5px; color: var(--gray-700); line-height: 1.7; margin-bottom: 20px;">
        To deliver the complete Executive BI & Management Analytics cockpit aggregating data across all 8 ERP modules within the <strong>4 Working Weeks (1.0 Month / 20 Working Days)</strong> timeframe, SaNDS Lab allocates a specialized 5-member engineering team.
      </p>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width: 28%;">Engineering Role & Designation</th>
              <th style="width: 36%;">Core Responsibilities & Dedicated Scope</th>
              <th style="width: 12%; text-align: center;">Monthly Rate</th>
              <th style="width: 12%; text-align: center;">Allocation</th>
              <th style="width: 12%; text-align: right;">Total Fee</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <strong>Project Manager & BI Solutions Architect</strong><br>
                <span class="text-muted" style="font-size: 11.5px;">Senior Level • 10+ Yrs BI Experience</span>
              </td>
              <td>Cross-module KPI formula definitions, executive dashboard information architecture, C-Suite sign-off governance, and data accuracy validation.</td>
              <td style="text-align: center;">BD 545.455</td>
              <td style="text-align: center;"><span class="badge-tag badge-accent">1.0 Mo (100%)</span></td>
              <td style="text-align: right; font-weight: 700; color: var(--navy);">BD 545.455</td>
            </tr>
            <tr>
              <td>
                <strong>Senior BI & Data Analytics / Python Engineer</strong><br>
                <span class="text-muted" style="font-size: 11.5px;">Back-End OLAP & ETL Specialist</span>
              </td>
              <td>Data warehouse rollup aggregators, fast hourly indexing, background anomaly detection engine, and automated WhatsApp/Email PDF digest generator.</td>
              <td style="text-align: center;">BD 227.273</td>
              <td style="text-align: center;"><span class="badge-tag badge-accent">1.0 Mo (100%)</span></td>
              <td style="text-align: right; font-weight: 700; color: var(--navy);">BD 227.273</td>
            </tr>
            <tr>
              <td>
                <strong>Senior Data Visualization & UI Specialist</strong><br>
                <span class="text-muted" style="font-size: 11.5px;">React 18 & Chart.js / ApexCharts Expert</span>
              </td>
              <td>Interactive executive charts, multi-branch comparative drill-downs, responsive mobile executive cockpit, dark/light themes, and export widgets.</td>
              <td style="text-align: center;">BD 227.273</td>
              <td style="text-align: center;"><span class="badge-tag badge-accent">1.0 Mo (100%)</span></td>
              <td style="text-align: right; font-weight: 700; color: var(--navy);">BD 227.273</td>
            </tr>
            <tr>
              <td>
                <strong>Database Query Optimization & DW Architect</strong><br>
                <span class="text-muted" style="font-size: 11.5px;">MySQL / MariaDB Performance Lead</span>
              </td>
              <td>High-speed aggregate views, indexing multi-million transaction records across all 8 modules, query latency optimization (<100ms response).</td>
              <td style="text-align: center;">BD 204.545</td>
              <td style="text-align: center;"><span class="badge-tag badge-accent">1.0 Mo (100%)</span></td>
              <td style="text-align: right; font-weight: 700; color: var(--navy);">BD 204.545</td>
            </tr>
            <tr>
              <td>
                <strong>QA Data Integrity & Reconciliation Specialist</strong><br>
                <span class="text-muted" style="font-size: 11.5px;">Financial & Operational Audit QA Lead</span>
              </td>
              <td>100% mathematical reconciliation between operational transactions (Modules 1-8) and Executive BI numbers; rigorous boundary and stress testing.</td>
              <td style="text-align: center;">BD 159.091</td>
              <td style="text-align: center;"><span class="badge-tag badge-accent">1.0 Mo (100%)</span></td>
              <td style="text-align: right; font-weight: 700; color: var(--navy);">BD 159.091</td>
            </tr>
            <tr style="background: var(--gray-50); font-size: 13.5px;">
              <td colspan="4" style="text-align: right; font-weight: 800; color: var(--navy);">
                TOTAL DEDICATED ENGINEERING INVESTMENT (4 WORKING WEEKS / 1.0 MONTH):
              </td>
              <td style="text-align: right; font-weight: 900; color: var(--primary); font-size: 15px;">
                BD 1,363.636
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>"""

content = pricing_sec_pattern.sub(new_pricing_sec, content)

# Section 4.0 Detailed Milestones Replacement
milestones_sec_pattern = re.compile(r'<section class="doc-section" id="detailed-milestones">.*?</section>', re.DOTALL)
new_milestones_sec = """<section class="doc-section" id="detailed-milestones">
      <div class="section-header">
        <div class="section-title-wrap">
          <span class="section-num">04. Milestones</span>
          <h2 class="section-title">Detailed Milestone Breakdown & Deliverables (4-Week Roadmap)</h2>
        </div>
        <span class="section-badge">Sprint Execution Plan</span>
      </div>

      <p style="font-size: 13.5px; color: var(--gray-700); line-height: 1.7; margin-bottom: 24px;">
        Structured across four rigorous weekly sprints, delivering complete management intelligence across all 8 operational domains of Popular Auto Spare & A/C Parts Co. W.L.L.
      </p>

      <!-- WEEK 1 (MILESTONE 9.1) -->
      <div class="milestone-card" style="border-left: 5px solid #2563eb; margin-bottom: 24px; padding: 20px; background: #fff; border-radius: 8px; box-shadow: var(--shadow-sm); border-top: 1px solid var(--gray-200); border-right: 1px solid var(--gray-200); border-bottom: 1px solid var(--gray-200);">
        <div class="milestone-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--gray-200); padding-bottom: 12px; margin-bottom: 16px;">
          <div>
            <span class="badge-tag badge-primary" style="font-size: 11px;">WEEK 1 • MILESTONE 9.1</span>
            <h3 style="margin: 6px 0 0 0; color: var(--navy); font-size: 17px;">Data Warehouse OLAP Aggregation Schema, Cross-Module ETL Pipelines & KPI Models</h3>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 11px; color: var(--gray-500); text-transform: uppercase; font-weight: 700;">Tranche 1 (25%)</div>
            <div style="font-size: 17px; font-weight: 900; color: #2563eb;">BD 340.909</div>
          </div>
        </div>
        <p style="font-size: 13px; color: var(--gray-700); line-height: 1.6; margin-bottom: 14px;">
          Architecting the high-speed Data Warehouse OLAP layer that extracts, normalizes, and aggregates raw transactional data from all 8 active ERP modules without degrading live operational database performance.
        </p>
        <div class="deliverable-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="deliverable-item" style="background: #f8fafc; border: 1px solid var(--gray-200); border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: var(--navy); font-size: 13px; margin-bottom: 6px;">1. Cross-Module OLAP Aggregate Schema</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Creation of pre-aggregated summary tables (hourly, daily, monthly rollups) for fast executive querying across multi-million transaction records.</p>
          </div>
          <div class="deliverable-item" style="background: #f8fafc; border: 1px solid var(--gray-200); border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: var(--navy); font-size: 13px; margin-bottom: 6px;">2. Non-Blocking Background ETL Daemon</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Asynchronous queue consumers syncing live POS checkouts, store transfers, and journal vouchers into the BI data lake with zero table locks.</p>
          </div>
          <div class="deliverable-item" style="background: #f8fafc; border: 1px solid var(--gray-200); border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: var(--navy); font-size: 13px; margin-bottom: 6px;">3. Executive KPI Formula Mathematical Engine</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Standardized mathematical modeling for Gross Margin Return on Investment (GMROI), Inventory Turnover Ratio (ITR), Days Sales Outstanding (DSO), and OTIF supplier scorecards.</p>
          </div>
          <div class="deliverable-item" style="background: #f8fafc; border: 1px solid var(--gray-200); border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: var(--navy); font-size: 13px; margin-bottom: 6px;">4. Multi-Branch Dimension Data Modeling</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Configuring multi-branch dimension hierarchies (Company-wide -> Regional Hubs -> Salmabad Central Warehouse -> Retail Branch Counters -> Individual Salesperson).</p>
          </div>
        </div>
      </div>

      <!-- WEEK 2 (MILESTONE 9.2) -->
      <div class="milestone-card" style="border-left: 5px solid #059669; margin-bottom: 24px; padding: 20px; background: #fff; border-radius: 8px; box-shadow: var(--shadow-sm); border-top: 1px solid var(--gray-200); border-right: 1px solid var(--gray-200); border-bottom: 1px solid var(--gray-200);">
        <div class="milestone-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--gray-200); padding-bottom: 12px; margin-bottom: 16px;">
          <div>
            <span class="badge-tag badge-success" style="font-size: 11px;">WEEK 2 • MILESTONE 9.2</span>
            <h3 style="margin: 6px 0 0 0; color: var(--navy); font-size: 17px;">Executive Commercial, Inventory & Supply Chain Performance Cockpit (Modules 1, 2, 3, 4)</h3>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 11px; color: var(--gray-500); text-transform: uppercase; font-weight: 700;">Tranche 2 (25%)</div>
            <div style="font-size: 17px; font-weight: 900; color: #059669;">BD 340.909</div>
          </div>
        </div>
        <p style="font-size: 13px; color: var(--gray-700); line-height: 1.6; margin-bottom: 14px;">
          Visualizing commercial sales velocity, retail branch margins, warehouse inventory turnover, store verification accuracy, and vendor procurement compliance in high-impact interactive dashboards.
        </p>
        <div class="deliverable-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="deliverable-item" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #166534; font-size: 13px; margin-bottom: 6px;">1. Sales & POS Executive Cockpit (Module 4)</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Real-time Gross & Net Revenue by Branch, Top-Selling PCodes, Counter vs. Mobile POS volume, Hourly Traffic Heatmap, Salesperson Commission Leaderboard, and Cash Drawer Discrepancy Index.</p>
          </div>
          <div class="deliverable-item" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #166534; font-size: 13px; margin-bottom: 6px;">2. Inventory Health & Velocity Matrix (Modules 1 & 3)</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Fast / Slow / Dead Stock SKU Classification, Stock Holding Cost, Total Stock Valuation (FIFO/Landed Cost), and Goods-in-Transit (GIT) inter-branch real-time valuation.</p>
          </div>
          <div class="deliverable-item" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #166534; font-size: 13px; margin-bottom: 6px;">3. Store Verification & Shrinkage Radar (Module 3)</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">60/40 Sampling Daily Stock Audit Accuracy %, Discrepancy Variance Index by Zone/Rack, Damaged Stock Scrapping Loss Value, and Day-Closing Hard Lock Compliance tracker.</p>
          </div>
          <div class="deliverable-item" style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #166534; font-size: 13px; margin-bottom: 6px;">4. Vendor Procurement & SLA Scorecard (Module 2)</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Supplier On-Time In-Full (OTIF) Rate, Purchase Price Variance (PPV), MOQ Buffer Stockout Prevention Rate, CTO Strategic Requisition Approval Cycle Time, and RFQ Savings Matrix.</p>
          </div>
        </div>
      </div>

      <!-- WEEK 3 (MILESTONE 9.3) -->
      <div class="milestone-card" style="border-left: 5px solid #7c3aed; margin-bottom: 24px; padding: 20px; background: #fff; border-radius: 8px; box-shadow: var(--shadow-sm); border-top: 1px solid var(--gray-200); border-right: 1px solid var(--gray-200); border-bottom: 1px solid var(--gray-200);">
        <div class="milestone-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--gray-200); padding-bottom: 12px; margin-bottom: 16px;">
          <div>
            <span class="badge-tag" style="background: #f5f3ff; color: #6d28d9; border: 1px solid #ddd6fe; font-size: 11px;">WEEK 3 • MILESTONE 9.3</span>
            <h3 style="margin: 6px 0 0 0; color: var(--navy); font-size: 17px;">Financial, HR Workforce & Operational Efficiency Analytics (Modules 5, 6, 7, 8)</h3>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 11px; color: var(--gray-500); text-transform: uppercase; font-weight: 700;">Tranche 3 (25%)</div>
            <div style="font-size: 17px; font-weight: 900; color: #7c3aed;">BD 340.909</div>
          </div>
        </div>
        <p style="font-size: 13px; color: var(--gray-700); line-height: 1.6; margin-bottom: 14px;">
          Integrating double-entry financial statements, cash flow liquidity, corporate fixed asset depreciation, HR payroll & statutory compliance, and infrastructure uptime into a unified executive cockpit.
        </p>
        <div class="deliverable-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="deliverable-item" style="background: #faf5ff; border: 1px solid #e9d5ff; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #6b21a8; font-size: 13px; margin-bottom: 6px;">1. Financial Liquidity & VAT Cockpit (Module 5)</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Real-Time P&L, Operating Cash Flow, Days Sales Outstanding (DSO) & Aging Bucket Risk, Days Payable Outstanding (DPO), Net GCC VAT 10% Position, and Multi-Bank BRS Balance.</p>
          </div>
          <div class="deliverable-item" style="background: #faf5ff; border: 1px solid #e9d5ff; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #6b21a8; font-size: 13px; margin-bottom: 6px;">2. HR Workforce & Payroll Efficiency (Module 7)</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Total Labor Cost-to-Revenue Ratio, Monthly Overtime Spikes %, Biometric Punctuality & Absenteeism Index, LMRA/SIO Compliance Audit, and End-of-Service Benefit (EOSB) Liability Accrual.</p>
          </div>
          <div class="deliverable-item" style="background: #faf5ff; border: 1px solid #e9d5ff; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #6b21a8; font-size: 13px; margin-bottom: 6px;">3. Fixed Assets & Fleet Governance (Module 6)</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Asset Book Value vs. Monthly Depreciation Curves, Vehicle Fleet Fuel & Maintenance Cost per Kilometer, Lease & CR Expiry Timeline Alert Radar.</p>
          </div>
          <div class="deliverable-item" style="background: #faf5ff; border: 1px solid #e9d5ff; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #6b21a8; font-size: 13px; margin-bottom: 6px;">4. Infrastructure Health & Device Monitoring (Module 8)</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Cloud Server Uptime SLA (99.95%), REST API Latency (<80ms), Mobile Handheld Scanner Offline Queue Sync Status, and Biometric Device Connectivity Heartbeats.</p>
          </div>
        </div>
      </div>

      <!-- WEEK 4 (MILESTONE 9.4) -->
      <div class="milestone-card" style="border-left: 5px solid #d97706; margin-bottom: 24px; padding: 20px; background: #fff; border-radius: 8px; box-shadow: var(--shadow-sm); border-top: 1px solid var(--gray-200); border-right: 1px solid var(--gray-200); border-bottom: 1px solid var(--gray-200);">
        <div class="milestone-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--gray-200); padding-bottom: 12px; margin-bottom: 16px;">
          <div>
            <span class="badge-tag" style="background: #fffbeb; color: #b45309; border: 1px solid #fde68a; font-size: 11px;">WEEK 4 • MILESTONE 9.4</span>
            <h3 style="margin: 6px 0 0 0; color: var(--navy); font-size: 17px;">Role-Based Access Control, Automated Executive Digests, Anomaly Alerts & Final Sign-Off</h3>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 11px; color: var(--gray-500); text-transform: uppercase; font-weight: 700;">Tranche 4 (25%)</div>
            <div style="font-size: 17px; font-weight: 900; color: #d97706;">BD 340.909</div>
          </div>
        </div>
        <p style="font-size: 13px; color: var(--gray-700); line-height: 1.6; margin-bottom: 14px;">
          Hardening role-based executive permissions, configuring scheduled daily executive digests via WhatsApp & Email, deploying automated anomaly alerts, and completing executive management UAT.
        </p>
        <div class="deliverable-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="deliverable-item" style="background: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #92400e; font-size: 13px; margin-bottom: 6px;">1. Role-Based Management Filtering</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Fine-grained data visibility: Board / CEO (Company-wide consolidated P&L and strategic KPIs), General Manager (All branch operations), Branch Manager (Branch-specific KPIs and stock).</p>
          </div>
          <div class="deliverable-item" style="background: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #92400e; font-size: 13px; margin-bottom: 6px;">2. Automated 7:00 AM Executive Digest</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Automated cron daemon generating high-level 1-page PDF executive summary delivered daily via Email & WhatsApp to top management with previous day's sales, cash collections, and stock alerts.</p>
          </div>
          <div class="deliverable-item" style="background: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #92400e; font-size: 13px; margin-bottom: 6px;">3. Real-Time Anomaly Alert Engine</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Instant push notifications when business anomalies occur (e.g. Gross margin drop >5%, Cash variance >BD 5, Stock audit discrepancy >BD 100, or Server latency spike).</p>
          </div>
          <div class="deliverable-item" style="background: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 12px;">
            <div style="font-weight: 700; color: #92400e; font-size: 13px; margin-bottom: 6px;">4. Executive Mobile UAT & Formal Sign-Off</div>
            <p style="font-size: 12px; color: var(--gray-600); margin: 0; line-height: 1.5;">Mobile and tablet responsive testing, executive user training session, BI administration manual handoff, and formal milestone execution certificate.</p>
          </div>
        </div>
      </div>
    </section>"""

content = milestones_sec_pattern.sub(new_milestones_sec, content)

# Section 5.0 Payment Schedule Replacement
payment_sec_pattern = re.compile(r'<section class="doc-section" id="payment-schedule">.*?</section>', re.DOTALL)
new_payment_sec = """<section class="doc-section" id="payment-schedule">
      <div class="section-header">
        <div class="section-title-wrap">
          <span class="section-num">05. Disbursement</span>
          <h2 class="section-title">Milestone Payment Structure & Invoicing Schedule (4-Week Model)</h2>
        </div>
        <span class="section-badge">Deliverable-Based Invoicing</span>
      </div>

      <p style="font-size: 13.5px; color: var(--gray-700); line-height: 1.7; margin-bottom: 20px;">
        Structured in four equal tranches tied strictly to verified milestone deliverables, UAT verification, and management sign-off for Popular Auto Spare & A/C Parts Co. W.L.L.
      </p>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width: 15%;">Milestone ID</th>
              <th style="width: 45%;">Deliverable Scope & Verification Gate</th>
              <th style="width: 15%; text-align: center;">Timeline</th>
              <th style="width: 10%; text-align: center;">Percentage</th>
              <th style="width: 15%; text-align: right;">Amount (BHD)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>MS-009.1</strong></td>
              <td>Data Warehouse OLAP Schema, Non-Blocking ETL Pipelines & KPI Data Models</td>
              <td style="text-align: center;">End of Week 1</td>
              <td style="text-align: center;"><span class="badge-tag badge-accent">25.00%</span></td>
              <td style="text-align: right; font-weight: 700; color: var(--navy);">BD 340.909</td>
            </tr>
            <tr>
              <td><strong>MS-009.2</strong></td>
              <td>Commercial, Stock Velocity, Warehouse Verification & Vendor SLA Cockpit (Modules 1, 2, 3, 4)</td>
              <td style="text-align: center;">End of Week 2</td>
              <td style="text-align: center;"><span class="badge-tag badge-accent">25.00%</span></td>
              <td style="text-align: right; font-weight: 700; color: var(--navy);">BD 340.909</td>
            </tr>
            <tr>
              <td><strong>MS-009.3</strong></td>
              <td>Financial Liquidity, VAT, HR Payroll, Fixed Assets & Infrastructure Health Analytics (Modules 5, 6, 7, 8)</td>
              <td style="text-align: center;">End of Week 3</td>
              <td style="text-align: center;"><span class="badge-tag badge-accent">25.00%</span></td>
              <td style="text-align: right; font-weight: 700; color: var(--navy);">BD 340.909</td>
            </tr>
            <tr>
              <td><strong>MS-009.4</strong></td>
              <td>Role-Based Management Filtering, 7:00 AM Executive WhatsApp/Email Digest, Anomaly Engine & Final Sign-Off</td>
              <td style="text-align: center;">End of Week 4</td>
              <td style="text-align: center;"><span class="badge-tag badge-accent">25.00%</span></td>
              <td style="text-align: right; font-weight: 700; color: var(--navy);">BD 340.909</td>
            </tr>
            <tr style="background: var(--gray-50); font-size: 14px;">
              <td colspan="4" style="text-align: right; font-weight: 800; color: var(--navy);">
                TOTAL EXECUTIVE BI & MANAGEMENT KPIS MILESTONE INVESTMENT (4 WEEKS / 1.0 MONTH):
              </td>
              <td style="text-align: right; font-weight: 900; color: var(--primary); font-size: 16px;">
                BD 1,363.636
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>"""

content = payment_sec_pattern.sub(new_payment_sec, content)

# Write output files
with open('SL-POP-ERP-MS-009.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('popular/SL-POP-ERP-MS-009.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Generated SL-POP-ERP-MS-009.html successfully.")

# Run Chrome Headless to generate PDF
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
pdf_out = os.path.abspath("SL-POP-ERP-MS-009.pdf")
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_out}",
    "http://localhost:8000/SL-POP-ERP-MS-009.html"
]

res = subprocess.run(cmd, capture_output=True, text=True)
print(f"PDF conversion exit code: {res.returncode}")

# Copy to popular/ and create alias
with open('SL-POP-ERP-MS-009.pdf', 'rb') as src:
    pdf_data = src.read()

with open('popular/SL-POP-ERP-MS-009.pdf', 'wb') as dst:
    dst.write(pdf_data)

with open('Executive_Management_KPIs_and_BI_Dashboard_Milestone.pdf', 'wb') as dst:
    dst.write(pdf_data)

print("PDF distributed successfully.")

# Check Page count
doc = fitz.open('SL-POP-ERP-MS-009.pdf')
print(f"Generated PDF Page Count: {len(doc)}")
doc.close()

# Update SQLite Database
for db_path in ['.auth_portal.db', 'popular/.auth_portal.db']:
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO document_meta (doc_id, title, status, finalized_at, finalized_by)
            VALUES (?, ?, ?, NULL, NULL)
        ''', ('SL-POP-ERP-MS-009', 'Module 9: Executive Management Dashboard, Cross-Module BI Analytics, 8-Module KPI Engine & Mobile Reporting Milestone', 'IN_REVIEW'))
        conn.commit()
        conn.close()
        print(f"Updated document_meta in {db_path}")
