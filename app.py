# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:32:55 2021

@author: kylej
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
import pandas as pd

########
# Data and Variables
########

url_github_data = "https://github.com/kylejwaters/PatronsOfCulture/blob/main/data/top_200_eth_addresses_20210507.xlsx?raw=True"
df_data = pd.read_excel(url_github_data)

########### Initiate the app
app = dash.Dash(__name__,update_title=None)
server = app.server
app.title="PatronsOfCulture"

########### Each Page ###############
rankings = html.Div(
    [
    
    html.Div(
    html.H5("Aggregate Rankings:"),
    style={'color':'#04D9FF',"font-family":"NeueMachina-Regular"}
    ),
    
    html.Div(
    
    dbc.Table.from_dataframe(df_data, striped=True, bordered=True, hover=True,style={'color':'#723BC9',"font-family":"NeueMachina-Regular"}),
    )

    ]
            )
    
########### About  ##################
about = html.Div([
    html.H5("Patrons of the new creative economy.")],style={'color':'#04D9FF',"font-family":"NeueMachina-Regular"})

########### Set up the base layout ###############
content = html.Div(id="page-content")

base_header = html.Div([
    
    html.Div(className="app-header",
             children=[
             
             html.H1('PATRONS OF CULTURE',
                     className="app-header--title",style={'color':'#723BC9'}),
            
            html.Div(
                    children=[
                        dbc.NavLink("rankings", id="app-header--rankings",href="/", active="exact"),
                        dbc.NavLink("about", id="app-header--about", href="/about", active="exact")
                        ]
                    )
            ]
            )
                ],
    style={"font-family":"NeueMachina-Regular"}
    )
                                        
app.layout = html.Div([dcc.Location(id="url"), base_header, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return rankings
    elif pathname == "/about":
        return about
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )                  
                     
if __name__ == '__main__':
    app.run_server()
      
