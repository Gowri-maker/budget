import pandas as pd
import os
from catboost import CatBoostClassifier

# Load processed dataset safely
current_dir = os.path.dirname(__file__)
data_path = os.path.abspath(
    os.path.join(current_dir, "..", "data", "processed_expenses.csv")
)
df = pd.read_csv(data_path)

# Define target and features
target = "Is_Feasible"

features = [
    'Monthly_Income',
    'Monthly_Expenditure',
    'Savings_Ratio',
    'Debt_to_Income_Ratio',
    'Financial_Stability_Index',
    'Investment_Amount',
    'Credit_Score',
    'Risk_Tolerance_Level',
    'Expense_Category',
    'Purchase_Amount',
    'Purchase_Priority',
    'Urgency_Score',
    'Remaining_Budget',
    'Budget_Utilization_Percentage'
]

X = df[features].copy()
y = df[target]

# Explicitly enforce categorical columns as STRING (CRITICAL FIX)
categorical_columns = [
    'Risk_Tolerance_Level',
    'Expense_Category',
    'Purchase_Priority'
]

for col in categorical_columns:
    X[col] = X[col].astype(str)

# Get categorical feature indices for CatBoost
categorical_features = [X.columns.get_loc(col) for col in categorical_columns]

# Initialize CatBoost model (simple & review-safe)
model = CatBoostClassifier(
    iterations=200,
    learning_rate=0.1,
    depth=6,
    verbose=False
)

# Train model
model.fit(X, y, cat_features=categorical_features)

# Save trained model
model_path = os.path.abspath(
    os.path.join(current_dir, "..", "models", "catboost_purchase_model.cbm")
)
model.save_model(model_path)

print("CatBoost model trained successfully.")
print("Model saved at:")
print(model_path)