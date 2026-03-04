class DecisionAgent:

    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, decision, prob, flags):

        reasons = []

        if decision is None:

            if prob < self.threshold:
                decision = "Approve"
                reasons.append("Predicted default probability is below optimized approval threshold")

            elif prob < (self.threshold + 0.15):
                decision = "Manual Review"
                reasons.append("Predicted risk falls within calibrated review band")

            else:
                decision = "Reject"
                reasons.append("Predicted default probability exceeds optimized rejection threshold")

        # Escalation Override
        if decision == "Approve" and len(flags) >= 2:
            decision = "Manual Review"
            reasons.append("Escalated due to multiple risk indicators")

        return {
            "decision": decision,
            "reasons": reasons
        }
