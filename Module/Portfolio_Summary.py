import numpy as np
import pandas as pd 

class Portfolio_Summary():

    def Annual_Return(Daily_Returns):
        
        return np.mean(Daily_Returns) * 252

    def Annual_Volitiliy(Daily_Returns):

        return np.std(Daily_Returns) * np.sqrt(252)

    def Cumulative_Return(Daily_Returns):

        return np.cumsum(Daily_Returns)[-1]

    def Sharpe_Ratio(Daily_Returns):

        u = np.mean(Daily_Returns) * 252
        sigma = np.std(Daily_Returns) * np.sqrt(252)

        sharpe_ratio = u/sigma

        return sharpe_ratio
        
    def Maximun_drawdown(Daily_Returns):

        max_drawdown = max(pd.Series(np.cumsum(Daily_Returns)).cummax().values - np.cumsum(Daily_Returns))
        
        return max_drawdown

    def Calmar_Ratio(Daily_Returns):

        u = np.mean(Daily_Returns) * 252
        max_drawdown = max(pd.Series(np.cumsum(Daily_Returns)).cummax().values - np.cumsum(Daily_Returns))

        Calmar_Ratio = u/max_drawdown

        return Calmar_Ratio

    def Omega_Ratio(Daily_Returns,benchmark):

        Number_of_Win = len(np.where(Daily_Returns - benchmark > 0)[0])
        Number_of_Loss = len( np.where(Daily_Returns - benchmark < 0)[0])

        return Number_of_Win / Number_of_Loss

    def Sortino_Ratio(Daily_Returns,benchmark):

        Adjusted_Return = np.mean(Daily_Returns - benchmark) * 252
        benchmark_std   = np.std(benchmark) * np.sqrt(252)
        Sortino_Ratio   = Adjusted_Return / benchmark_std

        return Sortino_Ratio 

    def Value_at_Risk(Daily_Returns,confidence_level=0.95):

        type_1 = 1 - confidence_level
        var    = np.quantile(Daily_Returns,type_1)
            
        return  var


def Backtest_Summay_DF(start_date,end_date,Daily_Returns,Benchmark=None,Benchmark_Returns=None):

    if Benchmark==True:

        BackTesint_Summary_Df = pd.DataFrame({

            "Start Date"        : [start_date] , 
            "End   Date"        : [end_date]   , 
            "-"                 : ["-"] ,
            "Annual Return"     : [Portfolio_Summary.Annual_Return(Daily_Returns)]         , 
            "Annual Volitiliy"  : [Portfolio_Summary.Annual_Volitiliy(Daily_Returns)]      , 
            "Cumulative Return" : [Portfolio_Summary.Cumulative_Return(Daily_Returns)]     ,
            "Sharpe Ratio"      : [Portfolio_Summary.Sharpe_Ratio(Daily_Returns)]          ,
            "Calmar Ratio"      : [Portfolio_Summary.Calmar_Ratio(Daily_Returns)]          ,

            "Omega Ratio"       : [Portfolio_Summary.Omega_Ratio(Daily_Returns,Benchmark_Returns)]           ,
            "Sortino Ratio"     : [Portfolio_Summary.Sortino_Ratio(Daily_Returns,Benchmark_Returns)]         ,

            "Daily Value at Risk"   : [ Portfolio_Summary.Value_at_Risk(Daily_Returns,confidence_level=0.95)    ]     ,
            "Maximum Drawdown"      : [ Portfolio_Summary.Maximun_drawdown(Daily_Returns)]                            ,
            

        },index=["Model Result"])
    
    else :
        
        BackTesint_Summary_Df = pd.DataFrame({

            "Start Date"        : [start_date] , 
            "End   Date"        : [end_date]   , 
            "-"                 : ["-"] ,
            "Annual Return"     : [Portfolio_Summary.Annual_Return(Daily_Returns)]         , 
            "Annual Volitiliy"  : [Portfolio_Summary.Annual_Volitiliy(Daily_Returns)]      , 
            "Cumulative Return" : [Portfolio_Summary.Cumulative_Return(Daily_Returns)]     ,
            "Sharpe Ratio"      : [Portfolio_Summary.Sharpe_Ratio(Daily_Returns)]          ,
            "Calmar Ratio"      : [Portfolio_Summary.Calmar_Ratio(Daily_Returns)]          ,
            "Daily Value at Risk"   : [ Portfolio_Summary.Value_at_Risk(Daily_Returns,confidence_level=0.95)    ]     ,
            "Maximum Drawdown"      : [ Portfolio_Summary.Maximun_drawdown(Daily_Returns)]                            ,
            

        },index=["Backtest"])



    return  BackTesint_Summary_Df.T