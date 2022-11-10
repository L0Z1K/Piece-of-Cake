from dash import Dash, html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc

from utils import search_bar
from data import draw_chart

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        # html.H1("Multi-page app with Dash Pages"),
        html.Div(
            [
                dbc.NavbarSimple(
                    children=[search_bar],
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
    Output("my-output", "children"),
    Output("my-graph", "figure"),
    State("my-input", "value"),
    Input("my-button", "n_clicks"),
)
def update_output_div(input_value, click):
    if click:
        fig = draw_chart(input_value)
        if fig is None:
            return f"{input_value} not found", {}
        else:
            return f"{input_value}", fig
    else:
        return None, None


if __name__ == "__main__":
    app.run_server(debug=True)
