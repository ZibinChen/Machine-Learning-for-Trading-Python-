import BagLearner as bl
import LinRegLearner as lrl
import numpy as np
class InsaneLearner(object):
    def __init__(self, verbose = False): 
        self.num = 20
        self.verbose = verbose
        List = []
        for i in range(self.num):
            List.append(bl.BagLearner(lrl.LinRegLearner, kwargs = {}, bags = 20, boost = False, verbose = self.verbose))  
        self.List = List
    def addEvidence(self, dataX, dataY):
        for learner in self.List:
            learner.addEvidence(dataX, dataY)
    def query(self, points):
        predY = []
        for i in range(self.num):
            predY_temp = self.List[i].query(points) 
            predY.append(predY_temp)
        return np.mean(predY, axis = 0)