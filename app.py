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
import numpy as np

########
# Data and Variables
########
url_github_data = "https://github.com/kylejwaters/PatronsOfCulture/blob/main/data/top_200_eth_addresses_20210508.xlsx?raw=True"
df_data = pd.read_excel(url_github_data)

#df_data["Name"] = np.where(
#    df_data["Name"].notnull(),
#    df_data.apply(lambda x: html.A(html.P(x.Name),href="https://opensea.io/accounts/"+x.Adr,target="_blank"),axis=1),
#    df_data.Adr.apply(lambda x: html.A(html.P(x[:5]+"..." +x[-4:]),href="https://opensea.io/accounts/"+x,target="_blank"))
#    )

link_names = "/"+df_data.Adr
  
df_data["Name"] = np.where(
    df_data["Name"].notnull(),
    df_data.apply(lambda x: html.A(html.P(x.Name),href="/"+x.Adr),axis=1),
    df_data.Adr.apply(lambda x: html.A(html.P(x[:5]+"..." +x[-4:]),href="/"+x))
    )

df_data.drop("Adr",inplace=True,axis=1)
df_data.columns = ['Rank', 'Name', 'Total', 'SuperRare', 'Foundation',
       'KnownOrigin', 'MakersPlace', 'ASYNC', 'First', 'Recent']

########### Initiate the app #######
app = dash.Dash(__name__,update_title=None)
server = app.server
app.title="Patrons of Culture"

"""
########### Content by Page #########
"""
#####################################
########### RANKINGS  ###############
#####################################
rankings = html.Div(className="rankingsPage",
    children=[
    #HEADER
    html.Div([
    
        html.Div(className="app-header",
             children=[
             
             html.A(html.H1('PATRONS OF CULTURE',
                    className="app-header--title",style={'color':'#723BC9'}),
                    href="/",
                    style={'text-decoration': 'none'}),
            
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
    html.H2("Aggregate Rankings:",style={
    "right":"280px",
    "color":"#723BC9"}),
    style={'color':'#04D9FF',"font-family":"NeueMachina-Regular"}
    ),
    
    html.Div(
    children=dbc.Table.from_dataframe(df_data, id="top-200-table",
                                  )
    ),
    
    #FOOTER
    html.Div(className="footer",
        children= [
        html.Br(),
        html.Div("©2021 Patrons of Culture. Designed by Kyle Waters & Jacob Zurita.",
                 id="footer-text"),
        html.Br()
    ]
            )
    ]
    )
    
#####################################
########### About  ##################
#####################################
about = html.Div(className="aboutPage",
    children=[
    html.Div([
    
        html.Div(className="app-header",
             children=[
             
             html.A(html.H1('PATRONS OF CULTURE',
                    className="app-header--title",style={'color':'#723BC9'}),
                    href="/",
                    style={'text-decoration': 'none'}),
            
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
    html.Div(className="about-section",
             children=[
                 html.H1("about", id="about-section-header"),
                 html.Div(id="about-section-content",
                          children=[
                 html.H3("Patrons of the new creative economy."),
                 html.H3("We are an analytics resource spotlighting the most prolific crypto art collectors who are supporting creativity and longevity in digital art.")
                 ]
                         ),
                         
    ]),
    #FOOTER
    html.Div(className="footer",
        children= [
        html.Br(),
        html.Div("©2021 Patrons of Culture. Designed by Kyle Waters & Jacob Zurita.",
                 id="footer-text"),
        html.Br()
    ]
            )
    ]
    )

#####################################
########### NEWSLETTER ##############
#####################################
newsletter = html.Div(className="newsletterPage",
    children=[
    html.Div([
    
    html.Div(className="app-header",
             children=[
             
             html.A(html.H1('PATRONS OF CULTURE',
                    className="app-header--title",style={'color':'#723BC9'}),
                    href="/",
                    style={'text-decoration': 'none'}),
            
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
    
    html.Div(className="Newsletter-content",
             children=[
    html.H5("Newsletter:",
            id="subscribe"),
    html.H5("Coming Soon",
            id="button-sub")]),
    #FOOTER
    html.Div(className="footer",
        children= [
        html.Br(),
        html.Div("©2021 Patrons of Culture. Designed by Kyle Waters & Jacob Zurita.",
                 id="footer-text"),
        html.Br()
    ]
            )
    ]
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

collector_0xf52393e120f918ffba50410b90a29b1f8250c879 = base_header

app.layout = html.Div([dcc.Location(id="url"), content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return rankings
    elif pathname == "/about":
        return about
    elif pathname == "/newsletter":
        return newsletter
    elif pathname in link_names.tolist():
        return collector_0xf52393e120f918ffba50410b90a29b1f8250c879
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...",style={"font-family":"NeueMachina-Regular"}),
        ]
    )                  
                     
if __name__ == '__main__':
    app.run_server()
      
