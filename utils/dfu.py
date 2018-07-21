# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-10  15:09
# NAME:assetPricing-dfu.py


import pandas as pd
import ast
import operator
import numpy as np


_ops = {'<': operator.lt, '>': operator.gt,
       '<=': operator.le, '>=': operator.ge,
       '==': operator.eq,
       'endswith': lambda element, s: element.endswith(s),
        'in':lambda element,l:element in l,
        'contains':lambda l,element:element in l,
       }

def _condition(arr, op, value):
    '''
    :param arr: array
    :param op: operator in ops
    :param value:
    :return:an array of True or False
    '''
    return [op(x, value) for x in arr]

def _filterDf(df, queryStr):
    '''
    :param df:
    :param queryStr:a string like 'Trdmnt endswith 12' or 'Mclsprc > 10'
    :return:
    '''
    colname, opStr, value = queryStr.split(' ')

    if opStr in ['<', '>', '<=', '>=']: #TODO: for '==' how to handle the format of the value?
        #TODO: in factor,'==' do not need to consider,since we can use the method of df[df[colname]==value] to query.
        value = float(value)
        newdf = df[_condition(df[colname], _ops[opStr], value)]
        return newdf
    elif opStr in ['in']:
        value=ast.literal_eval(value)
        newdf = df[_condition(df[colname], _ops[opStr], value)]
        return newdf
    elif opStr in ['endswith']:
        newdf=df[_condition(df[colname], _ops[opStr], value)]
        return newdf
    elif opStr in ['==']:
        if value.isdigit():#if the value can be converted into number,then compare as number,else compare as str
            value=float(value)
        newdf=df[df[colname]==value]
        return newdf
    elif opStr=='=':
        raise ValueError('Please using ==,<=,or >= in the queryStr!')
    elif opStr=='contains':
        value=str(value)
        newdf=df[_condition(df[colname],_ops[opStr],value)]
        return newdf
    elif value=='notnull':
        return df[df[colname].notnull()]


#TODO: df.query('a>b'), and this equals df[df.a>df.b]

def filterDf(df,query):
    '''
    df=pd.read_csv(r'D:\quantDb\mkt\monthly\mkt.csv',index_col=0,dtype={'Stkcd':str})

    query1='Trdmnt endswith "12"'
    query2='Markettype == 16'
    query3='Mclsprc < 10'
    query4='Mclsprc > 10'
    query5='Mclsprc <= 10'
    query6='Mclsprc >= 10'
    query7='Stkcd in ["000001","000002"]'
    query8='Markettype in [1,4,16]'
    query9='LstFlg in ["A","AB"}'
    query10='A_StkCd is notnull'

    query9=[query1,query7]


    df1=filterDf(df,query1)
    df2=filterDf(df,query2)
    df3=filterDf(df,query3)
    df4=filterDf(df,query4)
    df5=filterDf(df,query5)
    df6=filterDf(df,query6)
    df7=filterDf(df,query7)
    df8=filterDf(df,query8)
    df9=filterDf(df,query9)
    '''
    if isinstance(query,list):
        for qs in query:
            df=_filterDf(df,qs)
    elif isinstance(query,str):
        df=_filterDf(df,query)
    return df

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

def get_group_n(grouped,n):
    return list(grouped)[n][1]

def get_first_group(grouped):
    return list(grouped)[0][1]


def join_dfs(xs):
    '''
    join Series or DataFrames mixed with single and multiple index.
    :param xs:
    :return: DataFrame
    '''
    single_dfs=[]
    multi_dfs=[]
    for x in xs:
        if isinstance(x.index,pd.MultiIndex):
            multi_dfs.append(x)
        else:
            single_dfs.append(x)

    s=None
    if len(single_dfs)>=2:
        s = pd.concat(single_dfs, axis=1)
    elif len(single_dfs)==1:
        s=single_dfs[0]

    m=None
    if len(multi_dfs)>=2:
        m=pd.concat(multi_dfs,axis=1)
    elif len(multi_dfs)==1:
        m=multi_dfs[0]

    if s is None:
        return m
    elif m is None:
        return s
    else:#there is both singleIndex dataframe and multiIndex dataframe
        return m.join(s,how='outer')


def myroll(df, window):
    '''
    refer to
        https://stackoverflow.com/questions/39501277/efficient-python-pandas-stock-beta-calculation-on-many-dataframes
    '''
    #TODO: This method will consume too much memory, as an alternative, my_rolling_apply is memory saving but it is much slower


    # stack df.values window-times shifted once at each stack
    roll_array = np.dstack([df.values[i:i + window, :] for i in range(len(df.index) - window + 1)]).T
    # roll_array is now a 3-D array and can be read into
    # a pandas panel object
    panel = pd.Panel(roll_array,
                     items=df.index[window - 1:],
                     major_axis=df.columns,
                     minor_axis=pd.Index(range(window), name='roll'))
    # convert to dataframe and pivot + groupby
    # is now ready for any action normally performed
    # on a groupby object
    #trick: filter_observations=False
    return panel.to_frame(filter_observations=False).unstack().T.groupby(level=0)


def my_rolling_apply(df, func, w, min_periods=None, fillna='mean'):
    '''
    Args:
        df:DataFrame,with datetime index
        w: window
        func: function to apply, func should apply on a dataframe and return a Series

    Returns:DataFrame

    '''
    if min_periods is None:
        min_periods=int(w*3/4)

    days=df.index.tolist()
    ss=[]
    for day in days[w:]:
        print('Rolling: {}'.format(day))
        sub = df.loc[days[days.index(day) - w + 1]:day]
        sub = sub.dropna(thresh=min_periods, axis=1)
        if fillna=='mean':
            sub = sub.fillna(sub.mean())  # Trick: fillna with average
        s=func(sub)
        ss.append(s)
    frame = pd.concat(ss, axis=1, keys=days[w:],sort=True).T
    return frame
