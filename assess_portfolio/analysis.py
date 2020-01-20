"""Analyze a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""
import math
import sys
import util

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality


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


def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values
    
    prices_normalized, inital_price = normalization(prices, syms)
    prices_allocation = prices_normalized * allocs * sv
    prices_portfolio = prices_allocation.sum(axis = 1)
    daily_return = prices_portfolio/prices_portfolio.shift(1)-1
    daily_return = daily_return.dropna()
    
    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr = prices_portfolio.iloc[-1]/prices_portfolio.iloc[0] - 1
    adr = daily_return.mean()
    sddr = daily_return.std() 
    sr = (adr - rfr)/sddr * math.sqrt(sf)
    # add code here to compute stats

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        pass

    # Add code here to properly compute end value
    ev = prices_portfolio.iloc[-1]

    return cr, adr, sddr, sr, ev


def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        rfr=risk_free_rate, \
        sf=sample_freq, \
        gen_plot = False)

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
    test_code()
