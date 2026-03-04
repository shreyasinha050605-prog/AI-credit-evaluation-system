import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from database.db import SessionLocal
from database.models import CreditApplication
from backend.services.ai_report_generator import generate_llm_report
from backend.services.report_generator import generate_report_pdf

router = APIRouter(prefix="/report", tags=["Reports"])


def get_application_from_db(application_id: int):
    db = SessionLocal()
    app = (
        db.query(CreditApplication)
        .filter(CreditApplication.id == application_id)
        .first()
    )
    db.close()
    return app


@router.get("/{application_id}")
def get_report(application_id: int):
    application = get_application_from_db(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    context = {
        "business_type": application.business_type,
        "years_in_operation": application.years_in_operation,
        "annual_revenue": application.annual_revenue,
        "monthly_cashflow": application.monthly_cashflow,
        "loan_amount_requested": application.loan_amount_requested,
        "credit_score": application.credit_score,
        "existing_loans": application.existing_loans,
        "debt_to_income_ratio": application.debt_to_income_ratio,
        "collateral_value": application.collateral_value,
        "repayment_history": application.repayment_history,
        "decision": application.decision,
        "risk_level": application.risk_level,
        "default_probability": application.default_probability,
        "reasons": json.loads(application.reasons),
    }

    ai_summary = generate_llm_report(context)

    return {
        "application_id": application.id,
        "created_at": application.created_at,
        "decision": application.decision,
        "risk_level": application.risk_level,
        "default_probability": application.default_probability,
        "ai_report": ai_summary,
    }


@router.get("/{application_id}/pdf")
def download_report_pdf(application_id: int):
    application = get_application_from_db(application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    pdf_buffer = generate_report_pdf(application)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=credit_report_{application_id}.pdf"
        },
    )
