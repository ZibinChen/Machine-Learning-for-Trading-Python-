"""
Name: zibin chen
User ID: zchen393
"""


import datetime as dt
import StrategyLearner as sl
import marketsimcode as msc
import matplotlib.pyplot as plt

import ManualStrategy as ms
import pandas as pd
from numpy import random 

symbol = 'JPM'
sd=dt.datetime(2008,1,1)
ed=dt.datetime(2009,12,31)
sv = 100000

impact_list = [0, 0.005, 0.01, 0.03, 0.05, 0.07, 0.1]
summary = pd.DataFrame(0, index = impact_list, columns = ['Trade#'] + ['Cumulative Return'] + ['Daily Standard Deviation'] + ['Average Daily Return'])
'''
strategy learner
'''
i = 0

plt.figure(figsize=(20,5))
random.seed(12)
for impact in impact_list:
    random.seed(12)
    learner = sl.StrategyLearner(verbose = False, impact = impact) # constructor
    learner.addEvidence(symbol = symbol, sd=sd, ed=ed, sv = sv) # training phase
    df_trades = learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = sv) # testing phase
    daily_value_strategy = msc.compute_portvals(order = df_trades, symbol = symbol, start_val = sv, commission=0, impact=impact)/sv
    num_trade = df_trades.loc[df_trades['Order'] != 0].shape[0]
    cr_strategy, adr_strategy, sddr_strategy = ms.portstats(daily_value_strategy)
    summary.loc[impact_list[i],'Trade#'] = num_trade
    summary.loc[impact_list[i],'Cumulative Return'] = cr_strategy
    summary.loc[impact_list[i],'Daily Standard Deviation'] = sddr_strategy
    summary.loc[impact_list[i],'Average Daily Return'] = adr_strategy
    i += 1
    plt.plot(daily_value_strategy.index,daily_value_strategy, label = "Impact = " + str(impact))
plt.title("Learner behaviour with respect to the change of impact facotr")
plt.legend()
plt.xlabel("Date")
plt.show()

