import requests, json, os, base64
import pandas as pd
import pandas_ta as ta
import yfinance as yf

def get_weights():
    # Ensure this matches your ACTUAL repo name and branch
    url = "https://api.github.com/repos/maheshultimatum/Market-Weights-Lab/contents/optimal_weights.json?ref=main"
    headers = {
        "Authorization": f"token {os.getenv('GH_PAT')}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if 'content' not in data:
        print(f"API Error Response: {data}") # This will print the error in your Action log
        raise KeyError("Could not find 'content' in GitHub API response.")
        
    return json.loads(base64.b64decode(data['content']).decode('utf-8'))

def run_screener():
    weights = get_weights()
    lines = ["# Intraday Pulse Screener", "", "| Asset | Price | Fast/Slow | Trend | Signal |", "|---|---|---|---|---|"]
    
    for ticker, params in weights.items():
        df = yf.Ticker(ticker).history(period="2d", interval="5m")
        df['Fast'] = ta.ema(df['Close'], length=params['fast'])
        df['Slow'] = ta.ema(df['Close'], length=params['slow'])
        
        trend = "UPTREND" if df['Close'].iloc[-1] > df['Slow'].iloc[-1] else "DOWNTREND"
        signal = "BUY" if trend == "UPTREND" else "SELL"
        lines.append(f"| {ticker} | {df['Close'].iloc[-1]:.2f} | {params['fast']}/{params['slow']} | {trend} | **{signal}** |")
        
    with open("README.md", "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    run_screener()
