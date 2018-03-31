#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import os

#求加权平均
def mean(df,factor,weight=0):
    if weight != 0:
        #指定权重求平均
        return (df[factor]*df[weight]).sum()/df[weight].sum()
    else:
        #等权平均
        return df[factor].mean()

#求标准差
def std(df,factor,weight=0):
    if weight!=0:
        sigma=np.square(df[factor]-df[factor].mean()).sum()/df[factor].sum()
    else:
        sigma=df[factor].std()
    return sigma #TODO：检验该函数

#去极值
def handle_outliers(df,factor):
    factor_df=df[[factor]]
    factor_df[factor_df>np.percentile(factor_df,95)]=np.percentile(factor_df,95)
    factor_df[factor_df<np.percentile(factor_df,5)]=np.percentile(factor_df,5)
    return factor_df #a df
    #TODO:return a series or a dataframe or just adjust in the initial df

#标准化
def standardize(df,factor):
    tmp_df=df[[factor]]
    return (tmp_df-tmp_df.mean())/tmp_df.std()
    #TODO:as above

#内积为1
def dot(df,factor):
    pass

#映射到正态
def map_to_normal(df,factor):
    pass

#标准化的中心值为市值加权平均值
def standardize_by_cap_weight(df,factor):
    tmp_df=pd.read_csv(r'C:\data\zz800\universe_mktcap.csv',index_col=0)
    tmp_df=tmp_df.set_index('stockID')
    cap=tmp_df['cap']
    df['cap']=cap
    df=df.dropna(axis=0)
    cap_weighted_value=(df[factor]*df['cap']).sum()/df['cap'].sum()
    return (df[[factor]]-cap_weighted_value)/df[factor].std()

#TODO:加权标准差，python形参的调用










