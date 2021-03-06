#-*-coding: utf-8 -*-
#@author:tyhj
import numpy as np
import pandas as pd

from tyhj.backtestingWithPandas.base import Strategy,Portfolio
from tyhj.data import dataApi


class RandomForecastingStrategy(Strategy):
    '''
    Derives from Strategy to produce a set of signals that are randomly
    generated long/shorts.Clearly a nonsensical strategy,but perfectly
    acceptable for demonstrating the backtesting infrastructure!
    '''

    def __init__(self,symbol,bars):
        '''Requires the symbol ticker and the pandas DataFrame of bars'''
        self.symbol=symbol
        self.bars=bars

    def generate_signals(self):
        '''Craetes a pandas DataFrame of random signals.'''
        signals=pd.DataFrame(index=self.bars.index)
        signals['signal']=np.sign(np.random.randn(len(signals)))

        #The first five elements are set to zero in order to minimise
        #upstream NaN errors in the forecaster.
        signals['signal'][0:5]=0.0
        return signals

class MovingAverageCrossStrategy(Strategy):
    '''
    Requires:
    symbol-A stock symbol on which to form a strategy on
    bars-A DataFrame of bars for the above symbol
    short_window-Lookback period for short moving average
    long_window-Lookback period for long moving average.
    '''

    def __init__(self,symbol,bars,short_window=10,long_window=20):
        self.symbol=symbol
        self.bars=bars

        self.short_window=short_window
        self.long_window=long_window

    def generate_signals(self):
        '''
        Returns the DataFrame of symbols containing the signals
        to go long,short or hold {1,-1,0}
        '''

        signals=pd.DataFrame(index=self.bars.index)
        signals['signal']=0.0

        #Create the set of short and long simple moving averages
        #over the respective periods
        signals['short_mavg']=self.bars['close'].rolling(self.short_window,min_periods=1).mean()
        signals['long_mavg']=self.bars['close'].rolling(self.long_window,min_periods=1).mean()

        #Create a 'signal' (invested or not invested) when the short moving average cross the long
        #Moving average,but only for the period greater than the shortest moving average window
        signals['signal'][self.short_window:]=np.where(signals['short_mavg'][self.short_window:] \
                                                      >signals['long_mavg'][self.short_window:],1.0,0.0)

        #Take the difference of the signals in order to generate actual trading orders
        signals['positions']=signals['signal'].diff()

        return signals

class MarketOnOpenPortfolio(Portfolio):
    '''
    Inherits Portfolio to create a system that purchase 100 units of
    a particular symbol upon a long/short signal,assuming the market
    open price of a bar.

    In addition,there are zero transaction costs and cash can be immediately
    borrowed for shorting (no margin posting or interest requirements).

    Requires:
    symbol- A stock symbol which forms the basis of the portfolio
    bars- A dataFrame of bars for a symbol set.
    signals-A pandas DataFrame of signals(1,0,-1) for each symbol
    initial_capital-The amount in cash at the start of the portfolio.
    '''

    def __init__(self,symbol,bars,signals,initial_capital=100000.0):
        self.symbol=symbol
        self.bars=bars
        self.signals=signals
        self.initial_capital=float(initial_capital)
        self.positions=self.generate_positions()

    def generate_positions(self):
        '''
        Creates a 'positions' DataFrame that simply longs or shorts
        100 of the particular symbol based on the forecast signals of
        {1,0,-1}
        '''
        positions=pd.DataFrame(index=self.signals.index).fillna(0.0)
        positions[self.symbol]=100*self.signals['signal'] #TODO: the way to construct positions is different among random_forecast,ma_cross,snp_forecast
        return positions

    def backtest_portfolio(self):
        '''
        Construct a portfolio from the positions DataFrame by assuming
        the ability to trade at the precise market open price of each
        bar ( an unrealistic assumption!).

        Calculates the total of cash and the holdings (market price of
        each position per bar),in order to generate an equity curve
        ('total') and a set of bar-based returns('returns')

        returns the portfolio object to be used elsewhere.
        '''
        #Construct the portfolio DataFrame to use the same index
        #as 'positions' and with a set of 'trading orders' in the
        #'pos_diff' object,assuming market open prices

        #Create the 'holdings' and 'cash' series by running through
        #the trades and adding/subtracting the relevant quantity from
        #each column

        #Finalise the total and bar-based returns based on the 'cash'
        #and 'holdings' figures for the portfolio

        pf=pd.DataFrame(index=self.bars.index)
        pf['holdings']=self.positions.mul(self.bars['open'],axis='index')
        pf['cash']=self.initial_capital-pf['holdings'].cumsum()
        pf['total']=pf['cash']+self.positions[self.symbol].cumsum()*self.bars['open']
        pf['returns']=pf['total'].pct_change()
        return pf

class Performance:
    def __init__(self,returns):
        self.returns=returns

    def plot(self):
        pass

    def summary(self):
        pass

    def output(self):
        pass


def backtest(symbol,Strategy,Portfolio):
    bars=dataApi.getStockDf(symbol)
    st=Strategy(symbol,bars)
    signals=st.generate_signals()
    pf=Portfolio(symbol,bars,signals)
    equity=pf.backtest_portfolio()
    return equity


symbol='000005'
equity=backtest('000005',Strategy=MovingAverageCrossStrategy,Portfolio=MarketOnOpenPortfolio)

# symbol='000005'
# ohlcv=dataApi.getStockDf(symbol)
#
# # Create a set of random forecasting signals for symbol
# rfs = RandomForecastingStrategy(symbol, ohlcv)
# signals = rfs.generate_signals()
#
# # Create a portfolio of the symbol
# portfolio = MarketOnOpenPortfolio(symbol, ohlcv, signals, initial_capital=100000.0)
# returns = portfolio.backtest_portfolio()












