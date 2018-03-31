# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 13:54:41 2016

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

return_df=pd.read_csv(R'c:\cq\return_df.csv',index_col=0)
return_df_dates=list(return_df.index)
return_df_stocks=list(return_df.columns)

def shift_date(d,shift_num=1):
    d=int(d)
    if shift_num>=0:
        if d<return_df_dates[0]:
            print d,'out of return_df_date\'s range'
        elif d>return_df_dates[-shift_num-1]:
            return return_df_dates[-1]
        elif d in return_df_dates:
            ind=return_df_dates.index(d)
            return return_df_dates[ind+shift_num]
        else:
            for i in range(len(return_df_dates)):
                if return_df_dates[i]<d and return_df_dates[i+1]>d:
                    return return_df_dates[i+shift_num]
    elif shift_num<0:
        num=-shift_num
        if d<return_df_dates[num-1]:
            print d,'is too small'
        elif d>return_df_dates[-1]:
            print d,'is too large'
        elif d in return_df_dates:
            ind=return_df_dates.index(d)
            return return_df_dates[ind-num]
        else:
            for i in range(len(return_df_dates)):
                if return_df_dates[i]<=d and return_df_dates[i+1]>d:
                    return return_df_dates[i+1-num]

for length in range(0,1):
    alpha=[]
    lines=open(r'c:\cq\illegal\illegal.txt').read().split('\n')[:-1]
#    lines=open(r'c:\cq\announcement_date.txt').read().split('\n')[:-1]
    for l in lines:
        tmp_date=int(l.split('\t')[1])
        start_date=shift_date(tmp_date)
        end_date=shift_date(start_date,shift_num=length)
        stock=l.split('\t')[0]
        if stock in return_df_stocks and abs(return_df.at[start_date,stock])<0.09:####剔除涨跌停
            alpha.append((stock,start_date,end_date,1))
        print l
    
    target_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    target_df[target_df==0]=np.nan
    
    col=list(return_df.columns)
    for n,na in enumerate(alpha):
        if na[0] in col:
            col_index=col.index(na[0])
            start_index=return_df_dates.index(int(na[1]))
            end_index=return_df_dates.index(int(na[2]))
            for i in range(start_index,end_index+1):
                if pd.notnull(target_df.iat[i,col_index]):
                    target_df.iat[i,col_index]+=float(na[3])
                else:
                    target_df.iat[i,col_index]=na[3]
            print n
    
    
    t=target_df.sum(axis=1)
    r=return_df.mean(axis=1)
    for i in range(len(t)):
        if t.values[i]<0:
            r.values[i]=r.values[i]*(-1)
    
    
    pnl=((return_df*target_df).sum(axis=1))/abs(t)-r
    #pnl[abs(pnl)>0.09]=0
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
    fig.savefig(r'C:\cq\illegal\fig\length_%d.png'%length)