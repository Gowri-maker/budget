from unittest import result

from fastapi import FastAPI
from pydantic import BaseModel
from catboost import CatBoostClassifier
import pandas as pd
import shap
from scraper import scrape_amazon #Added for webscraping

app = FastAPI()

# -------- LOAD TRAINED MODEL --------
model = CatBoostClassifier()
# model.load_model("models/catboost_purchase_model.cbm")

import os

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

    # -------- CALCULATIONS --------
    remaining_budget = (
        input_dict["Monthly_Budget"]
        - input_dict["Monthly_Expenditure"]
        - input_dict["Purchase_Amount"]
    )

    budget_utilization = (
        ((input_dict["Monthly_Expenditure"] + input_dict["Purchase_Amount"])
         / input_dict["Monthly_Budget"]) * 100
        if input_dict["Monthly_Budget"] > 0 else 0
    )

    savings_ratio = (
        (input_dict["Monthly_Income"]
         - (input_dict["Monthly_Expenditure"] + input_dict["Purchase_Amount"]))
        / input_dict["Monthly_Income"]
        if input_dict["Monthly_Income"] > 0 else 0
    )

    # -------- PREPARE MODEL INPUT --------
    df = pd.DataFrame([{
        "Monthly_Income": input_dict["Monthly_Income"],
        "Monthly_Expenditure": input_dict["Monthly_Expenditure"],
        "Savings_Ratio": savings_ratio,
        "Debt_to_Income_Ratio": 0.2,
        "Financial_Stability_Index": savings_ratio,
        "Investment_Amount": 0,
        "Credit_Score": 700,
        "Risk_Tolerance_Level": "Medium",
        "Expense_Category": input_dict["Expense_Category"],
        "Purchase_Amount": input_dict["Purchase_Amount"],
        "Purchase_Priority": input_dict["Purchase_Priority"],
        "Urgency_Score": 1 if input_dict["Urgency_Level"] == "Very Urgent" else 0.5,
        "Remaining_Budget": remaining_budget,
        "Budget_Utilization_Percentage": budget_utilization
    }])

    # -------- MODEL PREDICTION --------
    prediction = model.predict(df)[0]
    result = "Feasible" if prediction == 1 else "Not Feasible"

    # Force not feasible if budget goes negative
    if remaining_budget < 0:
        result = "Not Feasible"

    # -------- SHAP EXPLANATION (SIMPLIFIED DISPLAY) --------
    explainer = shap.TreeExplainer(model)
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

    if input_dict["Urgency_Level"] == "Very Urgent":
        explanation.append(
            f"This purchase was marked as Very Urgent, so its priority was temporarily elevated from {input_dict['Original_Priority']} to 1."
        )

    if remaining_budget < 0:
        explanation.append(
            "This purchase would result in a negative remaining budget, which weakens financial stability."
        )
        # Added code here 
    best_deals = []

    if result == "Feasible":
        best_deals = scrape_amazon(input_dict["Product_Name"])
    # -------- FINAL RESPONSE --------
    return {
        "prediction": result,
        "explanation": explanation,
        "best_deals": best_deals
    }