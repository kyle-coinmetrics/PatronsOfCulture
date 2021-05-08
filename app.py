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
url_github_data = "https://github.com/kylejwaters/PatronsOfCulture/blob/main/data/top_200_eth_addresses_20210508.xlsx?raw=True"
df_data = pd.read_excel(url_github_data)
df_data['Adr'] = [html.A(html.P(x[:5]+"..." +x[-4:]),href="https://opensea.io/accounts/"+x,target="_blank") for x in df_data['Adr'].values]

########### Initiate the app #######
app = dash.Dash(__name__,update_title=None)
server = app.server
app.title="Patrons Of Culture"

"""
########### Content by Page #########
"""
#####################################
########### RANKINGS  ###############
#####################################
rankings = html.Div(
    [
    #HEADER
    html.Div([
    
        html.Div(className="app-header",
             children=[
             
             html.H1('PATRONS OF CULTURE',
                     className="app-header--title",style={'color':'#723BC9'}),
            
            html.Div(
                    children=[
                        dbc.NavLink("rankings", id="app-header--rankings",href="/", active="exact"),
                        dbc.NavLink("newsletter", id="app-header--newsletter", href="/newsletter", active="exact"),
                        dbc.NavLink("about", id="app-header--about", href="/about", active="exact")
                        ]
                    )
            ]
            )
                ],
    style={"font-family":"NeueMachina-Regular"}
    ),
    #RANKINGS TABLE
    html.Div(
    html.H5("Aggregate Rankings:"),
    style={'color':'#04D9FF',"font-family":"NeueMachina-Regular"}
    ),
    
    html.Div(
    dbc.Table.from_dataframe(df_data),
    id="top-200-table"
    ),
    
    #FOOTER
    html.Div("©2021 Patrons of Culture. Designed by Kyle Waters & Jacob Zurita.",style={'color':'#723BC9',"font-family":"NeueMachina-Regular",'border-top':"thin #04D9FF solid","position":"absolute","right":"20%"})
    
    ]
            )
    
#####################################
########### About  ##################
#####################################
about = html.Div(
    [
    html.Div([
    
        html.Div(className="app-header",
             children=[
             
             html.H1('PATRONS OF CULTURE',
                     className="app-header--title",style={'color':'#723BC9'}),
            
            html.Div(
                    children=[
                        dbc.NavLink("rankings", id="app-header--rankings",href="/", active="exact"),
                        dbc.NavLink("newsletter", id="app-header--newsletter", href="/newsletter", active="exact"),
                        dbc.NavLink("about", id="app-header--about", href="/about", active="exact")
                        ]
                    )
            ]
            )
                ],
    style={"font-family":"NeueMachina-Regular"}
    ),
    html.H3("Patrons of the new creative economy."),
    html.Br(),
    html.H3("Patrons of the new creative economy. We are an analytics resource to spotlight those who are supporting creativity and longevity in crypto art."),
    ],
    style={'color':'#04D9FF',"font-family":"NeueMachina-Regular",'background-color':'#C7F7E8'}
    )

#####################################
########### NEWSLETTER ##############
#####################################
newsletter = html.Div(
    [
    html.Div([
    
    html.Div(className="app-header",
             children=[
             
             html.H1('PATRONS OF CULTURE',
                     className="app-header--title",style={'color':'#723BC9'}),
            
            html.Div(
                    children=[
                        dbc.NavLink("rankings", id="app-header--rankings",href="/", active="exact"),
                        dbc.NavLink("newsletter", id="app-header--newsletter", href="/newsletter", active="exact"),
                        dbc.NavLink("about", id="app-header--about", href="/about", active="exact")
                        ]
                    )
            ]
            )
                ],
    style={"font-family":"NeueMachina-Regular"}
    ),
    html.H5("Subscribe:")
    ],
    style={'color':'#04D9FF',"font-family":"NeueMachina-Regular",'background-color':'#F7F2F9'}
    )

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
                        dbc.NavLink("newsletter", id="app-header--newsletter", href="/newsletter", active="exact"),
                        dbc.NavLink("about", id="app-header--about", href="/about", active="exact")
                        ]
                    )
            ]
            )
                ],
    style={"font-family":"NeueMachina-Regular"}
    )
                                        
app.layout = html.Div([dcc.Location(id="url"), content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return rankings
    elif pathname == "/about":
        return about
    elif pathname == "/newsletter":
        return newsletter
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
      
