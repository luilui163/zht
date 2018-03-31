#-*-coding: utf-8 -*-
#@author:tyhj
import time
from data.config import  DATA_BASE_DIR
import pandas as pd
import tushare as ts
import os
from util.dateu import getToday
from util.fileu import getModificationTime
from util.pathu import getStockDfPath
import datetime
from data.dataApi import getAllstockIds,getStockDf

def saveMarketData():
    '''
    save all the market data until the last trade date
    :return:
    '''
    basics=ts.get_stock_basics()
    stockIds=basics.index.tolist()
    localIds=getAllstockIds()
    newIds=[d for d in stockIds if d not in localIds]
    oldIds=[d for d in stockIds if d in localIds]

    for i,stockId in enumerate(newIds):
        print 'Saving stock:%s  %s/%s' % (stockId,i+1,len(newIds))
        df=_getDfFromTushare(stockId)
        if not df.empty:
            df.to_csv(os.path.join(DATA_BASE_DIR,stockId+'.csv'))

    toUpdateIds=[d for d in oldIds if _updateOrNot(d)]
    for i,stockId in enumerate(toUpdateIds):
        _updateStockData(stockId)
        print 'updating stock:%s  %s/%s'%(stockId,i+1,len(toUpdateIds))

def _updateOrNot(stockId):
    '''
    if the modification date != today,then update the data
    :param stockId:
    :return:
    '''
    filePath=getStockDfPath(stockId)
    mDate=getModificationTime(filePath)
    today=getToday()
    if mDate!=today:
        return True
    else:
        return False

def _updateStockData(stockId):
    oldDf=getStockDf(stockId)
    lastDate=oldDf.index[-1]
    newDf=_getDfFromTushare(stockId,sDate=lastDate)
    updatedDf=oldDf[:-1].append(newDf)
    updatedDf.to_csv(os.path.join(DATA_BASE_DIR,stockId+'.csv'))

def _getDfFromTushare(stockId,sDate='1900-01-01'):
    '''
    get 'qfq' data by using tushare API
    :param stockId:stock code without suffix
    :param sDate: start date in the format of 'YYYY-MM-DD'
    :return: dataFrame or None
    '''
    df = ts.get_k_data(stockId, start=sDate,ktype='D', index=False, autype='qfq')
    if not df.empty:#ignore those None df
        df.set_index('date', inplace=True)
        del df.index.name
        del df['code']
    return df


def getIndex():
    df = ts.get_index()
    pass






#TODO:use multithread or/and multiprocess accelerate the process




