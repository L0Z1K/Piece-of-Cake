import yfinance as yf
import plotly.express as px


def draw_chart(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="1y")
    if len(hist) == 0:
        return None
    else:
        fig = px.line(hist, x=hist.index, y=hist.Close)
        return fig
