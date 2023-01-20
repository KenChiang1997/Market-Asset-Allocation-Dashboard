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

def get_stock_price_data(tickers,start_date,end_date):
    """
    # Use yahoo API to get stock price data
    -----
    # Parameters Setting:
    tickers: List of "Stock Ticker"
    start_date: String Format of "yyyy-mm-dd"
    end_date: String Format of "yyyy-mm-dd"
    
    # Output:
    stock_price (datatype: pd.DataFrame)
    """
    ticks = yf.Tickers(tickers)
    stock_price = ticks.history(start=start_date, end=end_date).Close

    return stock_price


def plot_price_data(plot_df,title):

    fig = go.Figure()

    for ticker in plot_df.columns:
        
        if ticker in ["USA(SP500)"]:
            fig.add_trace(
            go.Scatter(x = plot_df.index,
                       y = plot_df[str(ticker)],
                       name = ticker,
                       yaxis="y2",
                       ))
        else:
            fig.add_trace(
            go.Scatter(x = plot_df.index,
                       y = plot_df[str(ticker)],
                       name = ticker))
    
    fig.update_layout(template = temp,
                      title = title,
                      hovermode = 'closest',
                      margin = dict(l=50, r=50, t=20, b=35),
                      height = 500, 
                      width = 1600, 
                      showlegend = True,
                      


                      yaxis = dict(title="Index_1(Others)",
                                   titlefont=dict(color=colors['text']),
                                   tickfont=dict(color=colors['text'])),
                    
                      yaxis2 = dict(title="Index_2(USA)",
                            titlefont=dict(color=colors['text']),
                            tickfont=dict(color=colors['text']),
                            overlaying="y", # specifyinfg y - axis has to be separated
                            side="right",), # specifying the side the axis should be present
                    
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
                                              dict(step="all") ]),),
            rangeslider = dict(visible=False),type="date",
            title_font_color = colors['text'],
            )
    
    fig.update_yaxes(
        title_font_color = colors['text'],
    )

    return fig
