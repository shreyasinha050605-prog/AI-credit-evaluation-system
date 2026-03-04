class RiskAgent:

    def __init__(self, model):
        self.model = model

    def evaluate(self, df):

        prob = float(self.model.predict_proba(df)[0][1])

        return {
            "default_probability": prob
        }
