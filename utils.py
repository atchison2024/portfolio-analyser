import json
import requests
import pandas as pd
import numpy as np

# URL to your JSON file in the data-collector repo (adjust as needed)
DATA_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/data-collector/main/portfolio.json"

def fetch_portfolio():
    response = requests.get(DATA_URL)
    if response.status_code != 200:
        raise Exception("Failed to load portfolio data.")
    return pd.DataFrame(response.json())

def calculate_portfolio_metrics(df):
    if df.empty:
        return 0.0, 0.0
    weights = df['allocation'] / df['allocation'].sum()
    port_return = np.dot(weights, df['return'])
    port_vol = np.sqrt(np.dot(weights ** 2, df['volatility'] ** 2))
    return round(port_return, 4), round(port_vol, 4)
