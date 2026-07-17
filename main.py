import os
import json
import base64
import requests
import pandas as pd
import pandas_ta as ta
import yfinance as yf

def get_weights():
    # Fetch parameters dynamically from your Lab repository
    url = "https://api.github.com/repos/maheshultimatum/Market-Weights-Lab/contents/optimal_weights.json?ref=main"
    headers = {
        "Authorization": f"token {os.getenv('GH_PAT')}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if 'content' not in data:
        print(f"API Error Response: {data}")
        raise KeyError("Could not find 'content' in GitHub API response.")
        
    return json.loads(base64.b64decode(data['content']).decode('utf-8'))

def run_screener():
    weights = get_weights()
    tickers = list(weights.keys()) # Extracts the .NS tickers dynamically
    results = []
    
    for ticker in tickers:
        params = weights[ticker]
        
        # Download 1 day of 5-minute intraday data
        df = yf.download(ticker, period='1d', interval='5m', progress=False)
        
        if df.empty:
            continue
            
        # Calculate EMAs using your pandas-ta syntax
        df['Fast'] = ta.ema(df['Close'], length=params['fast'])
        df['Slow'] = ta.ema(df['Close'], length=params['slow'])
        
        # Extract the most recent data points
        latest_close = float(df['Close'].iloc[-1])
        latest_fast = float(df['Fast'].iloc[-1])
        latest_slow = float(df['Slow'].iloc[-1])
        
        # Determine Trend and Intraday Signal
        trend = "UPTREND" if latest_fast > latest_slow else "DOWNTREND"
        signal = "BUY" if latest_close > latest_fast and trend == "UPTREND" else "SELL"
        
        results.append({
            "Asset": ticker,
            "Price": round(latest_close, 2),
            "Fast/Slow": f"{params['fast']}/{params['slow']}",
            "Trend": trend,
            "Signal": signal
        })
        
    update_readme(results)

def update_readme(results):
    # Construct the Markdown Dashboard
    markdown_table = "# Intraday Pulse Screener\n\n"
    markdown_table += "| Asset | Price | Fast/Slow | Trend | Signal |\n"
    markdown_table += "|---|---|---|---|---|\n"
    
    for row in results:
        markdown_table += f"| {row['Asset']} | {row['Price']} | {row['Fast/Slow']} | {row['Trend']} | **{row['Signal']}** |\n"
        
    # Write to README.md
    with open("README.md", "w") as f:
        f.write(markdown_table)
        
    print("README.md updated successfully with NSE signals.")

if __name__ == "__main__":
    run_screener()
