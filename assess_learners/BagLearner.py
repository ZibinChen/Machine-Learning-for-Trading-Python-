"""
    knn learner
    """

import numpy as np

class BagLearner(object):
    
    def __init__(self, learner, kwargs, bags, boost, verbose = False):
        self.bags = bags
        self.learner = learner
        self.kwargs = kwargs
    pass # move along, these aren't the drones you're looking for
    
    def author(self):
        return 'zchen393'
    
    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        ListX = []
        ListY = []
        n_sample = np.atleast_2d(dataX).shape[0]
        bag_sample = int(np.ceil(0.8 * n_sample))
        
        for i in range(self.bags):
            
            sample_selected = np.random.randint(n_sample, size = bag_sample)
            
            dataX_bag = dataX[sample_selected,:]
            dataY_bag = dataY[sample_selected]
            
            ListX.append(dataX_bag)
            ListY.append(dataY_bag)
        
        self.ListX = ListX
        self.ListY = ListY
    
    def query(self,points):
        """
            @summary: Estimate a set of test points given the model we built.
            @param points: should be a numpy array with each row corresponding to a specific query.
            @returns the estimated values according to the saved model.
            """
        predY = []
        
        for bag in range(self.bags):
            
            chosen_learner = self.learner(**self.kwargs)
            chosen_learner.addEvidence(self.ListX[bag], self.ListY[bag])
            predY_temp = chosen_learner.query(points)
            predY.append(predY_temp)
        
        predY = np.mean(predY, axis = 0)
        return predY


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"