import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd


def price_to_percentage(price):
    return (price - price[0]) / price[0] * 100


def draw_chart(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="1y")
    if len(hist) == 0:
        return None
    else:
        fig = px.line(x=hist.index, y=price_to_percentage(np.array(hist.Close)))
        return fig


def draw_charts(tickers, ratio=None):
    fig1 = go.Figure()
    fig2 = go.Figure()
    df = pd.DataFrame()
    for i, ticker in enumerate(tickers):
        data = yf.Ticker(ticker)
        hist = data.history(period="1y").reset_index()
        # No time-zone for mergin US and KR stock together
        hist.Date = hist.Date.dt.tz_localize(None)
        if i == 0:
            df["Date"] = pd.date_range(start=hist.Date.iloc[0], end=hist.Date.iloc[-1])
        hist[ticker] = price_to_percentage(np.array(hist.Close))
        df = df.merge(hist[["Date", ticker]], on="Date", how="left")
        fig1.add_trace(go.Scatter(x=hist.Date, y=hist[ticker], name=ticker))
    if ratio is None:
        df.set_index("Date", inplace=True)
        # should be changed when ratio comes in.
        df = df.interpolate("linear", limit_direction="both").mean(axis=1)
        fig2.add_trace(go.Scatter(x=df.index, y=df))
    else:
        raise NotImplementedError
    return fig2, fig1


def read_last_price(ticker: str):
    data = yf.Ticker(ticker)
    hist = data.history(period="1d")
    return hist.Close.iloc[-1]
