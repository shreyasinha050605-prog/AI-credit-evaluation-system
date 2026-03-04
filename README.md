# AI-Driven Smart Credit Evaluation System

An AI-powered credit risk assessment platform designed to enable fair, transparent, and efficient loan evaluation for MSMEs, farmers, and underserved businesses.

This system combines **Machine Learning, Explainable AI, Agent-based reasoning, and full-stack architecture** to automate underwriting decisions while maintaining human-interpretable explanations and auditability.

---

# Project Overview

Traditional credit underwriting processes are **slow, manual, and inconsistent**, often taking days to evaluate a single application. The goal of this project is to build a **modern AI-assisted decision intelligence platform** that accelerates credit evaluation while maintaining transparency and regulatory compliance.

The platform:

* Predicts credit default risk using machine learning
* Applies rule-based policy checks for regulatory compliance
* Generates natural language explanations for underwriting decisions
* Provides a full-stack dashboard for loan application workflows

Instead of replacing human underwriters, the system **augments their decisions with AI insights**.

---

# Key Features

## AI-Powered Credit Risk Prediction

* Machine learning model predicts default probability
* Converts predictions into a risk score (0–100)

## Explainable AI

* Feature importance analysis
* SHAP-based interpretability
* Natural-language explanations for underwriters

## Agent-Based Decision System

A modular **multi-agent architecture** handles underwriting:

* **Sanity Agent** – detects anomalies in financial data
* **Risk Agent** – predicts default probability using ML
* **Policy Agent** – applies business rules and regulatory constraints
* **Decision Agent** – generates final decision (Approve / Review / Reject)
* **Orchestrator** – coordinates the entire workflow

## Document Processing

* Upload financial documents (PDF / images)
* OCR extracts key financial information
* Automatically fills loan application fields

## Underwriter Dashboard

* View loan applications
* Inspect risk scores and explanations
* Download AI-generated credit reports
* Maintain a complete audit trail

---

# System Architecture

The system follows a **modular full-stack architecture**.

```
Frontend (React + TypeScript)
        │
        ▼
API Gateway (FastAPI)
        │
        ▼
Agentic Underwriting Engine
 ├── Sanity Agent
 ├── Risk Agent (ML Model)
 ├── Policy Agent
 └── Decision Agent
        │
        ▼
Database (SQLite)
```

This architecture separates **presentation, business logic, ML inference, and storage**, ensuring scalability and maintainability.

---

# Technology Stack

## Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* ShadCN UI
* React Router

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

## Machine Learning

* XGBoost
* scikit-learn
* NumPy
* Pandas

## Explainable AI

* SHAP
* Feature Importance Analysis

## AI Reasoning

* LLaMA-3 (via Groq API)

## Database

* SQLite
* SQLAlchemy ORM

## DevOps

* Docker
* Docker Compose
* Git & GitHub

---

# Machine Learning Pipeline

The ML system predicts **loan default probability** using a binary classification model.

## Target Variable

```
default_flag
0 → loan repaid
1 → loan defaulted
```

## Model Used

**XGBoost Gradient Boosting**

Reasons for choosing XGBoost:

* Excellent performance on tabular financial data
* Handles non-linear feature interactions
* Robust against overfitting
* Strong performance compared to other models

---

# Model Hyperparameters

```
Estimators: 500
Max Depth: 4
Learning Rate: 0.03
Subsample: 0.8
Column Sample: 0.8
Regularization: L1 / L2
```

Early stopping and threshold tuning were used to optimize performance.

---

# Feature Engineering

The model uses domain-specific features including:

## Business Profile

* Business type
* Industry sector
* Years in operation
* Revenue trends

## Financial Health

* Monthly cash flow
* Credit score
* Debt-to-income ratio

## Loan Characteristics

* Requested loan amount
* Existing loans
* Collateral availability

## Historical Behavior

* Repayment history
* Default history
* Banking relationship duration

Derived ratios such as **loan-to-revenue** and **cashflow stability metrics** improve model accuracy and interpretability.

---

# Model Evaluation

Models tested:

| Model               | Accuracy | ROC-AUC | F1    |
| ------------------- | -------- | ------- | ----- |
| Logistic Regression | 0.721    | 0.789   | 0.746 |
| Random Forest       | 0.765    | 0.848   | 0.787 |
| XGBoost             | 0.755    | 0.851   | 0.775 |

**Best model:**
XGBoost with optimized F1 threshold.

The model was selected because banks require:

* High ROC-AUC (good discrimination)
* Balanced precision & recall
* Controlled false approvals

---

# Hybrid Decision Logic

The final credit decision combines:

```
Machine Learning Score
        +
Policy Rules
        +
Business Constraints
```

Final outputs:

* Approve
* Manual Review
* Reject

Borderline cases can be reviewed by human underwriters.

---

# Backend APIs

## Predict Risk

```
POST /predict
```

Input: Applicant financial data
Output: Risk score + credit decision

---

## Upload Document

```
POST /upload
```

Uploads PDF/image and performs:

* OCR
* Field extraction
* Auto-fill application data

---

## Generate AI Report

```
POST /generate-report
```

Returns an **AI-generated explanation of the decision**.

---

# Database & Audit Trail

All credit evaluations are stored in the database including:

* Applicant data
* Risk scores
* Default probability
* Final decision
* AI explanations
* Model metadata

This ensures **traceability and regulatory compliance**.

---

# Containerized Deployment

The system uses **Docker containers** for deployment.

Containers:

```
Frontend Container
React + Vite

Backend Container
FastAPI + ML + Agent System

Database
SQLite
```

Benefits:

* Environment consistency
* Easy deployment
* Scalability
* Cloud-ready architecture

---

# How to Run the Project

## Clone Repository

```
git clone https://github.com/shreyasinha050605-prog/AI-credit-evaluation-system.git
cd AI-credit-evaluation-system
```

## Run with Docker

```
docker-compose up --build
```

## Run Backend

```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Run Frontend

```
cd frontend
npm install
npm run dev
```

---

# Demo Workflow

1. User fills loan application
2. Uploads supporting documents
3. Backend extracts data
4. ML model predicts default probability
5. Policy rules applied
6. Final decision generated
7. AI explanation produced
8. Results shown on dashboard

---

# Business Benefits

* Faster loan approvals
* Consistent underwriting decisions
* Reduced operational costs
* Transparent risk explanations
* Improved financial inclusion

---

# Challenges & Solutions

| Challenge                  | Solution                         |
| -------------------------- | -------------------------------- |
| No real banking dataset    | Synthetic data generation        |
| Class imbalance            | Weighted loss & threshold tuning |
| Explainability vs accuracy | SHAP explanations                |
| PDF variability            | OCR + flexible extraction        |
| LLM hallucinations         | Deterministic JSON outputs       |

---

# Engineering Concepts Demonstrated

* Full-Stack AI Systems
* Machine Learning Deployment
* Explainable AI (XAI)
* Agentic AI Architectures
* OCR + NLP Pipelines
* Human-in-the-Loop Decision Systems
* Containerized Deployment

---

# Authors

* Uzma Habeeba Shaik
* Akshaya Ashok Nair
* Shreya Sinha
