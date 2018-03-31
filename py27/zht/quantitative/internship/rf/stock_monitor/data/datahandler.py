#-*-coding: utf-8 -*-
#@author:tyhj
from EmQuantAPI import *
import time
import tool
import os
import pandas as pd
import csv
from data.settings import database_dir


def get_stocklist_in_database():
    # database_dir = r'C:\zht\OneDrive\script\rf\stock_monitor\marketdata'
    filenames=os.listdir(database_dir)
    stocklist=[fn[:-4] for fn in filenames if fn.endswith('.csv')]
    return stocklist

def __get_former_date():
    # database_dir=r'C:\zht\OneDrive\script\rf\stock_monitor\marketdata'
    filenames=os.listdir(database_dir)
    filenames=[fn for fn in filenames if fn.endswith('.csv')]
    df=pd.read_csv(database_dir+'\%s'%filenames[-1],index_col=0)
    former_date=df.index[-1]
    return str(former_date)

def get_tradedates(startdate,enddate=None):
    loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
    '''
    type:'20161111'
    if enddate==startdate,then the startdate will be returned
    '''
    if enddate==None:
        enddate=time.strftime('%Y%m%d',time.localtime(time.time()))
    tradedates=c.tradedates(startdate,enddate).Data
    tradedates=[tool.normalize_date_format(td) for td in tradedates]
    return tradedates

def initialises_df(stocklist,indicators):
    #initialises the df for every stock
    for stock in stocklist:
        df=pd.DataFrame(columns=indicators)
        df.to_csv(r'C:\zht\OneDrive\script\rf\stock_monitor\marketdata_target\%s.csv' % stock)

def update_history_marketdata(enddate=None):
    loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
    # try:
    #     startdate=__get_former_date()
    # except:
    #     startdate='20090101'
    startdate=__get_former_date()
    if enddate==None:
        enddate=time.strftime('%Y%m%d',time.localtime(time.time()))
    # startdate='20090101'
    tradedates=get_tradedates(startdate,enddate)

    stocknames=get_stocklist_in_database()
    indicators = open(r'C:\zht\OneDrive\script\rf\stock_monitor\file\indicators.txt').read().split('\n')

    for tradedate in tradedates:
        flag=1
        while flag:
            try:
                data = c.css(codes=','.join(stocknames), indicators=','.join(indicators), \
                             options='Tradedate=%s,AdjustFlag=3' % tradedate).Data
                flag=0
            except Exception as e:
                print e
                loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
        for sn in stocknames:
            #replace the last row,since there may be something lost in the last row.
            old_df=pd.read_csv(database_dir+'\%s.csv' % sn,index_col=0)
            old_df.loc[int(tradedate)]=data[sn]
            #notice that there may be same indexers.
            old_df.index.drop_duplicates(keep='last')
            old_df.to_csv(database_dir+'\%s.csv'%sn)
            print tradedate,sn,data[sn]

def get_data(stockname,length=None):
    '''
    stockname:'000001.SZ'
    return:df of the stock with suspended bars deleted
    '''
    df=pd.read_csv(database_dir+'\\%s.csv'%stockname,index_col=0)
    ind=list([str(m) for m in df.index])
    new_ind=[d[:4]+'-'+d[4:6]+'-'+d[6:] for d in ind]
    df.index=[pd.Timestamp(nd) for nd in new_ind]
    df=df.dropna(axis=0,how='any') #drop the missing bars
    df=df.drop(df[df['Volume'] == 0.0].index) #drop those suspended bars
    if length:
        return df.iloc[-length:]
    else:
        return df

def tmp_update_history_marketdata(enddate=None):
    loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
    if enddate==None:
        enddate=time.strftime('%Y%m%d',time.localtime(time.time()))
    startdate=__get_former_date()
    tradedates=get_tradedates(startdate,enddate)

    stocknames=[fn[:-4] for fn in get_filelist() if fn.endswith('.csv')]
    indicators = open(database_dir+'\indicators.txt').read().split('\n')

    for tradedate in tradedates:
        sn = '002074.SZ'
        flag=1
        while flag:
            try:
                data = c.css(codes=sn, indicators=','.join(indicators), \
                             options='Tradedate=%s,AdjustFlag=3' % tradedate).Data
                flag=0
            except Exception as e:
                print e
                time.sleep(1)
                loginResult = c.start('rflh0000', '719181', "ForceLogin=1")

        #replace the last row,since there may be something lost in the last row.
        old_df=pd.read_csv(database_dir+'\%s.csv' % sn,index_col=0)
        old_df.loc[int(tradedate)]=data[sn]
        #notice that there may be same indexers.
        # old_df.drop_duplicates(keep='last',inplace=True)
        old_df.index.drop_duplicates(keep='last')
        old_df.to_csv(database_dir+'\%s.csv'%sn)

        print tradedate,data[sn]

        # row=[tradedate]+data[sn]
        # with open(filedir+'\%s.csv'%sn,'a+') as f:
        #     f_csv=csv.writer(f)
        #     f_csv.writerow(row)
        # print row

if __name__=='__main__':
    # stocklist=open(r'C:\zht\OneDrive\script\rf\stock_monitor\20161201.txt').read().split('\n')
    # indicators=open(r'C:\zht\OneDrive\script\rf\stock_monitor\file\indicators.txt').read().split('\n')
    # initialises_df(stocklist,indicators)
    update_history_marketdata()
    # update_history_marketdata()
