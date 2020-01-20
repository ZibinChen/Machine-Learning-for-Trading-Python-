"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    row = np.random.randint(10,1001)
    column = np.random.randint(2,1001)
    X = np.random.random(size = (row,column))
    Y = X.sum(axis = 1)
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)
    row = np.random.randint(10,1001)
    column = np.random.randint(2,1001)
    X = np.random.random(size = (row,column))
    Y = np.sign(X[:,0] - np.median(X[:,0]))
    return X, Y

def author():
    return 'zchen393' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
