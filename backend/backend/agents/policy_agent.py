class PolicyAgent:

    def evaluate(self, application):

        decision = None
        reasons = []
        flags = []

        if (
            application.credit_score < 580 and
            application.repayment_history == "Poor" and
            application.debt_to_income_ratio > 0.75 and
            application.existing_loans >= 3
        ):
            decision = "Reject"
            reasons.extend([
                "Low credit score",
                "Poor repayment history",
                "High debt burden",
                "Multiple existing loans"
            ])

        if decision is None and application.credit_score < 550:
            decision = "Manual Review"
            reasons.append("Credit score below preferred threshold")

        # Grey Zone Flags (same as old code)

        if 600 <= application.credit_score < 680:
            flags.append("Moderate credit score range")

        if application.debt_to_income_ratio >= 0.5:
            flags.append("Elevated debt-to-income ratio")

        if application.existing_loans >= 2:
            flags.append("Multiple existing loans")

        if application.collateral_value < application.loan_amount_requested * 0.4:
            flags.append("Weak collateral coverage")

        if application.repayment_history == "Average":
            flags.append("Average repayment behavior")

        if application.years_in_operation < 2:
            flags.append("Limited operating history")

        if application.collateral_value < application.loan_amount_requested * 0.25:
            flags.append("Insufficient collateral coverage")

        return {
            "decision": decision,
            "reasons": reasons,
            "flags": flags
        }
