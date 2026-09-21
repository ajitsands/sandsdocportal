# SaNDS Lab Enterprise Document Portal & Authentication Engine

## Overview
A secure, device-authenticated enterprise document portal with built-in SQLite user management, permanent device verification, 6-digit OTP delivery, and responsive interactive proposal documentation for **Popular Auto Spare & A/C Parts Co. W.L.L ERP System**.

## Key Features
- **Super Admin Management (`ajit@sandslab.com`)**:
  - Add new authorized email addresses
  - Edit & update user profiles (Name, Organization, Role, Email)
  - 1-click Activate / Deactivate user status (instant token purge)
  - Revoke device access (forces OTP re-verification)
  - Audit trail of active devices and OTP requests
- **Zero-Config SQLite Database**: Auto-initializes tables and initial authorized users on first run (`.auth_portal.db`).
- **6-Digit OTP Delivery**: Corporate HTML email verification via PHP `mail()`.
- **Permanent Device Authentication**: 5-year persistent cookie with device fingerprinting.
- **Interactive Proposal Repository**: Mobile-friendly document viewer with embedded PDF downloads.

## Deployment
Upload files to your server directory (`public_html/docs.sandslab.com/popular/`):
- `index.php`
- `SL-POP-ERP-MS-001.html`
- `SL-POP-ERP-MS-001.pdf`
- `.htaccess`

&copy; 2026 SaNDS Lab Middle East W.L.L. All Rights Reserved.
