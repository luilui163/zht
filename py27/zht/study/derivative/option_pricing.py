# -*- coding: utf-8 -*-
"""
Created on Thu May 12 16:18:39 2016

@author: Administrator
"""
from math import log,sqrt,exp
from scipy.stats import norm
from scipy.optimize import brentq

def call_option_pricer(spot,strike,maturity,r,vol):
    d1=(log(spot/strike)+(r+0.5*vol*vol)*maturity)/vol/sqrt(maturity)
    d2=d1-vol*sqrt(maturity)
    
    price=spot*norm.cdf(d1)-strike*exp(-r*maturity)*norm.cdf(d2)
    return price

def put_option_pricer(spot,strike,maturity,r,vol):
    d1=(log(spot/strike)+(r+0.5*vol*vol)*maturity)/vol/sqrt(maturity)
    d2=d1-vol*sqrt(maturity)
    
    price=strike*exp(-r*maturity)*norm.cdf(-d2)-spot*norm.cdf(-d1)
    return price


def call_implied_vol(spot,strike,maturity,r,target):
    class call_cost_function:
        def __init__(self,target):
            self.target_value=target
        
        def __call__(self,x):
            return call_option_pricer(spot,strike,maturity,r,x)-self.target_value
            
    cost_sample=call_cost_function(target)
    implied_vol=brentq(cost_sample,0.00000001,10000000)
    print 'the implied valarility is:%f'%implied_vol

def put_implied_vol(spot,strike,maturity,r,target):
    class put_cost_function:
        def __init__(self,target):
            self.target_value=target
        
        def __call__(self,x):
            return put_option_pricer(spot,strike,maturity,r,x)-self.target_value
            
    cost_sample=put_cost_function(target)
    implied_vol=brentq(cost_sample,0.00000001,10000000)
    print 'the implied valarility is:%f'%implied_vol

call_implied_vol(spot=55,strike=55,maturity=0.25,r=0.04,target=1.18)
#put_implied_vol(spot=55,strike=60,maturity=0.25,r=0.04,target=5.59)
print call_option_pricer(spot=55,strike=60,maturity=0.25,r=0.04,vol=0.01)
