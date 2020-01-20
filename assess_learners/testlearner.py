"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import sys



if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)
    inf = open(sys.argv[1])
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])


    import pandas as pd
    file_path = '/Users/zibinchen/ML4T_2018Spring/assess_learners/Data/Istanbul.csv'

    data = pd.read_csv(file_path, index_col='date',
                parse_dates=True, na_values=['nan'])
    # compute how much of the data is training and testing
    train_rows = int(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data.iloc[:train_rows,0:-1]
    trainY = data.iloc[:train_rows,-1]
    testX = data.iloc[train_rows:,0:-1]
    testY = data.iloc[train_rows:,-1]

    trainX = np.atleast_2d(trainX)
    trainY = np.atleast_2d(trainY).reshape(-1,1)
    testX = np.atleast_2d(testX)
    sys.path.append('/Users/zibinchen/ML4T_2018Spring/assess_learners')

    import DTLearner as dt
    import BagLearner as bl
    import LinRegLearner as lrl
    import RTLearner as rt

    bl_learner = bl.BagLearner(learner = dt.DTLearner, kwargs = {"leaf_size":20}, bags = 10, boost = False, verbose = False)
    bl_learner.addEvidence(trainX, trainY)
    Y = bl_learner.query(testX)
  
    # evaluate in sample
    trainY = data.iloc[:train_rows,-1]
    predY = bl_learner.query(trainX) # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    # evaluate out of sample
    testY = data.iloc[train_rows:,-1]
    predY = bl_learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]

    learner = rt.RTLearner(leaf_size = 1, verbose = True)
    learner.addEvidence(trainX, trainY)
    print learner.author()
    
    # evaluate in sample
    trainY = data.iloc[:train_rows,-1]
    predY = learner.query(trainX) # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    # evaluate out of sample
    testY = data.iloc[train_rows:,-1]
    predY = learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]
    
    file_path = '/Users/zibinchen/ML4T_2018Spring/assess_learners/Data/Graph.csv'

    graph = pd.read_csv(file_path, index_col='Leaf_Size',
                parse_dates=True)
    
    plt.plot(graph.index,graph['In_Sample'], label = "Training RMSE")
    plt.plot(graph.index,graph['Out_of_Sample'], label = "Test RMSE")
    plt.title("RMSE vs Leaf Size")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.legend()
    
    plt.plot(graph.index,graph['Bag_In'], label = "Training RMSE")
    plt.plot(graph.index,graph['Bag_Out'], label = "Test RMSE")
    plt.title("Bagging: RMSE vs Leaf Size")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.legend()