from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_chat_response(
    extraction: dict,
    validation: dict,
    scenario: str
) -> str:
    """
    Generates WhatsApp-style chat response.
    scenario: 'success' | 'low_confidence' | 
              'validation_error' | 'preflight_fail'
    """

    if scenario == "preflight_fail":
        return (
            "📸 I couldn't read that image clearly. "
            "Please retake the photo in good lighting "
            "and make sure the invoice is flat. Try again!"
        )

    if scenario == "validation_error":
        errors = []
        if not validation.get("gstin", {}).get("valid"):
            errors.append(
                validation.get("gstin", {}).get(
                    "error_reason", "GSTIN issue"
                )
            )
        if not validation.get("tax_math", {}).get("valid"):
            errors.append(
                validation.get("tax_math", {}).get(
                    "error", "Tax math issue"
                )
            )
        error_text = "\n".join(errors) if errors else "Validation failed"
        return (
            f"⚠️ I found some issues with this invoice:\n\n"
            f"{error_text}\n\n"
            f"Please check and confirm the details."
        )

    if scenario == "low_confidence":
        return (
            "🔍 Invoice processed but I'm not fully confident "
            "about some fields shown in yellow. "
            "Please review and correct if needed before export."
        )

    # Success — use Groq for natural response
    try:
        invoice_no = extraction.get(
            "invoice_number", "this invoice"
        )
        total = extraction.get("total", 0)
        tx_type = validation.get(
            "classification", {}
        ).get("type", "B2CS")

        prompt = f"""You are KiranaBot, a friendly GST assistant 
for Indian kirana store owners.
An invoice was successfully processed.
Generate a SHORT WhatsApp message (2-3 lines max).

Invoice details:
- Invoice number: {invoice_no}
- Total amount: Rs.{total}
- Transaction type: {tx_type}
- All validations passed

Be friendly, use 1-2 emojis, mention invoice number,
say it was added to GSTR-1 draft.
Keep it under 50 words."""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        return response.choices[0].message.content

    except Exception as e:
        # Fallback if Groq fails
        invoice_no = extraction.get("invoice_number", "Invoice")
        return (
            f"✅ {invoice_no} processed successfully! "
            f"All fields validated and added to your "
            f"GSTR-1 draft. Ready for export."
        )