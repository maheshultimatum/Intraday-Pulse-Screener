import json
import pandas as pd
import yfinance as yf

def calculate_optimal_weights():
    # 1. Define your universe of Indian stocks (NSE suffix required)
    tickers = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']
    
    # 2. Fetch historical data (example logic for your optimization)
    # df = yf.download(tickers, period='1y')
    # ... insert your scipy/quant logic here to determine the best params ...
    
    # 3. Format the final output as a nested dictionary
    optimal_parameters = {
        "RELIANCE.NS": {
            "weight": 0.30,
            "fast": 9,
            "slow": 21
        },
        "TCS.NS": {
            "weight": 0.30,
            "fast": 12,
            "slow": 26
        },
        "INFY.NS": {
            "weight": 0.20,
            "fast": 10,
            "slow": 20
        },
        "HDFCBANK.NS": {
            "weight": 0.20,
            "fast": 8,
            "slow": 21
        }
    }
    
    # 4. Export to JSON for the Screener repo to consume
    with open('optimal_weights.json', 'w') as f:
        json.dump(optimal_parameters, f, indent=4)
        
    print("Optimization complete. optimal_weights.json updated for NSE stocks.")

if __name__ == "__main__":
    calculate_optimal_weights()
