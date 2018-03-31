#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
from zht.data import data_handler

def compare_fc_with_benchmark():
    combine=pd.DataFrame()
    style_returns=pd.read_csv(R'c:\data\result\style_returns.csv',index_col=0)
    combine['fc']=style_returns['fc']

    # benchmark=data_handler.get_index_df('000985')
    benchmark=pd.read_csv(R'c:\data\result\000985.csv',index_col=0)
    # benchmark=benchmark/benchmark['close'][0]

    benchmark=benchmark['close'].pct_change()

    startdate=benchmark.index[0]
    enddate=benchmark.index[-1]
    dates=pd.date_range(startdate,enddate,freq='M')[1:] #delete the first date,since the first month may not be complete
    benchmark.index=[pd.to_datetime(ind) for ind in benchmark.index]
    benchmark_monthly=pd.DataFrame()
    for date in dates:
        year_month=date.strftime('%Y-%m')
        sub_df=benchmark[year_month]
        last_date=sub_df.index[-1]
        benchmark_monthly.at[last_date.strftime('%Y-%m-%d'),'returns']=sub_df.sum()
        print date
    combine['benchmark']=benchmark_monthly
    combine=combine.dropna(axis=0)

    #累乘的方式画图
    # combine=combine+1
    # combine.cumprod().plot(figsize=(16,9)).get_figure()

    #累加的方式画图
    fig=combine.cumsum().plot(figsize=(16,9)).get_figure()
    fig.savefig(r'c:\data\result\fc_with_benchmark.png')

if __name__=='__main__':
    compare_fc_with_benchmark()









