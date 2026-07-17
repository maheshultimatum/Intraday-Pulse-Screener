import json
import pandas as pd
import yfinance as yf
import pandas_ta as ta

def get_weights():
    # Adjust this path or URL if you pull your JSON from a different location
    try:
        with open('optimal_weights.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: optimal_weights.json not found.")
        return {}

def run_screener():
    weights = get_weights()
    if not weights:
        return []
        
    tickers = list(weights.keys())
    results = []
    
    for ticker in tickers:
        params = weights[ticker]
        
        # Download 5 days of 5-minute data to prevent after-hours empty data errors
        df = yf.Ticker(ticker).history(period='5d', interval='5m')
        
        if df.empty:
            print(f"Warning: No data found for {ticker}")
            continue
            
        # Calculate EMAs
        df['Fast'] = ta.ema(df['Close'], length=params['fast'])
        df['Slow'] = ta.ema(df['Close'], length=params['slow'])
        
        # Check for NaN/None values caused by insufficient data
        if df['Fast'].iloc[-1] is None or pd.isna(df['Fast'].iloc[-1]) or \
           df['Slow'].iloc[-1] is None or pd.isna(df['Slow'].iloc[-1]):
            results.append({
                "Asset": ticker,
                "Price": round(float(df['Close'].iloc[-1]), 2),
                "Fast/Slow": f"{params['fast']}/{params['slow']}",
                "Trend": "INIT",
                "Signal": "WAIT"
            })
            continue 
            
        # If data is sufficient, proceed with calculations
        latest_close = float(df['Close'].iloc[-1])
        latest_fast = float(df['Fast'].iloc[-1])
        latest_slow = float(df['Slow'].iloc[-1])
        
        # Determine Trend
        trend = "UPTREND" if latest_fast > latest_slow else "DOWNTREND"
        
        # Determine Intraday Signal
        if trend == "UPTREND":
            signal = "BUY" if latest_close > latest_fast else "HOLD"
        else:
            signal = "SELL" if latest_close < latest_fast else "HOLD"
            
        results.append({
            "Asset": ticker,
            "Price": round(latest_close, 2),
            "Fast/Slow": f"{params['fast']}/{params['slow']}",
            "Trend": trend,
            "Signal": signal
        })
        
    return results

def update_readme(results):
    markdown_table = "# Intraday Pulse Screener\n\n"
    markdown_table += "| Asset | Price | Fast (5 EMA) / Slow (31 EMA) | Trend | Signal |\n"
    markdown_table += "|---|---|---|---|---|\n"
    
    for row in results:
        trend_display = f"**{row['Trend']}**" if row['Trend'] != "INIT" else row['Trend']
        signal_display = f"**{row['Signal']}**" if row['Signal'] != "WAIT" else row['Signal']
        
        markdown_table += f"| {row['Asset']} | {row['Price']} | {row['Fast/Slow']} | {trend_display} | {signal_display} |\n"
        
    # 'w' mode overwrites the file completely, preventing duplicate rows
    with open("README.md", "w") as f:
        f.write(markdown_table)
        
    print("README.md updated successfully.")

if __name__ == "__main__":
    screener_results = run_screener()
    if screener_results:
        update_readme(screener_results)
    else:
        print("No results to update.")
