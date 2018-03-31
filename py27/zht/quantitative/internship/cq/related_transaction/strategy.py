# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 13:23:31 2016

@author: hp
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

factor=pd.read_csv(r'c:\cq\related_transaction\annual_growing_relative_1.csv',index_col=0)


return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
date_df=pd.read_csv(r'C:\cq\announcement_date_annual.csv',index_col=0)
std_dates=list(return_df.index)
def shift_date(date):
    if date in std_dates:
        index=std_dates.index(date)
        return std_dates[index+1]
    else:
        for i in range(len(std_dates)):
            if std_dates[i-1]<date and std_dates[i]>date:
                break
        return std_dates[i]



factor=factor[abs(factor)>0.02]
col=factor.columns
ind=factor.index
alpha=[]
for i in range(len(ind)):
    for j in range(len(col)):
        if pd.notnull(factor.iat[i,j]) and pd.notnull(date_df.iat[i,j]):
            alpha.append((shift_date(date_df.iat[i,j]),col[j],factor.iat[i,j]))
            #compare
#            alpha.append((shift_date(date_df.iat[i,j]),col[j],1))
        print i,j

announcement_date_df=pd.read_csv(r'C:\cq\announcement_date_annual.csv',index_col=0)
q_date=list(announcement_date_df.index)
new_alpha=[]
for e,a in enumerate(alpha):
    start_date=a[0]
    for i in range(len(q_date)):
        try:
            if q_date[i]<start_date and q_date[i+1]>start_date:
                tmp_date=announcement_date_df.at[q_date[i+1],a[1]]
                return_dates=list(return_df.index)
                return_dates.append(tmp_date)
                date_set=set(return_dates)
                union_date=sorted(list(date_set))
                index=union_date.index(tmp_date)
                if index==len(union_date)-1:
                    end_date=union_date[-1]
                else:
                    end_date=union_date[index+1]
        except IndexError:
            end_date=return_df.index[-1]
    new_alpha.append((a[1],start_date,end_date,a[2]))
    print e

target_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
target_df[target_df==0]=np.nan

col=list(return_df.columns)
for n,na in enumerate(new_alpha):
    col_index=col.index(na[0])
    start_index=std_dates.index(int(na[1]))
    end_index=std_dates.index(int(na[2]))
    for i in range(start_index,end_index+1):
        target_df.iat[i,col_index]=na[3]
#    target_df.iloc[start_index:end_index][na[0]]=na[3]
#    target_df.loc[na[1]:na[2]][na[0]]=na[3]
    print n



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
fig.savefig(r'C:\cq\related_transaction\fig\test_.png')