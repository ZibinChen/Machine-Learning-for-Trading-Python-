"""MC1-P2: Optimize a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from scipy.optimize import minimize
from util import get_data, plot_data


def normalization(prices_all, symbols):
    dates = prices_all.index.values
    d_normalization = pd.DataFrame(index=dates)
    initial_price = prices_all.iloc[0]
    for symbol in symbols:
        price_temp = prices_all[symbol]
        initial_price_temp = price_temp[0]
        normalized_temp = price_temp/initial_price_temp
        d_normalization = d_normalization.join(normalized_temp)
        
    return d_normalization, initial_price

def daily_return_cal(allocs, prices_normalized):
    
    prices_allocation = prices_normalized * allocs
    prices_portfolio = prices_allocation.sum(axis = 1)
    daily_return = prices_portfolio/prices_portfolio.shift(1)-1
    daily_return = daily_return.dropna()
    
    return daily_return, prices_portfolio

def sd_cal(allocs, prices):
    
    daily_return = daily_return_cal(allocs, prices)[0]
    sddr = daily_return.std() 
    
    return sddr

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=True):
    rfr = 0
    sf = 252
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    
    prices_normalized = normalization(prices, syms)[0]
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    n_stock = len(syms)
    
    allocs = [0] * n_stock # add code here to find the allocations
    allocs[0] = 1
    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - 1},
            {'type': 'ineq', 'fun': lambda x: x})
    
    optimal_alloc = minimize(sd_cal, allocs, args=(prices_normalized,), constraints =cons)
    
    daily_return, prices_portfolio = daily_return_cal(optimal_alloc.x, prices_normalized)
    cr = prices_portfolio.iloc[-1]/prices_portfolio.iloc[0] - 1
    adr = daily_return.mean()
    sddr = daily_return.std() 
    sr = (adr - rfr)/sddr * math.sqrt(sf)  # add code here to compute stats
    
    # Get daily portfolio value
    port_val = prices_portfolio # add code here to compute daily portfolio values
    prices_SPY_normalized = prices_SPY/prices_SPY[0]
    
    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df = pd.concat([port_val, prices_SPY_normalized], keys=['Portfolio', 'SPY'], axis=1)
        ax = df.plot(title='Daily Portfolio Value and SPY', fontsize=12)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        plt.savefig('report.pdf')
        pass

    return optimal_alloc.x, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
