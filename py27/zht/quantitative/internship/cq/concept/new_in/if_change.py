# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 14:59:40 2016

@author: 13163
"""
import pandas as pd
#from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import os

limit=1
operate=1
def get_stocks_list():
    file_dir=r'C:\garbage\concept\signal'
    file_name=os.listdir(file_dir)
    file_path=[os.path.join(file_dir,fn) for fn in file_name]
    date=[int(fn[:-4]) for fn in file_name]
    target_stocks=[]
    for d in range(len(date)):
        lines=open(file_path[d]).read().split('\n')[:-1]
#        stocks=[l.split('-')[0] for l in lines]
        tmp_stocks=[l.split('-')[0] for l in lines]
        target_stocks.append(tmp_stocks)
#        print date[d]
    
    return date[1:],target_stocks[:-1]


def get_target_df(return_df):
    global limit
    dates,stocks_list=get_stocks_list()
#    return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
    target_df=pd.DataFrame(np.zeros((len(dates),len(return_df.columns))),index=dates,columns=return_df.columns)
    target_df[target_df==0]=np.nan
    
    for di in range(len(dates)):
        f=open(r'C:\garbage\wind\new_in\if_change\\alpha\alpha.%d'%dates[di],'w')
        stock_basket=[]
        for s in stocks_list[di]:
            if s in return_df.columns:
                stock_basket.append(s)
                if limit==1:
                    if -0.090<return_df.at[dates[di],s]<0.090:##########排除涨停的股票
                        target_df.at[dates[di],s]=return_df.at[dates[di],s]
                    else:
                        target_df.at[dates[di],s]=0
                        for d in range(-5,5):
                            try:
                                target_df.at[dates[di-d],s]=0
                            except:
                                pass
#                        if not pd.isnull(target_df.at[dates[di-1],s]):
#                            target_df.at[dates[di-1],s]=0
                else:
                    target_df.at[dates[di],s]=return_df.at[dates[di],s]
                    
        if len(stock_basket)!=0:
            for sb in stock_basket:
                f.write('%s|%0.2f\n'%(sb,10000000.0/len(stock_basket)))
        f.close()
#        print di
    return target_df

def fig():
#    global ma
#    global ratio
    global operate
    return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
    target_df=get_target_df(return_df)
    tmp_df=return_df.loc[target_df.index[0]:]
    if operate==1:
        pnl=target_df.mean(axis=1)-tmp_df.mean(axis=1)
    elif operate==-1:
        pnl=-target_df.mean(axis=1)+tmp_df.mean(axis=1)
    std=pnl.std()
    avg=pnl.mean()
    pnl.values[0]=0
    pnl=pnl.fillna(0)
    cum_sum=pnl.cumsum()
    information_ratio=avg/std
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(cum_sum)
    
    year=[y/10000 for y in cum_sum.index]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(year)):
        if year[i]>year[i-1]:
            xticks.append(i)
            xticklabels.append(str(year[i]))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=30,fontsize='small')
    ax.set_title('IR=%f'%information_ratio)
    
    if limit==1:
        fig.savefig(r'C:\garbage\wind\new_in\if_change\%s_limit.png'%{1:'long',-1:'short'}[operate])
    else:
        fig.savefig(r'C:\garbage\wind\new_in\if_change\%s.png'%{1:'long',-1:'short'}[operate])

for limit in [1]:
    for operate in [-1]:
        fig()
        print limit,operate
