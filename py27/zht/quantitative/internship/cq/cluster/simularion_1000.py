# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 20:47:03 2016

@author: Administrator
"""

import numpy as np
import random
import pandas as pd

def simulation(industry_number1,industry_number2,times=1000,stocks_number=1832):
    test=[0]*times
    for t in range(times):
        df=pd.DataFrame(np.zeros((industry_number1,industry_number2)))
        for s in range(stocks_number):
            lucky_industry1_index=random.randint(0,industry_number1-1)
            lucky_industry2_index=random.randint(0,industry_number2-1)
            df.iat[lucky_industry1_index,lucky_industry2_index]+=1
        test[t]=(df.max()/df.sum()).mean()
    significance_value=pd.Series(test).quantile(0.9)######for columns
    return significance_value


name=['ap','bbg','gx','wind','zx']
number=[253,301,191,129,187]


significant_matrix=pd.DataFrame(np.zeros((len(name),len(name))),index=name,columns=name)
for i in range(len(name)):
    for j in range(len(number)):
        significant_matrix.iat[i,j]=simulation(number[i],number[j])
significant_matrix.to_csv(r'/home/hzhang/cluster/significant_matrix_1000.csv')


