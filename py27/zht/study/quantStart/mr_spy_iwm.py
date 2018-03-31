#-*-coding: utf-8 -*-
#@author:tyhj

import matplotlib.pylot as plt
import numpy as np
import os,os.path
import pandas as pd

def create_pairs_dataframe(datadir,symbols):
    '''
    Create a pandas DataFrame containing the closing price of a
    paair of symbols based on CSV files containing a date time
    stamp and OHLCV data.
    '''

    #Open the individual CSV files and read
    print 'Importing CSV data...'
    sym1=pd.io.parses.read_csv(os.path.join(datadir,'%s.csv'%symbols[0]),
            header=0,index_col=0,names=['datetime','open','high','low','close','volume','na'])
    sym2=pd.io.parses.read_csv(os.path.join(datadir,'%s.csv'%symbols[1]),
            header=0,index_col=0,names=['datetime','open','high','low','close','volume','na'])

    #create a pandas DataFrame with the close prices of each symbol
    #correctly aligned and dropping missing entries
    print 'constructing dual matrix for %s and %s...'%symbols
    pairs=pd.DataFrame(index=sym1.index)
    pairs['%s_close'%symbols[0].lower()]=sym1['close']
    pairs['%s_close'%symbols[1].lower()]=sym2['close']
    pairs=pairs.dropna()
    return pairs

def calculate_spread_zscore(pairs,symbols,lookback=100):
    '''
    Creates a hedge ratio between the two symbols by calculating a
    rolling linear regression with a defined lookback period.This
    is then used to create a z-score of the 'spread' between' the two
    symbols based on a linear combination of the two.
    '''

    #Use the pandas Ordinary Least Squares method to fit a rolling
    #linear regression between the two closing price time series
    print 'Fitting the rolling Linear Regression...'
    model=pd.ols(y=pairs['%s_close'%symbols[0].lower()],
                 x=pairs['%s_close'%symbols[1].lower()],
                 window=lookback)

    #Construct the hedge ratio and eliminate the first
    #lookback-length empty/NaN period
    pairs['hedge_ratio']=model.beta['x']
    pairs=pairs.dropna()

    #Create the spread and then a z-score of the spread
    print 'Creating the spread/zscore columns...'
    pairs['spread']=pairs['%s_close'%symols[0].lower()]-pairs['hedge_ratio']*pairs['%s_close'%symbols[1].lower()]
    pairs['zscore']=(pairs['spread']-np.mean(pairs['spread']))/np.std(pairs['spread'])
    return pairs

def create_long_short_market_signals(pairs,symbols,z_entry_threshold=2.0,z_exit_threshold=1.0):
    '''
    Create the entry/exit signals based on the exceeding of z_enter_threshold
    for entering a position and falling below z_exit_threshold for exiting
    a position.
    '''
    #Calculate when to be long,short and when to exit
    pairs['longs']=(pairs['zscore']<=-z_entry_threshold)*1.0
    pairs['shorts']=(pairs['zscore'])>=z_entry_threshold)*1.0
    pairs['exits']=(np.abs(pairs['zscore'])<=z_exit_threshold)*1.0

    #The signals are needed because we need to propagate a
    #position forward,i.e.we need to stay long if the ascore
    #threshold is less than z_entry_threshold by still greater
    #than z_exit_threshold,and vice versa for shorts
    pairs['long_market']=0.0
    pairs['short_market']=0.0

    #These variables track whether to be long or short while
    #iterating through the bars
    long_market=0
    short_market=0

    #Calculates when to actually be 'in' the market,i.e.to have a
    #long or short position,as well as when not to be.
    #Since this is using iterrows to loop over a dataframe,it will
    #be significantly less efficient than a vectorised operation,i.e. slow!
    print 'Calculating when to be in the market (long or short)...'
    for i,b in enumerate(pairs.iterrows()):
        #Calculate longs
        if b[1]['longs']==1.0:
            long_market=1
        #calculate shorts
        if b[1]['shorts']==1.0:
            short_market=1
        #Calculate exists
        if b[1]['exits']==1.0:
            long_market=0
            short_market=0
        #This directly assigns a 1 or 0 to the long_market/short_market
        #columns,such that the strategy knows when to actually stay in!
        pairs.ix[i]['long_market']=long_market
        pairs.ix[i]['short_market']=short_market
    return pairs

def create_portfolio_returns(pairs,symbols):
    '''
    Create a portfolio pandas DataFrame which keeps track
    of the account equity and utimately generates an equity
    curve.
    This can be used to generate drawdown and risk/reward ratios.
    '''

    #Convenience variables for symbols
    sym1=symbols[0].lower()
    sym2=symbols[1].lower()

    #Construct the portfolio object with positions informations
    #Note that minuses to keep track of shorts!
    print 'Constructing a portfolio...'
    portfolio=pd.DataFrame(index=pairs.index)
    portfolio['positions']=pairs['long_market']-pairs['short_market']
    portfolio[sym1]=-1.0*pairs['%s_close'%sym1]*portfolio['positions']
    portfolio[sym2]=pairs['%s_close'%sym2]*portfolio['positions']
    portfolio['total']=portfolio[sym1]+portfolio[sym2]

    #Construct a percentage returns stream and eliminate all
    #of the NaN and -inf/+inf cells
    print 'Constructing the equity curve...'
    portfolio['returns']=portfolio['total'].pct_change()
    portfolio['returns'].fillna(0.0,inplace=True)
    portfolio['returns'].replace([np.inf,-np.inf],0.0,inplace=True)
    portfolio['returns'].replace(-1.0,0.0,inplace=True)

    #Calculate the full equity curve
    portfolio['returns']=(portfolio['returns']+1.0).cumprod()
    return portfolio

if __name__=='__main__':
    datadir='/your/path/to/data/'
    symbol=('SPY','IWM')

    lookbacks=range(50,210,10)
    returns=[]

    #Adjust lookback period from 50 to 200 increments
    #of 10 in order to produce sensitivities
    for lb in lookbacks:
        print 'Calculating lookback=%s...'%lb
        pairs=create_pairs_dataframe(datadir,symbols)
        pairs=calculate_spread_zscore(pairs,symbols,lookback=lb)
        pairs=create_long_short_market_signals(pairs,symbols,
                                               z_entry_threshold=2.0,
                                               z_exit_threshold=1.0)
        portfolio=create_portfolio_returns(pairs,symbols)
        returns.append(portfolio.ix[-1]['returns'])

        print 'Plot the lookback-performance scatterchart...'
        plt.plot(lookbacks,returns,'-o')
        plt.show()


    print 'Ploting the performance charts...'
    fig=plt.figure()
    fig.patch.set_facecolor('white')

    ax1=fig.add_subplot(211,ylabel='%s growth (%%)'%symbols[0])
    (pairs['%s_close'%symbols[0].lower()].pct_change()+1.0).cumprod().plot(ax=ax1,color='r',lw=2.)

    ax2=fig.add_subplot(212,ylabel='Portfolio value growth (%%)')
    portfolio['returns'].plot(ax=ax2,lw=2.)

    fig.show()



