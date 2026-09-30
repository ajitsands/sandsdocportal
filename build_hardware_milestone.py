import os
import re
import subprocess
import fitz
import sqlite3

# Read SL-POP-ERP-MS-007.html as base
with open('SL-POP-ERP-MS-007.html', 'r', encoding='utf-8') as f:
    template = f.read()

content = template

# Replace PHP doc_id and Title
content = content.replace("$doc_id = 'SL-POP-ERP-MS-007';", "$doc_id = 'SL-POP-ERP-MS-008';")
content = content.replace("'Module 7: Human Resource Management, Biometric Attendance, Bahrain Labour Law Leave, Automated Payroll & Gratuity Milestone'",
                          "'Module 8: Hardware Integration, QR Handheld Devices, Thermal Printers & Server Setup Infrastructure Milestone'")

# Replace title and header tags
content = content.replace("SL-POP-ERP-MS-007: Human Resource Management, Biometric Attendance, Payroll & Gratuity Milestone Agreement",
                          "SL-POP-ERP-MS-008: Hardware Integration, QR Code Handheld Devices, Thermal Printers & Server Setup Milestone Agreement")

content = content.replace("SL-POP-ERP-MS-007", "SL-POP-ERP-MS-008")
content = content.replace("DOC-007", "ARCH-001")
content = content.replace("DOC-008", "ARCH-001")

# Replace hero card and titles
content = content.replace("Module 7: Human Resource Management, Biometric Attendance, Bahrain Labour Law Leave, Automated Payroll & Gratuity / EOSB",
                          "Module 8: Hardware Integration, QR Code Handheld Device Integration, Biometric Clocks, ESC/POS Printers & Server Infrastructure Setup")

content = content.replace("Comprehensive 16-week milestone agreement, dedicated engineering team breakdown, Bahrain regulatory compliance matrix (SIO / GOSI / LMRA / WPS), and payment schedule based on the verified Business Analysis Report <strong>DOC-007 v1.0</strong> for <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong>.",
                          "Comprehensive 3-week milestone agreement, dedicated infrastructure engineering team breakdown, 3-tier server cluster deployment (Dev / Staging / Prod), QR handheld scanner listeners, ESC/POS thermal printing daemons, and biometric clock integrations based on the verified Technical Architecture Blueprint <strong>ARCH-001 v1.0</strong> for <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong>.")

content = content.replace("16 Working Weeks (4.0 Months / 80 Days)", "3 Working Weeks (0.75 Months / 15 Days)")
content = content.replace("16 Working Weeks (4.0 Mo / 80 Days)", "3 Working Weeks (0.75 Mo / 15 Days)")
content = content.replace("16 Working Weeks (80 Days)", "3 Working Weeks (15 Days)")
content = content.replace("BD 5,454.548", "BD 1,022.727")
content = content.replace("BD 1,363.637", "BD 340.909")
content = content.replace("Multi-Branch HRMS, Biometric Attendance & WPS Payroll", "3-Tier Server Cluster, QR Handhelds, Thermal Printers & Biometrics")
content = content.replace("HRMS, Attendance, Payroll & EOSB", "Server Setup, QR Handhelds & Hardware")
content = content.replace("DOC-007 v1.0 (80 pgs)", "ARCH-001 v1.0 (Architecture)")
content = content.replace("ARCH-001 v1.0 (25 pgs)", "ARCH-001 v1.0 (Architecture)")

# Replace Executive summary text
old_exec_summary = """Human Resource Management (Module 7) serves as the core workforce governance, statutory regulatory compliance, biometric timekeeping, automated payroll, and employee lifecycle engine for <strong>Popular Auto Spare & A/C Parts Co. W.L.L.</strong> Across multi-country supplier interactions, regional distribution hubs, branch showrooms, central warehouses, and service centers, managing over hundreds of multi-national employees with strict adherence to <strong>Bahrain Labour Law (Law No. 36 of 2012)</strong>, <strong>Social Insurance Organization (SIO / GOSI)</strong>, <strong>Labour Market Regulatory Authority (LMRA)</strong>, and <strong>Central Bank of Bahrain (CBB) Wage Protection System (WPS)</strong> is mission-critical."""

new_exec_summary = """Hardware Integration & Server Infrastructure (Module 8) establishes the foundational compute, networking, cybersecurity, hardware device connectivity, and offline synchronization topology powering the entire ERP transformation for <strong>Popular Auto Spare & A/C Parts Co. W.L.L.</strong> Derived from the master <strong>ERP Technical Architecture & Cybersecurity Specification (ARCH-001 v1.0)</strong>, this module delivers high-availability 3-tier domain isolation (Development, Staging/Sandbox, Production), RabbitMQ asynchronous messaging daemons, offline-first SQLite bi-directional synchronization, Android handheld QR code barcode scanner integration, ESC/POS thermal receipt and label printing daemons, RJ11 cash drawer triggers, and ZKTeco/Hikvision biometric time-clock listeners across all branch showrooms and warehouses."""

content = content.replace(old_exec_summary, new_exec_summary)

# Replace Core objective
old_obj = """To establish an enterprise Human Resource platform consolidating Multi-Branch Organization Structure, Employee 360° Profiles & Document Expiry Vault, Recruitment ATS, Biometric Attendance & Shift Rosters, Bahrain Statutory Leave Engine, Automated Monthly Payroll, SIO/LMRA Compliance, CBB WPS Bank Export, Employee Loans, and Bahrain End-of-Service Benefit (EOSB / Gratuity) Settlement."""

