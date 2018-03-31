# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:51:47 2016

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
return_df_stocks=list(return_df.columns)
return_df_dates=list(return_df.index)


def change_sid(sid):
    return_df_sid=[r.split('.')[0] for r in return_df_stocks]
    if sid in return_df_sid:
        ind=return_df_sid.index(sid)
        return return_df_stocks[ind]


def shift_date(d,shift_num=1):
    d=int(d)
    if shift_num>0:
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
    elif shift_num==0:
        if d<return_df_dates[0]:
            print d,'is too small'
        elif d>return_df_dates[-1]:
            print d,'is too large'
        elif d in return_df_dates:
            return d
        else:
            for i in range(len(return_df_dates)):
                if return_df_dates[i]<d<return_df_dates[i+1]:
                    return return_df_dates[i+1]
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
#                if return_df_dates[i]<=d and return_df_dates[i+1]>d:
                if return_df_dates[i]<d<return_df_dates[i+1]:
                    return return_df_dates[i+1-num]

lines=open(r'C:\cq\restricted_share\raw.txt').read().split('\n')
items=[]
for l in lines:
    sid=change_sid(l.split(',')[1])
    times=l.split(',')[2]
    unlock_date=int(l.split(',')[4].replace('-',''))
    ratio=l.split(',')[6]
    if sid:
        items.append((sid,unlock_date,ratio,times))
    else:
        print l.split(',')[1]


for length in [-3]:
    alpha=[]
    if length>=0:
        for item in items:
            start_date=shift_date(item[1])
            end_date=shift_date(start_date,shift_num=length)
            alpha.append((item[0],start_date,end_date,1))
    else:
        for item in items:
            end_date=shift_date(item[1],0)
            start_date=shift_date(item[1],length)
            alpha.append((item[0],start_date,end_date,1))
        
    target_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    target_df[target_df==0]=np.nan
    
    col=list(return_df.columns)
    for n,a in enumerate(alpha):
        col_index=col.index(a[0])
        if a[1] and a[2]:
            start_index=return_df_dates.index(int(a[1]))
            end_index=return_df_dates.index(int(a[2]))
            for i in range(start_index,end_index+1):
                target_df.iat[i,col_index]=a[3]
#            print n

    return_df_limit=return_df.copy()
    return_df_limit[abs(return_df_limit)>0.095]=0
    r=return_df.mean(axis=1)
    p=return_df_limit*target_df
    pnl=pd.Series([np.nan]*len(target_df),index=return_df.index)
    for i in range(len(target_df)):
        position=target_df.iloc[i]
        long_position=position[position>0].sum()
        short_position=abs(position[position<0].sum())
        if short_position<long_position:
            pnl.values[i]=(p.iloc[i]).sum()/long_position-r.values[i]
        elif short_position>long_position:
            pnl.values[i]=(p.iloc[i]).sum()/short_position+r.values[i]
        elif short_position and long_position:
            pnl.values[i]=(p.iloc[i]).sum()/long_position
    

#    for e,k in enumerate(pnl):
#        if pd.notnull(k):
#            break
#    pnl=pnl[e:][:-500]
    
    pnl=pnl[:-500]
    
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
#    fig.savefig(r'C:\cq\restricted_share\contrast4\{length}.png'.format(length=length))



#ind=list(target_df.index)
#col=list(target_df.columns)
#for i in range(len(ind)):
#	stocks=[]
#	for j in range(len(col)):
#		if pd.notnull(target_df.iat[i,j]):
#			stocks.append(col[j])
#	if len(stocks)>0:
#		position=10000000.0/len(stocks)
#		with open(r'C:\cq\restricted_share\alpha\alpha.{date}'.format(date=ind[i]),'w') as f:
#			for s in stocks:
#				f.write(s+'|'+str(position)+'\n')
#	print i
				