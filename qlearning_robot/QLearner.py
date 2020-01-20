"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.num_states = num_states
        
        self.s = 0
        self.a = 0
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        
        self.q = np.zeros(shape = (num_states, num_actions))
        
        if self.dyna > 0:
            self.Tc = np.ndarray(shape=(num_states, num_actions, num_states))
            self.Tc.fill(0.00001)
            self.R = np.ndarray(shape=(num_states, num_actions))
            self.R.fill(-1.0)    

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        
        if rand.random() <= self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.q[s,])
        
        if self.verbose: print "s =", s,"a =",action
        
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        
        self.q[self.s, self.a] = (1 - self.alpha) * self.q[self.s, self.a] + self.alpha * (r + self.gamma * np.max(self.q[s_prime,]))
        
        if rand.random() <= self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.q[s_prime,])   

        self.rar = self.rar * self.radr

        if self.dyna > 0:

            self.Tc[self.s, self.a, s_prime] = self.Tc[self.s, self.a, s_prime] + 1
            self.T = self.Tc / self.Tc.sum(axis=2, keepdims=True)
            self.R[self.s, self.a] = (1 - self.alpha) * self.R[self.s, self.a] + self.alpha * r

            dyna_a = np.random.randint(0, self.num_actions, self.dyna)
            dyna_s = np.random.randint(0, self.num_states, self.dyna)

            max_q = np.zeros(shape = (self.dyna))
            
            for i in range(0, self.dyna):
                dyna_s_prime = np.random.multinomial(1, self.T[dyna_s[i], dyna_a[i],]).argmax()
                max_q[i] = np.max(self.q[dyna_s_prime,])
                
            r = self.R[dyna_s, dyna_a]
            self.q[dyna_s, dyna_a] = (1 - self.alpha) * self.q[dyna_s, dyna_a] + self.alpha * (r + self.gamma * max_q)
            
        self.s = s_prime
        self.a = action
        
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

    def author(self):
        return 'zchen393'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