new_obj = """To commission a resilient enterprise infrastructure and hardware integration suite: 3-Tier Isolated Cloud Server Environments (Dev/Staging/Prod), RabbitMQ Message Queue Service, JetBackup 5 Daily Backups, Handheld Android 1D/2D QR Barcode Scanner Listeners, ESC/POS Thermal Receipt & Barcode Printers, RJ11 Cash Drawer Electronic Triggers, Biometric Attendance Hardware Daemons, and Zero-Trust AES-256 Encrypted Networks."""

content = content.replace(old_obj, new_obj)

# Replace Roadmap Box
old_roadmap_box = """        <!-- Master ERP Transformation Architecture (9 Core Modules) -->
        <div class="roadmap-box">
          <div class="roadmap-header">
            <h4>Master ERP Transformation Architecture (9 Core Process Modules)</h4>
            <span class="badge-tag badge-accent" style="font-size: 10.5px; padding: 4px 12px; letter-spacing: 0.5px;">CURRENT SCOPE: MODULE 07 ACTIVE</span>
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
            <div class="roadmap-item active">
              <span class="rm-badge">07</span>
              <span class="rm-name">HRMS & Biometric Payroll</span>
            </div>
            <div class="roadmap-item">
              <span class="rm-badge">08</span>
              <span class="rm-name">Hardware & Barcode Infrastructure</span>
            </div>
            <div class="roadmap-item">
              <span class="rm-badge">09</span>
              <span class="rm-name">Executive BI & Mobile Analytics</span>
            </div>
          </div>
        </div>"""

