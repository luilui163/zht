#-*-coding: utf-8 -*-
#@author:tyhj
from sklearn import datasets,linear_model
import pandas as pd
import numpy as np
from zht.data import data_handler
from datetime import datetime
import time
import math


length=500
def get_df():
    df=data_handler.get_return_df()
    df=df.dropna(axis=1,thresh=length*0.6)
    df.index=[pd.to_datetime(ind) for ind in df.index]
    return df

def get_month_end(df):
    start_date=df.index[length]
    end_date=df.index[-1]
    month_ends=pd.date_range(start_date,end_date,freq='M')
    return month_ends

def calculate_RSTR(df,month_end):
    #for one month
    df_sub=df.loc[:month_end]
    df_sub=df_sub[-length:]
    df_sub=df_sub.dropna(axis=1,thresh=length*0.6)
    df_sub=df_sub.fillna(0)
    ewm = [pow(0.5, i/120.0) for i in range(22, 22+length)[::-1]]
    w=np.matrix(ewm)
    rstr={}
    for code in df_sub.columns[:-1]:
        para=np.matrix(np.log(1+df_sub[code]))
        r=w*np.matrix(para).T
        rstr[code]=r.getA()[0][0]
    rstr=pd.DataFrame(rstr,index=[month_end])
    return rstr

def get_rstr():
    df=get_df()
    month_ends=get_month_end(df)
    rstr=pd.DataFrame(columns=df.columns[:-1])
    for month_end in month_ends:
        r=calculate_RSTR(df,month_end)
        rstr=rstr.append(r)
        print month_end
    return rstr

def run():
    RSTR=get_rstr()
    RSTR.to_csv(r'c:\data\gx\csvdata\factors\RSTR.csv')

if __name__=='__main__':
    run()





