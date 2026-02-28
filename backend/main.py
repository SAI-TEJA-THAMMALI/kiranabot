from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
import os
from fastapi.responses import Response
import csv, io



env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from core.preflight import preflight_check
from core.pipeline import run_full_pipeline
from core.chat import generate_chat_response
from db.invoice_ops import save_invoice, get_invoices
from db.session_ops import create_session, get_session

app = FastAPI(title="KiranaBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/upload-invoice")
async def upload_invoice(
    file: UploadFile = File(...),
    session_id: str = "default"
):
    # Read file bytes
    image_bytes = await file.read()

    # Step 1 — Preflight check
    preflight = preflight_check(image_bytes)
    if not preflight["passed"]:
        return {
            "status": "preflight_failed",
            "message": preflight["message"],
            "chat_response": preflight["message"]
        }

    # Step 2 — Run full AI pipeline
    pipeline_result = await run_full_pipeline(image_bytes)

    # Step 3 — Generate chat response
    chat_response = generate_chat_response(
        extraction=pipeline_result["extraction"],
        validation=pipeline_result["validation"],
        scenario=(
            "success"
            if pipeline_result["status"] == "READY"
            else "low_confidence"
            if pipeline_result["status"] == "REVIEW_NEEDED"
            else "validation_error"
        )
    )

    # Step 4 — Save to Supabase
    saved = save_invoice({
        "session_id": session_id,
        "filename": file.filename,
        "extraction": pipeline_result["extraction"],
        "classification": pipeline_result[
            "validation"]["classification"]["type"],
        "gstin_valid": pipeline_result[
            "validation"]["gstin"]["valid"],
        "tax_valid": pipeline_result[
            "validation"]["tax_math"]["valid"],
    })

    return {
        "status": "success",
        "pipeline_status": pipeline_result["status"],
        "extraction": pipeline_result["extraction"],
        "confidence": pipeline_result["confidence"],
        "validation": pipeline_result["validation"],
        "chat_response": chat_response,
        "invoice_id": saved.get("id")
    }

@app.post("/create-session")
async def new_session(period: str = "2026-02"):
    return create_session(period)

@app.get("/session/{session_id}")
async def fetch_session(session_id: str):
    return get_session(session_id)

@app.get("/session/{session_id}/invoices")
async def fetch_invoices(session_id: str):
    return get_invoices(session_id)