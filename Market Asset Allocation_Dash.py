import time
import numpy as np 
import pandas as pd
import datetime as dt
import yfinance as yf 

# Dash
import dash
from dash import dcc,html
from dash import Dash,Input, Output,dash_table

# Pratice Ploty
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode
temp = dict(layout=go.Layout(font=dict(family="Franklin Gothic", size=12), width=800))
colors = {'background': '#111111','text': '#7FDBFF'}

# Self-Built Module
from Module.Yahoo_API_Price import get_stock_price_data,plot_price_data
from Module.Drawdown import get_region_drawdown_df,plot_region_underwater
from Module.Return_Performance import Region_Annualized_Risk_Return_Performance,region_cumulative_return
from Module.Optimization_Algorithm import Long_Only_Markowitz_Optimization,Plot_Asset_Allocation_Pie_Chart
from Module.Portfolio_Summary import Backtest_Summay_DF


# Plotly Module Figure
from Module.Return_Performance import plot_correlation_matrix,plot_equity_convex_hull,plot_region_yearly_return


# ----- Parameters Setting ---------

start_date = '2000-01-01'
end_date = str(dt.datetime.today())[:10]

tickers = ["^GSPC",  # USA
            "^NSEI",  # India
            "^N225",  # Japan
            "^HSI",   # Hong Kong
            "^TWII"]    # Taiwan

Index_Dict = {"^GSPC":"USA(SP500)",  # USA
            "^NSEI":"Index(Nifty50)",  # India
            "^N225":"Japan(Nikkei 225)",  # Japan
            "^HSI":"Hong Kong(Hang Seng)",   # Hong Kong
            "^STOXX":"Europe(Europe 600)", # Eurpoe
            "IMOEX.ME":"Russia(MOEX Russia Index)", # Russia
            "^TWII":"Taiwan(Taiwan Weighted)"}


# -------- Back-End ----------

# Index Total Return INdex
stock_price_df = get_stock_price_data(tickers,start_date,end_date)
stock_price_df.columns = stock_price_df.columns.map(Index_Dict)
daterange = stock_price_df.index

# Region Drawdown 
Region_Drawdown_df = get_region_drawdown_df(stock_price_df)
Region_Drawdown_df

# Index Correlation Matrix
index_correlation_df = stock_price_df.pct_change().corr()

# Reutrn/Volatility Performance
stock_return_volatility_df = Region_Annualized_Risk_Return_Performance(stock_price_df)
stock_yearly_performance_df = region_cumulative_return(stock_price_df)


# Yearly Performance
Index_Year_Performance = stock_price_df.pct_change().to_period('Y').reset_index().groupby('Date')[stock_price_df.columns].sum().T
Index_Year_Performance = Index_Year_Performance.sort_values(by='2022',ascending=True)



# Mean-Variance Optimization
stock_return_df = stock_price_df.pct_change()[1:].dropna(axis=0) # Only include data with all markets are open.
stock_cov_matrix = stock_return_df.cov()

annualized_stock_cov_matrix = stock_cov_matrix.values * np.sqrt(252)
annualized_stock_expected_return_matrix = stock_return_df.mean(axis=0).values * 252 


Objective_Function = Long_Only_Markowitz_Optimization(annualized_stock_expected_return_matrix,annualized_stock_cov_matrix)
Asset_Weights = pd.DataFrame(np.round(Objective_Function.optimization()['x'],decimals=4),index=stock_return_df.columns,columns=['Asset Weights']).reset_index()
Asset_Weights.columns = ['Asset','Weight']

# Portfolio BackTesting
Portfolio_Performance = pd.DataFrame()
Portfolio_Performance['Benchmark Portfolio(SP500)'] = (stock_return_df['USA(SP500)'] + 1).cumprod() * 100
Portfolio_Performance['Mean-Variance Model Portfolio'] = ((stock_return_df @ Asset_Weights['Weight'].values).values + 1).cumprod() * 100

# Summary Resault
BT_Summary_Result = Backtest_Summay_DF( start_date = start_date,
                    end_date = end_date,
                    Daily_Returns = (stock_return_df @ Asset_Weights['Weight'].values).values,
                    Benchmark = True,
                    Benchmark_Returns = stock_return_df['USA(SP500)'].values)


