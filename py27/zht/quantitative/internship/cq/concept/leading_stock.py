# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 09:48:57 2016

@author: Administrator
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
ma=5
return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
url=r'c:\garbage\zhengquanzhixing\20160627'
files=os.listdir(url)
file_paths=[os.path.join(url,f) for f in files]
concepts=[ff[:-4] for ff in files]

def get_fig(concept,path):
    ##using leading stock to buy in 
    global ma
    stocks=open(path).read().split('\n')[:-1]
    target_stocks=[s for s in return_df.columns if s[:-3] in stocks]
    target_df=return_df[target_stocks]
    
    ma_df=pd.DataFrame()
    for stock in target_stocks:
        ma_df[stock]=pd.rolling_mean(return_df[stock],ma,min_periods=int(ma/2)+1)
    #target_df.to_csv(r'c:\garbage\target_df.csv')
    #ma_df.to_csv(r'c:\garbage\ma_df.csv')
    market_returns=return_df.mean(axis=1)
    target_returns=target_df.mean(axis=1)
    
    returns=[0]*len(ma_df.index)
    for i in range(5,len(ma_df.index)-1):
        tmp=ma_df.iloc[i].max()
        tmp_list=list(ma_df.iloc[i])
        j=tmp_list.index(tmp)
        if target_df.iat[i,j]>0:
            returns[i+1]=target_returns.values[i+1]-market_returns.values[i+1]
    
    pnl=pd.DataFrame({'returns':returns},index=ma_df.index)
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
    fig.savefig(r'c:\garbage\zhengquanzhixing\leading_stock\%s.png'%concept)

def ma_fig(concept,path):
    ma1=30
    ma2=3
    stocks=open(path).read().split('\n')[:-1]
    target_stocks=[s for s in return_df.columns if s[:-3] in stocks]
    target_df=return_df[target_stocks]
    
    ma1_df=pd.DataFrame()
    ma2_df=pd.DataFrame()
    for stock in target_stocks:
        ma1_df[stock]=pd.rolling_mean(return_df[stock],ma1,min_periods=int(ma1/2)+1)
        ma2_df[stock]=pd.rolling_mean(return_df[stock],ma2,min_periods=int(ma2/2)+1)
    #target_df.to_csv(r'c:\garbage\target_df.csv')
    #ma_df.to_csv(r'c:\garbage\ma_df.csv')
    market_returns=return_df.mean(axis=1)
    target_returns=target_df.mean(axis=1)
    
    returns=[0]*len(ma1_df.index)
    for i in range(5,len(ma1_df.index)-1):
        tmp=ma1_df.iloc[i].max()
        tmp_list=list(ma1_df.iloc[i])
        try:
            j=tmp_list.index(tmp)
            if target_df.iat[i,j]>0 and ma2_df.iat[i,j]>0:
                returns[i+1]=target_returns.values[i+1]-market_returns.values[i+1]
        except ValueError:
            pass

    pnl=pd.DataFrame({'returns':returns},index=ma1_df.index)
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
    dir_name=r'c:\garbage\zhengquanzhixing\leading_stock_ma_%d_%d'%(ma1,ma2)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    fig.savefig(dir_name+r'\%s.png'%concept)

def continue_fig(concept,path):
    ma1=30
#    ma2=3
    stocks=open(path).read().split('\n')[:-1]
    target_stocks=[s for s in return_df.columns if s[:-3] in stocks]
    target_df=return_df[target_stocks]
    
    ma1_df=pd.DataFrame()
#    ma2_df=pd.DataFrame()
    for stock in target_stocks:
        ma1_df[stock]=pd.rolling_mean(return_df[stock],ma1,min_periods=int(ma1/2)+1)
#        ma2_df[stock]=pd.rolling_mean(return_df[stock],ma2,min_periods=int(ma2/2)+1)
    #target_df.to_csv(r'c:\garbage\target_df.csv')
    #ma_df.to_csv(r'c:\garbage\ma_df.csv')
    market_returns=return_df.mean(axis=1)
    target_returns=target_df.mean(axis=1)
    
    returns=[0]*len(ma1_df.index)
    for i in range(5,len(ma1_df.index)-1):
        tmp=ma1_df.iloc[i].max()
        tmp_list=list(ma1_df.iloc[i])
        try:
            j=tmp_list.index(tmp)
            if target_df.iat[i,j]>0 and target_df.iat[i-1,j]>0:
                returns[i+1]=target_returns.values[i+1]-market_returns.values[i+1]
        except ValueError:
            pass

    pnl=pd.DataFrame({'returns':returns},index=ma1_df.index)
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
    dir_name=r'c:\garbage\zhengquanzhixing\leading_stock_ma_continue'
    
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    fig.savefig(dir_name+r'\%s.png'%concept)

