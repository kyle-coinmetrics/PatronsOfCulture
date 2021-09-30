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
import plotly.express as px
from plotly.subplots import make_subplots

#Functions
def update_fig_layout(fig, title:str=None, log:bool=False, log_y2:bool=False, show_legend=True, annotations:bool=True, annotation_x=-0.04, annotation_y=1.03, background_color:str='white', source:str='Coin Metrics', left_axis_format:str=None, number_of_yaxes:int=1, y_axis_range=None, y2_axis_range=None, show_ticks=True):
    
    _annotations = [{
        'text': f"Source: {source}",
        'font': {
            'size': 14,
            'color': 'black',
        },
        'showarrow': False,
        'align': 'left',
        'valign': 'top',
        'x': annotation_x,
        'y': annotation_y,
        'xref': 'paper',
        'yref': 'paper',
    }]
    background_color = background_color
    
    fig.layout.images = [dict(
        source='https://cdn.substack.com/image/fetch/w_96,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F4430351a-a92c-4505-8c8f-3822d76715df_256x256.png',
        xref="paper", yref="paper",
        x=1, y=1,
        sizex=0.15, sizey=0.15,
        xanchor="right", yanchor="bottom"
      )]
    
    fig.update_layout(
        title={
            'text': title,
            'font': {
                'family': 'Roboto',
                'size': 24
            }
        },
        font = {
            'family': 'Roboto'
        },
        xaxis_showgrid=False,
        yaxis_showgrid=True,
        showlegend= show_legend,
        xaxis = {
            'title': ''
        },
        yaxis = {
            'type': 'log' if log == True else 'linear',
            'title': None,
            'gridcolor': '#ECECED'
        },
        yaxis2 = {
            'type': 'log' if log_y2 == True else 'linear',
            'overlaying': 'y',
            'side': 'right'
        },
        paper_bgcolor = background_color,
        plot_bgcolor = background_color,
        legend= {
            'bgcolor': background_color, 
            'xanchor': 'center',
            'yanchor': 'top',
            'x': .5,
            'y': -.1,
            'orientation': 'h'
        },
        annotations= _annotations if annotations == True else None
    )
    
    if y_axis_range != None:
        fig.update_layout(
            yaxis={'range': y_axis_range}
        )

    if y2_axis_range != None:
        fig.update_layout(
            yaxis={'range': y_axis_range}
        )

    if number_of_yaxes > 1:
        # y_args = {f'yaxis{i + 1}':{'showgrid': True, 'gridwidth':1, 'gridcolor':'LightGray'} for i in range(number_of_yaxes)}
        # fig.update_layout(**y_args)
        y_args = {f'yaxis{i + 1}':{'showgrid': True, 'gridwidth':1, 'gridcolor':'LightGray', 'zeroline':False, 'zerolinewidth':1, 'zerolinecolor': '#000000'} for i in range(number_of_yaxes)}
        fig.update_layout(**y_args)

    if show_ticks == False:
        args = {f'yaxis{i + 1}':{'showticklabels': False} for i in range(number_of_yaxes)}
        fig.update_layout(**args)
        args = {f'xaxis{i + 1}':{'showticklabels': False} for i in range(number_of_yaxes)}
        fig.update_layout(**args)


    if left_axis_format == 'percentage':
        args = {f'yaxis{i + 1}':{'ticksuffix': '%', 'side': 'left'} for i in range(number_of_yaxes)}
        fig.update_layout(**args)

    if left_axis_format == 'growth':
        fig.update_layout(
            yaxis = {'tickformat': ',.0%', 'side': 'left'},
            )

    if left_axis_format == 'dollars':
        args = {f'yaxis{i+ 1}':{'tickprefix': '$', 'side': 'left'} for i in range(number_of_yaxes)}
        fig.update_layout(**args)

    return fig

