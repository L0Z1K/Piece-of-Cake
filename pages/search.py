import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path="/search")

layout = dbc.Container(
    [
        html.H1(id="my-output"),
        dcc.Graph(id="my-graph", figure={}),
        dbc.Button(
            "Add to my chart",
            id="my-submit-button",
            # href="/",
            color="primary",
            className="ms-2",
            n_clicks=0,
        ),
        html.Div(id="my-list"),
    ]
)


@callback(
    Output("my-list", "children"),
    Input("my-list", "children"),
    State("my-output", "children"),
    Input("my-submit-button", "n_clicks"),
)
def update_list(children, new_input, click):
    if click:
        return children + " " + new_input
    else:
        return children
