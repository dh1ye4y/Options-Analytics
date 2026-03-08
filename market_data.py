import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_data(ticker,start="2020-01-01",end="2024-01-01"):
    return yf.download(ticker,start=start,end=end)

def clean_data(data):
    # Flatten multi-index columns (Yahoo format)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Use Adj Close if available, else use Close
    if "Adj Close" in data.columns:
        price_col = "Adj Close"
    else:
        price_col = "Close"

    data = data[[price_col, "Volume"]]
    data.rename(columns={price_col: "Adj Close"}, inplace=True)

    return data


def add_returns(data):
    data["Log_Return"]=np.log(data["Adj Close"]/data["Adj Close"].shift(1))
    return data

def add_historical_volatility(data,window=21):
    data["Hist_Vol"]=data["Log_Return"].rolling(window).std()*np.sqrt(252)
    return data

def get_risk_free_rate():
    """
    Fetch US 10Y Treasury yield from Yahoo Finance
    ^TNX is quoted as yield*10 (e.g. 45 = 4.5%)
    """

    data = yf.download("^TNX", period="5d")

    # Fix Yahoo multi-index columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    latest_yield = data["Close"].iloc[-1]

    # convert to float and decimal form
    return float(latest_yield) / 100

