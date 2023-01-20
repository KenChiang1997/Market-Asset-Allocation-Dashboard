import numpy as np 
import pandas as pd 


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


def Region_Annualized_Risk_Return_Performance(stock_price_df):
    """
    # Calculate Annualized Performance Data
    """

    stock_return_df = stock_price_df.pct_change().mean().reset_index(name='AVG(Return)')
    stock_return_df['AVG(Return)'] = stock_return_df['AVG(Return)'] * 252

    stock_volatility_df = stock_price_df.pct_change().std().reset_index(name='Std(Return)')
    stock_volatility_df['Std(Return)'] = stock_volatility_df['Std(Return)'] * np.sqrt(252)

    stock_return_volatility_df = pd.merge(stock_return_df,stock_volatility_df,left_on='index',right_on='index')
    stock_return_volatility_df['Sharpe-Ratio'] = stock_return_volatility_df['AVG(Return)'] / stock_return_volatility_df['Std(Return)']
    
    return stock_return_volatility_df

def region_cumulative_return(stock_price_df):

    region_cumulative_return_by_year = stock_price_df.pct_change().to_period('y').reset_index().groupby('Date')[stock_price_df.columns].sum()
    region_cumulative_return_by_year.index = region_cumulative_return_by_year.index.astype('str')
    region_cumulative_return_by_year = region_cumulative_return_by_year.T

    region_cumulative_return_by_year = region_cumulative_return_by_year.sort_values(by=region_cumulative_return_by_year.columns[-1],ascending=False)
    
    return region_cumulative_return_by_year



def plot_region_yearly_return(plot_df):

    fig = px.imshow(plot_df, 
                    aspect="auto",
                    color_continuous_scale='RdBu_r',
                    text_auto='.2f',
                    )

    fig.update_layout(template = temp,
                    title='Region Index Daily Cumulative Return Yearly Performance - Sort By Current Year', 
                    hovermode = 'closest',
                    margin = dict(l=150, r=50, t=50, b=50),
                    height = 450, 
                    width = 1500, 
                    showlegend = True,

                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background'],
                    font_color=colors['text'])

    fig.update_xaxes(
        title = ' ',
        title_font_color = colors['text'],
        tickson="boundaries",
        ticklen=20
        )

    fig.update_yaxes(
        title_font_color = colors['text'],
        )

    fig.update_coloraxes(showscale=False)

    return fig 

def plot_correlation_matrix(plot_df):

    fig = px.imshow(plot_df, 
                    aspect="auto",
                    color_continuous_scale='RdBu_r',text_auto='.2f'
                    )

    fig.update_layout(template = temp,
                    title='Equity(Daily Return) Correlation Matrix - By Region', 
                    hovermode = 'closest',
                    margin = dict(l=150, r=150, t=50, b=50),
                    height = 450, 
                    width = 850, 
                    showlegend = True,

                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background'],
                    font_color=colors['text'])
    
    fig.update_xaxes(
        title_font_color = colors['text'],
        )
    
    fig.update_yaxes(
        title_font_color = colors['text'],
        )

    fig.update_coloraxes(showscale=False)

    return fig

def plot_equity_convex_hull(stock_return_volatility_df):

        fig = go.Figure() # hover text goes here

        for i in range(stock_return_volatility_df.shape[0]):

            fig.add_trace(
                        go.Scatter( 
                                x = [stock_return_volatility_df['Std(Return)'][i]],
                                y = [stock_return_volatility_df['AVG(Return)'][i]],
                                marker = dict(size=12,
                                                line=dict(width=2,color='DarkSlateGrey')
                                        ),
                                name = str(stock_return_volatility_df['index'][i]),
                                text = str(stock_return_volatility_df['index'][i]),)
                            )
                
            fig.add_annotation( x = stock_return_volatility_df['Std(Return)'][i],
                                y = stock_return_volatility_df['AVG(Return)'][i],
                                text = str(stock_return_volatility_df['index'][i]),
                                showarrow = True,
                                arrowhead=1 
                                )

        fig.update_layout(
                        template=temp,
                        title='Equity Convex Hull - By Region', 
                        hovermode='closest',
                        margin=dict(l=50, r=50, t=50, b=50),
                        height=450, 
                        width=600, 
                        showlegend=False,
                        
                        yaxis = dict(title="Annualize Return",
                        titlefont=dict(color=colors['text']),
                        tickfont=dict(color=colors['text'])),
                        xaxis = dict(title="Annualize Volatility"),

                        plot_bgcolor=colors['background'],
                        paper_bgcolor=colors['background'],
                        font_color=colors['text'],
                        )

        fig.update_xaxes(
                title_font_color = colors['text'],
                )

        fig.update_yaxes(
                title_font_color = colors['text'],
        )

        fig.update_traces(textposition='top center')

        return fig