"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
from util import get_data

def author():
    return 'zchen393'

def compute_portvals(order, symbol, start_val = 100000, commission=9.95, impact=0.005):
   
    start_date = order.index[0]
    end_date = order.index[-1]
    date = pd.date_range(start_date, end_date)
    stockvals = get_data([symbol], date).loc[:, [symbol]]
    order = order.loc[(order != 0).all(axis=1), :]  

    alloc = pd.DataFrame(0, index = stockvals.index, columns = ['Cash'] + [symbol])
    trade_date = alloc.shape[0]
    
    for td in range(0,trade_date):
        
        date_temp = alloc.index[td]
        execute_trade = order[order.index == date_temp]
        price_date = stockvals.iloc[stockvals.index == date_temp]
        
        if execute_trade.empty:
            alloc.iloc[td] = alloc.iloc[td]
        else:
            execute_deal = execute_trade.shape[0]
            for ed in range(0,execute_deal):
                share_temp = execute_trade['Order'].iloc[ed]
                alloc[symbol].iloc[td] = alloc[symbol].iloc[td] + share_temp
                alloc['Cash'].iloc[td] = alloc['Cash'].iloc[td] + (share_temp * price_date + commission + impact * abs(share_temp * price_date))[symbol].iloc[0]
                
    alloc = np.cumsum(alloc, 0)
    cash = start_val - alloc['Cash']
    daily_value = alloc[symbol] * stockvals[symbol]     
    portvals = cash + daily_value
    
    return portvals

