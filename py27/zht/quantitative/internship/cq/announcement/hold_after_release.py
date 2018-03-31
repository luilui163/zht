# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 09:44:20 2016

@author: hp
"""
import pandas as pd
import numpy as np
import os
import time
import collections
import matplotlib.pyplot as plt
import re


for day in [4,6,7,8,9]:

    return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
    announcement_date_df=pd.read_csv(r'C:\cq\announcement_date.csv',index_col=0)
    
    
    def date_pro(d):
        global day
        std_date=list(return_df.index)
        for i in range(len(std_date)):
            if d>=std_date[i] and d<std_date[i+1]:
                return std_date[i+day]
    #########
    alpha=[]
    date=list(announcement_date_df.index)
    stock=list(announcement_date_df.columns)
    
    
    
    for i in range(len(date)):
        for j in range(len(stock)):
            tmp_date=announcement_date_df.iat[i,j]
            if tmp_date<+20160324:
                investment_date=date_pro(tmp_date)
                alpha.append((stock[j],investment_date))
                print i,j
    
    std_date=list(return_df.index)
    alpha=[a for a in alpha if a[1] in std_date]
    
    
    target_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    target_df[target_df==0]=np.nan
    for n,a in enumerate(alpha):
        target_df.at[a[1],a[0]]=1
        print n
    
    ################
    return_df[abs(return_df)>0.095]=0
    
    t=target_df.sum(axis=1)
    r=return_df.mean(axis=1)
    for i in range(len(t)):
        if t.values[i]<0:
            r.values[i]=r.values[i]*(-1)    
    
    #alpha=-1*factor
    pnl=((return_df*target_df).sum(axis=1))/abs(t)-r
    pnl[abs(pnl)>0.1]=0
    
    #pnl=return_df[pd.notnull(target_df)].mean(axis=1)-return_df.mean(axis=1)
    
    pnl.values[0]=0
    pnl=pnl.fillna(0)
    std=pnl.std()
    avg=pnl.mean()
    cum_sum=pnl.cumsum()
    information_ratio=avg/std
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(cum_sum)
    
    year=[y/10000 for y in list(cum_sum.index)]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(year)):
        if year[i]>year[i-1]:
            xticks.append(i)
            xticklabels.append(str(year[i]))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=30,fontsize='small')
    ax.set_title('IR=%f'%information_ratio)
    fig.savefig(r'C:\cq\salary\fig\day%d.png'%day)