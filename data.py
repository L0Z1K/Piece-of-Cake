import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def price_to_percentage(price: np.ndarray):
    return (price - price[0]) / price[0] * 100


def draw_chart(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="1y")
    if len(hist) == 0:
        return None
    else:
        fig = px.line(hist, x=hist.index, y=price_to_percentage(np.array(hist.Close)))
        return fig


def draw_charts(tickers):
    fig = go.Figure()
    for ticker in tickers:
        data = yf.Ticker(ticker)
        hist = data.history(period="1y")
        fig.add_trace(
            go.Scatter(
                x=hist.index, y=price_to_percentage(np.array(hist.Close)), name=ticker
            )
        )
    return fig, fig
