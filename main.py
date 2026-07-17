import requests, json, datetime
import pandas as pd
import numpy as np
import mplfinance as mpf
import pandas_ta as ta
from sklearn.linear_model import LogisticRegression
import os
import requests

WEIGHTS_URL = "https://raw.githubusercontent.com/maheshultimatum/Market-Weights-Lab/main/optimal_weights.json"

def get_weights():
    # Fetch the token from the environment variable provided by GitHub Actions
    token = os.getenv("GH_PAT")
    headers = {"Authorization": f"token {token}"}
    
    # Use the token to access your private Market-Weights-Lab repo
    response = requests.get(
        "https://api.github.com/repos/maheshultimatum/Market-Weights-Lab/contents/optimal_weights.json",
        headers=headers
    )
    
    # Note: When accessing contents via API, the file content is base64 encoded
    # You will need to decode it:
    import base64
    content = response.json()['content']
    return json.loads(base64.b64decode(content).decode('utf-8'))

def run_screener():
    weights = get_weights()
    results = []
    
    for ticker, name in {"RELIANCE.NS": "Reliance", "TCS.NS": "TCS", "HDFCBANK.NS": "HDFC", "DRREDDY.NS": "DrReddy", "TRENT.NS": "Trent"}.items():
        df = pd.DataFrame() # Replace with yf.Ticker(ticker).history(...)
        params = weights[ticker]
        
        # Calculate indicators using fetched params
        df['EMA_Fast'] = ta.ema(df['Close'], length=params['fast'])
        df['EMA_Slow'] = ta.ema(df['Close'], length=params['slow'])
        
        # Signal Logic
        trend = "UPTREND" if df['Close'].iloc[-1] > df['EMA_Slow'].iloc[-1] else "DOWNTREND"
        signal = "BUY SETUP" if trend == "UPTREND" else "SELL SETUP"
        
        results.append({
            "name": name, "price": df['Close'].iloc[-1], 
            "fast": params['fast'], "slow": params['slow'], 
            "trend": trend, "signal": signal
        })
        
    # Write README
    with open("README.md", "w") as f:
        f.write("# Intraday Pulse Screener\n\n| Asset | Price | Fast/Slow | Trend | Signal |\n|---|---|---|---|---|\n")
        for r in results:
            f.write(f"| {r['name']} | {r['price']:.2f} | {r['fast']}/{r['slow']} | {r['trend']} | **{r['signal']}** |\n")

if __name__ == "__main__":
    run_screener()
