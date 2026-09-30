import re

with open('scratch/doc_004_summary.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect sections 1.1 to 1.21 in detail
section_names = [
    "1.1. Objective",
    "1.2. Business Overview and Operational Context",
    "1.3. Customer Master Management",
    "1.4. Sales Initiation and Customer Interaction",
    "1.5. Item Identification, Intelligent Search & Pricing Control",
    "1.6. Sales Process with Handheld Devices",
    "1.7. Sales Attribution & Performance Accountability",
    "1.8. Sales Return Management Module",
    "1.9. Inventory Impact and Item Handling in Sales Return",
    "1.10. Commission Adjustment on Sales Return",
    "1.11. Settlement Adjustment on Sales Return",
    "1.12. Less Item Handling Module",
    "1.13. Branch-to-Branch Transfer",
    "1.14. Branch-to-Garage Sales",
    "1.15. Sales Document Modules",
    "1.16. Other Accounting Documents Handling in Branches",
    "1.17. Accounting & Branch Financial Control Module",
    "1.18. Daily Closing Process",
    "1.19. Audit & Control",
    "1.20. Pricing Update Notification",
    "1.21. Conclusion"
]

print(f"Total length of summary: {len(text)} characters")
