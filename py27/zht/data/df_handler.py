#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import os
import math


#handle the outliers
def _handle_outliers1(df):
    # method 1,the largest and smallest quantile are delete
    new_df=pd.DataFrame(index=df.index)
    for code in df.columns:
        data=df[code]
        data[data>np.percentile(data,95)]=np.percentile(data,90)
        data[data<np.percentile(data,5)]=np.percentile(data,5)
        new_df[code]=data
    return new_df

def _handle_outliers2(df):
    #method 2,using 3 std as the threshhold
    new_df=pd.DataFrame(index=df.index)
    for code in df.columns:
        data=df[code]
        data[data-data.mean()<-3*data.std()]=data.mean()-3*data.std()
        data[data-data.mean()>3*data.std()]=data.mean()+3*data.std()
        new_df[code]=data
    return new_df

def _handle_outliers3(df,m=3):
    #median
    for code in df.columns:
        data=df[code]
        d=np.abs(data-np.median(data))
        mdev=np.median(d)
        for i in range(len(df[code])):
            s=df[code][i]/mdev if mdev else 0
            if s>m:
                print s
                df[code][i]=np.NaN
    return df

def regress(df,y_column,X_columns,intercept=1):
    '''
    y_column: a string from df.columns
    X_columns:a list of element from df.columns
    '''
    df=df[[y_column]+X_columns]
    # df=df.drop(df[pd.isnull(df[y_column])].index)
    # df=df.dropna(axis=0,thresh=len(df.columns)-2)
    # df=df.fillna(0)
    df=df.dropna(axis=0)
    mod=sm.OLS(y,X).fit()
    return mod

#
def combine_subdfs(dflist):
    df=pd.concat(dflist,axis=1)
    return df

#分组
def get_portfolio(df,colname,portfolio_number):
    new_df=df.sort_values(colname,ascending=True)
    number_middle=len(new_df)/portfolio_number
    number_low = number_middle + (len(new_df) % portfolio_number) / 2
    number_high = number_middle + len(new_df) % portfolio_number - (len(new_df) % portfolio_number / 2)

    stocklists={}
    stocklist_low=list(new_df[:number_low].index)
    stocklists[colname+'_low']=stocklist_low

    for j in range(portfolio_number-2):
        start=number_low+j*number_middle
        end=number_low+(j+1)*number_middle
        stocklist_middle=list(new_df[start:end].index)
        stocklists[colname+'_'+str(j+2)]=stocklist_middle

    stocklist_high=list(new_df[-number_high:].index)
    stocklists[colname+'_high']=stocklist_high

    for portfolio_name in stocklists:
        new_df.loc[stocklists[portfolio_name],'portfolio_name']=portfolio_name

    new_df=new_df[['portfolio_name']]
    return new_df


#add a sorting_type column to df
def add_sorting_type(df,colname,portfolio_number):
    new_df=df.sort_values(colname,ascending=True)
    number_middle=len(new_df)/portfolio_number
    number_low = number_middle + (len(new_df) % portfolio_number) / 2
    number_high = number_middle + len(new_df) % portfolio_number - (len(new_df) % portfolio_number / 2)

    stocklists={}
    stocklist_low=list(new_df[:number_low].index)
    stocklists[colname+'_low']=stocklist_low

    for j in range(portfolio_number-2):
        start=number_low+j*number_middle
        end=number_low+(j+1)*number_middle
        stocklist_middle=list(new_df[start:end].index)
        stocklists[colname+'_'+str(j+2)]=stocklist_middle

    stocklist_high=list(new_df[-number_high:].index)
    stocklists[colname+'_high']=stocklist_high

    for portfolio_name in stocklists:
        new_df.loc[stocklists[portfolio_name],colname+'_type']=portfolio_name
    return new_df

#均值或加权均值
def mean_self(df,factor,weight=None):
    df = df.dropna(axis=0) #TODO:if there is any NaN,the result will be NaN
    if weight:
        mean = np.average(df[factor], weights=df[weight])
    else:
        mean = np.average(df[factor])
    return mean

#标准差或加权标准差
def std_self(df,factor,weight=None):
    if weight:
        mean=np.average(df[factor],weights=df[weight])
        variance=np.average((df[factor]-mean)**2,weights=df[weight])
        std=math.sqrt(variance)
    else:
        std=df[factor].std()
    return std

#去极值
def winsorize(df,factor):
    sub_df = df[[factor]]
    sub_df[sub_df > np.percentile(sub_df, 95)] = np.percentile(sub_df, 95)
    sub_df[sub_df < np.percentile(sub_df, 5)] = np.percentile(sub_df, 5)
    return sub_df

#标准化 using std
def normalize(df,factor,weight=None):
    '''
    return a series
    '''
    # TODO:normalize func need to be modified,refer to initial edition
    mean_weighted=mean_self(df,factor,weight)
    std_weighted=std_self(df,factor,weight)
    normalized_df=(df[factor]-mean_weighted)/std_weighted
    return normalized_df

#normalize to [0,1]
def normalize1(df,factor):
    min=df[factor].min()
    max=df[factor].max()
    span=max-min
    s=(df[factor]-min)/span
    return s


#排序并构造组合，添加groupname
def add_group_name(df,colname,group_number):
    new_df=df.sort_values(colname,ascending=True)
    number_middle=len(new_df)/group_number
    number_low = number_middle + (len(new_df) % group_number) / 2
    number_high = number_middle + len(new_df) % group_number - (len(new_df) % group_number / 2)

    stocklists={}
    stocklist_low=list(new_df[:number_low].index)
    stocklists['1']=stocklist_low

    for j in range(group_number-2):
        start=number_low+j*number_middle
        end=number_low+(j+1)*number_middle
        stocklist_middle=list(new_df[start:end].index)
        stocklists[str(j+2)]=stocklist_middle

    stocklist_high=list(new_df[-number_high:].index)
    stocklists[str(group_number)]=stocklist_high

    for portfolio_name in stocklists:
        new_df.loc[stocklists[portfolio_name],colname+'_group']=portfolio_name

    return new_df

#filter,the corresponding values in pandas[colnames] are colvalues
def filter_df(df,colnames,colvalues):
    subdf=df.copy()
    for i in range(len(colnames)):
        subdf=subdf[subdf[colnames[i]]==colvalues[i]]
    return subdf

#using colname_sorting to construct portfolios,and then cal avg
def cal_portfolios(df,colname,colname_sorting):
    sts=df[colname_sorting].unique()
    avgs=[]
    for st in sts:
        subdf=df[df[colname_sorting]==st]
        avg=mean_self(subdf,colname)
        avgs.append(avg)
    avg_s=pd.Series(avgs,index=sts)
    return avg_s

def merge_all(path):
    '''
    merge all the subdfs to store them in one df
    '''
    fns=os.listdir(path)
    df=pd.DataFrame()
    for i,fn in enumerate(fns):
        name=fn[:-4]
        subdf=pd.read_csv(os.path.join(path,fn),index_col=0)
        subdf.columns=[name]
        df[name]=subdf[name]
        print 'merge_all',i,name
    df=df.dropna(axis=0,how='all')
    return df


def ts_to_cross(pathSrc, pathSave):
    '''
    change time series to cross df
    '''
    if not os.path.exists(pathSave):
        os.makedirs(pathSave)

    df = merge_all(pathSrc)
    dates = list(df.index)
    for date in dates:
        subDf = df.loc[[date], :]
        subDf = subDf.T
        subDf=subDf.dropna()
        if len(subDf) > 0:
            subDf.to_csv(os.path.join(pathSave, date + '.csv'))
        print 'ts_to_cross', date

