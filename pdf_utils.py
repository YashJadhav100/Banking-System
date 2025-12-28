from fpdf import FPDF

def generate_pdf(username, transactions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Bank Statement for {username}", ln=True)

    for t in transactions:
        pdf.cell(
            200,
            10,
            txt=f"{t[3]} | {t[0]} → {t[1]} | ${t[2]}",
            ln=True
        )

    return pdf.output(dest="S").encode("latin-1")
