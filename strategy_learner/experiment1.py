
"""
Name: zibin chen
User ID: zchen393
"""

import datetime as dt
import pandas as pd
import util as ut
import StrategyLearner as sl
import marketsimcode as msc
import ManualStrategy as ms
import matplotlib.pyplot as plt
from numpy import random 


symbol = 'JPM'
sd=dt.datetime(2008,1,1)
ed=dt.datetime(2009,12,31)
sv = 100000


'''
strategy learner
'''
          
random.seed(12)
learner = sl.StrategyLearner(verbose = False, impact = 0.000) # constructor
learner.addEvidence(symbol = symbol, sd=sd, ed=ed, sv = sv) # training phase
df_trades = learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = sv) # testing phase
daily_value_strategy = msc.compute_portvals(order = df_trades, symbol = symbol, start_val = sv, commission=0, impact=0.000)/sv



'''
benchmark
'''
date = pd.date_range(sd, ed)
stockvals = ut.get_data([symbol], date)
stockvals = stockvals.loc[:, [symbol]]
Benchmark = pd.DataFrame(0, index = stockvals.index[[0,-1]], columns = ['Order'])
Benchmark['Order'].iloc[0] = 1000
Benchmark['Order'].iloc[-1] = -1000
daily_value_benchmark = msc.compute_portvals(order = Benchmark, symbol = 'JPM', start_val = sv, commission=0, impact=0.000)/sv


'''
manuel strategy
'''
order = ms.testPolicy(symbol = 'JPM', sd = sd, ed = ed, sv = sv)
daily_value_manual = msc.compute_portvals(order = order, symbol = 'JPM', start_val = sv, commission=0, impact=0.000)/sv

cr_benchmark, adr_benchmark, sddr_benchmark = ms.portstats(daily_value_benchmark)
cr_manual, adr_manual, sddr_manual = ms.portstats(daily_value_manual)
cr_strategy, adr_strategy, sddr_strategy = ms.portstats(daily_value_strategy)




buy_m = order[order['Order'] > 0]
sell_m = order[order['Order'] < 0]

plt.figure(figsize=(20,5))
plt.plot(daily_value_benchmark.index, daily_value_benchmark, label = "Benchmark", color = "Blue")
plt.plot(daily_value_manual.index,daily_value_manual, label = "Manual Strategy", color = "Black")
buy_date = buy_m.shape[0]
for td in range(0,buy_date):
    plt.axvline(pd.to_datetime(buy_m.index[td]), color = "Green")
sell_date = sell_m.shape[0]
for td in range(0,sell_date):
    plt.axvline(pd.to_datetime(sell_m.index[td]), color = "Red")

plt.title("Manual Strategy vs Benchmark: In-Sample")
plt.legend()
plt.xlabel("Date")
plt.show()


buy_s = df_trades[df_trades['Order'] > 0]
sell_s = df_trades[df_trades['Order'] < 0]
plt.figure(figsize=(20,5))
plt.plot(daily_value_benchmark.index, daily_value_benchmark, label = "Benchmark", color = "Blue")

plt.plot(daily_value_manual.index,daily_value_strategy, label = "Strategy Learner", color = "Black")
buy_date = buy_s.shape[0]
for td in range(0,buy_date):
    plt.axvline(pd.to_datetime(buy_s.index[td]), color = "Green")
sell_date = sell_s.shape[0]
for td in range(0,sell_date):
    plt.axvline(pd.to_datetime(sell_s.index[td]), color = "Red")

plt.title("Strategy Learner vs Benchmark: In-Sample")
plt.legend()
plt.xlabel("Date")
plt.show()