import dash_bootstrap_components as dbc
from dash_extensions.enrich import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(id="my-input", type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search",
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
)
