# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 11:26:14 2016

@author: 13163
"""
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

ma=10
start_date=20100210
cap_df=pd.read_csv(r'c:\cq\cap_df.csv',index_col=0)

def get_index_df(concept,path):
    sid=open(path).read().split('\n')[:-1]
    stock_names=[c for c in cap_df.columns]
    
    dates=list(cap_df.index)
    mark=dates.index(start_date)
    
    target_stocks=[stock_name for stock_name in stock_names if stock_name[:6] in sid]
    #因为有些交易日，股票数据可能因为停牌等缺失，这里先向前填充，然后向后填充
    
    target_df=cap_df[target_stocks]
    target_df=target_df.fillna(method='pad')
    target_df=target_df.fillna(method='bfill')
    total=target_df.sum(axis=1)
    tmp=total/total.values[mark]*1000
    index=tmp.iloc[mark:]
    index_df=pd.DataFrame(index,columns=[concept])
    return index_df

def get_df():
    folder=r'C:\cq\concept\wind_new\%d'%start_date
    file_name=os.listdir(folder)
    concepts=[ff[:-4] for ff in file_name]
    file_path=[os.path.join(folder,f) for f in file_name]
    
    index0=get_index_df(concepts[0],file_path[0])
    for i in range(1,len(concepts)):
        index1=get_index_df(concepts[i],file_path[i])
        df=pd.concat([index0,index1],axis=1)
        index0=df
        print i,concepts[i]
    
    index_df=index0
    index_df.to_csv(r'c:\garbage\wind\index_df.csv')
    
    index_return_df=(index0-index0.shift(1))/index0
    index_return_df.to_csv(r'c:\garbage\wind\index_return_df.csv')
    
    index_rolling_return_df=pd.rolling_mean(index_return_df,ma)
    index_rolling_return_df.to_csv(r'c:\garbage\wind\index_rolling_return_df.csv')
    
    index_rolling_return_std_df=pd.rolling_std(index_return_df,ma)
    index_rolling_return_std_df.to_csv(r'c:\garbage\wind\index_rolling_return_std_df.csv')
    
    return index_df,index_return_df,index_rolling_return_std_df
    

index_df,index_return_df,index_rolling_return_std_df=get_df()






