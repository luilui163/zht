# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 16:00:31 2016

@author: 13163
"""
import pandas as pd
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt



stock_ma=0
operate=0

def get_head_stocks(date,stocks,stock_ir_df,return_df):
#    global head_number
    global operate
    df_stocks=list(stock_ir_df.columns)
    inter_stocks=[s for s in stocks if s in df_stocks]
    tmp_df=stock_ir_df[inter_stocks]
    s=tmp_df.loc[date]
    a=s.dropna()
    a.sort()
    stock1=a.index[:int(len(a)/5)][:20]
    stock2=a.index[int(len(a)/5):int(2*len(a)/5)][:20]
    stock3=a.index[int(2*len(a)/5):int(3*len(a)/5)][:20]
    stock4=a.index[int(3*len(a)/5):int(4*len(a)/5)][:20]
    stock5=a.index[int(4*len(a)/5):][-20:]
    
    return stock1,stock2,stock3,stock4,stock5
    
    
#    if operate==1:
#        head_stocks=list(s.nsmallest(head_number).index)
#    elif operate==-1:
#        head_stocks=list(s.nlargest(head_number).index)
#    return head_stocks


def get_stocks_list(return_df):
#    stock_ir_df=pd.read_csv(r'c:\garbage\wind\stock_ir_df.csv',index_col=0)
    global stock_ma
    return_rolling_mean_df=pd.rolling_mean(return_df,stock_ma,min_periods=int(stock_ma/2)+1)
    return_rolling_std_df=pd.rolling_std(return_df,stock_ma,min_periods=int(stock_ma/2)+1)
    stock_ir_df=return_rolling_mean_df/return_rolling_std_df
    dates=return_df.index[1000:]
    stocks=return_df.columns
    stocks_list=[]
    for d in dates:
        target_stocks=get_head_stocks(d,stocks,stock_ir_df,return_df)
        stocks_list.append(target_stocks)
        print d
    return dates[1:],stocks_list[:-1]#注意这里的时间，不要弄错了，他们需要向后shift一天

def get_target_dfs(return_df):
    dates,stocks_list=get_stocks_list(return_df)
#    target_df=pd.DataFrame(np.zeros((len(dates),len(return_df.columns))),index=dates,columns=return_df.columns)
#    target_df[target_df==0]=np.nan
    
    target_dfs=[]
    for p in range(5):
        target_df=pd.DataFrame(np.zeros((len(dates),len(return_df.columns))),index=dates,columns=return_df.columns)
        target_df[target_df==0]=np.nan
        for di in range(len(dates)):
    #        f=open(r'C:\garbage\wind\fig_std_l_h_head_stocks\ir\alpha\%d.alpha'%dates[di],'w')
    #        stock_basket=[]
            for s in stocks_list[di][p]:
                if s in return_df.columns:
                    target_df.at[dates[di],s]=return_df.at[dates[di],s]
                    
#                    if -0.09<return_df.at[dates[di],s]<0.09:##去除涨跌停的股票
#                        target_df.at[dates[di],s]=return_df.at[dates[di],s]
#                    else:
#                        target_df.at[dates[di],s]=0
                        
    #                    stock_basket.append(s)
    #        if len(stock_basket)!=0:
    #            for sb in stock_basket:
    #                f.write('%s|%0.2f\n'%(sb,10000000.0/len(stock_basket)))
    #        f.close()
            print di
        target_dfs.append(target_df)
    return target_dfs


def fig():
    global head_number
    global operate
    return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
    target_dfs=get_target_dfs(return_df)
    for t in range(len(target_dfs)):
        tmp_df=return_df.loc[target_dfs[t].index[0]:]
        if operate==1:
            pnl=target_dfs[t].mean(axis=1)-tmp_df.mean(axis=1)
        else:
            pnl=-target_dfs[t].mean(axis=1)+tmp_df.mean(axis=1)
        std=pnl.std()
        avg=pnl.mean()
        pnl.values[0]=0
        pnl=pnl.fillna(0)
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
        if operate==1:
            fig.savefig(r'C:\garbage\wind\test_ir\port\%d_%d.png'%(t,stock_ma))
        elif operate==-1:
            fig.savefig(r'C:\garbage\wind\test_ir\largest_short\%d_%d.png'%(stock_ma,head_number))

for operate in [1]:
    for stock_ma in [10]:
#        for head_number in [10,20]:
        fig()
        print operate,stock_ma