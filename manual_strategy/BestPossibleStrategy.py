"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
import datetime as dt
import marketsimcode as msc
from util import get_data
import matplotlib.pyplot as plt

def author():
    return 'zchen393'

def testPolicy(symbol = 'JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    
    date = pd.date_range(sd, ed)
    stockvals = get_data([symbol], date)[symbol]
    
    bps = pd.DataFrame(0, index = stockvals.index, columns = ['Order'])
    Diff = np.diff(stockvals)
    trade_date = bps.shape[0]
    
    for td in range(0,trade_date):
        
        if td+1 < trade_date:
            sign = np.sign(Diff[td])
            
            if td == 0:
                bps['Order'].iloc[td] = sign * 1000
            else:
                position = np.cumsum(bps['Order'].iloc[0:td])[-1]
                bps['Order'].iloc[td] = int(sign * np.sign(position) == -1) * sign * 2000
                
        else:
            position = np.cumsum(bps['Order'].iloc[0:td])[-1]
            bps['Order'].iloc[td] = -position
            
    return bps

def portstats(dailyvals):
    
    daily_return = dailyvals/dailyvals.shift(1)-1
    daily_return = daily_return.dropna()
    
    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr = dailyvals.iloc[-1]/dailyvals.iloc[0] - 1
    adr = daily_return.mean()
    sddr = daily_return.std() 
    
    return cr, adr, sddr


def main():
    
    symbol = 'JPM'
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    sv = 100000
    
    date = pd.date_range(sd, ed)
    stockvals = get_data([symbol], date)
    
    Benchmark = pd.DataFrame(0, index = stockvals.index[[0,-1]], columns = ['Order'])
    Benchmark['Order'].iloc[0] = 1000
    Benchmark['Order'].iloc[-1] = -1000
    
    BPS = testPolicy(symbol = 'JPM', sd = sd, ed = ed, sv = sv)
    
    daily_value_benchmark = msc.compute_portvals(order = Benchmark, symbol = 'JPM', start_val = sv, commission=0, impact=0)/sv
    daily_value_bps = msc.compute_portvals(order = BPS, symbol = 'JPM', start_val = sv, commission=0, impact=0)/sv
    
    cr_benchmark, adr_benchmark, sddr_benchmark = portstats(daily_value_benchmark)
    cr_bps, adr_bps, sddr_bps = portstats(daily_value_bps)
    
    plt.figure(figsize=(20,5))
    plt.plot(daily_value_benchmark.index, daily_value_benchmark, label = "Benchmark", color = "Blue")
    plt.plot(daily_value_bps.index,daily_value_bps, label = "Best Possible Strategy", color = "Black")
    plt.title("Best Possible Strategy vs Benchmark")
    plt.xlabel("Date")
    plt.legend()
    plt.show()

    return cr_benchmark, adr_benchmark, sddr_benchmark, cr_bps, adr_bps, sddr_bps