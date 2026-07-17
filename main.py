import requests, json, os, base64
import pandas as pd
import pandas_ta as ta
import yfinance as yf

def get_weights():
    url = "https://api.github.com/repos/maheshultimatum/Market-Weights-Lab/contents/optimal_weights.json"
    headers = {"Authorization": f"token {os.getenv('GH_PAT')}"}
    content = requests.get(url, headers=headers).json()['content']
    return json.loads(base64.b64decode(content).decode('utf-8'))

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
