"""
Pre-seeds Supabase with 5 realistic invoices
so the demo looks substantial immediately.
Run this once before the demo.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.supabase_client import get_supabase
from db.session_ops import create_session

DEMO_INVOICES = [
    {
        "seller_name": "Raj Wholesale Traders",
        "seller_gstin": "36AABCU9603R1ZX",
        "buyer_gstin": "29AABCT1234R1ZY",
        "invoice_number": "RWT/2026/0342",
        "invoice_date": "05/02/2026",
        "taxable_value": 15000.00,
        "gst_rate": 18,
        "cgst": 1350.00,
        "sgst": 1350.00,
        "igst": 0,
        "total": 17700.00,
        "hsn_code": "2106",
        "classification": "B2B",
        "gstin_valid": True,
        "tax_valid": True,
    },
    {
        "seller_name": "Hyderabad Food Supplies",
        "seller_gstin": "36AAACH1234R1ZP",
        "buyer_gstin": "",
        "invoice_number": "HFS/FEB/0891",
        "invoice_date": "08/02/2026",
        "taxable_value": 8500.00,
        "gst_rate": 5,
        "cgst": 212.50,
        "sgst": 212.50,
        "igst": 0,
        "total": 8925.00,
        "hsn_code": "1901",
        "classification": "B2CS",
        "gstin_valid": True,
        "tax_valid": True,
    },
    {
        "seller_name": "Telangana Beverages Ltd",
        "seller_gstin": "36AABCT9988R1ZQ",
        "buyer_gstin": "",
        "invoice_number": "TBL/2026/1123",
        "invoice_date": "12/02/2026",
        "taxable_value": 320000.00,
        "gst_rate": 28,
        "cgst": 0,
        "sgst": 0,
        "igst": 89600.00,
        "total": 409600.00,
        "hsn_code": "2202",
        "classification": "B2CL",
        "gstin_valid": True,
        "tax_valid": True,
    },
    {
        "seller_name": "Spice Garden Wholesale",
        "seller_gstin": "29AAACS5678R1ZM",
        "buyer_gstin": "36AABCU9603R1ZX",
        "invoice_number": "SGW/026/0445",
        "invoice_date": "15/02/2026",
        "taxable_value": 22000.00,
        "gst_rate": 12,
        "cgst": 0,
        "sgst": 0,
        "igst": 2640.00,
        "total": 24640.00,
        "hsn_code": "0910",
        "classification": "B2B",
        "gstin_valid": True,
        "tax_valid": True,
    },
    {
        "seller_name": "Quick Mart Distributors",
        "seller_gstin": "36AAACQ4321R1ZR",
        "buyer_gstin": "",
        "invoice_number": "QMD/FEB/0234",
        "invoice_date": "20/02/2026",
        "taxable_value": 5200.00,
        "gst_rate": 18,
        "cgst": 468.00,
        "sgst": 468.00,
        "igst": 0,
        "total": 6136.00,
        "hsn_code": "3304",
        "classification": "B2CS",
        "gstin_valid": True,
        "tax_valid": True,
    },
]

def seed_demo():
    print("Seeding demo data...")
    db = get_supabase()

    # Create demo session
    session = create_session("2026-02")
    session_id = session.get("id")
    print(f"Demo session created: {session_id}")

    # Insert all invoices
    for i, inv in enumerate(DEMO_INVOICES):
        inv["session_id"] = session_id
        db.table("invoices").insert(inv).execute()
        print(f"  Invoice {i+1} seeded: {inv['invoice_number']}")

    print(f"\nDemo data ready.")
    print(f"Session ID: {session_id}")
    print(f"Use this session_id in your demo URL.")
    return session_id

if __name__ == "__main__":
    seed_demo()