import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from dash import dcc , html , Input , Output ,Dash,callback
import dash_bootstrap_components as dbc
import datetime

# loading the dataset
df = pd.read_csv("train.csv" , encoding="iso-8859-1" )
df["Order Date"] = pd.to_datetime(df["Order Date"] ,dayfirst=True)
# df["month"] = datetime.date(df["Order Date"]).month()
# df["year"] = datetime.date(df["Order Date"]).year()

# sitting graph config
graph_config={
        "staticPlot":False,
        "scrollZoom":True,
        "doubleClick":"reset",
        "showTips":False,
        "displayModeBar":True,
        "watermark":True
                  }


app = Dash(__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# sitting app layout

app.layout=(dbc.Container([
    dbc.Row(dbc.Col("Sales Analysis Dashboard",width=12,
                    className="p-2 m-1 bg-primary text-light fw-bold rounded text-center fs-1")),
    dbc.Row(dbc.Col(dcc.Dropdown(id="drop1" ,multi=True,
                                  value=["Furniture","Office Supplies"],
                                 options=[{"label":x , "value":x} for x in sorted(df["Category"].unique())]),width=6)),
    dbc.Row([dbc.Col(dcc.Graph(id="line" , figure={}  ,config=graph_config ),width=12),
        (dbc.Col(dcc.Graph(id="pie" , figure={} , clickData=None , hoverData=None,
                  config=graph_config),width=12))])

]))

# callback for line chart
@app.callback(
    Output("line","figure"),
    Input("drop1","value")
)
# func for updating line chart
def upadate_graph(cate):
    dff = df[df["Category"].isin(cate)].set_index("Order Date")
    dff_line = dff.groupby(["Order Date","Category"])["Sales"].sum().reset_index()
    line = px.line(dff_line,x="Order Date" , y="Sales" ,color="Category" ,custom_data=["Category"])
    return line

# callback for line chart
@app.callback(
    Output("pie" ,"figure"),
    Input("line","hoverData"),
    Input("drop1","value")
)
# func for updating line chart
def update_pie(hover,cate):
    if hover is None :
        dff_pie = df[df["Category"].isin(cate)]
        dff_date=dff_pie[dff_pie["Order Date"]=="21/05/2015"]
        pie = px.pie(dff_date , names="Category", values="Sales")
        return pie
    else:
        
        date = hover["points"][0]["x"]
        dff_pie = df[df["Category"].isin(cate)]
        dff_date=dff_pie[dff_pie["Order Date"]==date]
        pie = px.pie(dff_date , names="Category", values="Sales" , title=f"Sales by category at {date}")
        
        return pie

# runnig the app
if __name__ == "__main__":
    app.run_server(debug = True)
