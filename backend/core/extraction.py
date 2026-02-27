import google.generativeai as genai
import json
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

EXTRACTION_PROMPT = """
You are a GST invoice data extraction specialist.
Extract ALL fields from this invoice image.
If a field is not visible return null.
Return ONLY valid JSON. No explanation. No markdown.

{
  "seller_name": "string or null",
  "seller_gstin": "string or null",
  "seller_state": "string or null",
  "buyer_name": "string or null",
  "buyer_gstin": "string or null",
  "buyer_state": "string or null",
  "invoice_number": "string or null",
  "invoice_date": "string or null",
  "taxable_value": "number or null",
  "gst_rate": "number or null",
  "cgst": "number or null",
  "sgst": "number or null",
  "igst": "number or null",
  "total": "number or null",
  "hsn_code": "string or null",
  "place_of_supply": "string or null"
}

Rules:
- All monetary values must be numbers not strings
- Dates in DD/MM/YYYY format
- GST rate as number like 18 not 18%
- Extract GSTIN exactly as printed
"""

async def extract_invoice_fields(image_bytes: bytes) -> dict:
    try:
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_bytes
        }
        response = model.generate_content(
            [EXTRACTION_PROMPT, image_part]
        )
        raw_text = response.text.strip()

        # Clean markdown if Gemini wraps in code block
        if "```" in raw_text:
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]

        extracted = json.loads(raw_text.strip())

        # Ensure all fields exist
        for field in _empty_extraction().keys():
            if field not in extracted:
                extracted[field] = None

        return extracted

    except Exception as e:
        print(f"Gemini extraction failed: {e}")
        return _empty_extraction()


def _empty_extraction() -> dict:
    return {
        "seller_name": None,
        "seller_gstin": None,
        "seller_state": None,
        "buyer_name": None,
        "buyer_gstin": None,
        "buyer_state": None,
        "invoice_number": None,
        "invoice_date": None,
        "taxable_value": None,
        "gst_rate": None,
        "cgst": None,
        "sgst": None,
        "igst": None,
        "total": None,
        "hsn_code": None,
        "place_of_supply": None
    }