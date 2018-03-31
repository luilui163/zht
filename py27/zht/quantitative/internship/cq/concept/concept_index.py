# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 11:26:14 2016

@author: 13163
"""
import re
import pandas as pd
import os
import time
import numpy as np
import matplotlib.pyplot as plt

start_date=20140620

folder=r'C:\cq\concept\wind_new\%d'%start_date
cap_df=pd.read_csv(r'c:\cq\cap_df.csv',index_col=0)

file_name=os.listdir(folder)
file_path=[os.path.join(folder,f) for f in file_name]



def index_fig(concept,path):
    sid=open(path).read().split('\n')[:-1]
    stock_names=[c for c in cap_df.columns]
    
    dates=list(cap_df.index)
    mark=dates.index(start_date)
    
    target_stocks=[stock_name for stock_name in stock_names if stock_name[:6] in sid]
    #因为有些交易日，股票数据可能因为停牌等缺失，这里先向前填充，然后向后填充
    
    target_df=cap_df[target_stocks]
    target_df=target_df.fillna(method='pad')
    target_df=target_df.fillna(method='bfill')
    total=target_df.sum(axis=1)
    tmp=total/total.values[mark]*1000
    index=tmp.iloc[mark:]
    
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(index)
    
    month=[y/100 for y in list(index.index)]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(month)):
        if month[i]>month[i-1]:
            xticks.append(i)
            xticklabels.append(str(month[i]))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=90,fontsize='small')
    fig.savefig(r'c:\garbage\wind\index_fig20140620\%s.png'%concept)

for i in range(len(file_name)):
    index_fig(file_name[i],file_path[i])
