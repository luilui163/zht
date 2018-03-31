#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
from zht.data import data_handler
import os
from tool import mark
import shutil
import time

# @mark
# def get_month_returns():
#     directory=r'c:\data\barra_factors_combined\month_returns'
#     if os.path.exists(directory):
#         shutil.rmtree(directory)
#     time.sleep(1)
#     os.makedirs(directory)
#
#     df = data_handler.get_return_df()
#     df.index = [pd.to_datetime(ind) for ind in df.index]
#     start_date = df.index[0]
#     end_date = df.index[-1]
#     month_ends = pd.date_range(start_date, end_date, freq='M')
#     for month_end in month_ends:
#         year = month_end.year
#         month = month_end.month
#         tmp_date = str(year) + '-' + str(month) if month >= 10 else str(year) + '-0' + str(month)
#         month_df = df[tmp_date]
#         month_df = month_df.dropna(axis=1, thresh=len(month_df) * 0.3)
#         month_return = month_df.sum()
#         cross_df=pd.DataFrame()
#         cross_df['returns']=month_return
#         cross_df.to_csv(os.path.join(directory,month_end.strftime('%Y-%m-%d')+'.csv'))


@mark
def get_month_returns():
    directory = r'C:\data\barra_factors_combined\month_returns'
    if os.path.exists(directory):
        shutil.rmtree(directory)
    time.sleep(1)
    os.makedirs(directory)
    codes=data_handler.get_code_list()

    #combine the price df
    dfs=[]
    for code in codes:
        tmp_df=data_handler.get_df(code)[['close']]
        tmp_df.columns=[code]
        dfs.append(tmp_df)
    price=pd.concat(dfs,axis=1)

    price.index = [pd.to_datetime(ind) for ind in price.index]
    start_date = price.index[0]
    end_date = price.index[-1]
    month_ends = pd.date_range(start_date, end_date, freq='M')
    for month_end in month_ends:
        year = month_end.year
        month = month_end.month
        tmp_date = str(year) + '-' + str(month) if month >= 10 else str(year) + '-0' + str(month)
        month_df = price[tmp_date]
        month_df = month_df.dropna(axis=1, thresh=len(month_df) * 0.3)
        month_return=month_df.pct_change(periods=len(month_df)-1)
        month_return=month_return.iloc[-1,:]
        month_return=month_return.dropna(axis=0)
        month_return=pd.DataFrame(month_return)
        month_return.columns=['returns']
        month_return.to_csv(r'C:\data\barra_factors_combined\month_returns\%s.csv'%month_end.strftime('%Y-%m-%d'))
        print 'get_month_returns',month_end

#TODO:change the way to calculate the month_returns












if __name__=='__main__':
    get_month_returns()















