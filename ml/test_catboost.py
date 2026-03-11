import pandas as pd
import os
from catboost import CatBoostClassifier

# Load trained model
current_dir = os.path.dirname(__file__)
model_path = os.path.abspath(
    os.path.join(current_dir, "..", "models", "catboost_purchase_model.cbm")
)

model = CatBoostClassifier()
model.load_model(model_path)

# Create ONE sample input (fake example for testing)
sample_data = {
    'Monthly_Income': [80000],
    'Monthly_Expenditure': [50000],
    'Savings_Ratio': [0.2],
    'Debt_to_Income_Ratio': [0.3],
    'Financial_Stability_Index': [0.7],
    'Investment_Amount': [10000],
    'Credit_Score': [750],
    'Risk_Tolerance_Level': ['0.7'],
    'Expense_Category': ['Electronics'],
    'Purchase_Amount': [15000],
    'Purchase_Priority': ['Medium'],
    'Urgency_Score': [0.5],
    'Remaining_Budget': [20000],
    'Budget_Utilization_Percentage': [60]
}

X_test = pd.DataFrame(sample_data)

# Predict feasibility
prediction = model.predict(X_test)

# Interpret result
result = "YES (Purchase Feasible)" if prediction[0] == 1 else "NO (Purchase Not Feasible)"

print("Prediction result:")
print(result)