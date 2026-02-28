from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
import os
from fastapi.responses import Response
import csv, io



env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="KiranaBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "KiranaBot API running"}

@app.get("/ping")
def ping():
    return {"status": "working"}
@app.get("/export-gstr1/{session_id}")
async def export_gstr1(session_id: str):
    invoices = get_invoices(session_id)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "GSTIN of Supplier", "Invoice Number", "Invoice Date",
        "Invoice Value", "Place of Supply", "Taxable Value",
        "GST Rate", "CGST", "SGST", "IGST", "Type"
    ])

    for inv in invoices:
        ext = inv.get("extraction", inv)
        writer.writerow([
            ext.get("seller_gstin", ""),
            ext.get("invoice_number", ""),
            ext.get("invoice_date", ""),
            ext.get("total", 0),
            ext.get("place_of_supply", ""),
            ext.get("taxable_value", 0),
            ext.get("gst_rate", 18),
            ext.get("cgst", 0),
            ext.get("sgst", 0),
            ext.get("igst", 0),
            inv.get("classification", "B2CS")
        ])

    csv_bytes = ('\ufeff' + output.getvalue()).encode('utf-8')

    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename=GSTR1_{session_id}.csv",
            "Access-Control-Expose-Headers":
            "Content-Disposition"
        }
    )    
