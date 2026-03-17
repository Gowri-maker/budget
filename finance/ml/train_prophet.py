import pandas as pd
import os
from prophet import Prophet

# Load processed dataset safely
current_dir = os.path.dirname(__file__)
data_path = os.path.abspath(
    os.path.join(current_dir, "..", "data", "processed_expenses.csv")
)
df = pd.read_csv(data_path)

# Prepare data for Prophet
prophet_df = df[['Date', 'Monthly_Expenditure']].copy()
prophet_df.columns = ['ds', 'y']

# Ensure correct data types
prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])
prophet_df['y'] = pd.to_numeric(prophet_df['y'])

# Initialize Prophet model (default settings)
model = Prophet()
model.fit(prophet_df)

# Create future dates (next 30 days)
future = model.make_future_dataframe(periods=30)

# Generate forecast
forecast = model.predict(future)

# Save forecast for later use (Power BI / backend)
forecast_path = os.path.abspath(
    os.path.join(current_dir, "..", "data", "expense_forecast.csv")
)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(
    forecast_path, index=False
)

print("Prophet forecasting completed successfully.")
print("Forecast saved at:")
print(forecast_path)
import pandas as pd
import os
from prophet import Prophet

# Load processed dataset safely
current_dir = os.path.dirname(__file__)
data_path = os.path.abspath(
    os.path.join(current_dir, "..", "data", "processed_expenses.csv")
)
df = pd.read_csv(data_path)

# Prepare data for Prophet
prophet_df = df[['Date', 'Monthly_Expenditure']].copy()
prophet_df.columns = ['ds', 'y']

# Ensure correct data types
prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])
prophet_df['y'] = pd.to_numeric(prophet_df['y'])

# Initialize Prophet model (default settings)
model = Prophet()
model.fit(prophet_df)

# Create future dates (next 30 days)
future = model.make_future_dataframe(periods=30)

# Generate forecast
forecast = model.predict(future)

# Save forecast for later use (Power BI / backend)
forecast_path = os.path.abspath(
    os.path.join(current_dir, "..", "data", "expense_forecast.csv")
)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(
    forecast_path, index=False
)

print("Prophet forecasting completed successfully.")
print("Forecast saved at:")
print(forecast_path)