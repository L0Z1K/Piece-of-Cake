import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from data import draw_chart

dash.register_page(__name__, path="/search")

layout = dbc.Container(
    [
        html.H1(id="my-output"),
        dcc.Graph(id="my-graph", figure={}),
        dbc.Button(
            "Add to my chart",
            id="my-submit-button",
            href="/",
            color="primary",
            className="ms-2",
            n_clicks=0,
        ),
        html.Div(id="my-list"),
    ]
)


@callback(
    Output("my-output", "children"),
    Output("my-graph", "figure"),
    # Output("my-submit-button", "disabled"),
    Input("my-store", "data"),
)
def update_figure(input_value):
    if input_value is None or input_value == "":
        raise PreventUpdate
    else:
        fig = draw_chart(input_value)
        if fig is None:
            return f"{input_value} not found", {}  # , True
        else:
            return input_value, fig  # , False


@callback(
    Output("my-chart-list", "data"),
    State("my-chart-list", "data"),
    State("my-output", "children"),
    Input("my-submit-button", "n_clicks"),
)
def update_list(chart_list, new_input, n_clicks):
    if new_input is None:
        raise PreventUpdate
    else:
        chart_list.append({"label": new_input, "value": new_input})
        return chart_list
