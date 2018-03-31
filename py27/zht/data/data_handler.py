#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import os
import datetime
import numpy as np
from zht import tool


def get_df(code,database_path=r'C:\data\gx\csvdata\stock_hfq'):
    '''
    :param code:like 000001.SZ
    :param database_path:
    :return:
    '''
    df=pd.read_csv(os.path.join(database_path,code+'.csv'),index_col=0)
    return df

def get_code_list(database_path=r'C:\data\gx\csvdata\stock_hfq'):
    file_names=os.listdir(database_path)
    codes=[fn[:-4] for fn in file_names]
    return codes

def get_valid_codes(database_path=r'C:\data\gx\csvdata\stock_hfq',least_length=500):
    '''
    valid_codes means the length of trading day is larger than least_length
    :param database_path:
    :return:
    '''
    codes=get_code_list(database_path)
    valid_codes=[]
    for code in codes:
        df=get_df(code)
        if len(df)>=least_length:
            valid_codes.append(code)
    return valid_codes

def get_index_df(index_code='000300',database_path=r'c:\data\gx\csvdata\index_hfq'):
    df=pd.read_csv(os.path.join(database_path,index_code+'.csv'),index_col=0)
    return df

def preprocess_data():
    '''
    delete the first 20 ticker if a stock is newly listed
    '''
    # TODO:preprocess the market data,such as newly listed and etc.
    # get the listed date,and delete the first several day
    pass

def calculate_return_df():
    '''
    the invalid the data will be removed,such as those returns larger than 0.11 and etc.
    :return:dataframe does not incluse hs300
    '''
    # TODO:get the listed date,and delete the first several day
    codes=get_code_list()
    df=pd.DataFrame()
    for code in codes:
        df[code]=get_df(code)['close']
        print code
    # df['hs300']=get_index_df()['close']
    df=df.pct_change()
    df[abs(df)>0.11]=np.NaN #handle the invalid data
    df.to_csv(r'C:\data\gx\csvdata\returns.csv')

def get_return_df():
    df=pd.read_csv(r'C:\data\gx\csvdata\returns.csv',index_col=0)
    return df

#get the intersection filenames of a dir,which has several subdirs
def get_intersection_filenames(dir):
    subNames=os.listdir(dir)
    filenames=os.listdir(os.path.join(dir,subNames[0]))
    for subName in subNames[1:]:
        filenamesTmp=os.listdir(os.path.join(dir,subName))
        filenames=list(set(filenames).intersection(set(filenamesTmp)))
    filenames.sort()
    return filenames


def get_lrets(code):
    close_price=get_df(code)['close']
    close_price=tool.index_to_datetime(close_price)
    lrets=tool.get_log_return(close_price)
    return lrets



