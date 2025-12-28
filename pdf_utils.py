from fpdf import FPDF

def generate_pdf(username, transactions):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Bank Statement – {username}", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(5)

    for tx in transactions:
        line = f"From: {tx[0]} | To: {tx[1]} | ${tx[2]} | {tx[3]}"
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1")