def get_graphs(collection):
    
    collection_url=collection.replace(" ","%20")
    url_github_data = "https://github.com/kyle-coinmetrics/PatronsOfCulture/blob/main/data/owners_token_count/{}_owners_tokens.csv?raw=True".format(collection_url)
    
    df = pd.read_csv(url_github_data)
    df['time'] = pd.to_datetime(df.time)
    df["Number of Owners"] = df["num_owners"]
    df["Number of NFTs"] = df["num_tokens"]
    df["Number of NFTs per Owner"] = df["supply_concentration"]
    
    df = df[["time","Number of Owners","Number of NFTs","Number of NFTs per Owner"]].melt(id_vars="time")
    df.columns = ['time','stat','value']
    
    #owners
    fig = px.line(df,
                  x='time',
                  y='value',
                  facet_col="stat",
                  color="stat")
    
    fig.layout.images = [dict(
    source='https://cdn.substack.com/image/fetch/w_96,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F4430351a-a92c-4505-8c8f-3822d76715df_256x256.png',
    xref="paper", yref="paper",
    x=1, y=1,
    xanchor="right", yanchor="bottom"
  )]
    fig.update_yaxes(matches=None, showticklabels=True, visible=True)
    
    fig.update_layout(
        title={
            'text': "{}".format(collection),
            'font': {
                'family': 'Roboto',
                'size': 24
            }
        },
        font = {
            'family': 'Roboto'
        },
        plot_bgcolor = 'white',
        paper_bgcolor="white",
        yaxis_showgrid=True)

    fig = fig.update_xaxes(title_text="")
    fig = fig.update_yaxes(title_text="")
    fig.update_yaxes(matches=None, showticklabels=True, visible=True, gridwidth=1, gridcolor='#ECECED')
    fig.update_xaxes(matches=None, showticklabels=True, visible=True)
    
    ##### HODl waves
    url_github_active = "https://github.com/kyle-coinmetrics/PatronsOfCulture/blob/main/data/active_supply/{}_active_supply.csv?raw=True".format(collection_url)
    df_active_supply = pd.read_csv(url_github_active,engine='python')
    
    df_active_supply.columns = ['Unnamed: 0', 'Never Moved', '2+ Years', '1-2 Years',
       '6 Months - 1 Year', '3 Months - 6 Months', '1 Month - 3 Months',
       '1 Week - 1 Month', '< 1 Week']
    df_active_supply[df_active_supply.columns[0]] = pd.to_datetime(df_active_supply[df_active_supply.columns[0]])
    df_active_supply.index = df_active_supply[df_active_supply.columns[0]]
    df_active_supply.drop(df_active_supply.columns[0],axis=1,inplace=True)
    
    color_discrete_map = {'< 1 Week':"darkred", 
                      '1 Week - 1 Month':"red", 
                      '1 Month - 3 Months':'darkorange',
                      '3 Months - 6 Months':'lightblue', 
                      '6 Months - 1 Year':'royalblue', 
                      '1-2 Years':'blue', 
                      '2+ Years':'darkblue',
                      'Never Moved':'purple'}
    
    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig_ = px.area(df_active_supply,color_discrete_map=color_discrete_map)
    fig_ = update_fig_layout(fig_,source="",left_axis_format="growth")
    fig_.update_layout(
        legend_title="")
    #fig.for_each_trace(lambda trace: trace.update(fillcolor = trace.line.color))
    fig_.add_hline(y=0.5,line_dash="dash")
    fig_.for_each_trace(lambda trace: trace.update(line={"width":0.01}))
    #fig.update_xaxes(range=[datetime(2018,4,6),datetime(2021,9,15)])
    
    #fig2 = px.line([],[])
    #fig2 = fig2.add_scatter(x=punk_MA_price.timestamp, y=punk_MA_price["500saleMA"],marker=dict(color="black"),name="Price: 500 Sales Moving Average ($, log scale RHS)",showlegend=True)
    #fig2.update_traces(yaxis="y2",showlegend=True)
    
    subfig.add_traces(fig_.data)# + fig2.data)
    subfig = update_fig_layout(subfig, show_legend=True, title="{} HODL Waves".format(collection),source="",left_axis_format="growth")
    subfig = subfig.update_layout(showlegend=True)
    subfig.layout.showlegend = True
    subfig.layout.yaxis2.type="log"
    subfig.add_hline(y=0.5,line_dash="dash")
 
    return fig,subfig

########### Initiate the app #######
app = dash.Dash(__name__)
server = app.server
app.title="jpegstats.io"

projects = ["CryptoPunks","SuperRare","Foundation","MakersPlace","Loot","Pudgy Penguins"]

"""
########### Content by Page #########
"""

base_header = html.Div([
    
        html.Div(className="app-header",
             children=[
             
             html.A(html.H1('JPEGstats.io',
                    className="app-header--title",style={'color':'#161823'}),
                    style={'text-decoration': 'none'}),
             html.Div(
                    children=[
                        html.Img(src='https://coinmetrics.io/wp-content/uploads/2020/12/coinmetrics-logo@2x.png',id="app-header--about")
                        ]
                    )
             
            ]
            )
                ],
    style={"font-family":"NeueMachina-Regular"}
    )
#FOOTER
footer = html.Div(className="footer",
        children= [
            html.Br(),
            html.Div("©2021",
                 id="footer-text"),
            html.Br()
                    ]
                )
#####################################
########### RANKINGS  ###############
#####################################
rankings = html.Div(className="rankingsPage",
    children=[
    base_header,
    #RANKINGS TABLE
    html.Div(
        dcc.Dropdown(
        id='collection',
        placeholder="Select an NFT collection",
        options=[{'label': k, 'value': k} for k in projects],
        multi=False
    ),
        ),
html.Div(children=[
    
    dcc.Graph(
        id='analytics'),
    dcc.Graph(
        id='hodl_waves')]
    ),
    footer
    ]
    )

########### Set up the base layout ###############
app.layout = rankings

@app.callback(
    [Output('analytics', 'figure'),
     Output('hodl_waves', 'figure')],
    [Input(component_id='collection', component_property='value')]
)

def update_graphs(collection):
    return get_graphs(collection)                
                     
if __name__ == '__main__':
    app.run_server()
      
