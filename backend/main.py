from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
import os

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

@app.post("/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):
    # STUB — real logic added in T18
    return {
        "status": "received",
        "filename": file.filename,
        "mock_extraction": {
            "gstin": "29AABCU9603R1ZX",
            "invoice_number": "INV-001",
            "invoice_date": "2024-01-15",
            "taxable_value": 10000,
            "cgst": 900,
            "sgst": 900,
            "total": 11800
        }
    }

@app.post("/create-session")
async def create_session(period: str = "2024-01"):
    return {"session_id": "mock-session-001", "period": period}

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    return {"session_id": session_id, "invoices": []}