#-*-coding: utf-8 -*-
#@author:tyhj

'''
tools to handle the problems in pandas
'''

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats.mstats import winsorize as wsz
from zht.util import mathu

from zht.util.listu import chunkify,chunkifyByBreakPoints

def _handle_outliers(df):
    new_df=pd.DataFrame(index=df.index)
    for code in df.columns:
        data=df[code]
        data[data-data.mean()<-3*data.std()]=data.mean()-3*data.std()
        data[data-data.mean()>3*data.std()]=data.mean()+3*data.std()
        new_df[code]=data
    return df

def _get_cap_weighted_avg(df,date):
    df=_handle_outliers(df)
    filename=date+'.csv'
    cwd=os.getcwd()
    path=os.path.join(os.path.split(cwd)[0],'barra_factors\market_value')
    filenames=os.listdir(path)
    if filename in filenames:
        combined_df=pd.DataFrame()
        cap=pd.read_csv(os.path.join(path,filename),index_col=0)
        combined_df['cap']=cap.iloc[:,0]
        combined_df['factor']=df.iloc[:,0]
        combined_df=combined_df.dropna(axis=0,how='any')
        weighted_avg=(combined_df['cap']*combined_df['factor']).sum()*1.0/combined_df['cap'].sum()
        return weighted_avg
    else:
        return 0

#均值或加权均值
def mean_self(df,factor,weight=None):
    df = df.dropna(axis=0) #TODO:if there is any NaN,the result will be NaN
    if df.shape[0]==0:
        return np.NaN

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
# def winsorize(df,factor):
#     sub_df = df[[factor]]
#     sub_df[sub_df > np.percentile(sub_df, 95)] = np.percentile(sub_df, 95)
#     sub_df[sub_df < np.percentile(sub_df, 5)] = np.percentile(sub_df, 5)
#     return sub_df

# def winsorize(df,axis=0):
#     '''
#
#     Args:
#         df:
#         axis:if axis=0,then remove the extreme value row by row
#              if axis=1,column by column
#
#     Returns:
#
#     '''
#     if axis==1:
#         for col in df.columns:
#             df[col][df[col]>np.nanpercentile(df[col],95)]=np.nanpercentile(df[col],95)
#             df[col][df[col]<np.nanpercentile(df[col],5)]=np.nanpercentile(df[col],5)
#         return df
#     elif axis==0:
#         df=df.T
#         for col in df.columns:
#             df[col][df[col]>np.nanpercentile(df[col],95)]=np.nanpercentile(df[col],95)
#             df[col][df[col] < np.nanpercentile(df[col], 5)] = np.nanpercentile(df[col], 5)
#         df=df.T
#         return df

def winsorize(df, limits, axis=1, inclusive=(True, True)):
    '''
    Different with scipy.stats.mstats.winsorize,this reconstructed function ignores
    the `np.NaN`s in the df.

    Args:
        df: pandas dataframe
        limits: (downlimit,uplimit),tuple of floats like (0.05,0.05)
        inclusive:{(True, True) tuple}, optional
            Tuple indicating whether the number of data being masked on each side
            should be rounded (True) or truncated (False).
        axis:{None, int}, optional
            Axis along which to trim,that is,if the axis==0,the function will take
            out a column to trim the data along the axis0 each time,and vice versa.
            If None,the whole array is trimmed,but its shape is maintained.
    Returns:

    '''
    newdf = pd.DataFrame(index=df.index, columns=df.columns)
    if axis == 1:#row-by-row
        for index, row in df.iterrows():
            series = row.dropna()
            series = pd.Series(wsz(series.values, limits, inclusive), index=series.index)
            newdf.loc[index] = series
    elif axis == 0:#col-by-col
        for col in df.columns.tolist():
            series = df[col]
            series = series.dropna()
            series = pd.Series(wsz(series.values, limits, inclusive), index=series.index)
            newdf[col] = series

    return newdf


#标准化
def normalize(df,factor,weight=None):
    '''
    return a series
    '''
    # TODO:normalize func need to be modified,refer to initial edition
    mean_weighted=mean_self(df,factor,weight)
    std_weighted=std_self(df,factor,weight)
    normalized_df=(df[factor]-mean_weighted)/std_weighted
    return normalized_df

#子因子合成最终的因子
def combine_factors(df,factorList,weightList,newName):
    s=df[factorList]*weightList
    s=s.mean(axis=1)
    s=pd.DataFrame(s,columns=[newName])
    s=normalize(s,newName)
    df[newName]=s
    return df

# def get_inter_frame(df1,df2):
#     '''
#     get the cells intersection of the df1 and df2
#     :param df1:
#     :param df2:
#     :return:
#     '''
#     inds=sorted(list(set(df1.index.tolist()).intersection(set(df2.index.tolist()))))
#     cols=sorted(list(set(df1.columns.tolist()).intersection(set(df2.columns.tolist()))))
#
#     df1=df1.loc[inds,cols]
#     df2=df2.loc[inds,cols]
#     return df1,df2

def get_inter_frame(dflist):
    '''
    get intersection of the dataframes
    Args:
        dflist: a list of dataframe

    Returns:a list of new dataframes sharing the same index and column

    '''
    #sometimes,the columns are unicode and the others are str,unify them.
    for df in dflist:
        df.rename(columns=lambda x:str(x),inplace=True)

    indsets=[set(df.index.tolist()) for df in dflist]
    colsets=[set(df.columns.tolist()) for df in dflist]

    indInter=sorted(list(set.intersection(*indsets)))
    colInter=sorted(list(set.intersection(*colsets)))

    return [df.reindex(index=indInter,columns=colInter) for df in dflist]
    # return [df.loc[indInter,colInter] for df in dflist]

