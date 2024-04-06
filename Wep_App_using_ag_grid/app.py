import dash
from dash import html, dcc ,callback ,Input , Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_ag_grid as dag




df = pd.read_csv(r"src\train.csv")

head = html.Header("web application where you can select the data you want to see in the graph and also you can control more filters from the table filter",
                   className="bg-opacity-50 p-2 m-1 bg-primary text-dark fw-bold rounded text-center fs-2")

drop = html.Div([html.H5("select the x axis of the graph")
                 ,dcc.Dropdown(id="drop" ,
                    options=[{"label":x , "value":x} for x in df.columns],
                    multi=False)])
table = dbc.Card([
    dbc.CardHeader("any filter you will choose will apply in the graph"),
    dbc.CardBody([dag.AgGrid(
    id="custom-theme-example",
    rowData=df.to_dict("records"),
    columnDefs=[{"field" : x} for x in df.columns],
    defaultColDef={"resizable":True , "sortable" : True , "filter" :True ,"floatingFilter" :True },
    columnSize="autoSize",
    dashGridOptions={"pagination":True ,"paginationPageSize":10},
    className="ag-theme-alpine dbc-ag-grid")]),
    dbc.CardFooter([dbc.Row([
        dbc.Col([dbc.Button(id="save" , children="save as csv")],width = 2)

                            ]),
        dbc.Row(dbc.Alert(id="alt" , children=[] ,is_open=False , duration=2000))])
])
    



graph = dcc.Graph(id="graph" , figure={})

app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([head,drop,graph , table])

@app.callback(
    Output("graph" , "figure"),
    Input("custom-theme-example" ,"virtualRowData"),
    Input("drop" ,"value"),
)

def update_fig(table , drop ):
    if drop :
        dff = pd.DataFrame(table)
        return px.histogram(dff , x=drop , y="Sales" ,histfunc="sum" ,text_auto="0.2f" ,color=drop )

    else:
        dff = pd.DataFrame(table)
        return px.histogram(dff , x="Region" , y="Sales" ,histfunc="sum" ,text_auto="0.2f" )
        
@app.callback(
    Output("custom-theme-example", "exportDataAsCsv"),
    Input("save" ,"n_clicks"),
)


def save (n):
    if n:
        return True 
    else :
        return False


if __name__ == "__main__" :
    app.run_server(debug = True , port = 7000)