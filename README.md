# Intraday Pulse Screener

An automated, data-driven trading tool designed to screen Indian market equities (NSE) using an optimized technical momentum strategy. The pipeline dynamically updates during market hours using serverless infrastructure.

## Key Features
* **Automated Asset Allocation:** Weights are dynamically optimized using an **Inverse Volatility Weighting** mathematical model based on 60 days of historical daily log returns.
* **Intraday Momentum Tracking:** Processes 5-minute interval market data to calculate high-velocity **5 EMA (Fast)** and **31 EMA (Slow)** trends.
* **Noise Filtering:** Uses a three-state execution matrix (`BUY`, `SELL`, `HOLD`) to distinguish between structural trend reversals and standard intraday pullbacks.
* **Serverless Infrastructure:** Powered entirely by GitHub Actions, executing every 5 minutes exclusively during Indian market trading windows (9:15 AM - 3:30 PM IST).

---

## Live Signal Dashboard

| Asset | Price | Fast (5 EMA) / Slow (31 EMA) | Trend | Signal |
|---|---|---|---|---|
| SBIN.NS | 1008.6 | 5/31 | **DOWNTREND** | **SELL** |
| DRREDDY.NS | 1158.9 | 5/31 | **UPTREND** | **BUY** |
| TITAN.NS | 4678.4 | 5/31 | **DOWNTREND** | **HOLD** |
| BAJAJFINSV.NS | 1892.0 | 5/31 | **UPTREND** | **HOLD** |
| TRENT.NS | 2896.6 | 5/31 | **DOWNTREND** | **SELL** |
| MARUTI.NS | 13504.0 | 5/31 | **DOWNTREND** | **SELL** |
| BAJFINANCE.NS | 1047.6 | 5/31 | **DOWNTREND** | **SELL** |

---

## Architecture & Strategy

### 1. Optimization (`optimize.py`)
Allocates portfolio weights inversely proportional to historical standard deviation (volatility). This minimizes concentration risk in high-beta assets:
$$w_i = \frac{\frac{1}{\sigma_i}}{\sum_{j=1}^{N} \frac{1}{\sigma_j}}$$

### 2. Signal Matrix (`main.py`)
* **`BUY`**: Triggered strictly when `Trend == UPTREND` and the current `Price > 5 EMA`.
* **`SELL`**: Triggered strictly when `Trend == DOWNTREND` and the current `Price < 5 EMA`.
* **`HOLD`**: Triggered during counter-trend pullbacks, preserving capital from choppy whipsaws.

*Disclaimer: This repository is for educational and research purposes only. Past performance does not guarantee future financial results.*
