#-*-coding: utf-8 -*-
#author:tyhj
#fama_macbeth1.py 2017.10.15 15:31

from datetime import datetime
import numpy as np
import pandas as pd

n=252
np.random.seed(12345)
begdate=datetime(2013,1,2)
dateRange=pd.date_range(begdate,periods=n)

#OLS
# x0=pd.DataFrame(np.random.randn(n,1),columns=['ret'],index=dateRange)
# y0=pd.Series(np.random.randn(n),index=dateRange)
# print pd.ols(y=y0,x=x0)



import statsmodels.api as sm
def makeDataFrame():
    data=pd.DataFrame(np.random.randn(n,7),columns=list('ABCDEFG'),index=dateRange)
    return data

data={'A':makeDataFrame(),'B':makeDataFrame(),'C':makeDataFrame()}
Y=makeDataFrame()
print pd.fama_macbeth(y=Y,x=data)










