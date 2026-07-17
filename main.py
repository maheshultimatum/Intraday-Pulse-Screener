import requests, json, datetime
import pandas as pd
import numpy as np
import mplfinance as mpf
import pandas_ta as ta
from sklearn.linear_model import LogisticRegression

WEIGHTS_URL = "https://raw.githubusercontent.com/maheshultimatum/Market-Weights-Lab/main/optimal_weights.json"

def get_weights():
    return requests.get(WEIGHTS_URL).json()

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
