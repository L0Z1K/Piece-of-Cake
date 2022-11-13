from dash import Dash, html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

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
        # dcc.Store(id="my-store", data={}),
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
    Output("my-submit-button", "disabled"),
    State("my-input", "value"),
    Input("my-button", "n_clicks"),
)
def update_output_div(input_value, n_clicks):
    if input_value is None:
        return "", {}, True
    input_value = input_value.upper()
    fig = draw_chart(input_value)
    if fig is None:
        return f"{input_value} not found", {}, True
    else:
        return input_value, fig, False


@app.callback(
    Output("my-list", "options"),
    # State("my-output", "children"),
    [State("my-list", "options")],
    [Input("my-submit-button", "n_clicks")],
)
def update_list(existing_options, n_clicks):
    print(n_clicks, existing_options)
    option_name = "Option {}".format(n_clicks)
    existing_options.append({"label": option_name, "value": option_name})
    return existing_options
    # if click:
    #     print(new_input, my_list, click)
    #     if my_list is None:
    #         my_list = [{"label": new_input, "value": new_input}]
    #     my_list.append({"label": new_input, "value": new_input})
    #     return my_list
    # else:
    #     raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