new_roadmap_box = """        <!-- Master ERP Transformation Architecture (9 Core Modules) -->
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

content = content.replace(old_roadmap_box, new_roadmap_box)

# Replace 3 Highlight feature cards in Section 1
old_grid_3 = """        <div class="grid-3">
          <div class="feature-card">
            <div class="feature-icon emerald"><i class="fas fa-users-cog"></i></div>
            <div class="feature-title">Org Hierarchy & Employee 360</div>
            <div class="feature-desc">Multi-branch organization tree, complete Employee 360 profile, document expiry alert vault (CPR, Passport, LMRA, Visas), and recruitment ATS with digital onboarding.</div>
            <div class="feature-tags">
              <span class="feature-tag">Org Master</span>
              <span class="feature-tag">Doc Vault</span>
              <span class="feature-tag">Recruitment ATS</span>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon gold"><i class="fas fa-fingerprint"></i></div>
            <div class="feature-title">Biometric Attendance & Leave</div>
            <div class="feature-desc">Live biometric sync across all branches, mobile GPS geofenced clock-in, multi-shift rosters, overtime calculation, and Bahrain Labour Law statutory leave engine.</div>
            <div class="feature-tags">
              <span class="feature-tag">Biometric Sync</span>
              <span class="feature-tag">Shift Rosters</span>
              <span class="feature-tag">Labour Law Leave</span>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon blue"><i class="fas fa-money-check-alt"></i></div>
            <div class="feature-title">Payroll, WPS & Gratuity EOSB</div>
            <div class="feature-desc">Automated payroll calculation, SIO/GOSI and LMRA compliance, CBB WPS bank file export, employee loans/advances, ESS portal, and Bahrain Law No. 36 Gratuity engine.</div>
            <div class="feature-tags">
              <span class="feature-tag">CBB WPS Export</span>
              <span class="feature-tag">SIO / GOSI</span>
              <span class="feature-tag">EOSB Gratuity</span>
            </div>
          </div>
        </div>"""

new_grid_3 = """        <div class="grid-3">
          <div class="feature-card">
            <div class="feature-icon blue"><i class="fas fa-server"></i></div>
            <div class="feature-title">3-Tier Server Cluster & RabbitMQ</div>
            <div class="feature-desc">Complete multi-environment deployment (dev.popular.com, sandbox.popular.com, erp.popular.com) with RabbitMQ message broker, Redis memory caching, and automated JetBackup 5.</div>
            <div class="feature-tags">
              <span class="feature-tag">3-Tier Cluster</span>
              <span class="feature-tag">RabbitMQ Broker</span>
              <span class="feature-tag">SSL / TLS 1.3</span>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon gold"><i class="fas fa-qrcode"></i></div>
            <div class="feature-title">QR Handheld & ESC/POS Printers</div>
            <div class="feature-desc">Zebra / Honeywell / Sunmi Android mobile terminal listeners, camera QR scanners, ESC/POS thermal receipt printers, EPL/ZPL thermal barcode label printers, and RJ11 cash drawers.</div>
            <div class="feature-tags">
              <span class="feature-tag">Android Handhelds</span>
              <span class="feature-tag">QR Listeners</span>
              <span class="feature-tag">ESC/POS Printers</span>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon emerald"><i class="fas fa-sync-alt"></i></div>
            <div class="feature-title">Offline Auto-Sync & Biometrics</div>
            <div class="feature-desc">Offline-first local SQLite/IndexedDB queue with bi-directional auto-sync, TCP/IP ZKTeco biometric clock daemons, and zero-trust AES-256 encryption.</div>
            <div class="feature-tags">
              <span class="feature-tag">Offline Sync</span>
              <span class="feature-tag">Biometric TCP/IP</span>
              <span class="feature-tag">AES-256 Security</span>
            </div>
          </div>
        </div>"""

content = content.replace(old_grid_3, new_grid_3)

# Replace Section 2 Functional Scope Breakdown
old_section_2 = """      <!-- Section 2: Functional Scope Breakdown (DOC-007) -->
      <section class="doc-section" id="module-scope">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 2.0</span>
            <h2 class="section-title">Module 7: Functional Scope & Architecture Breakdown (BA Ref: DOC-007)</h2>
          </div>
          <span class="section-badge">Full Specification Mapping</span>
        </div>

        <p>
          Derived directly from the 80 pages of <strong>DOC-007: Human Resource Management Business Analysis Report</strong>, the implementation scope is structured across 6 core operational pillars covering 17 sub-modules:
        </p>

        <div class="grid-2" style="margin-top: 24px;">
          
          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-sitemap"></i> 2.1 Organization Hierarchy & Employee 360 Master
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Multi-Branch Hierarchy:</strong> Corporate HQ, branch showrooms, central warehouses, workshop bays, and staff accommodations.</li>
                <li><strong>Employee 360° Profile:</strong> Personal, emergency contact, passport, CPR, LMRA work permit, residence visa, driving license, and bank account details.</li>
                <li><strong>Statutory Document Vault:</strong> Automated 90/60/30-day proactive expiration alerts for CPR, passports, visas, work permits, and occupational health cards.</li>
                <li><strong>Designation & Grade Pay Bands:</strong> Standardized job descriptions, grade ladders, reporting hierarchy, and matrix approval chains.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-user-plus"></i> 2.2 Recruitment Management & Digital Onboarding
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Manpower Requisition:</strong> Department vacancy budget approval, job posting, applicant tracking (ATS).</li>
                <li><strong>Applicant Tracking (ATS):</strong> Candidate pipeline, resume parsing, interview scheduling, scoring rubrics, and panel evaluation notes.</li>
                <li><strong>Offer & Contract Management:</strong> Standardized offer letter generation, salary breakdown preview, and digital contract execution.</li>
                <li><strong>Digital Onboarding Pipeline:</strong> 1-Click employee profile provisioning, IT access control (RBAC), asset allocation, and policy acknowledgements.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-business-time"></i> 2.3 Biometric Attendance, Shift Rosters & Overtime
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Biometric Device Integration:</strong> Real-time automated sync with fingerprint and facial recognition terminals across all branches.</li>
                <li><strong>Mobile Geofence Clock-In:</strong> GPS geofencing radius validation for delivery drivers, sales representatives, and off-site staff.</li>
                <li><strong>Multi-Shift Rostering:</strong> Split shifts, rotational branch rosters, Ramadan reduced hours, grace periods, and late penalty calculations.</li>
                <li><strong>Overtime Engine:</strong> Automatic calculation of standard weekday, weekend, and Bahrain public holiday overtime multipliers.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-calendar-check"></i> 2.4 Bahrain Labour Law Statutory Leave Engine
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Statutory Leave Types:</strong> 30-day annual leave, sick leave (15 full / 20 half / 20 unpaid), maternity, hajj, marriage, bereavement.</li>
                <li><strong>Automated Monthly Accrual:</strong> Pro-rata monthly leave credit calculation with carry-forward rules and maximum accumulation caps.</li>
                <li><strong>Approval & Substitution Workflow:</strong> Line manager and HR approvals with mandatory task handover and replacement assignments.</li>
                <li><strong>Leave Encashment:</strong> Automated salary formula encashment calculation linked directly to payroll and final settlement.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-file-invoice-dollar"></i> 2.5 Automated Payroll, SIO / GOSI & CBB WPS Banking
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Dynamic Salary Structure:</strong> Basic salary, housing allowance, transport, telephone, and performance sales commissions.</li>
                <li><strong>Social Insurance (SIO / GOSI):</strong> Automated contribution calculation for Bahraini nationals and expatriate occupational injury levy.</li>
                <li><strong>CBB WPS Bank Export:</strong> 1-Click generation of Central Bank of Bahrain Wage Protection System standard file format (.txt / .csv).</li>
                <li><strong>General Ledger Posting:</strong> Automated double-entry salary expense and liability journal voucher posting to Accounting Module 5.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-hand-holding-usd"></i> 2.6 Loans, ESS Portal, Performance & Gratuity (EOSB)
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Loans & Salary Advances:</strong> Emergency assistance loans with automated monthly payroll deduction schedules.</li>
                <li><strong>Employee Self-Service (ESS):</strong> Self-service portal for payslips, leave requests, loan applications, and document requests.</li>
                <li><strong>Performance & Training:</strong> KPI appraisal scorecards, 360° reviews, training needs analysis, and certifications.</li>
                <li><strong>Bahrain EOSB Gratuity Engine:</strong> Law No. 36 of 2012 end-of-service calculation, clearance checklist, and final settlement vouchers.</li>
              </ul>
            </div>
          </div>

        </div>
      </section>"""

new_section_2 = """      <!-- Section 2: Functional Scope Breakdown (ARCH-001) -->
      <section class="doc-section" id="module-scope">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 2.0</span>
            <h2 class="section-title">Module 8: Hardware Integration, QR Handhelds & Server Setup (Ref: ARCH-001)</h2>
          </div>
          <span class="section-badge">Technical Architecture Mapping</span>
        </div>

        <p>
          Derived directly from <strong>ARCH-001 v1.0: ERP Technical Architecture & Cybersecurity Specification</strong>, Module 8 encompasses the full commissioning of server environments, message queues, handheld mobile devices, printing daemons, and biometric time-clocks:
        </p>

        <div class="grid-2" style="margin-top: 24px;">
          
          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-network-wired"></i> 2.1 3-Tier Isolated Cloud Server Topology
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Environment Isolation:</strong> Independent sub-domains for Development (dev.popular.com), Sandbox Staging (sandbox.popular.com), and Production (erp.popular.com).</li>
                <li><strong>PHP 8.2+ MVC Runtime:</strong> Optimized PHP-FPM execution with OPcache, memory limits (512M), execution timeouts, and hardened security settings.</li>
                <li><strong>MySQL InnoDB Database Engine:</strong> Optimized buffer pools, ACID transaction guarantees, UTF8MB4 collation, and foreign key integrity.</li>
                <li><strong>JetBackup 5 Automated Engine:</strong> Scheduled daily multi-destination incremental snapshots with 30-day retention and 1-click restore.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-layer-group"></i> 2.2 Asynchronous Message Broker (RabbitMQ)
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Message Queue Topology:</strong> Dedicated exchanges and queues for high-volume background tasks (Email/SMS OTP, WPS bank files, PDF rendering).</li>
                <li><strong>Worker Daemon Architecture:</strong> Multi-threaded PHP CLI consumer daemons managed by Linux systemd with auto-restart on failure.</li>
                <li><strong>Dead-Letter Exchange (DLX):</strong> Automated capture and retry handling for failed background jobs with administrator alert notifications.</li>
                <li><strong>Queue Monitoring Console:</strong> Web-based metrics dashboard for message throughput, queue depth, and worker consumer health.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-mobile-alt"></i> 2.3 Android Mobile Handheld QR Scanner Integration
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Enterprise Handheld Terminals:</strong> Integration with Zebra, Honeywell, and Sunmi Android rugged mobile barcode scanners.</li>
                <li><strong>Hardware Laser & Camera Listeners:</strong> High-speed hardware scan intent broadcast receivers and camera QR fallback scanning engines.</li>
                <li><strong>Floor Sales & Warehouse Workflows:</strong> Mobile Assisted Sales, 1-Scan Dynamic QR Cart Handoff, and Goods Verification (PVN).</li>
                <li><strong>Continuous Barcode Buffer:</strong> Rapid continuous scanning mode for stock auditing, inter-branch transfers, and delivery handovers.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-print"></i> 2.4 ESC/POS Thermal Receipt & Thermal Barcode Printers
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>POS Receipt Printing:</strong> ESC/POS network, USB, and Bluetooth printing daemons with raw byte stream execution for instant bill printing.</li>
                <li><strong>Thermal Barcode Label Printers:</strong> Direct EPL/ZPL driver integration for product labels, bin tags, and fixed asset QR code stickers.</li>
                <li><strong>Electronic Cash Drawer Triggers:</strong> RJ11 standard kick-out pulses triggered automatically upon invoice settlement and manual manager override.</li>
                <li><strong>Multi-Printer Routing:</strong> Automatic routing of sales bills to counter printers and picking slips to warehouse packing stations.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-fingerprint"></i> 2.5 Biometric Time-Attendance Hardware Listener
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Biometric Terminal Connectivity:</strong> Real-time TCP/IP network integration with ZKTeco and Hikvision biometric fingerprint & face clocks.</li>
                <li><strong>Push / Pull Daemon:</strong> Background sync service capturing employee clock-in/out timestamps and populating raw attendance tables.</li>
                <li><strong>Offline Device Buffering:</strong> Automatic catch-up synchronization during network disconnects to prevent missing attendance punch logs.</li>
                <li><strong>Device Health Telemetry:</strong> Periodic ping checks alerting IT administrators if any branch time-clock goes offline.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-shield-alt"></i> 2.6 Zero-Trust Cybersecurity & Offline Sync Engine
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Offline-First SQLite Engine:</strong> Local browser / IndexedDB storage enabling POS checkout to continue uninterrupted during internet outages.</li>
                <li><strong>Bi-Directional Auto-Sync:</strong> Intelligent synchronization engine resolving conflict priority with atomic database transactions upon reconnect.</li>
                <li><strong>AES-256-GCM Cryptography:</strong> End-to-end data encryption for stored credentials, bank records, and document payloads.</li>
                <li><strong>TLS 1.3 & Zero-Trust RBAC:</strong> Strict HSTS, TLS 1.3 encryption in transit, IP access restrictions, and tamper-proof audit trails.</li>
              </ul>
            </div>
          </div>

        </div>
      </section>"""

content = content.replace(old_section_2, new_section_2)

# Replace Section 3 Resource table
old_sec_3 = """      <!-- Section 3: Dedicated Resource Pricing Matrix -->
      <section class="doc-section" id="pricing-matrix">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 3.0</span>
            <h2 class="section-title">Project Team Structure & Dedicated Resource Pricing (16 Weeks / 4.0 Months)</h2>
          </div>
          <span class="section-badge">Rate Card Compliance</span>
        </div>

        <p>
          In strict accordance with the <strong>SaNDS Lab Dedicated Engineering Rate Card</strong>, the resource allocation and cost breakdown for the 16-week (4.0 months / 80 working days) delivery of Module 7 is structured as follows (all figures in <strong>Bahraini Dinars - BHD</strong>):
        </p>

        <div class="table-responsive">
          <table class="table-custom">
            <thead>
              <tr>
                <th>Engineering Role / Core Domain</th>
                <th style="text-align: center;">Allocation</th>
                <th style="text-align: right;">Monthly Rate (BHD)</th>
                <th style="text-align: center;">Duration (Months)</th>
                <th style="text-align: right;">Total Milestone Cost (BHD)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <strong>Project Manager & Solution Architect</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Bahrain Labour Law, SIO/LMRA/WPS architecture, security governance & client sprint management</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 545.455</td>
                <td style="text-align: center;">4.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 2,181.820</td>
              </tr>
              <tr>
                <td>
                  <strong>Back-End Lead Engineer (PHP MVC / REST APIs)</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Payroll calculation engine, biometric sync listener, CBB WPS file generator, GL double-entry posting</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 227.273</td>
                <td style="text-align: center;">4.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 909.092</td>
              </tr>
              <tr>
                <td>
                  <strong>Front-End Lead Engineer (React / UI Design Tokens)</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">HR admin command console, ESS portal, responsive organogram, mobile clock-in interface</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 227.273</td>
                <td style="text-align: center;">4.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 909.092</td>
              </tr>
              <tr>
                <td>
                  <strong>Database & Cloud DevOps Specialist</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Encrypted document vault, automated daily backups, biometric queue daemon, high-availability schemas</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 204.545</td>
                <td style="text-align: center;">4.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 818.180</td>
              </tr>
              <tr>
                <td>
                  <strong>QA Automation & UAT Test Lead</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Payroll verification test suites, leave accrual boundary testing, WPS compliance, multi-branch UAT</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 159.091</td>
                <td style="text-align: center;">4.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 636.364</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="2" style="font-weight: 800; color: var(--primary);">TOTAL DEDICATED ENGINEERING TEAM FEE</td>
                <td style="text-align: right; font-weight: 800; color: var(--primary);">BD 1,363.636 / Mo</td>
                <td style="text-align: center; font-weight: 800; color: var(--primary);">16 Working Weeks</td>
                <td style="text-align: right; font-weight: 800; color: var(--accent); font-size: 15px;">BD 5,454.548</td>
              </tr>
            </tfoot>
          </table>
        </div>"""

new_sec_3 = """      <!-- Section 3: Dedicated Resource Pricing Matrix -->
      <section class="doc-section" id="pricing-matrix">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 3.0</span>
            <h2 class="section-title">Project Team Structure & Dedicated Resource Pricing (3 Weeks / 0.75 Months)</h2>
          </div>
          <span class="section-badge">Rate Card Compliance</span>
        </div>

        <p>
          In strict accordance with the <strong>SaNDS Lab Dedicated Engineering Rate Card</strong>, the resource allocation and cost breakdown for the 3-week (0.75 months / 15 working days) delivery of Module 8 is structured as follows (all figures in <strong>Bahraini Dinars - BHD</strong>):
        </p>

        <div class="table-responsive">
          <table class="table-custom">
            <thead>
              <tr>
                <th>Engineering Role / Core Domain</th>
                <th style="text-align: center;">Allocation</th>
                <th style="text-align: right;">Monthly Rate (BHD)</th>
                <th style="text-align: center;">Duration (Months)</th>
                <th style="text-align: right;">Total Milestone Cost (BHD)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <strong>Project Manager & Infrastructure Lead</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Server cluster architecture, network security, hardware vendor coordination & deployment SLA</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 545.455</td>
                <td style="text-align: center;">0.75 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 409.091</td>
              </tr>
              <tr>
                <td>
                  <strong>Back-End & Hardware Integration Lead</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">ESC/POS printing daemons, raw socket listeners, RabbitMQ consumers & biometric TCP/IP daemons</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 227.273</td>
                <td style="text-align: center;">0.75 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 170.455</td>
              </tr>
              <tr>
                <td>
                  <strong>Front-End & Mobile Handheld UI Specialist</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Android mobile scanner event listeners, barcode continuous buffer, mobile POS fast-checkout UI</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 227.273</td>
                <td style="text-align: center;">0.75 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 170.455</td>
              </tr>
              <tr>
                <td>
                  <strong>Cloud DevOps & Network Security Specialist</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">3-tier sub-domain isolation, SSL/TLS certificates, MySQL clustering, JetBackup 5 & VPN tunnel</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 204.545</td>
                <td style="text-align: center;">0.75 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 153.409</td>
              </tr>
              <tr>
                <td>
                  <strong>QA Hardware Test & Multi-Branch UAT Lead</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Hardware stress testing, print latency verification, biometric sync audits & failover simulation</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 159.091</td>
                <td style="text-align: center;">0.75 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 119.317</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="2" style="font-weight: 800; color: var(--primary);">TOTAL DEDICATED ENGINEERING TEAM FEE</td>
                <td style="text-align: right; font-weight: 800; color: var(--primary);">BD 1,363.636 / Mo</td>
                <td style="text-align: center; font-weight: 800; color: var(--primary);">3 Working Weeks</td>
                <td style="text-align: right; font-weight: 800; color: var(--accent); font-size: 15px;">BD 1,022.727</td>
              </tr>
            </tfoot>
          </table>
        </div>"""

content = content.replace(old_sec_3, new_sec_3)

# Replace Section 4 Detailed Roadmap
old_sec_4 = """      <!-- Section 4: Detailed Milestones -->
      <section class="doc-section" id="detailed-milestones">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 4.0</span>
            <h2 class="section-title">Detailed Milestone Breakdown & Deliverables (16-Week Roadmap)</h2>
          </div>
          <span class="section-badge">Phased Engineering Plan</span>
        </div>

        <p>
          The implementation is organized into 4 sequential 4-week milestones (25.00% each), guaranteeing focused execution, continuous integration, and transparent deliverable acceptance:
        </p>

        <div style="margin-top: 24px; display: flex; flex-direction: column; gap: 20px;">
          
          <!-- Milestone 1 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 1 (Weeks 1–4)</span>
                <span class="ms-heading">Organization Hierarchy, Employee Master, Recruitment & Digital Onboarding</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 1,363.637</div>
                <div class="ms-pct">25.00% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Multi-tier organization tree, branch registry, department structure & designation pay grades.</li>
                  <li>Employee Master Profile with CPR, passport, visa/LMRA, driving licenses, bank details & digital doc vault.</li>
                  <li>Proactive 90/60/30-day document expiration notification engine via email and dashboard alerts.</li>
                  <li>Manpower requisition workflow, vacancy tracking, resume parsing & interview scorecards.</li>
                  <li>Digital onboarding pipeline with user role-based access control (RBAC) & asset handover challans.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>Relational database schema for Org Structure, Employee Master, and Recruitment ATS.</li>
                  <li>Automated daily cron service for 90/60/30-day document expiry notifications.</li>
                  <li>RESTful API endpoints for candidate tracking, interview evaluation, and employee profile setup.</li>
                  <li>Responsive web dashboards for HR Executives, Line Managers, and System Administrators.</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Milestone 2 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 2 (Weeks 5–8)</span>
                <span class="ms-heading">Biometric Attendance, Shift Rostering & Statutory Leave Engine</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 1,363.637</div>
                <div class="ms-pct">25.00% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Hardware biometric device listeners & mobile GPS geofenced clock-in integration across all branches.</li>
                  <li>Flexible multi-shift schedules, Ramadan rosters, split shifts, grace period & late penalty logic.</li>
                  <li>Overtime computation engine (normal weekdays, weekends, official Bahrain public holidays).</li>
                  <li>Bahrain Labour Law No. 36 statutory leave engine (annual, sick, maternity, hajj, bereavement).</li>
                  <li>Automated monthly leave accrual calculator, carry-forward limits & multi-tier approval hierarchy.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>Biometric listener service with automated queue processing and network reconnect recovery.</li>
                  <li>Mobile GPS geofencing radius validation algorithm for off-site field attendance.</li>
                  <li>Real-time attendance anomaly detector (absenteeism, late-in, early-departure alerts).</li>
                  <li>Leave balance calculation daemon with pro-rata monthly accrual ledger integration.</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Milestone 3 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 3 (Weeks 9–12)</span>
                <span class="ms-heading">Automated Payroll Processing, SIO/LMRA Compliance, WPS Export & Loans</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 1,363.637</div>
                <div class="ms-pct">25.00% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Dynamic salary formulation engine integrating biometric attendance, unpaid leaves, and overtime.</li>
                  <li>Social Insurance Organization (SIO / GOSI) calculation for Bahraini and non-Bahraini staff.</li>
                  <li>Automated Central Bank of Bahrain (CBB) Wage Protection System (WPS) bank transfer file export (.txt / .csv).</li>
                  <li>Automated double-entry General Ledger (GL) payroll expense and salary payable journal posting.</li>
                  <li>Employee salary advances, emergency loans & automated monthly amortization payroll deductions.</li>
                  <li>Confidential PDF payslip generation with email delivery and ESS portal access.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>High-performance payroll batch calculation engine with transaction locking guards.</li>
                  <li>CBB WPS format validator ensuring strict compliance with local clearing house standards.</li>
                  <li>Automated double-entry accounting integration with General Ledger Module 5.</li>
                  <li>Encrypted PDF payslip batch generator with digital watermark security.</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Milestone 4 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 4 (Weeks 13–16)</span>
                <span class="ms-heading">Performance KPIs, ESS Portal, Gratuity / EOSB Engine & Production Go-Live</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 1,363.637</div>
                <div class="ms-pct">25.00% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Performance KPI scorecards, 360-degree appraisal cycles, and salary increment linkages.</li>
                  <li>Training needs analysis, course catalog, training budget tracking, and certifications.</li>
                  <li>Employee Self-Service (ESS) web and mobile portal for leaves, loans, claims, and certificate requests.</li>
                  <li>Bahrain Labour Law End-of-Service Benefit (EOSB / Gratuity) calculation engine.</li>
                  <li>Department clearance workflow, asset surrender verification, and final settlement voucher generation.</li>
                  <li>Comprehensive multi-branch UAT sign-off, historical employee data migration, and production deployment.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>Responsive Employee Self-Service (ESS) web and mobile frontend application.</li>
                  <li>Bahrain Law No. 36 compliant EOSB calculator with leave encashment integration.</li>
                  <li>Full regression test suite execution and multi-branch security audit.</li>
                  <li>Production rollout, data migration verification, and 90-day post-launch warranty activation.</li>
                </ul>
              </div>
            </div>
          </div>

        </div>
      </section>"""

new_sec_4 = """      <!-- Section 4: Detailed Milestones -->
      <section class="doc-section" id="detailed-milestones">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 4.0</span>
            <h2 class="section-title">Detailed Milestone Breakdown & Deliverables (3-Week Roadmap)</h2>
          </div>
          <span class="section-badge">Phased Engineering Plan</span>
        </div>

        <p>
          The implementation is organized into 3 sequential 1-week milestones (33.33% / 33.33% / 33.34%), guaranteeing rapid deployment, verified hardware handshake, and end-to-end operational readiness:
        </p>

        <div style="margin-top: 24px; display: flex; flex-direction: column; gap: 20px;">
          
          <!-- Milestone 1 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 1 (Week 1)</span>
                <span class="ms-heading">3-Tier Server Environment Setup, RabbitMQ Broker, SSL/TLS & Backup Automation</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 340.909</div>
                <div class="ms-pct">33.33% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Commissioning of 3 isolated sub-domain environments: Development (dev.popular.com), Sandbox (sandbox.popular.com), and Production (erp.popular.com).</li>
                  <li>Installation and configuration of RabbitMQ message broker with dedicated vhosts, exchanges, and dead-letter queues.</li>
                  <li>Setup of PHP 8.2/8.3 runtime with OPcache, memory limits (512M), and cPanel multi-PHP configuration.</li>
                  <li>Automated daily JetBackup 5 incremental snapshot configuration with off-site cloud replication.</li>
                  <li>Wildcard SSL/TLS 1.3 certificate deployment with strict HSTS and security header enforcement.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>Environment isolation verification and Git CI/CD branch deployment hooks.</li>
                  <li>RabbitMQ management web console configuration with operational telemetry metrics.</li>
                  <li>MySQL database engine tuning (innodb_buffer_pool_size, max_connections, query cache).</li>
                  <li>Backup restoration validation test report verifying 0% data loss recovery.</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Milestone 2 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 2 (Week 2)</span>
                <span class="ms-heading">Handheld Android QR Scanner Integration, ESC/POS Thermal Printers & Cash Drawers</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 340.909</div>
                <div class="ms-pct">33.33% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Integration with Zebra, Honeywell, and Sunmi Android mobile barcode terminals via hardware scan broadcast receivers.</li>
                  <li>ESC/POS thermal receipt printer daemon implementation for instant customer invoice and VAT tax bill printing.</li>
                  <li>EPL/ZPL thermal barcode label printer drivers for item master labels, shelf bin tags, and asset QR stickers.</li>
                  <li>RJ11 electronic cash drawer trigger signals activated on invoice finalization and authorized manager override.</li>
                  <li>ZKTeco and Hikvision biometric time-clock TCP/IP push/pull listener daemon deployment.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>JavaScript continuous barcode listener library with rapid keystroke-buffer debouncing.</li>
                  <li>Raw TCP socket printing driver supporting ESC/POS standard formatting commands.</li>
                  <li>Biometric raw punch listener service with background queue synchronization.</li>
                  <li>Physical device hardware compatibility test matrix across all showroom counter terminals.</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Milestone 3 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 3 (Week 3)</span>
                <span class="ms-heading">Offline Auto-Sync Engine, Multi-Branch Stress Testing, UAT Sign-Off & Go-Live</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 340.909</div>
                <div class="ms-pct">33.34% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Offline-first local browser / IndexedDB storage daemon enabling uninterrupted POS billing during internet disconnects.</li>
                  <li>Bi-directional auto-sync reconciliation resolving master record conflicts with atomic transactional commits.</li>
                  <li>Multi-branch network latency testing, bandwidth optimization, and hardware stress testing.</li>
                  <li>Full security penetration review, TLS cipher validation, and zero-trust access control checks.</li>
                  <li>Multi-branch hardware UAT sign-off, system handover, and official production infrastructure go-live.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>Service worker offline synchronization engine with automated retry exponential backoff.</li>
                  <li>Multi-terminal concurrent checkout load testing report under simulated high transaction volumes.</li>
                  <li>Final hardware and server infrastructure commissioning certificate.</li>
                  <li>90-day post-launch hardware integration and server maintenance warranty activation.</li>
                </ul>
              </div>
            </div>
          </div>

        </div>
      </section>"""

content = content.replace(old_sec_4, new_sec_4)

# Replace Section 5 Payment Schedule
old_sec_5 = """      <!-- Section 5: Payment Schedule -->
      <section class="doc-section" id="payment-schedule">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 5.0</span>
            <h2 class="section-title">Milestone Payment Structure & Invoicing Schedule (16-Week Model)</h2>
          </div>
          <span class="section-badge">Commercial Terms</span>
        </div>

        <p>
          Payments are structured in 4 equal milestone disbursements of 25.00% (BD 1,363.637 each), tied strictly to formal milestone deliverables and client sign-off:
        </p>

        <div class="table-responsive">
          <table class="table-custom">
            <thead>
              <tr>
                <th>Milestone Reference</th>
                <th>Target Timeline</th>
                <th>Deliverable Summary</th>
                <th style="text-align: center;">Percentage</th>
                <th style="text-align: right;">Invoice Amount (BHD)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Milestone 1</strong></td>
                <td>End of Week 04</td>
                <td>Org Structure, Employee Master, Recruitment & Digital Onboarding</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">25.00%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 1,363.637</td>
              </tr>
              <tr>
                <td><strong>Milestone 2</strong></td>
                <td>End of Week 08</td>
                <td>Biometric Attendance, Shift Rosters & Statutory Leave System</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">25.00%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 1,363.637</td>
              </tr>
              <tr>
                <td><strong>Milestone 3</strong></td>
                <td>End of Week 12</td>
                <td>Automated Payroll, SIO/LMRA Compliance, WPS/CBB Export & Loans</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">25.00%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 1,363.637</td>
              </tr>
              <tr>
                <td><strong>Milestone 4</strong></td>
                <td>End of Week 16</td>
                <td>Performance KPIs, ESS Portal, Gratuity / EOSB & Production Go-Live</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">25.00%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 1,363.637</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="3" style="font-weight: 800; color: var(--primary);">TOTAL FIXED CONTRACT VALUE (MODULE 7)</td>
                <td style="text-align: center; font-weight: 800; color: var(--primary);">100.00%</td>
                <td style="text-align: right; font-weight: 800; color: var(--accent); font-size: 15px;">BD 5,454.548</td>
              </tr>
            </tfoot>
          </table>
        </div>"""

new_sec_5 = """      <!-- Section 5: Payment Schedule -->
      <section class="doc-section" id="payment-schedule">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 5.0</span>
            <h2 class="section-title">Milestone Payment Structure & Invoicing Schedule (3-Week Model)</h2>
          </div>
          <span class="section-badge">Commercial Terms</span>
        </div>

        <p>
          Payments are structured in 3 milestone disbursements (33.33% / 33.33% / 33.34%), tied strictly to formal milestone deliverables, hardware verification, and client UAT sign-off:
        </p>

        <div class="table-responsive">
          <table class="table-custom">
            <thead>
              <tr>
                <th>Milestone Reference</th>
                <th>Target Timeline</th>
                <th>Deliverable Summary</th>
                <th style="text-align: center;">Percentage</th>
                <th style="text-align: right;">Invoice Amount (BHD)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Milestone 1</strong></td>
                <td>End of Week 1</td>
                <td>3-Tier Server Environment, RabbitMQ Broker, SSL/TLS & Backup Automation</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">33.33%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 340.909</td>
              </tr>
              <tr>
                <td><strong>Milestone 2</strong></td>
                <td>End of Week 2</td>
                <td>Handheld Android QR Scanners, ESC/POS Printers & Biometric Clocks</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">33.33%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 340.909</td>
              </tr>
              <tr>
                <td><strong>Milestone 3</strong></td>
                <td>End of Week 3</td>
                <td>Offline Auto-Sync Engine, Multi-Branch Stress Testing & Go-Live</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">33.34%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 340.909</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="3" style="font-weight: 800; color: var(--primary);">TOTAL FIXED CONTRACT VALUE (MODULE 8)</td>
                <td style="text-align: center; font-weight: 800; color: var(--primary);">100.00%</td>
                <td style="text-align: right; font-weight: 800; color: var(--accent); font-size: 15px;">BD 1,022.727</td>
              </tr>
            </tfoot>
          </table>
        </div>"""

content = content.replace(old_sec_5, new_sec_5)

# Write HTML files
with open('SL-POP-ERP-MS-008.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('Hardware_and_Server_Setup_Milestone_and_Payment_Structure.html', 'w', encoding='utf-8') as f:
    f.write(content)

if os.path.exists('popular'):
    with open('popular/SL-POP-ERP-MS-008.html', 'w', encoding='utf-8') as f:
        f.write(content)
    with open('popular/Hardware_and_Server_Setup_Milestone_and_Payment_Structure.html', 'w', encoding='utf-8') as f:
        f.write(content)

print("Generated SL-POP-ERP-MS-008.html successfully.")

# Convert HTML to PDF using Chrome Headless
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

html_abs = os.path.abspath('SL-POP-ERP-MS-008.html')
pdf_abs = os.path.abspath('SL-POP-ERP-MS-008.pdf')

cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    '--no-pdf-header-footer',
    '--print-to-pdf=' + pdf_abs,
    html_abs
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("PDF conversion exit code:", res.returncode)

if os.path.exists(pdf_abs):
    with open('Hardware_and_Server_Setup_Milestone_and_Payment_Structure.pdf', 'wb') as f:
        f.write(open(pdf_abs, 'rb').read())
    if os.path.exists('popular'):
        with open('popular/SL-POP-ERP-MS-008.pdf', 'wb') as f:
            f.write(open(pdf_abs, 'rb').read())
        with open('popular/Hardware_and_Server_Setup_Milestone_and_Payment_Structure.pdf', 'wb') as f:
            f.write(open(pdf_abs, 'rb').read())
    print("PDF distributed successfully.")

    doc = fitz.open(pdf_abs)
    print("Generated PDF Page Count:", len(doc))
    doc.close()

# Update document_meta in databases
for db_path in ['.auth_portal.db', 'popular/.auth_portal.db']:
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO document_meta (doc_id, title, status, finalized_at, finalized_by) VALUES (?, ?, ?, ?, ?)",
                    ('SL-POP-ERP-MS-008', 'Module 8: Hardware Integration, QR Handheld Devices, Thermal Printers & Server Setup Infrastructure Milestone', 'IN_REVIEW', None, None))
        conn.commit()
        conn.close()
        print(f"Updated document_meta in {db_path}")
