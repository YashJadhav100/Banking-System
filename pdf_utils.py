from fpdf import FPDF

def generate_pdf(username, transactions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"ABC Bank Statement - {username}", ln=True)

    pdf.ln(5)

    for t in transactions:
        line = f"{t['created_at']} | {t['sender']} → {t['receiver']} | ${t['amount']}"
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1")
