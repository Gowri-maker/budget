import pandas as pd
import os

# Get the directory of this current file (ml folder)
current_dir = os.path.dirname(__file__)

# Build path to data/expenses.csv safely
data_path = os.path.join(current_dir, "..", "data", "expenses.csv")

# Normalize path (important for Windows)
data_path = os.path.abspath(data_path)

print("Trying to load file from:")
print(data_path)

# Load dataset
df = pd.read_csv(data_path)

# Basic inspection
print("\nDataset shape (rows, columns):")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values in each column:")
print(df.isnull().sum())
