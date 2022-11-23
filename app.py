from dash import Dash, html, dcc, Input, Output, State
import os
import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from data import draw_chart

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    [
        dcc.Store(id="my-chart-list", data=[], storage_type="session"),
        dcc.Store(id="my-store", data=None),
        dcc.Location(id="url", refresh=False),
        # html.H1("Multi-page app with Dash Pages"),
        html.Div(
            [
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(
                            dbc.NavLink("Rebalance", href="/rebalance", active=True)
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Input(
                                        id="my-input",
                                        type="search",
                                        placeholder="Search",
                                    )
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "🔍",
                                        id="my-button",
                                        href="/search",
                                        color="primary",
                                        className="ms-2",
                                        n_clicks=0,
                                    ),
                                    width="auto",
                                ),
                            ],
                            className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                            align="center",
                        ),
                    ],
                    brand="Piece of Cake",
                    brand_href="/",
                    color="light",
                )
            ]
        ),
        dash.page_container,
    ]
)


@app.callback(
    Output("my-store", "data"),
    State("my-input", "value"),
    Input("my-button", "n_clicks"),
)
def update_search_key(input_value, n_clicks):
    if input_value is None:
        return ""
    else:
        return input_value.upper()


if __name__ == "__main__":
    if "DASH_DEBUG" not in os.environ:
        os.environ["DASH_DEBUG"] = "TRUE"
    app.run_server()
