from fpdf import FPDF
from io import BytesIO

def generate_pdf(username, transactions):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ABC Bank - Account Statement", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"User: {username}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", size=10)
    for amount, txn_type, timestamp in transactions:
        pdf.cell(
            0,
            8,
            f"{timestamp} | {txn_type} | ${amount}",
            ln=True
        )

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    return buffer.getvalue()