def ma_compare(concept,path):
    ma1=30
#    ma2=3
    ma3=10
    ma4=3
    
    stocks=open(path).read().split('\n')[:-1]
    target_stocks=[s for s in return_df.columns if s[:-3] in stocks]
    target_df=return_df[target_stocks]
    
    ma1_df=pd.DataFrame()
#    ma2_df=pd.DataFrame()
    ma3_df=pd.DataFrame()
    ma4_df=pd.DataFrame()
    
    for stock in target_stocks:
        ma1_df[stock]=pd.rolling_mean(return_df[stock],ma1,min_periods=int(ma1/2)+1)
#        ma2_df[stock]=pd.rolling_mean(return_df[stock],ma2,min_periods=int(ma2/2)+1)
        ma3_df[stock]=pd.rolling_mean(return_df[stock],ma3,min_periods=int(ma3/2)+1)
        ma4_df[stock]=pd.rolling_mean(return_df[stock],ma4,min_periods=int(ma4/2)+1)
        
    #target_df.to_csv(r'c:\garbage\target_df.csv')
    #ma_df.to_csv(r'c:\garbage\ma_df.csv')
    market_returns=return_df.mean(axis=1)
    target_returns=target_df.mean(axis=1)
    
    returns=[0]*len(ma1_df.index)
    for i in range(5,len(ma1_df.index)-1):
        tmp=ma1_df.iloc[i].max()
        tmp_list=list(ma1_df.iloc[i])
        try:
            j=tmp_list.index(tmp)
            if ma4_df.iat[i,j]>ma3_df.iat[i,j]:
                returns[i+1]=target_returns.values[i+1]-market_returns.values[i+1]
        except ValueError:
            pass

    pnl=pd.DataFrame({'returns':returns},index=ma1_df.index)
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
    dir_name=r'c:\garbage\zhengquanzhixing\leading_stock_ma_compare'
    
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    fig.savefig(dir_name+r'\%s.png'%concept)

def threshold(concept,path):
    ma1=30

    stocks=open(path).read().split('\n')[:-1]
    target_stocks=[s for s in return_df.columns if s[:-3] in stocks]
    target_df=return_df[target_stocks]
    
    ma1_df=pd.DataFrame()

    
    for stock in target_stocks:
        ma1_df[stock]=pd.rolling_mean(return_df[stock],ma1,min_periods=int(ma1/2)+1)

    market_returns=return_df.mean(axis=1)
    target_returns=target_df.mean(axis=1)
    
    returns=[0]*len(ma1_df.index)
    for i in range(5,len(ma1_df.index)-1):
        tmp=ma1_df.iloc[i].max()
        tmp_list=list(ma1_df.iloc[i])
        try:
            j=tmp_list.index(tmp)
            if target_df.iat[i,j]>0.05:
                returns[i+1]=target_returns.values[i+1]-market_returns.values[i+1]
        except ValueError:
            pass

    pnl=pd.DataFrame({'returns':returns},index=ma1_df.index)
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
    dir_name=r'c:\garbage\zhengquanzhixing\leading_stock_threshold'
    
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    fig.savefig(dir_name+r'\%s.png'%concept)



def contrast_fig(concept,path):
    global ma
    stocks=open(path).read().split('\n')[:-1]
    target_stocks=[s for s in return_df.columns if s[:-3] in stocks]
    target_df=return_df[target_stocks]
    
    market_returns=return_df.mean(axis=1)
    target_returns=target_df.mean(axis=1)
    pnl=target_returns-market_returns
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
    fig.savefig(r'c:\garbage\zhengquanzhixing\leading_stock_contrast\%s.png'%concept)
    
for i in range(len(concepts)):
#    get_fig(concepts[i],file_paths[i])
#    contrast_fig(concepts[i],file_paths[i])
#    ma_fig(concepts[i],file_paths[i])
#    continue_fig(concepts[i],file_paths[i])
#    ma_compare(concepts[i],file_paths[i])
    threshold(concepts[i],file_paths[i])
