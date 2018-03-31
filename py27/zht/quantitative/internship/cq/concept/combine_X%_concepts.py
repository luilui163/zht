# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 16:33:56 2016

@author: 13163
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ratio=0.01

def get_concepts_list():
    df=pd.read_csv(r'c:\garbage\wind\index_rolling_return_std_df.csv',index_col=0)
    concept_number=len(df.columns)
    target_number=int(concept_number*ratio)+1
    
    concepts_list=[]
    for i in range(len(df.index)):
        tmp_row=df.iloc[i]
        row_list=list(tmp_row)
        
        target_concept=[]
        for t in range(target_number):
            tmp_max=max(row_list)
            tmp_index=row_list.index(tmp_max)
            target_concept.append(df.columns[tmp_index])
            row_list.remove(tmp_max)
        concepts_list.append(target_concept)
#f=open(r'c:\garbage\wind\target_concepts.txt','w')
#for j in range(len(concepts_list)):
#    f.write('%d\t'%df.index[j])
#    for k in range(len(concepts_list[j])-1):
#        f.write('%s\t'%concepts_list[j][k])
#    f.write('%s\n'%concepts_list[j][k+1])
#f.close()
    '''因为是根据T的信号决定T+1的建仓，故日期需要向前shift'''
    return list(df.index)[2:],concepts_list[1:-1]

return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
dates,concepts_list=get_concepts_list()

target_df=pd.DataFrame(np.zeros((len(dates),len(return_df.columns))),index=dates,columns=return_df.columns)##initialize the target_df
target_df[target_df==0]=np.nan
stocks_of_df=list(return_df.columns)

for i in range(len(concepts_list)):
    date_index=list(return_df.index).index(dates[i])
    target_stocks_of_one_day=[]
    concepts_of_one_day=concepts_list[i]
    for c in concepts_of_one_day:
        #因为考虑到后边有些概念可能消失了，会找不到对应的文件记录
        try:
            stocks=open(r'c:\cq\concept\wind_new\%d\%s.txt'%(dates[i],c)).read().split('\n')[:-1]
        except IOError:
            pass
        for s in stocks_of_df:
            if s[:6] in stocks:
                target_stocks_of_one_day.append(s)
    
    row_index1=list(target_df.index).index(dates[i])
    row_index2=list(return_df.index).index(dates[i])
    for t in target_stocks_of_one_day:
        col_index=list(return_df.columns).index(t)
        target_df.iat[row_index1,col_index]=return_df.iat[row_index2,col_index]
    print dates[i]

tmp_df=return_df.iloc[list(return_df.index).index(list(target_df.index)[0]):]
pnl=target_df.mean(axis=1)-tmp_df.mean(axis=1)
std=pnl.std()
avg=pnl.mean()
cum_sum=pnl.cumsum()
information_ratio=avg/std
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(cum_sum)

ax.plot(cum_sum)
month=[y/100 for y in list(cum_sum.index)]
xticks=[]
xticklabels=[]
for i in range(1,len(month)):
    if month[i]>month[i-1]:
        xticks.append(i)
        xticklabels.append(str(month[i]))
ax.set_xticks(xticks)
ax.set_title('IR=%f'%information_ratio)
ax.set_xticklabels(xticklabels,rotation=90,fontsize='small')
fig.savefig(r'c:\garbage\wind\combine_%f_concepts.png'%ratio)
















