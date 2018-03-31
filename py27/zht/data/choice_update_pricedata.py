#-*-coding: utf-8 -*-
#@author:tyhj
from EmQuantAPI import *
import time
import datetime
import tool
import os
import pandas as pd
import numpy as np
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

def initialises_df(stocklist):
    #initialises the df for every stock
    # indicators = open(r'C:\zht\OneDrive\script\rf\stock_monitor\file\indicators.txt').read().split('\n')
    indicators = 'OPEN,HIGH,LOW,CLOSE,AVERAGE,TURN,VOLUME,AMOUNT,TNUM'.lower()
    for stock in stocklist:
        df=pd.DataFrame(columns=indicators)
        df.to_csv(r'C:\zht\OneDrive\script\rf\stock_monitor\marketdata\%s.csv' % stock)

def update_old_stocklist(stocklist_old,enddate=None):
    loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
    # try:
    #     startdate=__get_former_date()
    # except:
    #     startdate='20090101'
    startdate=__get_former_date()
    if enddate==None:
        enddate=time.strftime('%Y%m%d',time.localtime(time.time()))
    tradedates=get_tradedates(startdate,enddate)
    tradedates=[t[:4]+'-'+t[4:6]+'-'+t[6:] for t in tradedates]
    indicators = open(r'C:\zht\OneDrive\script\rf\stock_monitor\file\indicators.txt').read().split('\n')

    for tradedate in tradedates:
        flag=1
        while flag:
            try:
                data = c.css(codes=','.join(stocklist_old), indicators=','.join(indicators), \
                             options='Tradedate=%s,AdjustFlag=3' % tradedate).Data
                flag=0
            except Exception as e:
                print e
                loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
        for sn in stocklist_old:
            #replace the last row,since there may be something lost in the last row.
            old_df=pd.read_csv(database_dir+'\%s.csv' % sn,index_col=0)
            old_df.loc[tradedate]=data[sn]
            #notice that there may be same indexers.
            old_df.index.drop_duplicates(keep='last')
            old_df.to_csv(database_dir+'\%s.csv'%sn)
            print 'updating ',tradedate,sn,data[sn]

# def update_new_stocklist(stocklist_new,enddate=None):
#     initialises_df(stocklist_new)
#     loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
#     startdate='20090101'
#     if enddate==None:
#         enddate=time.strftime('%Y%m%d',time.localtime(time.time()))
#     tradedates=get_tradedates(startdate,enddate)
#
#     # indicators = open(r'C:\zht\OneDrive\script\rf\stock_monitor\file\indicators.txt').read().split('\n')
#     indicators='OPEN,HIGH,LOW,CLOSE,AVERAGE,TURN,VOLUME,AMOUNT,TNUM'
#     for tradedate in tradedates:
#         flag=1
#         while flag:
#             try:
#                 data = c.css(codes=','.join(stocklist_new), indicators=','.join(indicators), \
#                              options='Tradedate=%s,AdjustFlag=3' % tradedate).Data
#                 flag=0
#             except Exception as e:
#                 print e
#                 loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
#         for sn in stocklist_new:
#             #replace the last row,since there may be something lost in the last row.
#             old_df=pd.read_csv(database_dir+'\%s.csv' % sn,index_col=0)
#             old_df.loc[int(tradedate)]=data[sn]
#             #notice that there may be same indexers.
#             old_df.index.drop_duplicates(keep='last')
#             old_df.to_csv(database_dir+'\%s.csv'%sn)
#             print tradedate,sn,data[sn]

def update_new_stocklist(stocklist_new):
    loginResult = c.start('rflh0000', '719181', "ForceLogin=1")
    indicators = 'OPEN,HIGH,LOW,CLOSE,AVERAGE,TURN,VOLUME,AMOUNT,TNUM'
    startdate='20090101'
    enddate=datetime.datetime.today().strftime('%Y%m%d')
    for stockname in stocklist_new:
        flag=1
        while flag:
            try:
                data = c.csd(stockname, indicators, startdate, enddate, 'Period=1,AdjustFlag=3')#note:3 represents qfq in csc,but 1 represent qfq in css
                flag=0
            except Exception as e:
                print e
                c.start('rflh0000', '719181', "ForceLogin=1")

        pricedata = data.Data[stockname]
        pricedata = np.array(pricedata).transpose()
        dates = data.Dates
        dates = [d.replace('/', '-') for d in dates]
        df = pd.DataFrame(index=dates, data=pricedata, columns=indicators.lower().split(','))
        df.to_csv(database_dir+'\%s.csv'%stockname)
        print 'getting %s...'%stockname


def get_old_stocklist_and_new_stocklist():
    stocklist1=get_stocklist_in_database()
    path=os.getcwd()
    parent_path=os.path.dirname(path)
    stocklist2=open(os.path.join(parent_path,'file\\stocklist.txt')).read().split('\n')
    stocklist_new=list(set(stocklist2).difference(set(stocklist1)))
    return stocklist1,stocklist_new

def run():
    stocklist_old,stocklist_new=get_old_stocklist_and_new_stocklist()
    if len(stocklist_old)>0:
        update_old_stocklist(stocklist_old)
    if len(stocklist_new)>0:
        update_new_stocklist(stocklist_new)



# def tmp_run():
#     stocklist=['300136.SZ','300236.SZ','300499.SZ','000922.SZ','000019.SZ','600838.SH','000930.SZ','600097.SH','600072.SH','600685.SH']
#

if __name__=='__main__':
    run()
