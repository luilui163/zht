# -*- coding: utf-8 -*-
"""
Created on Mon Mar 07 13:24:50 2016

@author: Administrator
"""
import re
import pandas as pd
import os
import time
import numpy as np
import matplotlib.pyplot as plt

folder=r'C:\cq\concept\wind_new\20100210'
files=os.listdir(folder)
file_paths=[os.path.join(folder,f) for f in files]
concepts=[f[:-4] for f in files]
return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)

def get_fig(path,concept):
    sid=open(path).read().split('\n')[:-1]
    stock_names=[c for c in return_df.columns]
    target_stocks=[stock_name for stock_name in stock_names if stock_name[:6] in sid]
    target_df=return_df[target_stocks]
    
    pnl=target_df.mean(axis=1)-return_df.mean(axis=1)
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
#    ax.set_xticks([0,242,484,725,967,1213,1475,1699,1934,2186,2424,2669,2913])
#    ax.set_xticklabels(['2004','2005','2006','2007','2008','20009','2010','2011','2012','2013','2014','2015','2016'],rotation=30,fontsize='small')
    ax.set_title('IR=%f'%information_ratio)
    fig.savefig(r'c:\garbage\wind\fig20100210\%s.png'%concept)
    print concept
    return information_ratio

IR=[]
for i in range(len(concepts)):
    IR.append(get_fig(file_paths[i],concepts[i]))
sorted_IR=sorted(IR,reverse=True)
sorted_concepts=['']*len(concepts)
for i in range(len(concepts)):
    sorted_concepts[i]=concepts[IR.index(sorted_IR[i])]
f=open(r'c:\garbage\wind\IR20100210.txt','w')
for j in range(len(concepts)):
    f.write('%f\t%s\n'%(sorted_IR[j],sorted_concepts[j])) 
f.close()















