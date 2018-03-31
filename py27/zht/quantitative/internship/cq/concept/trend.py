# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 15:15:01 2016

@author: Administrator
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

return_df=pd.read_csv(r'c:\cq\return_df2016.csv',index_col=0)

path1=r'c:\garbage\zhengquanzhixing\20160627'
files=os.listdir(path1)
file_paths=[os.path.join(path1,f) for f in files]
concepts=[ff[:-4] for ff in files]

###test
concept=concepts[0]
sid=open(file_paths[0]).read().split('\n')[:-1]

mean_return=list(return_df.mean(axis=1))
adjusted_return_df=return_df
for m in range(len(return_df.index)):
    for n in range(len(return_df.columns)):
        adjusted_return_df.iat[m,n]=return_df.iat[m,n]-mean_return[m]

for z in range(len(concepts)):
    concept=concepts[z]
    sid=open(file_paths[z]).read().split('\n')[:-1]
    
    stock_names=[c for c in adjusted_return_df.columns]
    target_stocks=[stock_name for stock_name in stock_names if stock_name[:6] in sid]
    
        
    
    cumsum_return_df=adjusted_return_df.cumsum()
    
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    
    ax.plot(cumsum_return_df[target_stocks])
    month=[y/100 for y in list(cumsum_return_df.index)]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(month)):
        if month[i]>month[i-1]:
            xticks.append(i)
            xticklabels.append(str(month[i]))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=30,fontsize='small')
    fig.savefig(r'c:\garbage\zhengquanzhixing\co_movement20160627\%s.png'%concept)
    print z,concept

