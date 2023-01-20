import time
import numpy as np 
import pandas as pd
import datetime as dt
import yfinance as yf 

# Dash
import dash
from dash import dcc,html
from dash import Dash,Input, Output

# Pratice Ploty
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode


temp = dict(layout=go.Layout(font=dict(family="Franklin Gothic", size=12), width=800))

colors = {'background': '#111111',
          'text': '#7FDBFF'}


def Construct_Drawdown(Historical_Values,Variable_Name,DataFrame_Index,Max_Unit):
    """
    # Maximum Drawdown 定義:
    --------------------------
    程式交易中有許多數值來評價一個 策略的特性或表現，其中一個重要的數值 MDD (Max Drawdown) 也稱作 "最大回撤" 或 "最大跌幅" 。
    # Definition from Wikipedia:
    --------------------------
    The drawdown is the measure of the decline from a historical peak in some variable.
    (typically the cumulative profit or total open equity of a financial trading strategy)
    # Parameters Setting:
    --------------------------
    Input_Variable: 
    1.)  Historical values of "one" variable (Astype: List) 
    2.)  Variable Name (Astype: String) 
    3.)  Index for DataFrame --> Daily/Weekly/Monthly/Quarterly (Astype: List) 
    \\
    Output_Variable: 
    Maximum Drawdown Table (Astype: Pandas-DataFrame)
    """

    # Set up Parameters
    drawdown_df = pd.DataFrame()
    peak_values = [ Historical_Values[0] ]
    drawdown_values = [] 

    drawdown_duration = []
    drawdown_day = 0
    count_drawdown_duration = 0

    # Loop over the index range ( record historical peak date and construct maximun drawdown )
    for i in range(len(Historical_Values)):

        # compare wheather current peak values is bigger than the previous one , append the bigger one into the list.
        previous_peak_value = peak_values[i]
        current_value = Historical_Values[i]

        if drawdown_day >= Max_Unit:
            update_peak_value = current_value
        else:
            update_peak_value = max(previous_peak_value , current_value)
        
        peak_values.append( update_peak_value )  
        # lastest peak minus current equity values = current drawdown
        drawdown_values.append( update_peak_value - current_value ) 

        # drawdown duration 
        if update_peak_value - current_value == 0:
            drawdown_day = 0
            count_drawdown_duration += 1
            drawdown_duration.append(count_drawdown_duration)
        else:
            drawdown_day += 1
            # count_drawdown_duration +=1
            drawdown_duration.append(count_drawdown_duration)


    drawdown_df[str(Variable_Name)] = Historical_Values
    drawdown_df['Peak Values'] = peak_values[1:] # drop the first inital values
    drawdown_df['Drawdown Values'] = drawdown_values
    drawdown_df['Drawdown_Period_ID'] = drawdown_duration 
    drawdown_df.index = DataFrame_Index

    return drawdown_df

def get_region_drawdown_df(stock_price_df):

    Region_Drawdown_df = pd.DataFrame()

    for cols in stock_price_df.columns:

        drawdown_df = Construct_Drawdown(Historical_Values = stock_price_df[cols].pct_change().cumsum(),
                                         Variable_Name = cols,
                                         DataFrame_Index = stock_price_df.index,
                                         Max_Unit = 1080)

        Region_Drawdown_df[str(cols)] = drawdown_df['Drawdown Values']

    return Region_Drawdown_df


def plot_region_underwater(plot_df):

    fig = go.Figure()

    for ticker in plot_df.columns:
        fig.add_trace(
            go.Scatter(x = plot_df.index,
                       y = plot_df[str(ticker)],
                       name = ticker))
    
    fig.update_layout(template = temp,
                      title = 'Region Cumulative Return Underwater Plot',
                      hovermode = 'closest',
                      margin = dict(l=50, r=50, t=20, b=20),
                      height = 350, 
                      width = 1600, 
                      showlegend = True,

                      yaxis = dict(title="Maximum Drawdown",
                                   titlefont=dict(color=colors['text']),
                                   tickfont=dict(color=colors['text'])),
                                
                     plot_bgcolor=colors['background'],
                     paper_bgcolor=colors['background'],
                     font_color=colors['text'],
                     xaxis_rangeselector_font_color='black',
                     xaxis_rangeselector_activecolor='red',
                     xaxis_rangeselector_bgcolor='green',
                      )

    fig.update_xaxes(
            rangeselector = dict(buttons=list([ 
                                              dict(count=7,label="1w",step="day",stepmode="backward"),
                                              dict(count=1,label="1m",step="month",stepmode="backward"),
                                              dict(count=3,label="3m",step="month",stepmode="backward"),
                                              dict(count=6,label="6m",step="month",stepmode="backward"),
                                              dict(count=1,label="1y",step="year",stepmode="backward"),
                                              dict(count=2,label="2y",step="year",stepmode="backward"),
                                              dict(step="all") ]) ),
            rangeslider = dict(visible=False),type="date",
            title_font_color = colors['text'],
            )
        
    fig.update_yaxes(
        title_font_color = colors['text'],
        )
    return fig