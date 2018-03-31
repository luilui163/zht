#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import datetime
from zht.data import data_handler

df=data_handler.get_df('000001.SZ')

def get_log_return(ts):
    lrets=np.log(ts/ts.shift(1))
    return lrets

def index_to_datetime(df):
    index=pd.to_datetime(df.index,format='%Y-%m-%d')
    df.index=index
    return df



lrets=data_handler.get_lrets('000001.SZ')

lrets=index_to_datetime(lrets)

print lrets.index[0]
print type(lrets.index[0])
print type(lrets.index)

