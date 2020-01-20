"""
Name: zibin chen
User ID: zchen393
"""


import numpy as np

class RTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        pass # move along, these aren't the drones you're looking for
        
    def author(self):
        return 'zchen393' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        
        data = np.append(np.atleast_2d(dataX), dataY.reshape(-1,1), axis = 1)
        # build and save the model
        self.tree = self.Build_Tree(data)
            
    def treeSearch(self,singlepoint):
        
        i = 0
        start_feature = int(float(self.tree[0][0]))
        
        while True:
            
            start_feature = int(float(start_feature))
            start_spilt = float(self.tree[i][1])
            
            if singlepoint[start_feature].mean() <= start_spilt:
                i = i + int(float(self.tree[i][2]))
            else:
                i = i + int(float(self.tree[i][3]))
                
            start_feature = self.tree[i][0]
            
            if start_feature == "Leaf":
                break
        
        return(float(self.tree[i][1]))
                        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        n = np.atleast_2d(points).shape[0]
        y_predict = [0] * n
        for sample in range(n):
            y_predict[sample] = self.treeSearch(points[sample, :])
             
        return y_predict
    
    def Build_Tree(self, data):
        
        dataY = data[:,-1]
        if np.atleast_2d(data).shape[0] <= self.leaf_size:
            return np.atleast_2d(['Leaf', dataY.mean(), 'NA', 'NA'])
        
        if dataY.max() == dataY.min():
            return np.atleast_2d(['Leaf', dataY.mean(), 'NA', 'NA'])
        
        else:
            n_feature = np.atleast_2d(data).shape[1] - 1
            feature = np.random.randint(n_feature)
            SplitVal = np.median(data[:,feature])
    
            if data[:,feature].max() == SplitVal:
                lefttree = self.Build_Tree(data[data[:,feature] < SplitVal,:])
                righttree = np.atleast_2d(['Leaf', data[data[:,feature] == SplitVal, -1].mean(), 'NA', 'NA'])
            elif data[:,feature].max() == data[:,feature].min():
                return np.atleast_2d(['Leaf', data[data[:,feature] == SplitVal, -1].mean(), 'NA', 'NA'])
            else:
                righttree = self.Build_Tree(data[data[:,feature] > SplitVal, :])
                lefttree = self.Build_Tree(data[data[:,feature] <= SplitVal, :])
                
            root = np.atleast_2d([feature, SplitVal, 1, np.atleast_2d(lefttree).shape[0] + 1])
            root_left = np.append(root, lefttree, axis = 0)
            root_right = np.append(root_left, righttree, axis = 0)
        return (root_right)
         

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
