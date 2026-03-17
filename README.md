# 💰 Predictive Financial Decision Support System

An AI-powered web-based financial management system that helps users make intelligent purchase decisions using Machine Learning and Explainable AI.

---

## 🚀 Project Overview

This system provides:

- 📊 Budget tracking
- 🤖 Purchase feasibility prediction (CatBoost)
- 🔍 Explainable AI insights (SHAP)
- 📈 Expense forecasting (Prophet)
- 💡 Affordable alternative recommendations (Web Scraping)
- 📊 Power BI analytics dashboard

The system helps users avoid budget overruns and make financially stable decisions.

---

## 🏗️ System Architecture

- **Frontend:** Streamlit (Multi-page web app)
- **Backend:** FastAPI
- **Database:** SQLite
- **Machine Learning:** CatBoost
- **Forecasting:** Prophet
- **Explainable AI:** SHAP
- **Analytics:** Power BI
- **Version Control:** Git & GitHub

---

## 🧠 Machine Learning Logic

### 🔹 CatBoost
Used to predict whether a purchase is financially feasible based on:
- Monthly income
- Budget
- Current expenditure
- Savings ratio
- Category priority
- Urgency level

### 🔹 SHAP (Explainable AI)
Provides human-readable explanation of:
- Why a purchase is feasible or not
- Which financial factors influenced the decision

### 🔹 Prophet
Used for time-series forecasting of future expenses.

---

## 📊 Features

### 👤 User Management
- Secure Login / Registration
- Password hashing
- First-time setup configuration

### ⚙ Setup Configuration
- Monthly income & budget entry
- Category selection
- Priority assignment (1–5 scale)

### 🏠 Dashboard
- Total Budget
- Total Spent
- Remaining Budget
- Budget Utilization %
- Budget Health Score
- Date-wise expense tracking

### 🔮 Prediction Module
- Enter product details
- Feasibility prediction
- Dynamic urgency override
- SHAP explanation
- Alternative product recommendations

### 📈 Power BI Integration
- CSV export for analytics
- Category-wise spending analysis
- Budget vs actual comparison
- Financial performance trends

---

## 📂 Project Structure
