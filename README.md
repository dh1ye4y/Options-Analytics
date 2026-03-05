# Options Analytics & Volatility Modeling System

## Overview

This project is an end‑to‑end options analytics pipeline built in Python using the Black–Scholes model and real market data. It integrates financial theory, numerical methods, and data visualization to simulate how options are analyzed in trading environments.

The system retrieves stock data, computes historical volatility, prices options, extracts implied volatility, calculates Greeks, and generates multiple visual analytics used in quantitative finance.

## Key Features

Retrieve real stock market data using Yahoo Finance

Clean and preprocess financial time series

Compute log returns and historical volatility

Implement the Black–Scholes pricing model from scratch

Calculate option Greeks (Delta, Gamma, Vega)

Estimate implied volatility using the Newton–Raphson method

Compare historical vs implied volatility

Analyze volatility behavior around earnings events

Generate volatility smile

Visualize theta decay

Perform option price sensitivity analysis

## Project Structure

```
options-analytics/
│
├── main.py              # Main script executing the analytics pipeline
├── black_scholes.py     # Black–Scholes model implementation
├── market_data.py       # Market data retrieval and preprocessing
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Files ignored by Git
```

## Installation

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/options-analytics.git
cd options-analytics

2. Install required packages

pip install -r requirements.txt

Usage

Run the main script:

python main.py

You will be prompted to provide:

Stock ticker (example: AAPL)

Days to option expiry (example: 30)

Strike percentage relative to current price (example: 1.05 for 5% OTM)

The script will then perform the full analytics workflow and generate multiple plots.

## Analytics Produced

1. Historical vs Implied Volatility

Compares realized volatility with model‑derived implied volatility over time.

2. Earnings Volatility Analysis

Examines volatility behavior in a ±30 day window around earnings announcements.

3. Options Pricing Dashboard

Displays:

Current stock price

Historical volatility

Risk‑free rate

Black–Scholes option price

Option Greeks

4. Sensitivity Analysis

Plots showing how option price and delta change with stock price.

5. Volatility Smile

Illustrates how implied volatility varies across different strike prices.

6. Theta Decay

Shows how option value decreases as time to expiry approaches.

## Financial Concepts Used

Black–Scholes Model

Used to price European options based on five parameters:

Stock price (S)

Strike price (K)

Time to maturity (T)

Risk‑free interest rate (r)

Volatility (σ)

Historical Volatility

Historical Volatility = Std(Log Returns) × √252

**Implied Volatility

Implied volatility is computed numerically using the Newton–Raphson method, solving for volatility such that the Black–Scholes price matches the observed market price.

## Limitations

Assumes European option exercise

Assumes constant volatility (Black–Scholes assumption)

Market option prices are simulated for demonstration purposes

Uses US 10Y Treasury yield as a proxy for the risk‑free rate

## Possible Improvements

Integrate real option chain data

Add support for put option analytics

Implement stochastic volatility models (e.g., Heston model)

Build an interactive dashboard using Streamlit

## Dependencies

The project uses the following Python libraries:

numpy

pandas

matplotlib

scipy

yfinance

Install them with:

pip install -r requirements.txt

## Author

Dhyey Desai

Aman Kapadia

## License

This project is intended for educational and research purposes.
