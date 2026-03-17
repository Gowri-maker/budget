#main.py

from fastapi import FastAPI
from pydantic import BaseModel
from catboost import CatBoostClassifier
import pandas as pd
import shap
from scraper import scrape_amazon
import os

app = FastAPI()

# -------- LOAD TRAINED MODEL --------
model = CatBoostClassifier()

current_dir = os.path.dirname(__file__)
model_path = os.path.abspath(
    os.path.join(current_dir, "..", "models", "catboost_purchase_model.cbm")
)

model.load_model(model_path)

# -------- REQUEST SCHEMA --------
class PurchaseRequest(BaseModel):
    Monthly_Income: float
    Monthly_Budget: float
    Monthly_Expenditure: float
    Purchase_Amount: float
    Expense_Category: str
    Purchase_Priority: str
    Original_Priority: int
    Urgency_Level: str
    Product_Name: str


# -------- FEASIBILITY CHECK ROUTE --------
@app.post("/check-feasibility")
def check_feasibility(data: PurchaseRequest):

    input_dict = data.dict()

    purchase_amount     = input_dict["Purchase_Amount"]
    monthly_budget      = input_dict["Monthly_Budget"]
    monthly_expenditure = input_dict["Monthly_Expenditure"]
    monthly_income      = input_dict["Monthly_Income"]
    urgency             = input_dict["Urgency_Level"]

    # -------- CALCULATIONS --------
    remaining_budget_before = monthly_budget - monthly_expenditure  # before this purchase

    budget_ratio = (
        (purchase_amount / remaining_budget_before * 100)
        if remaining_budget_before > 0 else 999
    )

    urgency_threshold_exceeded = int(
        (urgency == "Normal"      and budget_ratio > 60) or
        (urgency == "Urgent"      and budget_ratio > 80) or
        (urgency == "Very Urgent" and budget_ratio > 95)
    )

    remaining_budget = remaining_budget_before - purchase_amount

    budget_utilization = (
        ((monthly_expenditure + purchase_amount) / monthly_budget) * 100
        if monthly_budget > 0 else 0
    )

    savings_ratio = (
        (monthly_income - (monthly_expenditure + purchase_amount)) / monthly_income
        if monthly_income > 0 else 0
    )

    # -------- PREPARE MODEL INPUT (original features only — no retraining needed) --------
    df = pd.DataFrame([{
        "Monthly_Income":                monthly_income,
        "Monthly_Expenditure":           monthly_expenditure,
        "Savings_Ratio":                 savings_ratio,
        "Debt_to_Income_Ratio":          0.2,
        "Financial_Stability_Index":     savings_ratio,
        "Investment_Amount":             0,
        "Credit_Score":                  700,
        "Risk_Tolerance_Level":          "Medium",
        "Expense_Category":              input_dict["Expense_Category"],
        "Purchase_Amount":               purchase_amount,
        "Purchase_Priority":             input_dict["Purchase_Priority"],
        "Urgency_Score":                 1 if urgency == "Very Urgent" else (0.5 if urgency == "Urgent" else 0.0),
        "Remaining_Budget":              remaining_budget,
        "Budget_Utilization_Percentage": budget_utilization
    }])

    # -------- MODEL PREDICTION --------
    prediction = model.predict(df)[0]
    result = "Feasible" if prediction == 1 else "Not Feasible"

    # -------- RULE-BASED SAFETY GATE (rules are final — override model in BOTH directions) --------
    if remaining_budget < 0:
        result = "Not Feasible"
    elif urgency_threshold_exceeded:
        result = "Not Feasible"
    else:
        result = "Feasible"  # ✅ rule says it's fine — trust the rule, not CatBoost

    # -------- SHAP EXPLANATION --------
    explainer   = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df)

    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    explanation = []

    explanation.append(
        f"After this purchase, your remaining budget will be approximately ₹{remaining_budget:.2f}."
    )
    explanation.append(
        f"Your budget utilization will become {budget_utilization:.1f}%."
    )
    explanation.append(
        f"Your savings ratio will adjust to {savings_ratio:.2f}."
    )

    if urgency == "Very Urgent":
        explanation.append(
            f"This purchase was marked as Very Urgent, so its priority was temporarily elevated "
            f"from {input_dict['Original_Priority']} to 1."
        )

    if remaining_budget < 0:
        explanation.append(
            "This purchase would result in a negative remaining budget, which weakens financial stability."
        )

    if urgency_threshold_exceeded:
        thresholds = {"Normal": 60, "Urgent": 80, "Very Urgent": 95}
        limit = thresholds.get(urgency, 60)
        explanation.append(
            f"This purchase uses {budget_ratio:.1f}% of your remaining budget, "
            f"which exceeds the {limit}% safe limit for '{urgency}' urgency."
        )

    if result == "Not Feasible" and urgency == "Normal":
        explanation.append(
            "Since this purchase is not urgent and consumes a large portion of "
            "your remaining budget, it is recommended to postpone it."
        )

    # -------- WEB SCRAPING FOR BEST DEALS --------
    best_deals = []

    if result == "Feasible":
        best_deals = scrape_amazon(input_dict["Product_Name"], budget=input_dict["Purchase_Amount"])

    # -------- FINAL RESPONSE --------
    return {
        "prediction":  result,
        "explanation": explanation,
        "best_deals":  best_deals
    }