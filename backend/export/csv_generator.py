import csv
import io

def generate_gstr1_csv(rows: list[dict]) -> str:
    output = io.StringIO()
    if not rows:
        return ""

    fieldnames = sorted({k for r in rows for k in r.keys()})
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return output.getvalue()

