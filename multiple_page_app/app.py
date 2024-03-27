import dash
from dash import html, dcc
import dash_bootstrap_components as dbc



app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP ,dbc.icons.BOOTSTRAP],
                use_pages=True)

sidebar = dbc.Nav([
            dbc.NavLink([
                html.Div(page["name"],className="navlink") ] ,
                href=page["path"],
                active = "exact") 
                for page in dash.page_registry.values()
            ],
vertical=True,
pills=True,
className="sidebar-1")

app.layout = html.Div(
   [
        html.Div("Sales Analysis Web App" , className="bg-opacity-75 p-2 m-1 bg-primary text-light fw-bold rounded text-center fs-1" ),
        html.Hr(),
        dbc.Row([dbc.Col([sidebar],width=2  ),
                 dbc.Col(dash.page_container,width=10)]),
        

   ]
)





if(__name__) == "__main__":
    app.run_server( debug = True,port = 7050)