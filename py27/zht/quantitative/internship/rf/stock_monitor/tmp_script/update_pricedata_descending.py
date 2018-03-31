# -*-coding: utf-8 -*-
# @author:tyhj
from EmQuantAPI import *
import time
import tool
import os
import pandas as pd
import csv
import datetime
import threading

def get_database_path():
    abspath = os.getcwd()
    parentpath = '\\'.join(abspath.split('\\')[:-1])
    database_path = parentpath + '\\' + 'pricedata'
    return database_path

def get_stocklist_of_today():
    today=datetime.datetime.today()
    today=today.strftime('%Y%m%d')
    c.start('rflh0000', '719181', "ForceLogin=1")
    data=c.sector('2000032254',today).Data
    stocklist=[data[i] for i in range(0,len(data),2)]
    return stocklist

def get_stocklist_in_database():
    database_path =get_database_path()
    filenames=os.listdir(database_path)
    stocklist=[fn[:-4] for fn in filenames if fn.endswith('.csv')]
    return stocklist

def get_tradedates(startdate, enddate=None):
    c.start('rflh0000', '719181', "ForceLogin=1")
    '''
    type:'20161111'
    if enddate==startdate,then the startdate will be returned
    '''
    if enddate == None:
        enddate = time.strftime('%Y%m%d', time.localtime(time.time()))
    tradedates = c.tradedates(startdate, enddate).Data
    tradedates = [tool.normalize_date_format(td) for td in tradedates]
    return tradedates

def initialises_df(stocklist,indicators):
    #initialises the df for every stock
    database_path=get_database_path()
    for stock in stocklist:
        df=pd.DataFrame(columns=indicators)
        df.to_csv(database_path+'\\%s.csv' % stock)

def get_former_date():
    # database_dir=r'C:\zht\OneDrive\script\rf\stock_monitor\marketdata'
    database_path=get_database_path()
    filenames=os.listdir(database_path)
    filenames=[fn for fn in filenames if fn.endswith('.csv')]
    df=pd.read_csv(database_path+'\%s'%filenames[-1],index_col=0)
    former_date=df.index[0]
    return str(former_date)

def save_df(data,q):
    while not q.empty():
        sn=q.get()
        old_df = pd.read_csv(database_path + '\%s.csv' % sn, index_col=0)
        old_df.loc[int(tradedate)] = data[sn]
        # notice that there may be same indexers.
        old_df.index.drop_duplicates(keep='last')
        old_df.to_csv(database_path + '\%s.csv' % sn)
        print tradedate, sn, data[sn]

def multi_save_df(data,q):
    ths=[]
    for i in range(10):
        th=threading.Thread(target=save_df,args=[data,q])
        ths.append(th)
    for i in range(10):
        ths[i].start()
    for i in range(10):
        ths[i].join()

def update_history_marketdata(startdate='20090101',enddate=None):
    database_path=get_database_path()
    c.start('rflh0000', '719181', "ForceLogin=1")
    if enddate == None:
        enddate = get_former_date()
    tradedates = get_tradedates(startdate, enddate)
    #construct dataframes for the new listed stocks
    stocknames = get_stocklist_of_today()
    stocknames_old = get_stocklist_in_database()
    stocklist_new=[s for s in stocknames if s not in stocknames_old]
    indicators = open('indicators.txt').read().split('\n')
    initialises_df(stocklist_new,indicators)

    for tradedate in tradedates[::-1]:
        flag = 1
        while flag:
            try:
                data = c.css(codes=','.join(stocknames), indicators=','.join(indicators), \
                             options='Tradedate=%s,AdjustFlag=3' % tradedate).Data
                flag = 0
            except Exception as e:
                print e
                c.start('rflh0000', '719181', "ForceLogin=1")
        for i,sn in enumerate(stocknames):
            # replace the last row,since there may be something lost in the last row.
            old_df = pd.read_csv(database_path + '\%s.csv' % sn, index_col=0)
            old_df.loc[int(tradedate)] = data[sn]
            # notice that there may be same indexers.
            old_df.index.drop_duplicates(keep='last')
            old_df=old_df.sort_index(ascending=True)
            old_df.to_csv(database_path + '\%s.csv' % sn)
            print tradedate, i,sn


if __name__ == '__main__':
    # stocklist=open(r'C:\zht\OneDrive\script\rf\stock_monitor\20161201.txt').read().split('\n')
    # indicators=open(r'C:\zht\OneDrive\script\rf\stock_monitor\file\indicators.txt').read().split('\n')
    # initialises_df(stocklist,indicators)

    update_history_marketdata('20150101')


