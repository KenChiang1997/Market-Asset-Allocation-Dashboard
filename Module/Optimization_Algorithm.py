import numpy as np 
from scipy.optimize import minimize

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode
temp = dict(layout=go.Layout(font=dict(family="Franklin Gothic", size=12), width=800))
colors = {'background': '#111111',
          'text': '#7FDBFF'}

class Long_Only_Markowitz_Optimization():

    def __init__(self,returns_matrix,cov_matrix):

        self.initial_weight = np.zeros((cov_matrix.shape[0], 1)) # setting expected portfolio return and the tolerate portfolio variance
        self.bounds         = [(0,0.4) for i in range(cov_matrix.shape[0])]   # can't short stock
        self.cov            = cov_matrix
        self.ret            = returns_matrix
    
    def objective_function(self,w) :  # portfolio Shrape Ratio --> maximize

        w_tp           = w.transpose()
        portfolio_risk = w_tp @ self.cov @ w
        portfolio_return = w_tp @ self.ret
        
        return -(portfolio_return - (1/2) * portfolio_risk)

    def equality_constraint(self,w) : # weight sum = 1

        return 1 - np.sum(w)
    
    def optimization(self):

        constraint_1 = {'type': 'eq','fun':  self.equality_constraint} # weight sum = 1
        constraint   = [constraint_1]
        
        result = minimize(self.objective_function,self.initial_weight, method='SLSQP', bounds=self.bounds , constraints=constraint)
            
        return result
    

def Plot_Asset_Allocation_Pie_Chart(Asset_Weights):

    fig = go.Figure(data=[go.Pie(labels=Asset_Weights['Asset'], values=Asset_Weights['Weight'], textinfo='label+percent',
                                insidetextorientation='radial'
                                )])

    fig.update_layout(template = temp,
                    title='Mean-Variance Optimization Result', 
                    hovermode = 'closest',
                    margin = dict(l=150, r=50, t=50, b=50),
                    height = 450, 
                    width = 650, 
                    showlegend = True,

                    plot_bgcolor=colors['background'],
                    paper_bgcolor=colors['background'],
                    font_color=colors['text'])
    
    return fig 