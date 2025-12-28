from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_statement(username, transactions):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, "ABC Bank")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 80, f"Account Statement for: {username}")

    y = height - 120
    pdf.setFont("Helvetica", 10)

    pdf.drawString(50, y, "From")
    pdf.drawString(150, y, "To")
    pdf.drawString(250, y, "Amount")
    pdf.drawString(330, y, "Date")

    y -= 20

    for tx in transactions:
        pdf.drawString(50, y, tx[0] or "-")
        pdf.drawString(150, y, tx[1] or "-")
        pdf.drawString(250, y, f"${tx[2]}")
        pdf.drawString(330, y, tx[3].strftime("%Y-%m-%d %H:%M"))
        y -= 18

        if y < 50:
            pdf.showPage()
            y = height - 50

    pdf.save()
    buffer.seek(0)
    return buffer
