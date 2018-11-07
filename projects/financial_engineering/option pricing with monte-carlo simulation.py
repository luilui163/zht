# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-10-28  21:44
# NAME:zht-option pricing with monte-carlo simulation.py
import numpy as np
import math
import time



class OptionPricing:
    def __init__(self,S0,K,T,rf,sigma,iterations=10000):
        self.S0=S0
        self.K=K
        self.T=T
        self.rf=rf
        self.sigma=sigma
        self.iterations=iterations

    def call_option_simulation(self):
        #first with 0s and the second colum will store the payoff
        option_data=np.zeros([self.iterations,2])
        # 1 dimensional array with as many items as the iterations
        rand=np.random.normal(0,1,[1,self.iterations])
        stock_price=self.S0*np.exp(self.T*(self.rf-0.5*self.sigma**2)+self.sigma*np.sqrt(self.T)*rand)
        # we need S-E because we have to calculate the max(S-K,0)
        option_data[:,1]=stock_price-self.K
        #average for the Monte-carlo method
        #np.amax() returns the max(0,S-K) according to the formula
        option_price=np.exp(-1.0*self.rf*self.T)*np.amax(option_data,axis=1)
        average=np.sum(option_price)/self.iterations
        # have to use the exp(-rT) discount factor
        lower=np.percentile(option_price,2.5)
        upper=np.percentile(option_price,97.5)
        print(f'iterations:{self.iterations}-[{lower},{upper}]--{average}')

S0=100
K=100
T=0.25
rf=0.05
sigma=0.18

for N in [1000,10000,100000,1000000,10000000]:
    OptionPricing(S0,K,T,rf,sigma).call_option_simulation()





