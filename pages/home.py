import dash
from dash import html, dcc, callback, Input, Output, State, ALL, MATCH
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from data import draw_charts
from utils import buying_calculate

dash.register_page(__name__, path="/")

layout = dbc.Container(
    [
        html.H1("My Portfolio"),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Draw by individual",
                    children=[dcc.Graph(id="individual-graph", figure={})],
                ),
                dcc.Tab(
                    label="Draw by One",
                    children=[dcc.Graph(id="whole-graph", figure={})],
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
        dcc.Store(id="ratio-data", data={}),
        html.Div(
            children=[],
            id="slider",
        ),
        html.Div(
            [
                html.Div(id="alert-calculator", style={"margin": "20px"}),
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
                            html.Div(id="buying-result", children=[]),
                        ]
                    ),
                    id="offcanvas",
                    title="Buying Calculator",
                    is_open=False,
                    scrollable=True,
                ),
            ],
            # align center
            style={
                "textAlign": "center",
                "margin-top": "20px",
                "margin-bottom": "20px",
            },
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
    Input("ratio-data", "data"),
)
def update_graph(input_values, ratios):
    if input_values is None:
        raise PreventUpdate
    else:
        whole_fig, ind_fig = draw_charts(input_values, ratios)
        return whole_fig, ind_fig


@callback(
    Output("offcanvas", "is_open"),
    Output("alert-calculator", "children"),
    Input("buying-calculator", "n_clicks"),
    [State("offcanvas", "is_open")],
    Input("ratio-data", "data"),
)
def toggle_offcanvas(n1, is_open, ratio):
    if n1:
        if sum(ratio.values()) == 100:
            return not is_open, None
        else:
            return (
                is_open,
                dbc.Alert(
                    ["Total Value should be 100."],
                    color="danger",
                ),
            )
    else:
        return is_open, None


def make_receipt(result):
    card_content = [
        dbc.Row(
            [
                dbc.Col(
                    html.H4(children=key),
                    width=4,
                    # style={"width": "30%"},
                ),
                dbc.Col(
                    html.H4(
                        children=value,
                        style={"text-align": "right"},
                    ),
                    width=6,
                    # style={"width": "70%"},
                ),
            ],
            justify="between",
        )
        for key, value in result.items()
    ]
    return dbc.Card(
        [
            dbc.CardHeader("Result"),
            dbc.CardBody(card_content),
        ],
        style={"margin": "10px"},
    )


@callback(
    Output("buying-result", "children"),
    Input("cash", "value"),
    Input("ratio-data", "data"),
)
def update_buying_result(cash, input_values):
    if cash is None or input_values == {}:
        raise PreventUpdate
    else:
        result = buying_calculate(cash, input_values)
        return make_receipt(result)


@callback(
    Output("slider", "children"),
    Input("my-list", "value"),
)
def update_slider(tickers):
    if tickers is None:
        raise PreventUpdate
    else:
        x = []
        for ticker in tickers:
            x.append(html.P(ticker))
            x.append(
                dcc.Slider(
                    0,
                    100,
                    marks=None,
                    value=0,
                    tooltip={"placement": "bottom", "always_visible": True},
                    id={
                        "type": "slider-by-ticker",
                        "index": ticker,
                    },
                )
            )

        return html.Div(x, style={"margin-bottom": "20px"})


@callback(
    Output("ratio-data", "data"),
    State({"type": "slider-by-ticker", "index": ALL}, "id"),
    Input({"type": "slider-by-ticker", "index": ALL}, "value"),
)
def update_ratio_store(id, values):
    if id == [] or id is None:
        raise PreventUpdate
    else:
        result = {x["index"]: y for x, y in zip(id, values)}
        return result
