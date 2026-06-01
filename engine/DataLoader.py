import yfinance as yf
import numpy as np
import pandas as pd
from datetime import date, timedelta

def load_data(ticker_symbol):
    today = date.today()
    year_length = 10
    dat = yf.Ticker(ticker_symbol)

    recent_data = dat.history(
        period='1mo',
        interval="1d",
        auto_adjust=False,
        )["Close"].dropna()
    if recent_data.empty:
        raise ValueError(f"{ticker_symbol}: 최근 1달 Close 데이터가 없습니다.")
    end_date = recent_data.index[-1].date()
    
    start_date = end_date - timedelta(days=365 * year_length)
    
    data = dat.history(
        start=start_date.isoformat(),
        end=(end_date + timedelta(days=1)).isoformat(),
        interval="1d",
        auto_adjust=False
        )["Close"].dropna()
    data=data.reset_index()

    data = data[['Date', 'Close']]
    time = data["Date"].apply(pd.Timestamp.toordinal).values
    price = np.log(data["Close"]).values.reshape(-1)

    observations = np.array([time, price])

    return observations, end_date