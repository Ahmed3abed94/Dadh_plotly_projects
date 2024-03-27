import dash
from dash import html, dcc
import dash_bootstrap_components as dbc



dash.register_page(__name__ , name="Forcasting")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                      html.I( "Sales Forcasting" ,className="card-title"),
                                      html.H4(id="Total sales" , children="machine learning is loading........" ) 
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)