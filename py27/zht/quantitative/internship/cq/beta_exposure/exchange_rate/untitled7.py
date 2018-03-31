# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 12:09:27 2016

@author: hp
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
shibor_diff=pd.read_csv(r'C:\cq\beta_exposure\shibor_diff.csv',index_col=0)
return_df_dates=list(return_df.index)
return_df_stocks=list(return_df.columns)

#t1=time.time()
#corr1=return_df.corr()
#t2=time.time()
#stocks=list(return_df.columns)[:-1]
#corr2=pd.Series([np.nan]*(len(return_df.columns)-1),index=stocks)
#for i in range(len(stocks)):
#    corr2.values[i]=return_df[stocks[i]].corr(return_df.iloc[:,-1])
#t3=time.time()
#
#print t2-t1
#print t3-t2



diff=shibor_diff['on']

intersection_dates=[d for d in diff.index if d in return_df_dates]
new_return_df=return_df.loc[intersection_dates]
new_diff=diff.loc[intersection_dates]
dates=list(new_diff.index)
window=30

#for d in range(window,len(dates)):
d=dates[50]
e=diff.iloc[d-window:d]
tmp_df=new_return_df.iloc[d-window:d].copy()
tmp_df['e']=e
tmp_df[tmp_df==0]=np.nan
m=tmp_df.dropna(axis=1,thresh=int(window*0.8))
corr=m.corr().iloc[-1][:-1]
corr.sort()

tmp_corr=corr.copy()
m_corr=abs(tmp_corr)
m_corr.sort()