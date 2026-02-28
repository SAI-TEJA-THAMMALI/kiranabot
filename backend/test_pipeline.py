import asyncio
from core.pipeline import run_full_pipeline

async def test():
    with open("../invoice_samples/clean_printed.png", "rb") as f:
        image_bytes = f.read()

    result = await run_full_pipeline(image_bytes)

    print("PIPELINE STATUS:", result["status"])
    print("MESSAGE:", result["message"])
    print("\nVALIDATION:")
    print("  GSTIN valid:", result["validation"]["gstin"]["valid"])
    print("  Tax valid:", result["validation"]["tax_math"]["valid"])
    print("  Type:", result["validation"]["classification"]["type"])
    print("\nCONFIDENCE:")
    for field, conf in result["confidence"].items():
        icon = "🟢" if conf=="HIGH" else "🟡" if conf=="MEDIUM" else "🔴"
        print(f"  {icon} {field}: {conf}")

asyncio.run(test())