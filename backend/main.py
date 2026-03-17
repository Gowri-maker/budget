<<<<<<< HEAD
from unittest import result

=======
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
from fastapi import FastAPI
from pydantic import BaseModel
from catboost import CatBoostClassifier
import pandas as pd
import shap
<<<<<<< HEAD
from scraper import scrape_amazon #Added for webscraping
=======
from scraper import scrape_amazon
import os
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82

app = FastAPI()

# -------- LOAD TRAINED MODEL --------
model = CatBoostClassifier()
<<<<<<< HEAD
# model.load_model("models/catboost_purchase_model.cbm")

import os
=======
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82

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

<<<<<<< HEAD
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
=======
    purchase_amount = input_dict["Purchase_Amount"]
    monthly_budget = input_dict["Monthly_Budget"]
    monthly_expenditure = input_dict["Monthly_Expenditure"]
    monthly_income = input_dict["Monthly_Income"]
    urgency = input_dict["Urgency_Level"]

    # -------- CALCULATIONS --------
    remaining_budget = monthly_budget - monthly_expenditure - purchase_amount

    budget_utilization = (
        ((monthly_expenditure + purchase_amount) / monthly_budget) * 100
        if monthly_budget > 0 else 0
    )

    savings_ratio = (
        (monthly_income - (monthly_expenditure + purchase_amount)) / monthly_income
        if monthly_income > 0 else 0
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
    )

    # -------- PREPARE MODEL INPUT --------
    df = pd.DataFrame([{
<<<<<<< HEAD
        "Monthly_Income": input_dict["Monthly_Income"],
        "Monthly_Expenditure": input_dict["Monthly_Expenditure"],
=======
        "Monthly_Income": monthly_income,
        "Monthly_Expenditure": monthly_expenditure,
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
        "Savings_Ratio": savings_ratio,
        "Debt_to_Income_Ratio": 0.2,
        "Financial_Stability_Index": savings_ratio,
        "Investment_Amount": 0,
        "Credit_Score": 700,
        "Risk_Tolerance_Level": "Medium",
        "Expense_Category": input_dict["Expense_Category"],
<<<<<<< HEAD
        "Purchase_Amount": input_dict["Purchase_Amount"],
        "Purchase_Priority": input_dict["Purchase_Priority"],
        "Urgency_Score": 1 if input_dict["Urgency_Level"] == "Very Urgent" else 0.5,
=======
        "Purchase_Amount": purchase_amount,
        "Purchase_Priority": input_dict["Purchase_Priority"],
        "Urgency_Score": 1 if urgency == "Very Urgent" else 0.5,
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
        "Remaining_Budget": remaining_budget,
        "Budget_Utilization_Percentage": budget_utilization
    }])

    # -------- MODEL PREDICTION --------
    prediction = model.predict(df)[0]
    result = "Feasible" if prediction == 1 else "Not Feasible"

<<<<<<< HEAD
    # Force not feasible if budget goes negative
    if remaining_budget < 0:
        result = "Not Feasible"

    # -------- SHAP EXPLANATION (SIMPLIFIED DISPLAY) --------
=======
    # -------- RULE-BASED SAFETY CHECK --------
    if purchase_amount > (monthly_budget - monthly_expenditure):
        result = "Not Feasible"

    elif urgency == "High":
        result = "Feasible"

    elif urgency == "Normal" and purchase_amount > (monthly_budget - monthly_expenditure) * 0.7:
        result = "Not Feasible"

    elif urgency == "Low" and purchase_amount > (monthly_budget - monthly_expenditure) * 0.5:
        result = "Not Feasible"

    # -------- SHAP EXPLANATION --------
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
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

<<<<<<< HEAD
    if input_dict["Urgency_Level"] == "Very Urgent":
=======
    if urgency == "Very Urgent":
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
        explanation.append(
            f"This purchase was marked as Very Urgent, so its priority was temporarily elevated from {input_dict['Original_Priority']} to 1."
        )

    if remaining_budget < 0:
        explanation.append(
            "This purchase would result in a negative remaining budget, which weakens financial stability."
        )
<<<<<<< HEAD
        # Added code here 
=======

    if result == "Not Feasible" and urgency == "Normal":
        explanation.append(
            "Since this purchase is not urgent and consumes a large portion of your remaining budget, it is recommended to postpone it."
        )

    # -------- WEB SCRAPING FOR BEST DEALS --------
>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
    best_deals = []

    if result == "Feasible":
        best_deals = scrape_amazon(input_dict["Product_Name"])
<<<<<<< HEAD
=======

>>>>>>> 641f13997c0c67e4d9cd1b9fc35b8edf4e1f7c82
    # -------- FINAL RESPONSE --------
    return {
        "prediction": result,
        "explanation": explanation,
        "best_deals": best_deals
    }