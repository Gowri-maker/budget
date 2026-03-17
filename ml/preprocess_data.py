import pandas as pd
import os

# Get path to dataset safely
current_dir = os.path.dirname(__file__)
data_path = os.path.abspath(os.path.join(current_dir, "..", "data", "expenses.csv"))

# Load dataset
df = pd.read_csv(data_path)

# Convert Date column to datetime (for Prophet)
df['Date'] = pd.to_datetime(df['Date'])

# Convert categorical columns to string (IMPORTANT for CatBoost)
categorical_features = [
    'Expense_Category',
    'Purchase_Priority',
    'Risk_Tolerance_Level'
]

for col in categorical_features:
    df[col] = df[col].astype(str)

print("Preprocessing completed successfully.")
print("Dataset shape:", df.shape)
print("Categorical columns converted to string:", categorical_features)

# Save processed dataset
processed_path = os.path.abspath(os.path.join(current_dir, "..", "data", "processed_expenses.csv"))
df.to_csv(processed_path, index=False)

print("Processed dataset saved at:")
print(processed_path)