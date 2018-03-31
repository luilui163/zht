#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import os
from tyhj.data.config import  DATA_BASE_DIR
from tyhj.util import pathu,stru

__all__=['getAllstockIds','getStockDf']


def getAllstockIds():
    fileNames=os.listdir(DATA_BASE_DIR)
    stockIds=[fn[:-4] for fn in fileNames]
    return stockIds

def getStockDf(stockId,sDate='2003-01-01',length=None):#TODO:which day to start? reform?
    sDate=stru.extractDate(sDate)
    path=pathu.getStockDfPath(stockId)
    df=pd.read_csv(path,index_col=0,parse_dates=True) #using parse_dates to set the index as timestamp

    df=df.loc[sDate:]
    if length:
        return df[-length:]
    else:
        return df

def _getReturn(stockId,logR):
    '''
    :param stockId:str
    :param logR:True or False,if True,return log return,else return relative return
    :return: pandas series
    '''
    df=getStockDf(stockId)

    if logR:
        return np.log(df['close'])-np.log(df['close'].shift(1))
    else:
        return df['close'].pct_change()

def getReturn(stockIds,logR=False):
    '''
    :param stockIds:str or list
    :param logR: True of False ,if True,return log return,or return ordinary return
    :return: pandas dataframe,even if there is only one stock,the format is still
        dataframe,rather than pandas series
    '''
    if not isinstance(stockIds,(str,list)):
        raise TypeError('stockIds should be a str or a list of str')

    if isinstance(stockIds,str):
        return _getReturn(stockIds,logR).to_frame(name=stockIds)

    elif isinstance(stockIds,list):
        returnDf=pd.DataFrame()
        for stockId in stockIds:
            returnDf[stockId]=_getReturn(stockId,logR)
        return returnDf


def getClosePriceDf(stockIds):
    if not isinstance(stockIds,list):
        raise TypeError('stockIds should be a list')
    closeDf=pd.DataFrame()
    for stockId in stockIds:
        closeDf[stockId]=getStockDf(stockId)['close']
        print stockId
    return closeDf

def getPanelDf(stockIds,colname='close'):
    '''
    :param stockIds:list
    :param colname:str,the target colname to extract
    :return: dataframe
    '''
    if not isinstance(colname,str):
        raise ValueError('the colname should be a str')
    df=pd.DataFrame()
    for stockId in stockIds:
        df[stockId]=getStockDf(stockId)[colname]
        print 'Getting stock:%s'%stockId
    return df


# stockIds=getAllstockIds()[:10]
#
# closeDf=getClosePriceDf(stockIds)
# print closeDf.head()
