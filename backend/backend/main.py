from backend.agents.risk_agent import RiskAgent
from backend.agents.policy_agent import PolicyAgent
from backend.agents.sanity_agent import SanityAgent
from backend.agents.underwriting_orchestrator import UnderwritingOrchestrator
from backend.agents.decision_agent import DecisionAgent

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, validator
import joblib
import pandas as pd
import datetime
import json


from database.db import SessionLocal
from database.models import CreditApplication as CreditApplicationDB


# -------------------------------------------------
# APP INIT
# -------------------------------------------------
app = FastAPI(title="AI Credit Evaluation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from backend.routes import document_upload
app.include_router(document_upload.router)


# -------------------------------------------------
# LOAD ARTIFACTS
# -------------------------------------------------
model = joblib.load("models/xgboost_model.pkl")
scaler = joblib.load("models/scaler.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

# Load optimized threshold
with open("models/xgb_threshold.json", "r") as f:
    threshold_data = json.load(f)

BEST_THRESHOLD = threshold_data["best_threshold"]

# -------------------------------------------------
# FEATURE ORDER
# -------------------------------------------------
TRAINING_FEATURE_ORDER = [
    "business_type",
    "years_in_operation",
    "annual_revenue",
    "credit_score",
    "existing_loans",
    "repayment_history",
    "monthly_cashflow",
    "loan_amount_requested",
    "collateral_value",
    "debt_to_income_ratio",
    "loan_to_revenue_ratio",
    "cashflow_to_loan_ratio"
]

sanity_agent = SanityAgent()
policy_agent = PolicyAgent()
risk_agent = RiskAgent(model)
decision_agent = DecisionAgent(BEST_THRESHOLD)

orchestrator = UnderwritingOrchestrator(
    sanity_agent,
    policy_agent,
    risk_agent,
    decision_agent
)



# -------------------------------------------------
# CONSTANTS
# -------------------------------------------------
MAX_REVENUE = 1e9
MAX_LOAN = 5e8
MAX_YEARS = 60
MIN_CREDIT_SCORE = 300
MAX_CREDIT_SCORE = 900


# -------------------------------------------------
# INPUT SCHEMA
# -------------------------------------------------
class CreditApplication(BaseModel):
    business_type: str
    years_in_operation: float = Field(ge=0, le=MAX_YEARS)
    annual_revenue: float = Field(gt=0, le=MAX_REVENUE)
    monthly_cashflow: float
    loan_amount_requested: float = Field(gt=0, le=MAX_LOAN)
    credit_score: float = Field(ge=MIN_CREDIT_SCORE, le=MAX_CREDIT_SCORE)
    existing_loans: int = Field(ge=0, le=20)
    debt_to_income_ratio: float = Field(ge=0, le=2)
    collateral_value: float = Field(ge=0)
    repayment_history: str

    @validator("business_type", "repayment_history", pre=True)
    def normalize_strings(cls, v):
        return v.strip().title()

# -------------------------------------------------
# RISK LABEL
# -------------------------------------------------
def qualitative_risk_label(decision, flags_count):
    if decision == "Reject":
        return "Very High"
    if decision == "Manual Review":
        return "High" if flags_count >= 2 else "Moderate"
    return "Low"

# -------------------------------------------------
# PREDICTION ENDPOINT
# -------------------------------------------------
@app.post("/predict")
def predict(application: CreditApplication):

    df = pd.DataFrame([application.dict()])

    for col in ["business_type", "repayment_history"]:
        df[col] = label_encoders[col].transform(df[col])

    df["loan_to_revenue_ratio"] = df["loan_amount_requested"] / df["annual_revenue"]
    df["cashflow_to_loan_ratio"] = df["monthly_cashflow"] / df["loan_amount_requested"].clip(lower=1)

    numeric_cols = [
        "years_in_operation", "annual_revenue", "monthly_cashflow",
        "loan_amount_requested", "credit_score", "existing_loans",
        "debt_to_income_ratio", "collateral_value",
        "loan_to_revenue_ratio", "cashflow_to_loan_ratio"
    ]

    df[numeric_cols] = scaler.transform(df[numeric_cols])
    df = df[TRAINING_FEATURE_ORDER]

    # 🔥 Fully Agentic Call
    result = orchestrator.process(application, df)

    decision = result["decision"]
    prob = result["default_probability"]
    risk_score = result["risk_score"]
    reasons = result["reasons"]
    flags = result["flags"]

    risk_level = qualitative_risk_label(decision, len(flags))

    # -------------------------------
    # DATABASE SAVE
    # -------------------------------
    db = SessionLocal()
    try:
        db.add(CreditApplicationDB(
            **application.dict(),
            default_probability=round(prob * 100, 2),
            risk_score=risk_score,
            risk_level=risk_level,
            decision=decision,
            reasons=json.dumps(reasons),
            model_used="XGBoost_v1"
        ))
        db.commit()
    finally:
        db.close()

    return {
        "decision": decision,
        "risk_level": risk_level,
        "default_probability": round(prob * 100, 2),
        "risk_score": risk_score,
        "reasons": reasons,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

# -------------------------------------------------
# APPLICATION HISTORY (FOR DASHBOARD)
# -------------------------------------------------
@app.get("/applications")
def get_applications():
    db = SessionLocal()
    try:
        applications = (
            db.query(CreditApplicationDB)
            .order_by(CreditApplicationDB.created_at.desc())
            .all()
        )

        return [
            {
                "application_id": app.id,
                "business_type": app.business_type,
                "loan_amount_requested": app.loan_amount_requested,
                "credit_score": app.credit_score,
                "risk_level": app.risk_level,
                "created_at": app.created_at.isoformat() if app.created_at else None,
            }
            for app in applications
        ]
    finally:
        db.close()

from backend.routes import report
app.include_router(report.router)

# -------------------------------------------------
# ROOT
# -------------------------------------------------
@app.get("/")
def root():
    return RedirectResponse(url="/docs")
