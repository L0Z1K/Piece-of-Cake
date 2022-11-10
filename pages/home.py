import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path="/")

layout = dbc.Container(
    [
        html.H1(id="my-list"),
    ]
)
