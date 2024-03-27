import dash
from dash import html, dcc ,callback ,Input , Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__ , name="items")

df = pd.read_csv(r"src\train.csv" ,encoding="iso-8859-1" )
df["Order Date"] = pd.to_datetime(df["Order Date"] ,dayfirst=True) 
df["year"] = df["Order Date"].dt.year
df["month"] = df["Order Date"].dt.month
layout = dbc.Container(
    [   dbc.Row([dbc.Col([html.H6("choose years :")
                          ,dcc.Dropdown(id="drop11" ,options=[x for x in sorted(df["year"].unique())],
                     multi=True , value=[2015,2016] ,className="drop-year" )],width=3),
                dbc.Col([html.H6("choose month :")
                          ,dcc.Dropdown(id="drop12" ,options=[x for x in sorted(df["month"].unique())],
                     multi=True , value=[1,2,3,4,5,6,7,8,9,10,11,12] ,className="drop-month" )],width=3),
                dbc.Col([html.H6("choose product :")
                          ,dcc.Dropdown(id="drop13" ,options=[x for x in sorted(df["Category"].unique())],
                     multi=True , value=["Furniture","Office Supplies"] ,className="drop-Product" )],width=3)]),
        dbc.Row(
            [
                dbc.Col([dbc.Card([dbc.CardHeader(html.H1(children=[html.I(className="bi bi-currency-dollar") , "Total Sales"]
                                                           ,className="card-title") ),
                                dbc.CardBody(
                                    [
                                      html.H4(id="T-Saless" ,children=[] , className="text-center fw-bold"  )  
                                    ],
                                     )],color="light")]),
                dbc.Col([dbc.Card([dbc.CardHeader(html.H1(children=[html.I(className = "bi bi-person-check"),"Cus. Count"] 
                                                          ,className="card-title" )),
                                dbc.CardBody(
                                    [
                                      html.H4(id="cus-counts" ,children=[]  ,className="text-center fw-bold" )  
                                    ])],color="light")]),
                dbc.Col([dbc.Card([dbc.CardHeader(html.H1(children=[html.I(className = "bi bi-receipt"),"Order Count"]
                                                           ,className="card-title" )),
                                dbc.CardBody(
                                    [
                                      
                                      html.H4(id="order-counts" ,children=[]  , className="text-center fw-bold" )  
                                    ])],color="light")]),
                dbc.Col([dbc.Card([dbc.CardHeader(html.H1(children=[html.I(className = "bi bi-pencil-square"),"Product Count"]
                                                           ,className="card-title" )),
                                dbc.CardBody(
                                    [
                                      
                                      html.H4(id="item-counts" ,children=[]  , className="text-center fw-bold" )  
                                    ])],color="light")])
            ]
        ),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="barr" , figure={} ,className="fig1")
            ],width=5),
            dbc.Col([
                dcc.Graph(id="pie" , figure={} ,className="fig2")
            ],width=6)
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(id="linee" , figure={})])
        ])
    ]
)

@callback(
        Output("barr" , "figure"),
        Output("T-Saless" ,"children"),
        Output("cus-counts" ,"children"),
        Output("order-counts" ,"children"),
        Output("item-counts" , "children"),
        Output("linee" ,"figure"),
        Output("pie" , "figure"),
        
    Input("drop11" , "value"),
    Input("drop12" , "value"),
    Input("drop13" , "value")   
)

def update_bar(year ,month ,item):
    updated_df = df.query("year in @year & month in @month & Category in @item ")
    sales = format(updated_df["Sales"].sum() , "0.2f")
    cus_count = updated_df["Customer ID"].nunique()
    orders = updated_df["Order ID"].nunique()
    items = updated_df["Product ID"].nunique()
    bar_df = updated_df.groupby(["year" ,"Category"])["Sales"].sum().reset_index()
    line_df = updated_df.groupby(["year","month"])["Sales"].sum().reset_index()
    bar = px.bar(bar_df , x="Category" ,y="Sales" ,color=bar_df["year"]  ,barmode="group") 
    line = px.line(line_df , x=line_df["month"] , y="Sales" ,color="year" )
    pie = px.pie(updated_df , names="Sub-Category")
    return bar ,sales,cus_count,orders,items,line,pie