# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 16:09:36 2016

@author: hp
"""
import pandas as pd
import numpy as np
import os
import collections
import matplotlib.pyplot as plt
import re

def get_position(path):
#    path=r'C:\garbage\wind\new_in\if_change\alpha'
    p=re.compile(r'[0-9]')
    file_name=os.listdir(path)
    file_name=[fn for fn in file_name if fn.endwith()]
    file_path=[os.path.join(path,fn) for fn in file_name]
    position=collections.OrderedDict()
    for fp in file_path:
        date=int(fp.split('.')[1])
        lines=open(fp).read().split('\n')[:-1]
        stock=[l.split('|')[0] for l in lines]
        amount=[l.split('|')[1] for l in lines]
        position[date]=(stock,amount)
    return position

def get_result(alpha_file_path):
    trade=get_position(alpha_file_path)
    return_df=pd.read_csv(R'c:\cq\return_df.csv',index_col=0)
    position_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    position_df[position_df==0]=np.nan
    
    date_intersection=set(trade.keys()).intersection(set(return_df.index))
    for p in date_intersection:
        stock=trade[p][0]
        position=trade[p][1]
        for i in range(len(stock)):
            position_df.at[p,stock[i]]=position[i]
    #adjust return_df
    return_df[abs(return_df)>0.95]=0
#    pnl_df=return_df*position_df.sum(axis=1)
    pnl_adjusted=(return_df*position_df).sum(axis=1)-return_df.mean(axis=1)*position_df.sum(axis=1)
    
    pnl=pnl_adjusted
    
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
    fig.save(alpha_file_path+'fig.png')
if __name__=='__main__':
    get_result(r'C:\cq\salary\alpha1')

    


