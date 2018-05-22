# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-05-22  15:12
# NAME:xiangqi-sp.py

import pandas as pd


import database_api as dpi

def get_inter_df(df1,df2):
    interInd=df1.index.intersection(df2.index)
    df1=df1.reindex(interInd)
    df2=df2.reindex(interInd)
    return df1,df2




def func_(dd):
    result=dd.groupby(pd.Grouper(freq='M',level='trd_dt')).last()
    return result

def handle_duplicates(df):
    #keep the last duplicated value
    if df.index.has_duplicates:
        print('df has duplicated index and the last one will be kept')
    df=df[~df.index.duplicated(keep='last')]
    return df

def convert_freq(df,freq='M'):
    col=df.columns[0]
    new=df[col].unstack().resample(freq).last().stack()
    new.name=col
    new=new.to_frame()
    return new

def pre_process(df):
    df=handle_duplicates(df)
    df=convert_freq(df,freq='M')
    return df

#TODO:sort index

oper_rev=dpi.get_stocks_data('equity_selected_income_sheet_q',['oper_rev'],
                             '2004-01-01', '2018-03-01',)

cap=dpi.get_stocks_data('equity_fundamental_info',['cap'])

oper_rev=pre_process(oper_rev)
cap=pre_process(cap)








