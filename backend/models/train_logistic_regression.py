import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, classification_report
from sklearn.metrics import f1_score
import joblib

# Load processed data
df = pd.read_csv("data/processed/credit_data_processed.csv")

# Separate features and target
X = df.drop(columns=["default_flag"])
y = df["default_flag"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Logistic Regression model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# Evaluation
print("\n📊 LOGISTIC REGRESSION RESULTS")
print("------------------------------")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("ROC-AUC  :", roc_auc_score(y_test, y_prob))
print("F1 Score :", f1_score(y_test, y_pred))


# Save model
joblib.dump(model, "models/logistic_regression_model.pkl")

print("\n✅ Logistic Regression model trained and saved successfully!")

