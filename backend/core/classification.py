from .validation import validate_gstin

def classify_transaction(buyer_gstin: str,
                          invoice_value: float,
                          seller_state: str,
                          buyer_state: str) -> dict:
    """
    Full B2B / B2CS / B2CL classification with IGST logic.
    """
    is_interstate = seller_state != buyer_state

    # B2B — registered buyer
    if buyer_gstin and validate_gstin(buyer_gstin)["valid"]:
        return {
            "type": "B2B",
            "tax_type": "IGST" if is_interstate else "CGST+SGST",
            "gstr1_table": "Table 4"
        }

    # B2CL — unregistered buyer, high value, interstate
    if invoice_value > 250000 and is_interstate:
        return {
            "type": "B2CL",
            "tax_type": "IGST",
            "gstr1_table": "Table 5"
        }

    # B2CS — everything else
    return {
        "type": "B2CS",
        "tax_type": "IGST" if is_interstate else "CGST+SGST",
        "gstr1_table": "Table 7"
    }


def calculate_confidence(extracted_fields: dict) -> dict:
    """
    Assigns HIGH/MEDIUM/LOW confidence to each field.
    """
    confidence = {}

    for field, value in extracted_fields.items():
        if value is None or value == "":
            confidence[field] = "LOW"
        elif field == "gstin":
            from .validation import validate_gstin
            result = validate_gstin(str(value))
            confidence[field] = "HIGH" if result["valid"] else "LOW"
        elif field in ["invoice_number", "invoice_date"]:
            confidence[field] = "HIGH" if value else "LOW"
        elif field in ["taxable_value", "cgst", "sgst", "total"]:
            confidence[field] = "HIGH" if isinstance(
                value, (int, float)) and value > 0 else "MEDIUM"
        else:
            confidence[field] = "MEDIUM"

    return confidence