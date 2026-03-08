from market_data import *
from black_scholes import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# -------------------------------------------------
# USER INPUT (LIVE COMPONENT)
# -------------------------------------------------

ticker = input("Enter stock ticker (e.g., AAPL): ")
days = int(input("Enter days to expiry (e.g., 30): "))
strike_pct = float(input("Enter strike % (e.g., 1.05 for 5% OTM): "))

# -------------------------------------------------
# DATA PIPELINE
# -------------------------------------------------

df = get_stock_data(ticker, "2023-01-01", "2024-01-01")
df = clean_data(df)
df = add_returns(df)
df = add_historical_volatility(df)
df = df.dropna()

# -------------------------------------------------
# HISTORICAL VS IMPLIED VOLATILITY
# -------------------------------------------------

iv_list = []
dates = df.index[-60:]

for date in dates:
    S_temp = df.loc[date, "Adj Close"]
    sigma_temp = df.loc[date, "Hist_Vol"]

    K_temp = S_temp * strike_pct
    T_temp = days / 365
    r_temp = 0.05

    bs = black_scholes_call(S_temp, K_temp, T_temp, r_temp, sigma_temp)
    market = bs * 1.1

    iv = implied_volatility_call(market, S_temp, K_temp, T_temp, r_temp)
    iv_list.append(iv)

df_iv = df.tail(60).copy()
df_iv["Implied_Vol"] = iv_list

plt.figure(figsize=(10,5))
plt.plot(df_iv.index, df_iv["Hist_Vol"], label="Historical Vol")
plt.plot(df_iv.index, df_iv["Implied_Vol"], label="Implied Vol")
plt.legend()
plt.title("Historical vs Implied Volatility")
plt.savefig("results/historical_vs_implied_vol.png")
plt.show()

# -------------------------------------------------
# EARNINGS VOLATILITY ANALYSIS
# -------------------------------------------------

earnings_dates = pd.to_datetime([
    "2023-02-02","2023-05-04","2023-08-03","2023-11-02"
])

vol_windows = []

for date in earnings_dates:
    window = df.loc[
        date - pd.Timedelta(days=30):
        date + pd.Timedelta(days=30)
    ].copy()

    window["Days_From_Earnings"] = (window.index - date).days
    vol_windows.append(window)

plt.figure(figsize=(10,5))
for w in vol_windows:
    plt.plot(w["Days_From_Earnings"], w["Hist_Vol"], alpha=0.6)

plt.axvline(0)
plt.title("Volatility Around Earnings")
plt.savefig("results/vol_around_earnings.png")
plt.show()

# -------------------------------------------------
# OPTIONS ANALYTICS DASHBOARD
# -------------------------------------------------

S = df["Adj Close"].iloc[-1]
sigma = df["Hist_Vol"].iloc[-1]

K = S * strike_pct
T = days / 365
r = get_risk_free_rate()

print("\n------ OPTIONS ANALYTICS ------")
print("Ticker:", ticker)
print("Stock Price:", S)
print("Historical Vol:", sigma)
print("Risk-Free Rate:", r)

call_price = black_scholes_call(S, K, T, r, sigma)

print("\nCall Option Price:", call_price)

print("\nGreeks:")
print("Delta:", delta_call(S, K, T, r, sigma))
print("Gamma:", gamma(S, K, T, r, sigma))
print("Vega:", vega(S, K, T, r, sigma))

# -------------------------------------------------
# OPTION PRICE VS STOCK PRICE
# -------------------------------------------------

S_range = np.linspace(0.8*S, 1.2*S, 50)

call_prices = []
for s in S_range:
    call_prices.append(black_scholes_call(s, K, T, r, sigma))

plt.figure(figsize=(10,5))
plt.plot(S_range, call_prices)
plt.title("Call Option Price vs Stock Price")
plt.xlabel("Stock Price")
plt.ylabel("Call Price")
plt.savefig("results/option_vs_stock.png")
plt.show()

# -------------------------------------------------
# DELTA VS STOCK PRICE
# -------------------------------------------------

deltas = []
for s in S_range:
    deltas.append(delta_call(s, K, T, r, sigma))

plt.figure(figsize=(10,5))
plt.plot(S_range, deltas)
plt.title("Delta vs Stock Price")
plt.xlabel("Stock Price")
plt.ylabel("Delta")
plt.savefig("results/delta_vs_stock.png")
plt.show()

# -------------------------------------------------
# VOLATILITY SMILE
# -------------------------------------------------

strike_range = np.linspace(0.85*S, 1.15*S, 10)
iv_smile = []

for K_smile in strike_range:
    bs_price = black_scholes_call(S, K_smile, T, r, sigma)
    market_price = bs_price * 1.10
    iv = implied_volatility_call(market_price, S, K_smile, T, r)
    iv_smile.append(iv)

plt.figure(figsize=(10,5))
plt.plot(strike_range, iv_smile)
plt.title("Volatility Smile")
plt.xlabel("Strike Price")
plt.ylabel("Implied Volatility")
plt.savefig("results/vol_smile.png")
plt.show()

# -------------------------------------------------
# THETA DECAY
# -------------------------------------------------

days_to_expiry = np.linspace(1, 90, 50)
option_prices_time = []

for d in days_to_expiry:
    T_temp = d / 365
    price = black_scholes_call(S, K, T_temp, r, sigma)
    option_prices_time.append(price)

plt.figure(figsize=(10,5))
plt.plot(days_to_expiry, option_prices_time)
plt.title("Option Price Decay Over Time (Theta)")
plt.xlabel("Days to Expiry")
plt.ylabel("Call Price")
plt.savefig("results/theta_decay.png")
plt.show()

