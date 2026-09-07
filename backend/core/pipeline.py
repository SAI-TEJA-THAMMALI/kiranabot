from core.extraction import extract_invoice_fields
from core.validation import validate_gstin, validate_tax_math
from core.classification import classify_transaction, calculate_confidence

async def run_full_pipeline(image_bytes: bytes) -> dict:
    """
    Complete pipeline:
    Gemini extraction → GSTIN validation →
    Tax math check → Classification →
    Confidence scoring
    Returns everything needed for frontend display.
    """

    # Stage 1 — Gemini extraction
    extraction = await extract_invoice_fields(image_bytes)

    # Stage 2 — GSTIN validation
    seller_gstin = extraction.get("seller_gstin") or ""
    gstin_result = validate_gstin(seller_gstin)

    # Stage 3 — Tax math validation
    tax_result = validate_tax_math(
        taxable=extraction.get("taxable_value") or 0,
        cgst=extraction.get("cgst") or 0,
        sgst=extraction.get("sgst") or 0,
        igst=extraction.get("igst") or 0,
        rate=extraction.get("gst_rate") or 18
    )

    # Stage 4 — Transaction classification
    classification = classify_transaction(
        buyer_gstin=extraction.get("buyer_gstin") or "",
        invoice_value=extraction.get("total") or 0,
        seller_state=extraction.get("seller_state") or "",
        buyer_state=extraction.get("buyer_state") or ""
    )

    # Stage 5 — Confidence scoring
    confidence = calculate_confidence(extraction)

    # Stage 6 — Overall status
    all_valid = gstin_result["valid"] and tax_result["valid"]
    has_low_confidence = "LOW" in confidence.values()

    if all_valid and not has_low_confidence:
        status = "READY"
        message = (
            f"Invoice {extraction.get('invoice_number', 'processed')} "
            f"validated successfully. "
            f"Added to GSTR-1 as {classification['type']}."
        )
    elif all_valid and has_low_confidence:
        status = "REVIEW_NEEDED"
        low_fields = [f for f, c in confidence.items() if c == "LOW"]
        message = (
            f"Extracted with low confidence on: "
            f"{', '.join(low_fields)}. Please verify."
        )
    else:
        errors = []
        if not gstin_result["valid"]:
            errors.append(gstin_result["error_reason"])
        if not tax_result["valid"]:
            errors.append(tax_result["error"])
        message = "Validation issues found: " + " | ".join(errors)
        status = "VALIDATION_FAILED"

    return {
        "extraction": extraction,
        "confidence": confidence,
        "validation": {
            "gstin": gstin_result,
            "tax_math": tax_result,
            "classification": classification
        },
        "status": status,
        "message": message
    }