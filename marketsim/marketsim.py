"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import matplotlib.pyplot as plt

def author():
    return 'zchen393'

def compute_portvals(orders_file = "./orders/orders-10.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    
    order = pd.read_csv(orders_file, index_col = 'Date', parse_dates = True, na_values=['nan'])
    start_date = order.index[0]
    end_date = order.index[-1]
    date = pd.date_range(start_date, end_date)
    syms = list(order['Symbol'].unique())
    stockvals = get_data(syms, date)
    stockvals = stockvals[syms]

    alloc = pd.DataFrame(0, index = stockvals.index, columns = ['Cash'] + syms)
    
    trade_date = alloc.shape[0]
    
    for td in range(0,trade_date):
        
        date_temp = alloc.index[td]
        execute_trade = order[order.index == date_temp]
        price_date = stockvals[stockvals.index == date_temp]
        
        if execute_trade.empty:
            alloc.iloc[td] = alloc.iloc[td]
        else:
            execute_deal = execute_trade.shape[0]
            for ed in range(0,execute_deal):
                symbol_temp = execute_trade['Symbol'].iloc[ed]
                trade_temp = execute_trade['Order'].iloc[ed]
                if trade_temp == 'BUY':
                    sign = 1
                else:
                    sign = -1
                share_temp = execute_trade['Shares'][ed]
                alloc[symbol_temp].iloc[td] = alloc[symbol_temp].iloc[td] + sign*share_temp
                alloc['Cash'].iloc[td] = alloc['Cash'].iloc[td] + (sign + impact) * share_temp * price_date[symbol_temp].iloc[0] + commission
                
    alloc = np.cumsum(alloc, 0)
    cash = start_val - alloc['Cash']
    daily_value = alloc[syms] * stockvals         
    portvals = daily_value.join(cash).sum(1)
    
    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
