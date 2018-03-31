#-*-coding: utf-8 -*-
#@author:tyhj


'''
https://www.joinquant.com/post/131
'''
from data import datahandler_all
import pandas as pd
import talib
import matplotlib.pyplot as plt

# def macd(price,fastperiod=12,slowperiod=26,signalperiod=9):
#     ewma12=pd.ewma(price,span=fastperiod,min_periods=fastperiod/2)
#     ewma60=pd.ewma(price,span=slowperiod,min_periods=slowperiod/2)
#     dif=ewma12-ewma60
#     dea=pd.ewma(dif,span=signalperiod,min_periods=signalperiod/2)
#     bar=(dif-dea)
#     return dif,dea,bar

def macd(priceSeries,fastperiod=12,slowperiod=26,signalperiod=9):
    '''
    Parameters:
    priceSeries - A pandas Series
    '''
    ewma12=priceSeries.ewm(span=fastperiod,min_periods=fastperiod/2).mean()
    ewma60 = priceSeries.ewm(span=slowperiod, min_periods=slowperiod/2).mean()
    dif=ewma12-ewma60
    dea=dif.ewm(span=signalperiod,min_periods=signalperiod/2).mean()
    bar=(dif-dea)
    return dif,dea,bar

df=datahandler_all.get_data('002074.SZ')
df=df.iloc[-400:]
m,signal,hist=talib.MACD(df['Close'].values,fastperiod=12,slowperiod=26,signalperiod=9)
mydif,mydea,mybar=macd(df['Close'],fastperiod=12,slowperiod=26,signalperiod=9)

# fig = plt.figure(figsize=[18,5])
# plt.plot(df.index,m,label='macd dif')
# plt.plot(df.index,signal,label='signal dea')
# plt.plot(df.index,hist,label='hist bar')
# plt.plot(df.index,mydif,label='my dif')
# plt.plot(df.index,mydea,label='my dea')
# plt.plot(df.index,mybar,label='my bar')
# plt.legend(loc='best')

for window in [10,20,50,70,100,120]:
    df['ma%s'%window]=df['Close'].rolling(window=window,min_periods=window).mean()
# df.to_csv('test.csv')

df[['Close','ma10','ma50','ma120']].plot()

slowma=df['Close'].rolling(20).mean()
slowmstd=df['Close'].rolling(20).std()
fastma=df['Close'].rolling(10).mean()
fastmstd=df['Close'].rolling(10).std()

fig=plt.figure()
plt.plot(df.index,df['Close'],'k')
plt.plot(slowma.index,slowma,'b')
plt.fill_between(slowmstd.index,slowma-2*slowmstd,slowma+2*slowmstd,color='r',alpha=0.2)
plt.fill_between(slowmstd.index,slowma-slowmstd,slowma+slowmstd,color='b',alpha=0.2)
# plt.fill_between(fastmstd.index,fastma-2*fastmstd,fastma+2*fastmstd,color='b',alpha=0.4)

def mean_reversion(priceSeries,narrow=1,broad=2,window=20):
    '''
    Parameters:
    priceSeries - A pandas Series of price
    narrow - narrow line
    broad - broad line
    '''
    ma=priceSeries.rolling(window).mean()
    mstd=priceSeries.rolling(window).std()
    fig=plt.figure()
    plt.plot(priceSeries.index,priceSeries,'k')
    plt.plot(ma.index,ma,'b')
    plt.fill_between(mstd.index,ma-broad*mstd,ma+broad*mstd,color='r',alpha=0.2)
    plt.fill_between(mstd.index,ma-narrow*mstd,ma+narrow*mstd,color='b',alpha=0.4)
    plt.fill_between(mstd.index,ma-broad*mstd,ma-narrow*mstd,color='r',alpha=0.2)
    plt.fill_between(mstd.index,ma-narrow*mstd,ma,color='b',alpha=0.4)
    #TODO:analyze more frequently bars to find the 'buy signal'. For example,we can regress the \
    #TODO:those bars the movement,if the movement is toward the narrow line,buy it.
    #TODO:This strategy may be great in the oscillation market.


if __name__=='__main__':
    mean_reversion(df['Close'])










