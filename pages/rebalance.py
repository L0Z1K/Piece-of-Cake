import dash
from dash import html, dcc, Input, Output, State, callback, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from utils import rebalance

dash.register_page(__name__, path="/rebalance")

layout = dbc.Container(
    [
        html.H1("Rebalance your portfolio"),
        html.Div(children=[], id="your-stock-list"),
        html.Div(children=[], id="rebalance-result"),
    ]
)


@callback(
    Output("your-stock-list", "children"),
    Input("my-chart-list", "data"),
)
def update_your_stock_list(values):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.H4(children=value["value"]), width=2),
                    dbc.Col(
                        dbc.Input(
                            type="number",
                            placeholder="Enter your quantity",
                            id={
                                "type": "stock-quantity",
                                "index": value["value"],
                            },
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dcc.Slider(
                            0,
                            100,
                            # marks=None,
                            value=0,
                            tooltip={"placement": "bottom", "always_visible": True},
                            id={
                                "type": "r-slider-by-ticker",
                                "index": value["value"],
                            },
                        ),
                        width=6,
                    ),
                ],
                style={"width": "100%", "margin-bottom": "10px"},
            )
            for value in values
        ]
        + [
            dbc.Button(
                "Rebalance!",
                color="primary",
                n_clicks=0,
                id="rebalance-button",
                style={"margin": "10px"},
            )
        ],
    )


@callback(
    Output("rebalance-result", "children"),
    Input("rebalance-button", "n_clicks"),
    State({"type": "r-slider-by-ticker", "index": ALL}, "id"),
    State({"type": "r-slider-by-ticker", "index": ALL}, "value"),
    State({"type": "stock-quantity", "index": ALL}, "id"),
    State({"type": "stock-quantity", "index": ALL}, "value"),
)
def rebalance_portfolio(n_clicks, ids, ideal_ratio, _ids, quantity):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        result = rebalance(
            stocks={id["index"]: quantity[i] for i, id in enumerate(ids)},
            ideal_ratio=ideal_ratio,
        )
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(html.H4(children=k), width=2),
                        dbc.Col(
                            html.H4(children=v, style={"text-align": "right"}), width=4
                        ),
                    ],
                    justify="between",
                    style={"margin-bottom": "10px"},
                )
                for k, v in result.items()
            ]
        )
