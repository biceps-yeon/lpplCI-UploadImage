import yfinance as yf
import numpy as np
import pandas as pd
from datetime import date, timedelta

def test(ticker_symbol):
    # ticker_symbol = "^KS11"
    today = date.today()
    year_length = 10
    dat = yf.Ticker(ticker_symbol)

    recent_data = dat.history(period='1mo', interval="1d",auto_adjust=False,)["Close"].dropna()
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



obs, end_date = test('^KS11')
print(obs)

def tested():
    ticker_symbol="^KS11"
    dat = yf.Ticker(ticker_symbol)

    # get historical market data
    # print(dat.history(period='1mo')['Close'])


    recent = dat.history(
        period="1mo",
        interval="1d",
        auto_adjust=False
    )

    recent_close = recent["Close"].dropna()

    if recent_close.empty:
        raise ValueError(f"{ticker_symbol}: 최근 거래 데이터가 없습니다.")

    latest_market_date = recent_close.index[-1].date()


    start_date = latest_market_date - timedelta(days=365 * 10)
    end_date = latest_market_date + timedelta(days=1)

    hist = dat.history(
        start=start_date.isoformat(),
        end=end_date.isoformat(),
        interval="1d",
        auto_adjust=False
    )

    close = hist["Close"].dropna()

    print(hist['Close'])