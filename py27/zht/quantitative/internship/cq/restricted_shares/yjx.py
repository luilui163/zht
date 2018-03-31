# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:51:47 2016

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

#lines=open(r'C:\cq\restricted_share\raw.txt').read().split('\n')
#items=[]
#for l in lines:
#    sid=change_sid(l.split(',')[1])
#    times=l.split(',')[2]
#    unlock_date=int(l.split(',')[4].replace('-',''))
#    ratio=l.split(',')[6]
#    if sid:
#        items.append((sid,unlock_date,ratio,times))
#    else:
#        print l.split(',')[1]

lines=open(R'c:\cq\restricted_share\yjx.txt').read().split('\n')[:-1]
items=[]
for l in lines:
    sid=l.split('\t')[0]
    announcement_date=l.split('\t')[1]
    exercise_date=l.split('\t')[2]
    items.append((sid,exercise_date))
    

for length in [-100,-50,-30,-20,-10,-5,-3,-2,-1]:
    alpha=[]
    for item in items:
#        start_date=shift_date(item[1],shift_num=length)
#        end_date=shift_date(item[1])
        
#        start_date=shift_date(item[1],length)
#        end_date=shift_date(start_date,length)
        
        end_date=shift_date(item[1],0)
        start_date=shift_date(item[1],length)
#        end_date=shift_date(start_date,shift_num=length)
        if start_date and end_date:
            alpha.append((item[0],start_date,end_date,1))
        
    target_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    target_df[target_df==0]=np.nan
    
    col=list(return_df.columns)
    for n,a in enumerate(alpha):
        if a[0] in return_df_stocks:
            col_index=col.index(a[0])
            start_index=return_df_dates.index(int(a[1]))
            end_index=return_df_dates.index(int(a[2]))
            for i in range(start_index,end_index+1):
                target_df.iat[i,col_index]=a[3]
#            print n
    
    
    t=target_df.sum(axis=1)
    r=return_df.mean(axis=1)
    for i in range(len(t)):
        if t.values[i]<0:
            r.values[i]=r.values[i]*(-1)
    
    #delete harden stock
    return_df_limit=return_df
    return_df_limit[abs(return_df_limit)>0.095]=0
    
    pnl=((return_df_limit*target_df).sum(axis=1))/abs(t)-r
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
    fig.savefig(r'C:\cq\restricted_share\contrast1\{length}.png'.format(length=length))
#    fig.savefig(r'C:\cq\restricted_share\fig\ratio_{length}.png'.format(length=length))
