import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from data import draw_charts

dash.register_page(__name__, path="/")

layout = dbc.Container(
    [
        html.H1("My Portfolio"),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Draw by One",
                    children=[dcc.Graph(id="whole-graph", figure={})],
                ),
                dcc.Tab(
                    label="Draw by individual",
                    children=[dcc.Graph(id="individual-graph", figure={})],
                ),
            ]
        ),
        # dcc.Graph(id="my-whole-graph", figure={}),
        dcc.Dropdown(
            id="my-list",
            options=[],
            value=None,
            clearable=False,
            multi=True,
        ),
    ]
)


@callback(Output("my-list", "options"), Input("my-chart-list", "data"))
def update_chart_list(chart_list):
    print(chart_list)
    return chart_list


@callback(
    Output("whole-graph", "figure"),
    Output("individual-graph", "figure"),
    Input("my-list", "value"),
)
def update_graph(input_values):
    if input_values is None:
        raise PreventUpdate
    else:
        whole_fig, ind_fig = draw_charts(input_values)
        return whole_fig, ind_fig
