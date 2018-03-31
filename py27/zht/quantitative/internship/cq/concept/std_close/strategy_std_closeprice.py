# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 16:00:31 2016

@author: 13163
"""
import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt



'''
构建index的时候，注意，每个concept的基准日期不同，都以concept出现的日期为基准日期




'''

ma=5
ratio=0.01
index_return_df=pd.read_csv(r'c:\garbage\wind\closeprice_df.csv',index_col=0)
return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)




def get_target_concept(date):
#    date=20100212
    global ma
    global ratio
    
#    index_return_df=pd.read_csv(r'c:\garbage\wind\closeprice_df.csv',index_col=0)

    
    
#    index_return_rolling_mean_df=pd.rolling_mean(index_return_df,ma,min_periods=int(ma/2)+1)
    index_return_rolling_std_df=pd.rolling_std(index_return_df,ma,min_periods=int(ma/2)+1)
#    index_return_rolling_std_df.to_csv(R'c:\garbage\wind\index_return_rolling_std_df.csv')
    df=index_return_rolling_std_df
#    df=index_return_rolling_mean_df/index_return_rolling_std_df
    
#    index_return_rolling_mean_df.to_csv(r'c:\garbage\wind\index_return_rolling_mean_df.csv')
#    index_return_rolling_std_df.to_csv(r'c:\garbage\wind\index_return_rolling_std_df.csv')
#    df.to_csv(r'c:\garbage\wind\ir_df.csv')    
    
    row=list(df.loc[date])
    c=Counter(np.isnan(row))
    total_concept_number=c[False]
    target_number=int(total_concept_number*ratio+1)
    target_concepts=[]
    for t in range(target_number):
        tmp_max=max(row)
        tmp_index=row.index(tmp_max)
        target_concepts.append(df.columns[tmp_index])
        row[tmp_index]=-1#不能直接删除这个地址
        
    return target_concepts#注意信号的滞后一期，所以此处的target_concepts是明天该投资股票

def get_stocks_list():
#    index_return_df=pd.read_csv(r'c:\garbage\wind\closeprice_df.csv',index_col=0)
    dates=index_return_df.index
#    concepts_list=[]
    stocks_list=[]
    for d in dates:
        concept=get_target_concept(d)
#        concepts_list.append(concept)
        stocks=[]
        for c in concept:
            lines=open(r'C:\cq\concept\wind_formatted\data\%d.txt'%d).read().split('\n')[:-1]
            for l in lines:
                belonging_concepts=l.split('\t')[1:]
                if c in belonging_concepts:
                    stocks.append(l.split('\t')[0])
        stocks_list.append(stocks)
#        print d
    return dates[1:],stocks_list[:-1]#注意这里的时间，不要弄错了，他们需要向后shift一天

def get_target_df():
    dates,stocks_list=get_stocks_list()
    
#    return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
    target_df=pd.DataFrame(np.zeros((len(dates),len(return_df.columns))),index=dates,columns=return_df.columns)
    target_df[target_df==0]=np.nan
    
    for di in range(len(dates)):
        for s in stocks_list[di]:
            if s in return_df.columns:
                target_df.at[dates[di],s]=return_df.at[dates[di],s]
        print di
    return target_df

def fig():
    global ma
    global ratio
    target_df=get_target_df()
#    return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
    tmp_df=return_df.iloc[list(return_df.index).index(list(target_df.index)[0]):]
    pnl=target_df.mean(axis=1)-tmp_df.mean(axis=1)
    std=pnl.std()
    avg=pnl.mean()
    pnl=pnl+1
    pnl.values[0]=1
    cum_sum=pnl.cumprod()
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
    fig.savefig(r'C:\garbage\wind\fig_std_closeprice\%d_%0.2f.png'%(ma,ratio))


for ma in [5,10,15,20,30]:
    for ratio in [0.01,0.02,0.05,0.1,0.2,0.3]:
        fig()
        print ma,ratio