def get_outer_frame(dflist):
    indsets=[set(df.index.tolist()) for df in dflist]
    colsets=[set(df.columns.tolist()) for df in dflist]
    indOuter=sorted(list(set.union(*indsets)))
    colOuter=sorted(list(set.union(*colsets)))
    return [df.reindex(index=indOuter,columns=colOuter) for df in dflist]


def get_inter_index(dflist):
    '''
    get intersection of the dataframe index
    Args:
        dflist:a list of dataframe

    Returns:a list of new dataframe sharing the same index.

    '''
    indsets=[set(df.index.tolist()) for df in dflist]
    indInter=sorted(list(set.intersection(*indsets)))
    return [df.loc[indInter,:] for df in dflist]

def reg(regdf):
    '''
    :param df:the first column is the dependent variable,the others are the
              independent variable.Notice that the function will add constant variable
              automatically,so,df do not contains a constant column even if the regression
              contains an intercept.
    :return:slope,tvalue,rsquared,residuals
    '''
    regdf=regdf.dropna(axis=0,how='any')

    y=regdf.iloc[:,0].values
    X=regdf.iloc[:,1:].as_matrix()
    X=sm.add_constant(X)

    # yname=df.columns[0]
    # xnames=['const']+df.columns[1:].tolist()

    model=sm.OLS(y,X)
    r=model.fit()

    coefs=r.params
    tvalues=r.tvalues
    r2=r.rsquared_adj
    resids=r.resid

    return coefs,tvalues,r2,resids

def flatten2panel(df,indVar,colVar,vname):
    '''
        transfer df like:

               Stkcd     Trddt  Dretwd
            0      1  1991/4/3   0.225
            1      2  1991/4/3   0.465
            2      3  1991/4/3   0.142
            3      1  1991/4/4   0.225
            4      2  1991/4/4   0.465
            5      3  1991/4/4   0.142

        to
                          1      2      3
            1991/4/3  0.225  0.465  0.142
            1991/4/4  0.225  0.465  0.142

    Args:
        df: dataframe
        indVar: variable name in df.columns to set as the index of the new dataframe
        colVar: variable name in df.columns to set as the column of the new dataframe
        vname: the value to be stored in new dataframe cells

    Returns: dataframe

    '''
    subdfs=[]
    g=df.groupby(colVar)
    for col,x in list(g):
        sub=x[[indVar,vname]]
        sub=sub.set_index(indVar)
        sub=sub.sort_index(ascending=True)
        del sub.index.name
        sub.columns=[col]
        subdfs.append(sub)
    w=pd.concat(subdfs,axis=1)
    return w

def getMonthStartAndEnd(df):
    '''
    get the end dates of the df.index

    Args:
        df: the index frequence is day

    Returns:a list

    '''
    newdf=pd.DataFrame()
    newdf['date']=df.index
    newdf['month']=newdf['date'].apply(lambda x:x[:-3])
    g=newdf.groupby('month')
    monthStarts=[]
    monthEnds=[]
    for month,x in list(g):
        monthEnds.append(x['date'].values[-1])
        monthStarts.append(x['date'].values[0])
    return monthStarts,monthEnds


def _arrPortId(arr,param):
    '''
    sort the arr and divide them into n portfolio,then return the portfolio id.
    the id begin with 1,and the large the element the large the id
    :param arr:an array or list
    :param param:int or list
    :return:
    For example:
        arr=np.array(range(50))
        np.random.shuffle(arr)
        id=getPortId(arr,5)

    '''
    #TODO:optimize this function by using the method in scipy.stats.mstats.winsorize to
    if not isinstance(arr,np.ndarray):
        raise TypeError('"arr" should be a np.ndarray!')

    df = pd.DataFrame(arr)
    df.columns = ['arr']
    df = df.sort_values('arr')
    df['id'] = 0

    if isinstance(param,int):
        chunks=chunkify(range(len(arr)),param)
        idlist=[]
        for n,chunk in enumerate(chunks):
            idlist+=[n+1]*len(chunk)
        df['id']=idlist

    else:#break points
        chunks=chunkifyByBreakPoints(range(len(arr)),param)
        idlist=[]
        for n,chunk in enumerate(chunks):
            idlist+=[n+1]*len(chunk)
        df['id']=idlist
    df = df.sort_index()
    return df['id'].values

def getSortedPortId(mydata,param,axis=0):
    '''

    Args:
        mydata: array,series or dataframe
        param: int or a list of break points such as [0.3,0.7]
        axis: 0 or 1,0 denotes row by row,1 means column by column,
              so,usually the index in mydata is time and the column in mydata
              is stock codes.

    Returns:

    '''
    if len(np.shape(mydata))==1:
        if isinstance(mydata,pd.DataFrame):
            ids=pd.DataFrame(index=mydata.index,columns=mydata.columns)
            tmpdf=mydata.dropna().to_frame()
            tmpdf['id']=_arrPortId(tmpdf.values,param)
            ids.loc[tmpdf.index,ids.columns[0]]=tmpdf['id'].values
            return ids

        elif isinstance(mydata,pd.Series):
            ids=pd.Series(index=mydata.index)
            tmpdf=mydata.dropna().to_frame()
            tmpdf['id']=_arrPortId(tmpdf.values,param)
            ids.loc[tmpdf.index]=tmpdf['id'].values
            return ids

        elif isinstance(mydata,np.ndarray):
            return _arrPortId(mydata,param)

    elif len(np.shape(mydata))==2:
        if isinstance(mydata,pd.DataFrame):
            ids = pd.DataFrame(columns=mydata.columns)
            for ind in mydata.index.tolist():
                sub = mydata.loc[ind].to_frame()
                sub = sub.dropna()  # this will negnect the NaN
                sub['id'] = _arrPortId(sub.values, param)
                ids.loc[ind] = sub['id']
            return ids



