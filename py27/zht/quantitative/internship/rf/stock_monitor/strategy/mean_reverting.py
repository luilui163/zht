#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from data import datahandler_all
'''
strategy introduction:
According to the mean reversion ideology.When the stock price is below the broad line and
have a growing movement, buy it in the next trading period,around the  broadline and clear
the position at the narrow line.If the stock turn around after we holding it and continue
to go down,then stop the lose at the broad line and waiting the opportunity to hold it again.

Open position when the price hits the 2 standard deviation band for two consective times
Close position when the ratio hits the mean(or 1 standard deviation band)

1,use long ma line short ma line open or close signals
2,use the deviation from ma as signals
3,how to get ma,equil weighted or expotentially weighted pd.ewma()


Notice:
This strategy may be only effective in the oscilision market.

stop loss method:
if the stock is not in line with the predicted movement and it has broken through the stop line,
clear the position.


'''
narrow=1
stop=1.1
broad=2
window=70


strategy_params = {
    "short_window": 500,
    "long_window": 2000
}


def mean_reversion(df,narrow=1,broad=2,window=20):
    '''
    Parameters:
    df['Close'] - A pandas Series of price
    narrow - narrow line
    broad - broad line
    '''
    ma=df['Close'].rolling(window).mean()
    mstd=df['Close'].rolling(window).std()
    fig=plt.figure()
    plt.plot(df['Close'].index,df['Close'],'blue')
    plt.plot(ma.index,ma,'red')
    plt.fill_between(mstd.index,ma-broad*mstd,ma+broad*mstd,color='y',alpha=0.2)
    plt.fill_between(mstd.index,ma-narrow*mstd,ma+narrow*mstd,color='magenta',alpha=0.4)
    plt.fill_between(mstd.index,ma-broad*mstd,ma-narrow*mstd,color='r',alpha=0.2)
    plt.fill_between(mstd.index,ma-narrow*mstd,ma,color='b',alpha=0.4)
    #TODO:analyze more frequently bars to find the 'buy signal'. For example,we can regress the \
    #TODO:those bars the movement,if the movement is toward the narrow line,buy it.
    #TODO:This strategy may be great in the oscillation market.


def get_buy_signal(df):
    df['ma%s'%window]=df['Close'].rolling(window).mean()
    df['ma%sstd'%window]=df['Close'].rolling(window).std()
    df['in_line']=df['ma%s'%window]-broad*df['ma%sstd'%window]
    df['stop_line']=df['ma%s'%window]-stop*df['ma%sstd'%window]
    df['out_line']=df['ma%s'%window]-narrow*df['ma%sstd'%window]
    # df['signal']=np.NaN
    # df.loc[(df['Close']<df['in_line']),'signal']=1 #buy in
    # df.loc[(df['Close']>=df['out_line']),'signal']=-1 #clear the position
    return df


#the postion should be construct during the movement toward in_line from downside bottom
#to top  ,
#rather than during it just hit the in_line from above.
def get_signal(df):
    df['ma%s'%window]=df['Close'].rolling(window).mean()
    df['ma%sstd'%window]=df['Close'].rolling(window).std()
    df['in_line']=df['ma%s'%window]-broad*df['ma%sstd'%window]
    df['stop_line']=df['ma%s'%window]-stop*df['ma%sstd'%window]
    df['out_line']=df['ma%s'%window]-narrow*df['ma%sstd'%window]
    df['signal']=np.NaN
    df['current_position']=0
    for i in range(1,len(df.index)):
        if df['current_position'].values[i-1]==0 and df['Close'].values[i]<df['in_line'].values[i]:
            df['signal'].values[i]=1
            df['current_position'].values[i]=1
        elif df['current_position'].values[i-1]==1 and (df['Close'].values[i]<df['stop_line'].values[i] or df['Close'].values[i]>=df['out_line'].values[i]):
            df['signal'].values[i]=-1
            df['current_position'].values[i]=0
    return df


def visualize_the_signal(stock_name,df):
    fig=plt.figure()
    plt.plot(df.index,df['Close'])
    plt.plot(df[df['signal']==1].index,df['Close'][df['signal']==1],'^',markersize=5,color='m')
    plt.plot(df[df['signal']==-1].index,df['Close'][df['signal']==-1],'v',markersize=5,color='orange')
    plt.fill_between(df.index,df['in_line'],df['out_line'],color='goldenrod',alpha=0.2)
    # plt.fill_between(df.index,df['out_line'],df['Close'],color='lime',alpha=0.2)
    fig.savefig(r'c:\trash\%s.png'%stock_name)
    print stock_name


stock_names = datahandler_all.get_stocklist_in_database()
stock_name=stock_names[0]
df = datahandler_all.get_data(stock_name, 1000)
df = get_signal(df)
visualize_the_signal(stock_name, df)


# def portfolio(df):
#     df['returns_avg']=df['AvgPrice'].pct_change()
#     cash=[1]
#     pnl=[0]
#     for i in range(1,df.index):
#         if df['signal']==1











