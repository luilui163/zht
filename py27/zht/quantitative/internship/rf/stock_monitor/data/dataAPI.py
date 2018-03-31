#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
from settings import  database_dir
import os


def get_stocklist_in_database():
    # database_dir = r'C:\zht\OneDrive\script\rf\stock_monitor\marketdata'
    filenames=os.listdir(database_dir)
    stocklist=[fn[:-4] for fn in filenames if fn.endswith('.csv')]
    return stocklist

def get_stock_data(stockname,length=None):
    '''
    stockname:'000001.SZ'
    return:df of the stock with suspended bars deleted
    '''
    df=pd.read_csv(database_dir+'\\%s.csv'%stockname,index_col=0)
    df.index=[pd.Timestamp(nd) for nd in df.index]
    df=df.dropna(axis=0,how='any') #drop the missing bars
    df=df.drop(df[df['volume'] == 0.0].index) #drop those suspended bars
    if length:
        return df.iloc[-length:-1]#sometimes the last row has some null values
    else:
        return df[:-1]










