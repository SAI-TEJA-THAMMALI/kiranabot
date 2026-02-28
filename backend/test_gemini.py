import asyncio
from core.extraction import extract_invoice_fields

async def test():
    # Use any jpg from invoice_samples folder
    # If no samples yet create a simple test
    with open("../invoice_samples/clean_printed.png", "rb") as f:
        image_bytes = f.read()

    result = await extract_invoice_fields(image_bytes)
    print("GEMINI EXTRACTION:")
    for field, value in result.items():
        icon = "✅" if value is not None else "⬜"
        print(f"  {icon} {field}: {value}")

asyncio.run(test())