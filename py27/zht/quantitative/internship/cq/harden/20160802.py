# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 17:11:20 2016

@author: hp
"""

import pandas as pd
import numpy as np

return_df=pd.read_csv(R'c:\cq\return_df.csv',index_col=0)
announcement_date_annual_df=pd.read_csv(R'c:\cq\announcement_date_annual.csv',index_col=0)
ind=list(return_df.index)
stock=list(return_df.columns)


def get_target_stock_and_ipo_date():
    stock_past=[]
    for i in range(30):
        for j in range(len(stock)):
            if pd.notnull(return_df.iat[i,j]):
                stock_past.append(stock[j])
    for i in range(30,len(ind)):
        for j in range(len(stock)):
            if stock[j] not in stock_past and stock
            if pd.notnull(return_df.iat[i,j]):
                stock_past.append(stock[j])
                
                



def find_peak():
    pass


def find_bottom():
    pass

def get_position():
    pass

def get_alpha():
    pass


def get_result(alpha):
    pass



def shift_date(d,shift_num=1):
    d=int(d)
    if d<return_df_dates[0]:
        print d,'out of return_df_date\'s range'
    elif d>return_df_dates[-shift_num-1]:
        return return_df_dates[-1]
    elif d in return_df_dates:
        ind=return_df_dates.index(d)
        return return_df_dates[ind+shift_num]
    else:
        for i in range(len(return_df_dates)):
            if return_df_dates[i]<=d and return_df_dates[i+1]>d:
                return return_df_dates[i+1+shift_num]

def get_result(alpha):
    target_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    target_df[target_df==0]=np.nan
    
    for n,na in enumerate(alpha):
        col_index=return_df_stocks.index(na[0])
        start_index=return_df_dates.index(int(na[1]))
        end_index=return_df_dates.index(int(na[2]))
        for i in range(start_index,end_index+1):
            target_df.iat[i,col_index]=na[3]
    
    t=target_df.sum(axis=1)
    r=return_df.mean(axis=1)
    for i in range(len(t)):
        if t.values[i]<0:
            r.values[i]=r.values[i]*(-1)    
    
    #alpha=-1*factor
    pnl=((return_df*target_df).sum(axis=1))/abs(t)-r
    pnl[abs(pnl)>0.09]=0
    
    for e,p in enumerate(pnl):
        if pd.notnull(p):
            break
    
    pnl=pnl[e:]
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
