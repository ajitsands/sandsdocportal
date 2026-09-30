import os
import re
import subprocess
import fitz
import sqlite3

# Read SL-POP-ERP-MS-006.html as the base template
with open('SL-POP-ERP-MS-006.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace document IDs and titles
content = template

# Replace PHP doc_id and Title
content = content.replace("$doc_id = 'SL-POP-ERP-MS-006';", "$doc_id = 'SL-POP-ERP-MS-007';")
content = content.replace("'Module 6: Enterprise Administration, Facility Management, Fixed Assets, Fleet & Document Control Milestone'",
                          "'Module 7: Human Resource Management, Biometric Attendance, Bahrain Labour Law Leave, Automated Payroll & Gratuity Milestone'")

# Replace title and header tags
content = content.replace("SL-POP-ERP-MS-006: Enterprise Administration, Facility, Fixed Assets & Fleet Milestone Agreement",
                          "SL-POP-ERP-MS-007: Human Resource Management, Biometric Attendance, Payroll & Gratuity Milestone Agreement")

content = content.replace("SL-POP-ERP-MS-006", "SL-POP-ERP-MS-007")
content = content.replace("DOC-006", "DOC-007")

# Replace hero card and titles
content = content.replace("Module 6: Enterprise Administration, Facility Management, Fixed Assets, Fleet & Corporate Document Control",
                          "Module 7: Human Resource Management, Biometric Attendance, Bahrain Labour Law Leave, Automated Payroll & Gratuity / EOSB")

content = content.replace("Comprehensive 12-week milestone agreement, engineering effort breakdown, resource cost schedule, and acceptance criteria based on the verified Business Analysis Report <strong>DOC-007 v1.0</strong> for <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong>.",
                          "Comprehensive 16-week milestone agreement, dedicated engineering team breakdown, Bahrain regulatory compliance matrix (SIO / GOSI / LMRA / WPS), and payment schedule based on the verified Business Analysis Report <strong>DOC-007 v1.0</strong> for <strong>Popular Auto Spare & A/C Parts Co. W.L.L</strong>.")

content = content.replace("12 Working Weeks (3.0 Months)", "16 Working Weeks (4.0 Months / 80 Days)")
content = content.replace("12 Working Weeks (3.0 Months / 60 Days)", "16 Working Weeks (4.0 Months / 80 Days)")
content = content.replace("BD 4,090.909", "BD 5,454.548")
content = content.replace("BD 1,022.727", "BD 1,363.637")
content = content.replace("Multi-Branch Admin & Asset Tracking", "Multi-Branch HRMS, Biometric Attendance & WPS Payroll")
content = content.replace("Facility, Assets, Fleet & Docs", "HRMS, Attendance, Payroll & EOSB")
content = content.replace("DOC-007 v1.0 (25 pgs)", "DOC-007 v1.0 (80 pgs)")

# Replace Executive summary text
old_exec_summary = """The <strong>Enterprise Administration Modules</strong> (Module 6) provide the operational infrastructure, asset tracking, facility governance, fleet control, and statutory legal document compliance framework for Popular Auto Spare & A/C Parts Co. W.L.L. As the enterprise expands across regional distribution hubs, retail branches, and central warehouses, managing physical facilities, tracking fixed assets with QR codes, optimizing fleet operations, and safeguarding legal corporate records become vital for cost control, security, and statutory readiness."""

new_exec_summary = """Human Resource Management (Module 7) serves as the core workforce governance, statutory regulatory compliance, biometric timekeeping, automated payroll, and employee lifecycle engine for <strong>Popular Auto Spare & A/C Parts Co. W.L.L.</strong> Across multi-country supplier interactions, regional distribution hubs, branch showrooms, central warehouses, and service centers, managing over hundreds of multi-national employees with strict adherence to <strong>Bahrain Labour Law (Law No. 36 of 2012)</strong>, <strong>Social Insurance Organization (SIO / GOSI)</strong>, <strong>Labour Market Regulatory Authority (LMRA)</strong>, and <strong>Central Bank of Bahrain (CBB) Wage Protection System (WPS)</strong> is mission-critical."""

content = content.replace(old_exec_summary, new_exec_summary)

# Replace Core objective
old_obj = """To establish an integrated administrative operations platform consolidating Workplace Facility Management, QR-based Fixed Asset Lifecycle Tracking & Depreciation, Commercial Fleet & Vehicle Logistics Management, Staff Physical Locker Allocations, and Secure Digital Document & Statutory Renewal Governance."""

new_obj = """To establish an enterprise Human Resource platform consolidating Multi-Branch Organization Structure, Employee 360° Profiles & Document Expiry Vault, Recruitment ATS, Biometric Attendance & Shift Rosters, Bahrain Statutory Leave Engine, Automated Monthly Payroll, SIO/LMRA Compliance, CBB WPS Bank Export, Employee Loans, and Bahrain End-of-Service Benefit (EOSB / Gratuity) Settlement."""

content = content.replace(old_obj, new_obj)

# Replace Roadmap Box
old_roadmap_box = """        <!-- Master ERP Transformation Architecture (9 Core Modules) -->
        <div class="roadmap-box">
          <div class="roadmap-header">
            <h4>Master ERP Transformation Architecture (9 Core Process Modules)</h4>
            <span class="badge-tag badge-primary" style="font-size: 10.5px; padding: 4px 12px; letter-spacing: 0.5px;">CURRENT SCOPE: MODULE 06 ACTIVE</span>
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
            <div class="roadmap-item active">
              <span class="rm-badge">06</span>
              <span class="rm-name">Administration & Security</span>
            </div>
            <div class="roadmap-item">
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

content = content.replace(old_roadmap_box, new_roadmap_box)

# Replace 3 Highlight feature cards in Section 1
old_grid_3 = """        <div class="grid-3">
          <div class="feature-card">
            <div class="feature-icon gold"><i class="fas fa-building"></i></div>
            <div class="feature-title">Facility, Lease & Utility Control</div>
            <div class="feature-desc">Centralized facility registry, preventive/corrective work orders, utility expense tracking, property lease renewal alerts, and visitor access control.</div>
            <div class="feature-tags">
              <span class="feature-tag">Facility Master</span>
              <span class="feature-tag">Lease Alerts</span>
              <span class="feature-tag">Utility Log</span>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon emerald"><i class="fas fa-qrcode"></i></div>
            <div class="feature-title">QR Fixed Asset Lifecycle & Audit</div>
            <div class="feature-desc">QR code tagging, custodian assignment, multi-branch asset transfers, straight-line depreciation calculation, and annual physical audit verification.</div>
            <div class="feature-tags">
              <span class="feature-tag">QR Tagging</span>
              <span class="feature-tag">Depreciation</span>
              <span class="feature-tag">Asset Audit</span>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-icon blue"><i class="fas fa-truck-moving"></i></div>
            <div class="feature-title">Fleet Logistics & Document Vault</div>
            <div class="feature-desc">Commercial vehicle tracking, driver bookings, fuel consumption logs, insurance/road tax compliance, physical locker allocation, and corporate digital document repository.</div>
            <div class="feature-tags">
              <span class="feature-tag">Fleet TCO</span>
              <span class="feature-tag">Fuel Log</span>
              <span class="feature-tag">Digital Vault</span>
            </div>
          </div>
        </div>"""

new_grid_3 = """        <div class="grid-3">
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

content = content.replace(old_grid_3, new_grid_3)

# Replace Section 2 Functional Scope Breakdown
old_section_2 = """      <!-- Section 2: Functional Scope Breakdown (DOC-006) -->
      <section class="doc-section" id="module-scope">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 2.0</span>
            <h2 class="section-title">Module 6: Functional Scope & Architecture Breakdown (BA Ref: DOC-006)</h2>
          </div>
          <span class="section-badge">Full Specification Mapping</span>
        </div>

        <p>
          Derived directly from the 25 pages of <strong>DOC-006: Administration Modules Business Analysis Report</strong>, the implementation scope is structured across 4 core operational pillars:
        </p>

        <div class="grid-2" style="margin-top: 24px;">
          
          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-city"></i> 2.1 Facility & Workplace Office Management
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Facility Master:</strong> Centralized registry of corporate offices, regional branches, central warehouses, workshops, retail outlets, and staff accommodations.</li>
                <li><strong>Maintenance Work Orders:</strong> Preventive scheduled maintenance calendars, AMC vendor contracts, breakdown ticketing, and repair sign-off.</li>
                <li><strong>Employee Service Requests:</strong> Internal ticketing portal for electrical, HVAC/air conditioning, plumbing, carpentry, and IT infrastructure requests.</li>
                <li><strong>Utility & Consumption Control:</strong> Monthly tracking of electricity, water, internet, telephone, gas, and generator fuel with budget variance analysis.</li>
                <li><strong>Visitor Management (VMS):</strong> Digital visitor registration, badge generation, host employee notification, and entry/exit timestamp logging.</li>
                <li><strong>Lease & Property Governance:</strong> Landlord agreements, rent payment schedules, commercial lease terms, and automated renewal notifications.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-barcode"></i> 2.2 Fixed Asset Management & QR Lifecycle Tracking
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Asset Master Registry:</strong> Comprehensive cataloging of IT equipment, warehouse machinery, tools, office furniture, vehicles, and facilities.</li>
                <li><strong>QR Code Tagging & Scanner:</strong> Unique asset QR label generation with handheld scanner integration for rapid location identification and audits.</li>
                <li><strong>Asset Custody & Movements:</strong> Tracking of employee custodians, department assignments, and inter-branch transfer delivery challans.</li>
                <li><strong>Warranty & AMC Management:</strong> Supplier warranty coverage tracking, AMC renewal alerts, and maintenance history logging.</li>
                <li><strong>Depreciation Engine:</strong> Automated straight-line and reducing-balance depreciation posting integrated directly with General Ledger (GL).</li>
                <li><strong>Physical Audit & Disposal:</strong> Periodic physical inventory verification, variance logging, asset write-off, and scrap disposal workflows.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-truck"></i> 2.3 Fleet Logistics, Vehicle Maintenance & Total Cost of Ownership
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Vehicle Master Registry:</strong> Profile management for commercial delivery vans, heavy transport trucks, pickups, and corporate cars.</li>
                <li><strong>Vehicle Allocation & Booking:</strong> Driver assignment, delivery route scheduling, key management, and trip odometer logging.</li>
                <li><strong>GPS & Route Monitoring:</strong> Integration with telematics for real-time delivery tracking and mileage verification.</li>
                <li><strong>Preventive Maintenance:</strong> Service intervals by mileage/date, oil changes, tire replacement logs, and workshop repair history.</li>
                <li><strong>Fuel Management:</strong> Fuel card reconciliation, fuel receipt uploads, kilometer-per-liter efficiency analysis, and fuel theft anomaly detection.</li>
                <li><strong>Statutory Vehicle Compliance:</strong> Traffic registration renewals, comprehensive insurance policies, fitness certificates, and accident claim workflows.</li>
                <li><strong>Vehicle TCO Analytics:</strong> Real-time Total Cost of Ownership (TCO) tracking per vehicle combining fuel, maintenance, insurance, and depreciation.</li>
              </ul>
            </div>
          </div>

          <div class="feature-card">
            <div class="feature-title" style="color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i class="fas fa-folder-open"></i> 2.4 Staff Locker & Corporate Document Management System
            </div>
            <div class="feature-desc">
              <ul style="padding-left: 18px; margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">
                <li><strong>Staff Locker Management:</strong> Branch physical locker registry, employee key allocation, locker inspections, and surrender protocols.</li>
                <li><strong>Digital Document Repository:</strong> Encrypted digital vault for Commercial Registrations (CR), municipality licenses, lease agreements, vehicle titles, and contracts.</li>
                <li><strong>Role-Based Access Control (RBAC):</strong> Granular permissions restricting document access to authorized executive and HR/Admin personnel.</li>
                <li><strong>Physical Document Movement:</strong> Barcoded checkout/check-in tracking for original legal deeds, bank guarantees, and official certificates.</li>
                <li><strong>Automated Expiry & Renewal Alerts:</strong> Proactive 90/60/30-day notifications for CR renewals, chamber of commerce, civil defense, and trade permits.</li>
                <li><strong>Compliance Audit Readiness:</strong> Full historical audit trail of document uploads, version updates, downloads, and custodian modifications.</li>
              </ul>
            </div>
          </div>

        </div>
      </section>"""

new_section_2 = """      <!-- Section 2: Functional Scope Breakdown (DOC-007) -->
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
                <li><strong>Manpower Requisition:</strong> Department vacancy requisition, budget validation, multi-tier approval, and internal/external job postings.</li>
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

content = content.replace(old_section_2, new_section_2)

# Replace Section 3 Resource table
old_sec_3 = """      <!-- Section 3: Dedicated Resource Pricing Matrix -->
      <section class="doc-section" id="pricing-matrix">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 3.0</span>
            <h2 class="section-title">Project Team Structure & Dedicated Resource Pricing (12 Weeks / 3.0 Months)</h2>
          </div>
          <span class="section-badge">Rate Card Compliance</span>
        </div>

        <p>
          In strict accordance with the <strong>SaNDS Lab Dedicated Engineering Rate Card</strong>, the resource allocation and cost breakdown for the 12-week (3.0 months / 60 working days) delivery of Module 6 is structured as follows (all figures in <strong>Bahraini Dinars - BHD</strong>):
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
                  <span style="font-size: 11.5px; color: var(--gray-500);">Facility architecture, asset tracking workflows, sprint management & client sign-offs</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 545.455</td>
                <td style="text-align: center;">3.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 1,636.365</td>
              </tr>
              <tr>
                <td>
                  <strong>Back-End Lead Engineer (PHP MVC / REST APIs)</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Depreciation engine, QR tracking backend, fleet logistics APIs & document security vault</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 227.273</td>
                <td style="text-align: center;">3.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 681.819</td>
              </tr>
              <tr>
                <td>
                  <strong>Front-End Lead Engineer (React / UI Design Tokens)</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Responsive admin dashboards, asset QR scanner interface, vehicle scheduling & locker UI</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 227.273</td>
                <td style="text-align: center;">3.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 681.819</td>
              </tr>
              <tr>
                <td>
                  <strong>Database & Cloud DevOps Specialist</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">MySQL asset schemas, document repository encryption, backup automation & performance tuning</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 204.545</td>
                <td style="text-align: center;">3.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 613.635</td>
              </tr>
              <tr>
                <td>
                  <strong>QA Automation & UAT Test Lead</strong><br>
                  <span style="font-size: 11.5px; color: var(--gray-500);">Depreciation verification test suites, barcode scanning tests, multi-branch UAT & security audits</span>
                </td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">100% Dedicated</span></td>
                <td style="text-align: right;">BD 159.091</td>
                <td style="text-align: center;">3.0 Months</td>
                <td style="text-align: right; font-weight: 700;">BD 477.273</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="2" style="font-weight: 800; color: var(--primary);">TOTAL DEDICATED ENGINEERING TEAM FEE</td>
                <td style="text-align: right; font-weight: 800; color: var(--primary);">BD 1,363.636 / Mo</td>
                <td style="text-align: center; font-weight: 800; color: var(--primary);">12 Working Weeks</td>
                <td style="text-align: right; font-weight: 800; color: var(--accent); font-size: 15px;">BD 4,090.909</td>
              </tr>
            </tfoot>
          </table>
        </div>"""

new_sec_3 = """      <!-- Section 3: Dedicated Resource Pricing Matrix -->
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

content = content.replace(old_sec_3, new_sec_3)

# Replace Section 4 Detailed Roadmap
old_sec_4 = """      <!-- Section 4: Detailed Milestones -->
      <section class="doc-section" id="detailed-milestones">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 4.0</span>
            <h2 class="section-title">Detailed Milestone Breakdown & Deliverables (12-Week Roadmap)</h2>
          </div>
          <span class="section-badge">Phased Engineering Plan</span>
        </div>

        <p>
          The implementation is organized into 4 sequential 3-week milestones (25.00% each), guaranteeing focused execution, continuous integration, and transparent deliverable acceptance:
        </p>

        <div style="margin-top: 24px; display: flex; flex-direction: column; gap: 20px;">
          
          <!-- Milestone 1 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 1 (Weeks 1–3)</span>
                <span class="ms-heading">Facility Master, Maintenance Work Orders, Utility Tracking & Lease Governance</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 1,022.727</div>
                <div class="ms-pct">25.00% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Centralized Facility Master across corporate HQ, regional branches, central warehouses, and staff accommodations.</li>
                  <li>Preventive and breakdown maintenance ticketing system with AMC vendor contract tracking and repair sign-offs.</li>
                  <li>Employee internal service request portal (HVAC, electrical, plumbing, carpentry, IT).</li>
                  <li>Utility bill tracking (electricity, water, internet, telephone, gas, generator fuel) with budget variance analysis.</li>
                  <li>Digital Visitor Management System (VMS) with badge printing and host notifications.</li>
                  <li>Commercial property lease repository, landlord payment schedules, and automated renewal alerts.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>Relational database schema for Facilities, Work Orders, Utilities, and Leases.</li>
                  <li>Automated daily cron service for 90/60/30-day lease renewal notifications.</li>
                  <li>RESTful API endpoints for work order logging and service ticket status updates.</li>
                  <li>Responsive web dashboards for Facility Supervisors and Office Managers.</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Milestone 2 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 2 (Weeks 4–6)</span>
                <span class="ms-heading">Fixed Assets Master, QR Barcode Tagging, Custody Transfers & Depreciation Engine</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 1,022.727</div>
                <div class="ms-pct">25.00% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Centralized Fixed Assets Master categorized by IT, machinery, tools, furniture, vehicles, and facilities.</li>
                  <li>Unique QR code label generation and handheld scanner integration for physical audits.</li>
                  <li>Employee asset custody assignments, department allocations, and inter-branch asset delivery challans.</li>
                  <li>Supplier warranty and AMC renewal tracking.</li>
                  <li>Automated Straight-Line & Declining Balance Depreciation Calculation Engine integrated with General Ledger (GL).</li>
                  <li>Periodic physical inventory audit reconciliation, asset write-off, and scrap disposal workflows.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>QR Code generator library integration with thermal label printing support.</li>
                  <li>Real-time asset movement logging and custody handoff authorization workflows.</li>
                  <li>Automated monthly depreciation journal voucher posting daemon.</li>
                  <li>Physical audit handheld scanner listener and discrepancy report generator.</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Milestone 3 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 3 (Weeks 7–9)</span>
                <span class="ms-heading">Vehicle Fleet Registry, Route Allocation, Fuel Tracking & Statutory Vehicle Compliance</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 1,022.727</div>
                <div class="ms-pct">25.00% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Vehicle Master Profiles for delivery vans, heavy transport trucks, pickups, and company cars.</li>
                  <li>Driver allocation, delivery route dispatching, key management, and trip odometer logging.</li>
                  <li>Telematics / GPS integration for live route tracking and mileage verification.</li>
                  <li>Mileage-based and date-based preventive maintenance scheduling (oil change, tire rotations, brake inspection).</li>
                  <li>Fuel card reconciliation, kilometer-per-liter efficiency monitoring, and fuel theft anomaly detection.</li>
                  <li>Statutory vehicle compliance tracking (traffic registration renewals, comprehensive insurance, fitness certificates, accident claims).</li>
                  <li>Vehicle Total Cost of Ownership (TCO) analytics.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>Fleet logistics database schema and trip tracking API endpoints.</li>
                  <li>Automated statutory vehicle document expiry notification daemon.</li>
                  <li>Fuel receipt image upload and mileage efficiency calculation service.</li>
                  <li>Vehicle TCO analytics dashboard with comparative monthly cost breakdowns.</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Milestone 4 -->
          <div class="milestone-block">
            <div class="ms-top-bar">
              <div class="ms-title-area">
                <span class="ms-tag">Milestone 4 (Weeks 10–12)</span>
                <span class="ms-heading">Staff Locker Management, Corporate Legal Document Control, UAT & Production Go-Live</span>
              </div>
              <div class="ms-amount-box">
                <div class="ms-amount">BD 1,022.727</div>
                <div class="ms-pct">25.00% Allocation</div>
              </div>
            </div>
            <div class="ms-body">
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-check-circle" style="color: var(--success);"></i> Core Functional Deliverables</div>
                <ul class="ms-list">
                  <li>Branch staff physical locker master, key assignments, inspection logs, and surrender protocols.</li>
                  <li>Encrypted Corporate Legal Document Vault with Role-Based Access Control (RBAC).</li>
                  <li>Physical document barcoded movement tracking for original deeds, bank guarantees, and commercial agreements.</li>
                  <li>Automated 90/60/30-day proactive expiry notifications for Commercial Registrations (CR), Municipality Licenses, Civil Defense, and Leases.</li>
                  <li>Comprehensive multi-branch UAT sign-off, data migration, and full production deployment.</li>
                </ul>
              </div>
              <div class="ms-col">
                <div class="ms-col-title"><i class="fas fa-microchip" style="color: var(--secondary);"></i> Technical & Architectural Outputs</div>
                <ul class="ms-list">
                  <li>AES-256 encrypted digital document storage engine.</li>
                  <li>Barcoded physical document checkout/check-in tracking subsystem.</li>
                  <li>Full regression test suite execution and performance load testing.</li>
                  <li>Production rollout, SSL certification, and automated daily backup verification.</li>
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
                  <li>Training needs analysis, course catalog, training budget tracking, and employee certifications.</li>
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

content = content.replace(old_sec_4, new_sec_4)

# Replace Section 5 Payment Schedule
old_sec_5 = """      <!-- Section 5: Payment Schedule -->
      <section class="doc-section" id="payment-schedule">
        <div class="section-header">
          <div class="section-title-wrap">
            <span class="section-num">Section 5.0</span>
            <h2 class="section-title">Milestone Payment Structure & Invoicing Schedule (12-Week Model)</h2>
          </div>
          <span class="section-badge">Commercial Terms</span>
        </div>

        <p>
          Payments are structured in 4 equal milestone disbursements of 25.00% (BD 1,022.727 each), tied strictly to formal milestone deliverables and client sign-off:
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
                <td>End of Week 03</td>
                <td>Facility Master, Maintenance Orders, Utility Tracking & Lease Governance</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">25.00%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 1,022.727</td>
              </tr>
              <tr>
                <td><strong>Milestone 2</strong></td>
                <td>End of Week 06</td>
                <td>Fixed Asset Master, QR Barcode Tagging, Custody & Depreciation Engine</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">25.00%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 1,022.727</td>
              </tr>
              <tr>
                <td><strong>Milestone 3</strong></td>
                <td>End of Week 09</td>
                <td>Vehicle Fleet Management, Fuel Tracking, Maintenance & Statutory Renewals</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">25.00%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 1,022.727</td>
              </tr>
              <tr>
                <td><strong>Milestone 4</strong></td>
                <td>End of Week 12</td>
                <td>Staff Lockers, Legal Doc Vault, Multi-Branch UAT & Production Go-Live</td>
                <td style="text-align: center;"><span class="badge-tag badge-primary">25.00%</span></td>
                <td style="text-align: right; font-weight: 700;">BD 1,022.727</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="3" style="font-weight: 800; color: var(--primary);">TOTAL FIXED CONTRACT VALUE (MODULE 6)</td>
                <td style="text-align: center; font-weight: 800; color: var(--primary);">100.00%</td>
                <td style="text-align: right; font-weight: 800; color: var(--accent); font-size: 15px;">BD 4,090.909</td>
              </tr>
            </tfoot>
          </table>
        </div>"""

new_sec_5 = """      <!-- Section 5: Payment Schedule -->
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

content = content.replace(old_sec_5, new_sec_5)

# Write HTML files
with open('SL-POP-ERP-MS-007.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('Human_Resource_Management_Milestone_and_Payment_Structure.html', 'w', encoding='utf-8') as f:
    f.write(content)

if os.path.exists('popular'):
    with open('popular/SL-POP-ERP-MS-007.html', 'w', encoding='utf-8') as f:
        f.write(content)
    with open('popular/Human_Resource_Management_Milestone_and_Payment_Structure.html', 'w', encoding='utf-8') as f:
        f.write(content)

print("Generated SL-POP-ERP-MS-007.html successfully.")

# Convert HTML to PDF using Chrome Headless
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

html_abs = os.path.abspath('SL-POP-ERP-MS-007.html')
pdf_abs = os.path.abspath('SL-POP-ERP-MS-007.pdf')

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
    with open('Human_Resource_Management_Milestone_and_Payment_Structure.pdf', 'wb') as f:
        f.write(open(pdf_abs, 'rb').read())
    if os.path.exists('popular'):
        with open('popular/SL-POP-ERP-MS-007.pdf', 'wb') as f:
            f.write(open(pdf_abs, 'rb').read())
        with open('popular/Human_Resource_Management_Milestone_and_Payment_Structure.pdf', 'wb') as f:
            f.write(open(pdf_abs, 'rb').read())
    print("PDF distributed successfully.")

    doc = fitz.open(pdf_abs)
    print("Generated PDF Page Count:", len(doc))
    doc.close()
