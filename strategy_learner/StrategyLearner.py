"""
Name: zibin chen
User ID: zchen393
"""


import datetime as dt
import pandas as pd
import util as ut
import numpy as np
import BagLearner as bl
import RTLearner as rl
import indicator as ind


class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        
        self.verbose = verbose
        self.impact = impact
        self.learner = bl.BagLearner(learner = rl.RTLearner, kwargs = {"leaf_size":5}, bags = 30, boost = False, verbose = False)
        self.window = 5
        self.threshold = 0.01
        self.buysell = 0.2
        
    def Xindicator(self, syms, dates):
        
        sma = ind.SMA(syms,20, dates)
        bb = ind.BB(syms, 20, 2, dates)
        _, macd = ind.MACD(syms, 12, 26, 9, dates)
        rsi = ind.RSI(syms, 14, dates)
        
        X = pd.DataFrame({'SMA':sma, 'BB':bb, "MACD":macd, "RSI":rsi})
        return X
    

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 

        # add your code to do learning here
        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd - dt.timedelta(days=50), ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        
        Y = prices.shift(-self.window)/prices - 1
        Y_pos = Y.loc[Y[symbol]>0,symbol] - 2 * self.impact
        Y_neg = Y.loc[Y[symbol]<0,symbol] + 2 * self.impact
        Y_pos.loc[Y_pos<0] = 0
        Y_neg.loc[Y_neg>0] = 0
        
        Y.loc[Y[symbol]>0,symbol] = Y_pos
        Y.loc[Y[symbol]<0,symbol] = Y_neg
        Y = Y[Y.index >= sd]
        Y[Y >= self.threshold] = 1
        Y[Y <= -self.threshold] = -1 
        Y[abs(Y) < 1] = 0
        
        self.Y = Y.dropna()
        
        X = self.Xindicator(symbol, dates)
        X = X[X.index >= sd]
        X = X[X.index <= self.Y.index[-1]]
        self.X = X
    
        self.learner.addEvidence(np.atleast_2d(self.X),np.atleast_2d(self.Y))
        

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "JPM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd - dt.timedelta(days=50), ed)
        X = self.Xindicator(symbol, dates)
        X = X[X.index >= sd]
        signal = self.learner.query(np.atleast_2d(X))
        signal[signal >= self.buysell] = 1
        signal[signal <= -self.buysell] = -1 
        signal[abs(signal) < 1] = 0
        trades = pd.DataFrame(0, index = X.index, columns = ['signal'])
        trades['signal'] = signal
        
        
        trades = self.Order(trades)
        
        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        
        return trades
    
    
    def Order(self,signal):
        
        order = pd.DataFrame(0, index = signal.index, columns = ['Order'])
        signal = signal.fillna(0)
        
        trade_date = order.shape[0]
        for td in range(0,trade_date):
            sign = int(signal.iloc[td])
            
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


if __name__=="__main__":
    print "One does not simply think up a strategy"
