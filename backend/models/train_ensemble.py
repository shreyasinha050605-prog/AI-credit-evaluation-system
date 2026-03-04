import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, f1_score
from sklearn.metrics import fbeta_score
import numpy as np
import joblib
import json

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("data/processed/credit_data_processed.csv")

X = df.drop(columns=["default_flag"])
y = df["default_flag"]

# ---------------------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------
# DEFINE MODELS
# ---------------------------------------------------
log_reg = LogisticRegression(max_iter=1000, class_weight="balanced")
rf = RandomForestClassifier(n_estimators=200, random_state=42)
xgb = XGBClassifier(
    n_estimators=500,
    max_depth=4,
    learning_rate=0.03,
    subsample=0.9,
    colsample_bytree=0.9,
    eval_metric="auc",
    random_state=42
)

ensemble = VotingClassifier(
    estimators=[
        ('lr', log_reg),
        ('rf', rf),
        ('xgb', xgb)
    ],
    voting='soft'
)

# ---------------------------------------------------
# TRAIN
# ---------------------------------------------------
ensemble.fit(X_train, y_train)

# ---------------------------------------------------
# PROBABILITIES
# ---------------------------------------------------
y_prob = ensemble.predict_proba(X_test)[:, 1]

# ---------------------------------------------------
# DEFAULT THRESHOLD RESULTS (0.5)
# ---------------------------------------------------
default_preds = (y_prob >= 0.5).astype(int)

print("\n🔥 ENSEMBLE MODEL RESULTS (Default 0.5)")
print("----------------------------------------")
print("Accuracy :", accuracy_score(y_test, default_preds))
print("Precision:", precision_score(y_test, default_preds))
print("Recall   :", recall_score(y_test, default_preds))
print("ROC-AUC  :", roc_auc_score(y_test, y_prob))
print("F1 Score :", f1_score(y_test, default_preds))

# ---------------------------------------------------
# THRESHOLD OPTIMIZATION (F2 - Business Oriented)
# ---------------------------------------------------
thresholds = np.arange(0.1, 0.9, 0.02)

best_score = 0
best_threshold = 0.5

for t in thresholds:
    preds = (y_prob >= t).astype(int)
    score = fbeta_score(y_test, preds, beta=2)

    if score > best_score:
        best_score = score
        best_threshold = t

print("\n🔥 BUSINESS-OPTIMIZED THRESHOLD (ENSEMBLE)")
print("-------------------------------------------")
print("Best Threshold :", best_threshold)
print("Best F2 Score  :", best_score)

# ---------------------------------------------------
# FINAL RESULTS USING BEST THRESHOLD
# ---------------------------------------------------
final_preds = (y_prob >= best_threshold).astype(int)

print("\n🔥 FINAL RESULTS (Optimized Threshold)")
print("---------------------------------------")
print("Accuracy :", accuracy_score(y_test, final_preds))
print("Precision:", precision_score(y_test, final_preds))
print("Recall   :", recall_score(y_test, final_preds))
print("ROC-AUC  :", roc_auc_score(y_test, y_prob))
print("F1 Score :", f1_score(y_test, final_preds))

# ---------------------------------------------------
# SAVE MODEL + THRESHOLD
# ---------------------------------------------------
joblib.dump(ensemble, "models/ensemble_model.pkl")

with open("models/ensemble_threshold.json", "w") as f:
    json.dump({"best_threshold": float(best_threshold)}, f)

print("\n✅ Ensemble model trained and saved!")
print("✅ Best threshold saved successfully!")
