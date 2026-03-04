class SanityAgent:

    def evaluate(self, application):

        decision = None
        reasons = []
        flags = []

        if application.monthly_cashflow < 0:
            decision = "Reject"
            reasons.append(
                "Reported monthly cashflow is negative, indicating the business is operating at a loss"
            )

        if application.monthly_cashflow * 12 > application.annual_revenue * 1.5:
            flags.append("Cashflow appears inconsistent with annual revenue")

        if application.loan_amount_requested > application.annual_revenue * 3:
            flags.append("Loan amount is disproportionately high relative to revenue")

        if application.debt_to_income_ratio > 1:
            flags.append("Debt-to-income ratio exceeds acceptable limits")

        return {
            "decision": decision,
            "reasons": reasons,
            "flags": flags
        }
