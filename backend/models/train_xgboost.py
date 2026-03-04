import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    f1_score
)

from xgboost import XGBClassifier


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_csv("data/processed/credit_data_processed.csv")

X = df.drop(columns=["default_flag"])
y = df["default_flag"]


# ---------------------------------------------------
# TRAIN-TEST SPLIT
# ---------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ---------------------------------------------------
# MODEL CONFIGURATION
# ---------------------------------------------------
model = XGBClassifier(
    n_estimators=500,
    max_depth=4,
    learning_rate=0.03,
    subsample=0.9,
    colsample_bytree=0.9,
    reg_alpha=0.5,
    reg_lambda=1.0,
    scale_pos_weight=(y_train.value_counts()[0] / y_train.value_counts()[1]),
    eval_metric="auc",
    random_state=42
)


# ---------------------------------------------------
# TRAIN MODEL
# ---------------------------------------------------
model.fit(X_train, y_train)


# ---------------------------------------------------
# PREDICTIONS
# ---------------------------------------------------
y_prob = model.predict_proba(X_test)[:, 1]

# Default threshold
threshold = 0.5
y_pred = (y_prob >= threshold).astype(int)


# ---------------------------------------------------
# EVALUATION
# ---------------------------------------------------
print("\n⚡ XGBOOST RESULTS")
print("------------------")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("ROC-AUC  :", roc_auc_score(y_test, y_prob))
print("F1 Score :", f1_score(y_test, y_pred))


# ---------------------------------------------------
# THRESHOLD OPTIMIZATION
# ---------------------------------------------------
thresholds = np.arange(0.1, 0.9, 0.05)
best_f1 = 0
best_threshold = 0.5

for t in thresholds:
    preds = (y_prob >= t).astype(int)
    score = f1_score(y_test, preds)
    if score > best_f1:
        best_f1 = score
        best_threshold = t

print("\n🔥 BEST THRESHOLD SEARCH")
print("----------------------------")
print("Best Threshold :", best_threshold)
print("Best F1 Score  :", best_f1)


# ---------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------
joblib.dump(model, "models/xgboost_model.pkl")

print("\n✅ XGBoost model trained and saved!")

# ---------------------------------------------------
# SAVE BEST THRESHOLD
# ---------------------------------------------------
import json

with open("models/xgb_threshold.json", "w") as f:
    json.dump({"best_threshold": float(best_threshold)}, f)

print("✅ Best threshold saved successfully!")
