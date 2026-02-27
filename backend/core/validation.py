import re

# All 37 Indian state codes
STATE_CODES = {
    "01": "Jammu & Kashmir", "02": "Himachal Pradesh",
    "03": "Punjab", "04": "Chandigarh",
    "05": "Uttarakhand", "06": "Haryana",
    "07": "Delhi", "08": "Rajasthan",
    "09": "Uttar Pradesh", "10": "Bihar",
    "11": "Sikkim", "12": "Arunachal Pradesh",
    "13": "Nagaland", "14": "Manipur",
    "15": "Mizoram", "16": "Tripura",
    "17": "Meghalaya", "18": "Assam",
    "19": "West Bengal", "20": "Jharkhand",
    "21": "Odisha", "22": "Chhattisgarh",
    "23": "Madhya Pradesh", "24": "Gujarat",
    "27": "Maharashtra", "28": "Andhra Pradesh",
    "29": "Karnataka", "30": "Goa",
    "31": "Lakshadweep", "32": "Kerala",
    "33": "Tamil Nadu", "34": "Puducherry",
    "35": "Andaman & Nicobar", "36": "Telangana",
    "37": "Andhra Pradesh (New)",
}

def validate_gstin(gstin: str) -> dict:
    """
    Validates GSTIN format and checksum.
    Returns: {valid: bool, error_reason: str, state: str}
    """
    if not gstin:
        return {"valid": False, "error_reason": "GSTIN is empty", "state": ""}

    gstin = gstin.strip().upper()

    # Format check: 15 characters
    if len(gstin) != 15:
        return {
            "valid": False,
            "error_reason": f"GSTIN must be 15 characters, got {len(gstin)}",
            "state": ""
        }

    # Regex pattern check
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    if not re.match(pattern, gstin):
        return {
            "valid": False,
            "error_reason": "GSTIN format is invalid",
            "state": ""
        }

    # State code check
    state_code = gstin[:2]
    if state_code not in STATE_CODES:
        return {
            "valid": False,
            "error_reason": f"Invalid state code: {state_code}",
            "state": ""
        }

    # Checksum validation
    charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    total = 0
    for i, char in enumerate(gstin[:-1]):
        val = charset.index(char)
        if i % 2 != 0:
            val *= 2
        total += val // len(charset) + val % len(charset)

    checksum = (len(charset) - total % len(charset)) % len(charset)
    expected = charset[checksum]

    if gstin[-1] != expected:
        return {
            "valid": False,
            "error_reason": f"GSTIN checksum invalid",
            "state": STATE_CODES[state_code]
        }

    return {
        "valid": True,
        "error_reason": "",
        "state": STATE_CODES[state_code]
    }


def validate_tax_math(taxable: float, cgst: float,
                       sgst: float, igst: float,
                       rate: float) -> dict:
    """
    Validates tax calculations within ₹1 tolerance.
    """
    expected_each = round(taxable * (rate / 2) / 100, 2)
    expected_igst = round(taxable * rate / 100, 2)

    cgst_ok = abs(cgst - expected_each) <= 1.0
    sgst_ok = abs(sgst - expected_each) <= 1.0
    igst_ok = igst == 0 or abs(igst - expected_igst) <= 1.0

    return {
        "valid": cgst_ok and sgst_ok and igst_ok,
        "expected_cgst": expected_each,
        "expected_sgst": expected_each,
        "expected_igst": expected_igst,
        "actual_cgst": cgst,
        "actual_sgst": sgst,
        "error": "" if (cgst_ok and sgst_ok) else
                 f"Tax mismatch: expected {expected_each} got CGST={cgst} SGST={sgst}"
    }


def classify_transaction(buyer_gstin: str,
                          invoice_value: float) -> str:
    """
    Classifies transaction as B2B, B2CS, or B2CL.
    """
    if buyer_gstin and validate_gstin(buyer_gstin)["valid"]:
        return "B2B"
    if invoice_value > 250000:
        return "B2CL"
    return "B2CS"