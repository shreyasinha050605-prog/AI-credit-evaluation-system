from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from groq import Groq
import json
import os
import io

# -------------------------------------------------
# GROQ CLIENT
# -------------------------------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------------------------------
# LLM REPORT (HUMAN‑READABLE)
# -------------------------------------------------
def generate_llm_report(context: dict):
    prompt = f"""
You are a senior credit underwriter.
Using the data below, write a professional, easy-to-read AI Credit Evaluation Report.

Rules:
- Use clear section headings
- Explain the decision in simple language
- Reference the risk level and probability
- Summarize key reasons as bullet points
- Do NOT invent numbers
- Do NOT contradict the decision
- Keep tone professional and human-friendly

DATA:
{json.dumps(context, indent=2)}

Output plain text only.
"""

    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return completion.choices[0].message.content.strip()


# -------------------------------------------------
# SUMMARY WRAPPER (USED BY ROUTES)
# -------------------------------------------------
def generate_ai_summary(app) -> str:
    context = {
        "Decision": app.decision,
        "Risk Level": app.risk_level,
        "Default Probability (%)": app.default_probability,
        "Business Type": app.business_type,
        "Years in Operation": app.years_in_operation,
        "Annual Revenue": app.annual_revenue,
        "Monthly Cashflow": app.monthly_cashflow,
        "Loan Amount Requested": app.loan_amount_requested,
        "Credit Score": app.credit_score,
        "Existing Loans": app.existing_loans,
        "Debt to Income Ratio": app.debt_to_income_ratio,
        "Collateral Value": app.collateral_value,
        "Repayment History": app.repayment_history,
        "Key Risk Reasons": json.loads(app.reasons),
        "Model Used": app.model_used
    }

    return generate_llm_report(context)

# -------------------------------------------------
# PDF GENERATION
# -------------------------------------------------
def generate_report_pdf(app):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    text = c.beginText(40, 800)
    text.setFont("Helvetica", 10)

    summary = generate_ai_summary(app)

    for line in summary.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