# -------- Front-End ----------

stock_price_fig = plot_price_data(stock_price_df,title='Different Markets Index Overview')
stock_region_underwater_fig =  plot_region_underwater(Region_Drawdown_df*-1)

stock_correlation_fig = plot_correlation_matrix(index_correlation_df)
stock_convex_hull_fig = plot_equity_convex_hull(stock_return_volatility_df)
stock_yearly_performacne_fig =  plot_region_yearly_return(stock_yearly_performance_df )

asset_allocation_pie_chart = Plot_Asset_Allocation_Pie_Chart(Asset_Weights[Asset_Weights['Weight']!=0])
model_backtesting_result_fig = plot_price_data(Portfolio_Performance,title='In-Sample Period Result')


# --- Dash APP Layout ---

app = dash.Dash(__name__)

# Main App Layouy
app.layout = html.Div(
                style = {'backgroundColor': colors['background']},
                children = [
                        # Index Price Overview
                        html.Div([
                                html.H1(children = "Stock Market Analysis - Price Overall Outlook", style={'textAlign': 'center','color': colors['text'],'text-align': 'left'}),
                                dcc.Graph(
                                    id = 'Stock_Price_Data_Fig',
                                    figure = stock_price_fig
                                    ),
                                dcc.Graph(
                                    id = 'Stock_Underwater_Fig',
                                    figure = stock_region_underwater_fig
                                    ),
                                ]),
                
                        # Index Return Performance
                        html.Div(children=[
                                html.H1(children = "Stock Market Analysis - Index Return/Volatility Comparison",style={'textAlign': 'center','color': colors['text'],'text-align': 'left'}),
                                html.Div(children = [
                                                dcc.Graph(
                                                    id = 'yearly perfromance',
                                                    figure = stock_yearly_performacne_fig,
                                                )
                                                        ]),
                                html.Div(children = [
                                                dcc.Graph(
                                                    id = 'Index_Correlation',
                                                    figure = stock_correlation_fig,
                                                    style={'display': 'inline-block'}
                                                    ),
                                                dcc.Graph(
                                                    id = 'Index Region Risk/Return Performance',
                                                    figure = stock_convex_hull_fig,
                                                    style={'display': 'inline-block'}
                                                    ),
                                                ]),
                                ]),
                        
                        
                        # Mean-Variance Model
                        html.Div([
                                html.H1(children = "Morden Portfolio Theory - Mean-Variance Optimization", style={'textAlign': 'center','color': colors['text'],'text-align': 'left'}),

                                dcc.Graph(
                                        id = 'BackTesting',
                                        figure = model_backtesting_result_fig,
                                        style = {'display': 'inline-block'}
                                        ),
                                
                                html.Div(children = [
                                            dcc.Graph(
                                                    id = 'Asset_Allocation',
                                                    figure = asset_allocation_pie_chart,
                                                    style = {'display': 'inline-block'}
                                                    ),

                                            dash_table.DataTable(
                                                    data = BT_Summary_Result.reset_index().to_dict('records'),
                                                    columns = [{'id': c, 'name': c} for c in BT_Summary_Result.reset_index().columns],
                                                    style_as_list_view=True,
                                                    style_cell={'textAlign': 'left'},
                                                    style_cell_conditional=[
                                                                            {'if': {'column_id': 'Region'},
                                                                            'textAlign': 'left',
                                                                            'width': '400px'
                                                                            }],
                                                    style_header={
                                                        'backgroundColor': colors['background'],
                                                        'color': colors['text'],
                                                        'fontWeight': 'bold'
                                                        },
                                                    style_data={
                                                            'backgroundColor': colors['background'],
                                                            'color': colors['text'],
                                                            'whiteSpace': 'normal',
                                                            'width': '300px'
                                                        },
                                                    fill_width=False
                                                    ),
                                            
                                        ],style={'display': 'flex'}),
                                ]),
                        
                        ],
                )


if __name__ == "__main__":
    app.run_server(debug=True)


