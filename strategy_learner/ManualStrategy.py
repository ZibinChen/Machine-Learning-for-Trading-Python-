"""
Name: zibin chen
User ID: zchen393
"""


import pandas as pd
import numpy as np
import datetime as dt
import marketsimcode as msc
from util import get_data
import matplotlib.pyplot as plt
import indicator as ind
from scipy.optimize import differential_evolution

def author():
    return 'zchen393'

def signal(sma, bb, macd, rsi, thres):
    
    signal = pd.DataFrame(0, index = sma.index, columns = ['SMA'] + ['BB'] + ['MACD'] + ['RSI'])
    signal['SMA'] = np.where(sma.shift(1)*sma < 0, np.where(sma > 0, 1, np.where(sma < 0, -1, 0)), 0)
    signal['BB'] = np.where((bb.shift(1)-thres[0])*(bb-thres[0]) < 0, np.where(bb < thres[0], -1, 0), np.where((bb.shift(1)+thres[0])*(bb+thres[0]) < 0, np.where(bb > -thres[0], 1, 0), 0))
    signal['MACD'] = np.where(macd.shift(1)*macd < 0, np.where(macd > 0, 1, np.where(macd < 0, -1, 0)), 0)
    signal['RSI'] = np.where(rsi > thres[1], -1, np.where(rsi < thres[2], 1, 0))
     
    return signal

def Order(signal):
    
    signal = signal.sum(1)
    order = pd.DataFrame(0, index = signal.index, columns = ['Order'])
    
    signal = signal.fillna(0)
    trade_date = order.shape[0]
    
    for td in range(0,trade_date):
        
        sign = int(signal.iloc[td])
        if sign >= 2:
            sign = 1
        else:
            if sign <= -2:
                sign = -1
            else:
                sign = 0
        
        if td+1 < trade_date:
            if td == 0:
                position = 0
            else:
                position = np.cumsum(order['Order'].iloc[0:td])[-1]
                order['Order'].iloc[td] = int(sign * np.sign(position) == -1) * sign * 2000 + int(sign * np.sign(position) == 0) * sign * 1000
                
        else:
            position = np.cumsum(order['Order'].iloc[0:td])[-1]
            order['Order'].iloc[td] = -position

            
    return order

def portstats(dailyvals):
    
    daily_return = dailyvals/dailyvals.shift(1)-1
    daily_return = daily_return.dropna()
    
    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr = dailyvals.iloc[-1]/dailyvals.iloc[0] - 1
    adr = daily_return.mean()
    sddr = daily_return.std() 
    
    return cr, adr, sddr

def optimalize(thres, sma, bb, macd, rsi, symbol = 'JPM', sv = 100000):
    
    order_signal = signal(sma, bb, macd, rsi, thres)
    order = Order(order_signal)
    daily_value = msc.compute_portvals(order = order, symbol = symbol, start_val = sv)/sv
    cr, _, _ = portstats(daily_value)
    
    return -cr

def calculate_thres():
    
    symbol = 'JPM'
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    
    date = pd.date_range(sd  - dt.timedelta(days=50), ed)
    stockvals = get_data([symbol], date)
    stockvals = stockvals.loc[:, [symbol]]
    
    sma = ind.SMA(symbol, 20, date, gen_plot = False)
    sma = sma[sma.index >= sd]
    bb = ind.BB(symbol, 20, 2, date, gen_plot = False)
    bb = bb[bb.index >= sd]
    _, macd = ind.MACD(symbol, 12, 26, 9, date, gen_plot = False)
    macd = macd[macd.index >= sd]
    rsi = ind.RSI(symbol, 14, date, gen_plot = False)
    rsi = rsi[rsi.index >= sd]
    
    bounds = [(0, 1), (60, 85), (15,40)]
    optimal_thres = differential_evolution(optimalize, bounds, args=(sma, bb, macd, rsi, ))
    
    return(optimal_thres)
    

