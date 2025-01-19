# File: src/forecasting.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_cash_flow(df, forecast_period=30, output_dir="extracted_texts"):
    """
    Forecast future daily cash flow based on historical transaction data.
    
    Parameters:
        df (DataFrame): A DataFrame containing at least two columns:
                        - "date": datetime values
                        - "amount": numeric transaction amounts (can be positive or negative)
        forecast_period (int): Number of days to forecast into the future.
        output_dir (str): Directory where the forecast plot will be saved.
        
    Returns:
        forecast (Series): The forecasted values as a pandas Series.
        output_path (str): The file path where the forecast plot image is saved.
    """
    
    # Ensure the 'date' column is a datetime type and set it as the index.
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    
    # Aggregate transactions to compute daily net cash flow
    daily_flow = df.groupby(df["date"].dt.date)["amount"].sum().sort_index()
    daily_flow.index = pd.to_datetime(daily_flow.index)
    
    # Make sure we have a continuous date range; fill missing days with 0.
    daily_flow = daily_flow.asfreq("D", fill_value=0)
    
    # Fit the Exponential Smoothing model (additive trend; no seasonality).
    model = ExponentialSmoothing(daily_flow, trend="add", seasonal=None)
    model_fit = model.fit(optimized=True)
    
    # Forecast the specified number of future days.
    forecast = model_fit.forecast(forecast_period)
    
    # Create a plot to show historical and forecasted cash flows.
    plt.figure(figsize=(12, 6))
    plt.plot(daily_flow, label="Historical Cash Flow")
    plt.plot(forecast, label="Forecasted Cash Flow", linestyle="--")
    plt.xlabel("Date")
    plt.ylabel("Daily Net Amount")
    plt.title("Cash Flow Forecast")
    plt.legend()
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the plot image to the specified directory.
    output_path = os.path.join(output_dir, "forecast_cash_flow.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    
    return forecast, output_path

# For standalone testing:
if __name__ == "__main__":
    # Example usage: expect extracted transaction data in "extracted_texts" via your existing module
    # For demonstration, we'll create a simple DataFrame that mimics transaction data.
    data = {
        "date": pd.date_range(start="2022-01-01", periods=100, freq="D"),
        "amount": [100 if i % 5 == 0 else -50 for i in range(100)]
    }
    df_example = pd.DataFrame(data)
    
    forecast, plot_path = forecast_cash_flow(df_example, forecast_period=30)
    print("Forecasted Cash Flow:")
    print(forecast)
    print("Forecast plot saved to:", plot_path)
