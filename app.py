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
       

########
# Data and Variables
########

url_github_data = "https://github.com/kylejwaters/SuperRare-Network/blob/main/superrare%20top%20artists%20and%20collectors_2021-04-03.csv?raw=True"
tabtitle='SuperRare Network Viewer'
myheading='Who is in your SuperRare CryptoArt Sphere?'
githublink='https://github.com/kylejwaters/SuperRare-Network'
sourceurl='https://superrare.co/'  
kyletwitter = "https://twitter.com/waters_ky"
       
########### Initiate the app
app = dash.Dash(__name__,update_title=None)
server = app.server
app.title="PatronsOfCulture"

########### Each Page ###############
rankings = html.Div([
    html.H5("Aggregate Rankings:")],style={'color':'#04D9FF',"font-family":"NeueMachina-Regular"})

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
      