def testPolicy(symbol = 'JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    
    date = pd.date_range(sd  - dt.timedelta(days=50), ed)
    stockvals = get_data([symbol], date)
    stockvals = stockvals.loc[:, [symbol]]
    
    sma = ind.SMA(symbol, 20, date, gen_plot = False)
    sma = sma[sma.index >= sd]
    bb = ind.BB(symbol, 20, 2, date, gen_plot = False)
    bb = bb[bb.index >= sd]
    _, macd = ind.MACD(symbol, 12, 26, 9, date, gen_plot = False)
    macd = macd[macd.index >= sd]
    rsi = ind.RSI(symbol, 14, date, gen_plot = False)
    rsi = rsi[rsi.index >= sd]
    
    thres = [0.99243522, 84.70103144, 25.01519814] 
    """
    from calculate_thres
    """
    order_signal = signal(sma, bb, macd, rsi, thres)
    order = Order(order_signal)
             
    return order



def main_insample():
    
    symbol = 'JPM'
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    sv = 100000
    
    date = pd.date_range(sd, ed)
    stockvals = get_data([symbol], date)
    stockvals = stockvals.loc[:, [symbol]]
    Benchmark = pd.DataFrame(0, index = stockvals.index[[0,-1]], columns = ['Order'])
    Benchmark['Order'].iloc[0] = 1000
    Benchmark['Order'].iloc[-1] = -1000
    
    order = testPolicy(symbol = 'JPM', sd = sd, ed = ed, sv = sv)
    
    daily_value_benchmark = msc.compute_portvals(order = Benchmark, symbol = 'JPM', start_val = sv)/sv
    daily_value_manual = msc.compute_portvals(order = order, symbol = 'JPM', start_val = sv)/sv
    
    cr_benchmark, adr_benchmark, sddr_benchmark = portstats(daily_value_benchmark)
    cr_manual, adr_manual, sddr_manual = portstats(daily_value_manual)
    
    buy = order[order['Order'] > 0]
    sell = order[order['Order'] < 0]
    
    plt.figure(figsize=(20,5))
    plt.plot(daily_value_benchmark.index, daily_value_benchmark, label = "Benchmark", color = "Blue")
    plt.plot(daily_value_manual.index,daily_value_manual, label = "Manual Strategy", color = "Black")
    buy_date = buy.shape[0]
    for td in range(0,buy_date):
        plt.axvline(pd.to_datetime(buy.index[td]), color = "Green")
    sell_date = sell.shape[0]
    for td in range(0,sell_date):
        plt.axvline(pd.to_datetime(sell.index[td]), color = "Red")
    plt.title("Manual Strategy vs Benchmark: In-Sample")
    plt.legend()
    plt.xlabel("Date")
    plt.show()
   
    return cr_benchmark, adr_benchmark, sddr_benchmark, cr_manual, adr_manual, sddr_manual 

def main_outofsample():
    
    symbol = 'JPM'
    sd=dt.datetime(2010,1,1)
    ed=dt.datetime(2011,12,31)
    sv = 100000
    
    date = pd.date_range(sd, ed)
    stockvals = get_data([symbol], date)
    stockvals = stockvals.loc[:, [symbol]]
    Benchmark = pd.DataFrame(0, index = stockvals.index[[0,-1]], columns = ['Order'])
    Benchmark['Order'].iloc[0] = 1000
    Benchmark['Order'].iloc[-1] = -1000
    
    order = testPolicy(symbol = 'JPM', sd = sd, ed = ed, sv = sv)
    
    daily_value_benchmark = msc.compute_portvals(order = Benchmark, symbol = 'JPM', start_val = sv)/sv
    daily_value_manual = msc.compute_portvals(order = order, symbol = 'JPM', start_val = sv)/sv
    
    cr_benchmark, adr_benchmark, sddr_benchmark = portstats(daily_value_benchmark)
    cr_manual, adr_manual, sddr_manual = portstats(daily_value_manual)
    
    buy = order[order['Order'] > 0]
    sell = order[order['Order'] < 0]
    
    plt.figure(figsize=(20,5))
    plt.plot(daily_value_benchmark.index, daily_value_benchmark, label = "Benchmark", color = "Blue")
    plt.plot(daily_value_manual.index,daily_value_manual, label = "Manual Strategy", color = "Black")
    buy_date = buy.shape[0]
    for td in range(0,buy_date):
        plt.axvline(pd.to_datetime(buy.index[td]), color = "Green")
    sell_date = sell.shape[0]
    for td in range(0,sell_date):
        plt.axvline(pd.to_datetime(sell.index[td]), color = "Red")
    plt.title("Manual Strategy vs Benchmark: Out-of-Sample")
    plt.legend()
    plt.xlabel("Date")
    plt.show()
    
    return cr_benchmark, adr_benchmark, sddr_benchmark, cr_manual, adr_manual, sddr_manual 