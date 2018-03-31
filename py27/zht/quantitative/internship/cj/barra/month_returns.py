#-*-coding: utf-8 -*-
#@author:tyhj

from sklearn import datasets,linear_model
import pandas as pd
import numpy as np
from zht.data import data_handler
from datetime import datetime
import time

def get_month_returns():
    df=data_handler.get_return_df()
    df.index=[pd.to_datetime(ind) for ind in df.index]
    start_date=df.index[0]
    end_date=df.index[-1]

    month_ends=pd.date_range(start_date,end_date,freq='M')
    month_returns=pd.DataFrame(columns=df.columns)
    for month_end in month_ends:
        year=month_end.year
        month=month_end.month
        tmp_date=str(year)+'-'+str(month) if month>=10 else str(year)+'-0'+str(month)
        month_df=df[tmp_date]
        month_df = month_df.dropna(axis=1, thresh=len(month_df) * 0.3)
        month_return = month_df.sum()
        # month_return=pd.DataFrame(month_return,columns=[month_end]).T
        month_returns.loc[month_end] = month_return
        print month_end
    month_returns.to_csv(r'C:\data\gx\csvdata\month_returns.csv')



if __name__=='__main__':
    get_month_returns()










