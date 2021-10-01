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
def update_fig_layout(fig, cm_logo_sizex=0.15, cm_logo_sizey=0.15, title:str=None, log:bool=False, log_y2:bool=False, show_legend=True, annotations:bool=True, annotation_x=-0.005, annotation_y=1.05, background_color:str='white', source:str='Coin Metrics', left_axis_format:str=None, number_of_yaxes:int=1, y_axis_range=None, y2_axis_range=None, show_ticks=True):
    
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
        sizex=cm_logo_sizex, sizey=cm_logo_sizey,
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
    
    df = df.iloc[3:]
    df["Number of Owners"] = df["num_owners"]
    df["Number of NFTs"] = df["num_tokens"]
    df["Number of NFTs per Owner"] = df["supply_concentration"]
    
    df_melt = df[["time","Number of Owners","Number of NFTs","Number of NFTs per Owner"]].melt(id_vars="time")
    df_melt.columns = ['time','stat','value']
    
    #owners
    owners_tokens = px.line(df_melt,
                  x='time',
                  y='value',
                  facet_col="stat",
                  color="stat")
    
    owners_tokens.layout.images = [dict(
    source='https://cdn.substack.com/image/fetch/w_96,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F4430351a-a92c-4505-8c8f-3822d76715df_256x256.png',
    xref="paper", yref="paper",
    x=1, y=1,
    sizex=0.15, sizey=0.15,
    xanchor="right", yanchor="bottom"
  )]
    owners_tokens.update_yaxes(matches=None, showticklabels=True, visible=True)
    owners_tokens.update_layout(
        title={
            'text': "{} Owner Stats".format(collection),
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

    owners_tokens = owners_tokens.update_xaxes(title_text="")
    owners_tokens = owners_tokens.update_yaxes(title_text="")
    owners_tokens.update_yaxes(matches=None, showticklabels=True, visible=True, gridwidth=1, gridcolor='#ECECED')
    owners_tokens.update_xaxes(matches=None, showticklabels=True, visible=True)
    owners_tokens.update_layout(font_family="NeueMachina-Regular",title_font_family="NeueMachina-Regular")
    
    ##### HODl waves
    url_github_active = "https://github.com/kyle-coinmetrics/PatronsOfCulture/blob/main/data/active_supply/{}_active_supply.csv?raw=True".format(collection_url)
    df_active_supply = pd.read_csv(url_github_active,engine='python')
    
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
    
    hodl_waves = make_subplots(specs=[[{"secondary_y": True}]])
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
    
    hodl_waves.add_traces(fig_.data)# + fig2.data)
    hodl_waves = update_fig_layout(hodl_waves, show_legend=True, title="{} HODL Waves".format(collection),annotations=True,left_axis_format="growth")
    hodl_waves = hodl_waves.update_layout(showlegend=True)
    hodl_waves.layout.showlegend = True
    hodl_waves.layout.yaxis2.type="log"
    hodl_waves.add_hline(y=0.5,line_dash="dash")
    hodl_waves.update_layout(font_family="NeueMachina-Regular",title_font_family="NeueMachina-Regular")
    
    ###### Sales
    url_github_active = "https://github.com/kyle-coinmetrics/PatronsOfCulture/blob/main/data/sales/{}.csv?raw=True".format(collection_url)
    df_sales = pd.read_csv(url_github_active,engine='python')
    
    eth_only_sales = df_sales.symbol.isin(["ETH","WETH"])
    above_0_eth    = (df_sales.total_price > 0 )
    df_sales_onlyETH = df_sales[eth_only_sales&above_0_eth].copy()
    vol_by_day = df_sales_onlyETH.groupby("date",as_index=False).total_price_USD.sum()
    
    fig = px.bar(vol_by_day, x='date', y='total_price_USD')
    fig = update_fig_layout(fig, annotations=True,source="Coin Metrics Reference Rates & OpenSea API",title="Daily CryptoPunks Volume (USD)")
    
    #update_fig_layout(fig, yaxis_title="USD Volume", extra_annotations=None, extra_source=" Reference Rates & OpenSea API", source_override=None)
    fig2 = px.line([],[])
    fig2.add_scatter(x=df_sales_onlyETH.timestamp_dt,y=df_sales_onlyETH.total_price_USD.rolling(500).mean(),marker=dict(color="skyblue"))
    fig2 = fig2.update_traces(yaxis="y2")
    
    vol_price = make_subplots(specs=[[{"secondary_y": True}]])
    vol_price.add_traces(fig.data + fig2.data)
    vol_price = update_fig_layout(vol_price,log=False, log_y2=False,annotations=True,title="{} Last 500 Sales Moving Average & Daily Volume".format(collection),source='Coin Metrics Reference Rates & OpenSea API')
    vol_price['layout']['yaxis'].update(tickprefix = '$')
    vol_price['layout']['yaxis2'].update(tickprefix = '$')
    vol_price.update_layout(showlegend=False,font_family="NeueMachina-Regular",title_font_family="NeueMachina-Regular")
    
    top10 = df_sales_onlyETH.sort_values("total_price_USD",ascending=False).head(10)
    top10_fig = px.line([],[])
    top10_fig.add_table(header=dict(values=["NFT","Date","USD Price","ETH Price"]),cells=dict(values=[top10.name, top10.date, round(top10.total_price_USD,0), round(top10.total_price,0)], format=["","","$,.9",",.9",""]))
    top10_fig = update_fig_layout(top10_fig,title="{} Top 10 Highest Sales".format(collection),annotations=True,source="Coin Metrics Reference Rates & OpenSea API")
    top10_fig.update_layout(font_family="NeueMachina-Regular",title_font_family="NeueMachina-Regular")
    
    ## Realized Cap
    url_github_active = "https://github.com/kyle-coinmetrics/PatronsOfCulture/blob/main/data/realized_cap/{}.csv?raw=True".format(collection_url)
    df_realized_cap = pd.read_csv(url_github_active,engine='python')
    df_realized_cap[df_realized_cap.columns[0]] =  pd.to_datetime(df_realized_cap[df_realized_cap.columns[0]])
    realized_cap = px.area(df_realized_cap,x=df_realized_cap.columns[0],y="Realized Cap")
    realized_cap = update_fig_layout(realized_cap, annotations=True,source="Coin Metrics Reference Rates & OpenSea API",title='{} Realized Cap (USD)'.format(collection),show_legend=False) 
    realized_cap.update_layout(yaxis_tickprefix = '$')
    realized_cap.for_each_trace(lambda trace: trace.update(fillcolor = trace.line.color))
    realized_cap.update_layout(font_family="NeueMachina-Regular",title_font_family="NeueMachina-Regular")
    
    ## Headline Statistics
    realized_cap_recent    = df_realized_cap["Realized Cap"].iloc[-1]
    vol_last_30_days = vol_by_day.tail(30).total_price_USD.sum()
    unique_owners_recent    = df["Number of Owners"].iloc[-1] 
    cumulative_vol = vol_by_day.total_price_USD.sum()
    
    headline = px.line([],[],height=70)
    headline.add_table(header=dict(values=["Realized Cap","Unique Owners","USD Volume (30 Days)","USD Volume (All Time)"],height=40),cells=dict(values=[round(realized_cap_recent,0),unique_owners_recent,round(vol_last_30_days,0),round(cumulative_vol,0)], height=40,format=["$,",",","$,","$,"]))
    headline.update_layout(paper_bgcolor="white",plot_bgcolor="white",font=dict(size=22),font_family="NeueMachina-Regular",title_font_family="NeueMachina-Regular",    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ))
    
    return owners_tokens,hodl_waves,vol_price,realized_cap,top10_fig,headline

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
                    children=[html.A(
                        html.Div("An NFT Analytics Resource from Coin Metrics", id="app-header--about"),
                        )
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
    html.Div(
        dcc.Dropdown(
        id='collection',
        placeholder="Select an NFT project",
        options=[{'label': k, 'value': k} for k in projects],
        multi=False
    )),
html.Div(children=[
    
    dcc.Graph(
        id="headline_stats"),
    dcc.Graph(
        id='analytics'),
    dcc.Graph(
        id='hodl_waves'),
    dcc.Graph(
        id='realized_cap'),
    dcc.Graph(
        id='vol_avg_price'),
    dcc.Graph(
        id='10highest_sales')],
    ),
    footer
    ]
    )

########### Set up the base layout ###############
app.layout = rankings

@app.callback(
    [Output('analytics', 'figure'),
     Output('hodl_waves', 'figure'),
     Output('vol_avg_price', 'figure'),
     Output('realized_cap', 'figure'),
     Output('10highest_sales', 'figure'),
     Output('headline_stats', 'figure')],
    [Input(component_id='collection', component_property='value')]
)

def update_graphs(collection):
    return get_graphs(collection)                
                     
if __name__ == '__main__':
    app.run_server()
      
