"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import datetime as dt
from util import get_data
import matplotlib.pyplot as plt


def author():
    return 'zchen393'

def SMA(syms, N, date, gen_plot = False):
    
    stockvals = get_data([syms], date)
    stockvals = stockvals[syms]/stockvals[syms].iloc[0]
    
    sma = pd.rolling_mean(stockvals,N)
    price_sma = stockvals/sma - 1

    if gen_plot:
        plt.figure(figsize=(20,10))
        plt.subplot(211)
        plt.plot(sma.index, sma , label = str(N) + "-day" + " SMA")
        plt.plot(stockvals.index,stockvals, label = "Price")
        plt.title("Indicator:Simple Moving Average")
        plt.legend()
        plt.subplot(212)
        plt.plot(price_sma.index,price_sma, label = "Price/SMA")
        plt.xlabel("Date")
        plt.legend()
        plt.show()
        
    return price_sma
    
    
def BB(syms,N, sigma, date, gen_plot = False):
    
    stockvals = get_data([syms], date)
    stockvals = stockvals[syms]/stockvals[syms].iloc[0]
    
    sma = pd.rolling_mean(stockvals,N)
    sd = pd.rolling_std(stockvals,N)
    bb_upper = sma + sigma*sd
    bb_lower = sma - sigma*sd
    
    BB = (stockvals - sma)/(sigma*sd)
    if gen_plot:
        plt.figure(figsize=(20,10))
        plt.subplot(211)
        plt.plot(sma.index, sma, label = "SMA")
        plt.plot(stockvals.index,stockvals, label = "Price")
        plt.plot(bb_upper.index,bb_upper,'--', label = "Upper Bound")
        plt.plot(bb_lower.index,bb_lower,'--', label = "Lower Bound") 
        plt.title("Indicator:Bolinger Band")
        plt.legend()
        plt.subplot(212)
        plt.plot(BB.index,BB, label = "%BB")
        plt.xlabel("Date")
        plt.legend()
        plt.show()
        
    return BB


def MACD(syms, m1, m2, N, date, gen_plot = False):
    
    stockvals = get_data([syms], date)
   
    stockvals = stockvals[syms]/stockvals[syms].iloc[0]
    
    EMA_1 = stockvals.ewm(span = m1).mean()
    EMA_2 = stockvals.ewm(span = m2).mean()
    
    MACD_line = EMA_1 - EMA_2
    signal_line = MACD_line.ewm(span = N).mean()
    MACD_Hist = MACD_line - signal_line
    
    if gen_plot:
        plt.figure(figsize=(20,10))
        plt.subplot(211)
        plt.plot(MACD_line.index, MACD_line, label = "MACD")
        plt.plot(signal_line.index,signal_line, label = "Signal Line")
        plt.fill_between(MACD_line.index, MACD_Hist, color = 'gray', alpha=0.5, label='MACD Histogram')
        plt.title("Indicator:MACD")
        plt.legend()
        plt.subplot(212)
        plt.plot(stockvals.index, stockvals, label = "Price")
        plt.xlabel("Date")
        plt.legend()
        plt.show()
        
    return MACD_line, MACD_Hist


def RSI(syms, N, date, gen_plot = False):
    
    stockvals = get_data([syms], date)
    stockvals = stockvals[syms]/stockvals[syms].iloc[0]
    
    daily_return = stockvals/stockvals.shift(1)-1
    
    up = daily_return.copy()
    down = daily_return.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    
    roll_up = up.ewm(span = N).mean().abs()
    roll_down = down.ewm(span = N).mean().abs()
    rsi = 100.0 - (100.0 / (1.0 + roll_up / roll_down))
    
    if gen_plot:
        plt.figure(figsize=(20,10))
        plt.subplot(211)
        plt.plot(rsi.index, rsi, label = "RSI")
        plt.title("Indicator:RSI")
        plt.legend()
        plt.subplot(212)
        plt.plot(stockvals.index,stockvals, label = "Price")
        plt.xlabel("Date")
        plt.legend()
        plt.show()
        
    return rsi



def main():
 
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)
 
    date = pd.date_range(start_date, end_date)
    
    syms = 'JPM'
    N = 20
    SMA(syms, N, date, gen_plot = True)
    
    sigma = 2
    N = 20
    BB(syms,N, sigma, date, gen_plot = True)
    
    N = 9
    m1 = 12
    m2 = 26
    MACD(syms, m1, m2, N, date, gen_plot = True)
    
    N = 14
    RSI(syms, N, date, gen_plot = False)
