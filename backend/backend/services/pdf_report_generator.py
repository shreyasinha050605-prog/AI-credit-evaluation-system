from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf_report(ai_text: str):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 40

    for line in ai_text.split("\n"):
        pdf.drawString(40, y, line)
        y -= 14
        if y < 40:
            pdf.showPage()
            y = height - 40

    pdf.save()
    buffer.seek(0)
    return buffer
