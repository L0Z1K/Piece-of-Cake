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
        html.Div(
            [
                dbc.Button("Buying Calculator", id="buying-calculator", n_clicks=0),
                dbc.Offcanvas(
                    html.Div(
                        [
                            html.P(
                                [
                                    "So, how do you buy stocks for this portfolio? 🤔",
                                    html.Br(),
                                    "It's hard to calculate one by one by yourself. 😭",
                                    html.Br(),
                                    "Let me help you! Just enter the amount of cash you have. 😄",
                                ],
                            ),
                            dcc.Input(
                                type="number",
                                min=0,
                                id="cash",
                                placeholder="How much cash do you have?",
                                style={"width": "100%"},
                            ),
                        ]
                    ),
                    id="offcanvas",
                    title="Buying Calculator",
                    is_open=False,
                ),
            ],
            # align center
            style={"textAlign": "center", "margin-top": "20px"},
        ),
    ]
)


@callback(
    Output("my-list", "options"),
    Output("my-list", "value"),
    Input("my-chart-list", "data"),
)
def update_chart_list(chart_list):
    return chart_list, [x["value"] for x in chart_list]


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


@callback(
    Output("offcanvas", "is_open"),
    Input("buying-calculator", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open
