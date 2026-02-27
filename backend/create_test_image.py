from PIL import Image, ImageDraw
import os

img = Image.new('RGB', (800, 1000), color='white')
draw = ImageDraw.Draw(img)

lines = [
    "TAX INVOICE",
    "",
    "Seller: Raj Wholesale Traders",
    "GSTIN: 36AABCU9603R1ZX",
    "Address: Hyderabad, Telangana",
    "",
    "Bill To: Ramesh Kirana Store",
    "GSTIN: 29AABCT1234R1ZY",
    "",
    "Invoice No: RWT/2026/0342",
    "Date: 05/02/2026",
    "",
    "HSN Code: 2106",
    "Taxable Value: Rs. 15000.00",
    "CGST @ 9%:    Rs. 1350.00",
    "SGST @ 9%:    Rs. 1350.00",
    "TOTAL:        Rs. 17700.00",
]

y = 80
for line in lines:
    draw.text((80, y), line, fill='black')
    y += 50

path = os.path.join('..', 'invoice_samples', 'clean_printed.png')
img.save(path)
print(f"Created: {path} — 800x1000 pixels") 