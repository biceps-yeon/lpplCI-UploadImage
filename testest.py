import yfinance as yf
import numpy as np
import pandas as pd
from datetime import date, timedelta

def load_data(ticker_symbol):
    today = date.today()
    year_length = 10
    dat = yf.Ticker(ticker_symbol)

    recent_data = dat.history(period='1mo', interval="1d",auto_adjust=False,)["Close"].dropna()
    # recent_data = yf.download(ticker_symbol, start=(today - timedelta(days=7)).isoformat(), end=(today + timedelta(days=1)).isoformat())
    if recent_data.empty:
        raise ValueError(f"{ticker_symbol}: 최근 1달 Close 데이터가 없습니다.")
    end_date = recent_data.index[-1].date()
    
    try:
        start_date = end_date.replace(year=end_date.year - year_length)
    except ValueError:
        start_date = end_date - timedelta(days=365 * year_length)

    data = yf.download(ticker_symbol, start=start_date, end=(end_date + timedelta(days=1)).isoformat())
    data.reset_index(inplace=True)
    
    data = data[['Date', 'Close']]
    time = data['Date'].apply(pd.Timestamp.toordinal).values
    price = np.log(data['Close']).values.reshape(-1)

    observations = np.array([time, price])
    return observations, end_date
