#-*-coding: utf-8 -*-
#@author:tyhj
import time
from tyhj.data import dataApi
from cached_property import cached_property

def getSignal():
    '''
    produce trading signal
    :return: pandas dataframe with column=['stockId1','stockId2',...],index=['date1','date2',...]
        the value in dataframe cell represents the shares to trade.
    '''
    stockIds = dataApi.getAllstockIds()[:10]
    logRet=dataApi.getReturn(stockIds,logR=True)

    signal=logRet
    signal=signal.shift(1)   #TODO:the signal is produced at time T,and it will be traded at time T+1
    signal=signal.iloc[range(1,3000,53),:]


    signal=signal.dropna(axis=0,how='all')

    print signal.head()
    return signal



def unifyTradingVolumeUnit():
    pass



class Backtest(object):
    def __init__(self,signal,name='unknown'):
        '''
        :param signal: pandas dataframe
        :param name: str
        '''
        self.name = name
        self.signal=signal
        self.stockIds=list(signal.columns)

        self.runTime=time.strftime('%Y-%m-%d %H:%M',time.localtime())


    def __rper__(self):
        return 'Backtest(%s,%s)'%(self.name,self.runTime)


    def _ContructContext(self):
        #TODO: trading with open price,but the equity is computed based on the close price.
        #so,an effective method is need to get closePrice Df and openPrice Df.
        pass

    @cached_property
    def tradePrice(self):
        '''
        get the trading price for every stock,the default price is open price.
        :return: dataframe
        '''
        oPrice=dataApi.getPanelDf(self.stockIds,colname='open')
        tradePrice=oPrice.loc[self.signal.index,self.signal.columns]
        return tradePrice

    def positions(self):
        '''

        :return:
        '''


    def performance(self):
        pass

    def summary(self):
        pass

    def plot(self):
        #maxdd
        pass

    def outputLatex(self):
        pass





#TODO:hit or harder



class Position(object):
    def __init__(self):
        pass





