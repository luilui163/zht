#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import tool
import os
import data_preprocess
import shutil
import factors

#得到hs300的收益
def get_benchmark_return():
    df=pd.read_csv(r'c:\data\zz800\benchmark_mktcap.csv',index_col=0)
    df=df.set_index('stockID')
    benchmark_return=tool.mean(df,'pct_chg','cap')
    return benchmark_return

#把行业信息转化为矩阵
def get_sector_matrix_df():
    df=pd.read_csv(R'c:\data\zz800\universe_mktcap.csv',index_col=0)
    df=df.set_index('stockID')
    sector=df['sector']
    s=dict(sector)
    sector_matrix_df=pd.DataFrame()
    for stock in s:
        sector_matrix_df.at[stock,s[stock]]=1
    sector_matrix_df=sector_matrix_df.fillna(0)
    return sector_matrix_df

#获取截面回归时的数据，把他们全部存在一个df中
def get_cross_df():
    df=pd.read_csv(R'c:\data\zz800\universe_mktcap.csv',index_col=0)
    df=df.set_index('stockID')
    benchmark_return=get_benchmark_return()
    liquidity=pd.read_csv(R'C:\data\zz800\data_processed\liquidity\2016-06-30.csv',index_col=0)
    sector=get_sector_matrix_df()
    dfs=[df[['pct_chg']],liquidity,sector]
    cross_df=pd.concat(dfs,axis=1)
    cross_df['benchmark_return']=benchmark_return
    cross_df=cross_df.dropna(axis=0)
    cross_df.to_csv(r'C:\data\zz800\cross_df.csv')

#获取WLS时候的权重W，即市值的平方根，以矩阵形式返回
def get_weight_matrix():
    df=pd.read_csv(r'c:\data\zz800\universe_mktcap.csv',index_col=0)
    df=df.set_index('stockID')
    sqrt_cap=np.sqrt(df['cap'])
    weight_matrix=np.mat(np.diag(sqrt_cap/sqrt_cap.sum()))
    return weight_matrix












