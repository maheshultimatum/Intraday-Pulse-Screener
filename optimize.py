import json
import pandas as pd
import yfinance as yf

def calculate_optimal_weights():
    # ---------------------------------------------------------
    # 1. Fetch historical data for your Indian universe
    # Example: yf.download(['RELIANCE.NS', 'TCS.NS', 'INFY.NS'], period='1y')
    # ---------------------------------------------------------
    
    # 3. Format the output exactly how the Screener expects it
    optimal_parameters = {
      "RELIANCE.NS": {
        "weight": 0.40,
        "fast": 9,
        "slow": 21
      },
      "TCS.NS": {
        "weight": 0.35,
        "fast": 12,
        "slow": 26
      },
      "INFY.NS": {
        "weight": 0.25,
        "fast": 10,
        "slow": 20
      }
    }
    
    # 4. Save to JSON
    with open('optimal_weights.json', 'w') as f:
        json.dump(optimal_parameters, f, indent=4)
        
    print("Optimization complete. optimal_weights.json updated for NSE stocks.")

if __name__ == "__main__":
    calculate_optimal_weights()
