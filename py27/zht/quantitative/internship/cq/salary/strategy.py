# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 09:44:20 2016

@author: hp
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



#factor1
#absolute_growing_df3=pd.read_csv(r'c:\cq\salary\absolute_growing_df3.csv',index_col=0)
#data_df1=pd.read_csv(r'c:\cq\salary\data_df1.csv',index_col=0)
#factor=absolute_growing_df3/data_df1
##notice that some values in factor are -inf
#factor[factor<=-1.0]=-1.0
#factor[factor>=1.0]=1.0

#factor2
#relative_growing_df3=pd.read_csv(R'c:\cq\salary\relative_growing_df3.csv',index_col=0)
#factor=relative_growing_df3
##notice that some values in factor are -inf
#factor[factor<=-1.0]=-1.0
#factor[factor>=1.0]=1.0

#factor3
relative_growing_df3=pd.read_csv(R'c:\cq\salary\relative_growing_df3.csv',index_col=0)
revenue_growing_df=pd.read_csv(r'c:\cq\salary\revenue_growing_df.csv',index_col=0)
relative_growing_df3[relative_growing_df3<=-1.0]=-1.0
relative_growing_df3[relative_growing_df3>=1.0]=1.0
revenue_growing_df[revenue_growing_df<=-1.0]=-1.0
revenue_growing_df[revenue_growing_df>=1.0]=1.0
factor=relative_growing_df3-revenue_growing_df
#factor=revenue_growing_df-relative_growing_df3

#factor4
#revenue_growing_df=pd.read_csv(r'c:\cq\salary\revenue_growing_df.csv',index_col=0)
#revenue_growing_df[revenue_growing_df<=-1.0]=-1.0
#revenue_growing_df[revenue_growing_df>=1.0]=1.0
#factor=revenue_growing_df

return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
date_df=pd.read_csv(r'C:\cq\salary\date_df.csv',index_col=0)
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
tmp_df=date_df.copy(deep=True)
tmp_df[pd.notnull(tmp_df)]=1
factor=factor*tmp_df
col=factor.columns
ind=factor.index
alpha=[]
for i in range(len(ind)):
    for j in range(len(col)):
        if pd.notnull(factor.iat[i,j]):
            alpha.append((shift_date(date_df.iat[i,j]),col[j],factor.iat[i,j]))
            #compare
#            alpha.append((shift_date(date_df.iat[i,j]),col[j],1))
        print i,j

q_date=list(date_df.index)
std_dates=list(return_df.index)
new_alpha=[]
for e,a in enumerate(alpha):
    start_date=a[0]
    for i in range(len(q_date)):
        try:
            if q_date[i]<start_date and q_date[i+1]>start_date:
                tmp_date=date_df.at[q_date[i+1],a[1]]
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
#for n,na in enumerate(new_alpha):
#    target_df.loc[na[1]:na[2]][na[0]]=na[3]
#    print n

col=list(return_df.columns)
for n,na in enumerate(new_alpha):
    if na[0] in col:
        col_index=col.index(na[0])
        start_index=std_dates.index(int(na[1]))
        end_index=std_dates.index(int(na[2]))
        for i in range(start_index,end_index+1):
            target_df.iat[i,col_index]=na[3]
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
fig.savefig(r'C:\cq\salary\new\factor3.png')