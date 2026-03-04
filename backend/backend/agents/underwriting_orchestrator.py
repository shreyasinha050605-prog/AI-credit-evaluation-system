class UnderwritingOrchestrator:

    def __init__(self, sanity_agent, policy_agent, risk_agent, decision_agent):
        self.sanity_agent = sanity_agent
        self.policy_agent = policy_agent
        self.risk_agent = risk_agent
        self.decision_agent = decision_agent

    def process(self, application, df):

        decision = None
        reasons = []
        flags = []

        # 1️⃣ Sanity Layer
        sanity = self.sanity_agent.evaluate(application)
        decision = sanity["decision"]
        reasons.extend(sanity["reasons"])
        flags.extend(sanity["flags"])

        # 2️⃣ Policy + Grey Zone
        policy = self.policy_agent.evaluate(application)
        if decision is None:
            decision = policy["decision"]

        reasons.extend(policy["reasons"])
        flags.extend(policy["flags"])

        # 3️⃣ ML Layer
        risk = self.risk_agent.evaluate(df)
        prob = risk["default_probability"]

        # 4️⃣ Final Decision Logic (SAME AS OLD CODE)
        final = self.decision_agent.evaluate(
            decision,
            prob,
            flags
        )

        decision = final["decision"]
        reasons.extend(final["reasons"])

        risk_score = min(round(prob * 100 + len(flags) * 5, 2), 100)

        return {
            "decision": decision,
            "default_probability": prob,
            "risk_score": risk_score,
            "reasons": reasons,
            "flags": flags
        }
