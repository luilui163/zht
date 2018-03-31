#-*-coding: utf-8 -*-
#@author:tyhj
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from backtest import Strategy, Portfolio

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

class MarketOnClosePortfolio(Portfolio):
    '''
    Encapsulates the notion of a portfolio of positions
    based on a set of signals as provided by a Strategy.

    Requires:
    symbol - A stock symbol which forms the basis of the portfolio.
    bars - A DataFrame of bars for a symbol set.
    signals - A pandas DataFrame of signals {1,-1,0.0} for each symbol.
    initial_capital - The amount in cash at the start of the portfolio
    '''
    def __init__(self,symbol,bars,signals,initial_capital=100000.0):
        self.symbol=symbol
        self.bars=bars
        self.signals=signals
        self.initial_capital=float(initial_capital)
        self.positions=self.generate_positions()

    def generate_positions(self):
        positions=pd.DataFrame(index=self.signals.index).fillna(0.0)
        positions[self.symbol]=100*self.signals['positions']
        return positions

    def backtest_portfolio(self):
        pf=pd.DataFrame(index=self.bars.index)
        pf['holdings']=self.positions.mul(self.bars['close'],axis='index')
        pf['cash']=self.initial_capital-pf['holdings'].cumsum()
        pf['total']=pf['cash']+self.positions[self.symbol].cumsum()*self.bars['close']
        pf['returns']=pf['total'].pct_change()
        return pf

# def backtest_MovingAverageCrossStrategy():


symbol = '000001'
bars = pd.read_csv(r'000001.csv', index_col=0)
bars=bars.iloc[-100:,:]

ind = list([str(m) for m in bars.index])
new_ind = ['-'.join(d.split(r'/')) for d in ind]
bars.index = [pd.Timestamp(nd) for nd in new_ind]


# Create a Moving Average Cross Strategy instance with a short moving
# average window of 100 days and a long window of 400 days
mac = MovingAverageCrossStrategy(symbol, bars, short_window=10, long_window=15)
signals = mac.generate_signals()


# Create a portfolio of AAPL, with $100,000 initial capital
portfolio = MarketOnClosePortfolio(symbol, bars, signals, initial_capital=100000.0)
pf = portfolio.backtest_portfolio()


import matplotlib.pyplot as plt
import seaborn as sns
#Plot two charts to assess trades and equity curve
fig = plt.figure(figsize=(16, 12))
#fig = plt.figure()
fig.patch.set_facecolor('white')     # Set the outer colour to white
ax1 = fig.add_subplot(411,  ylabel='Price in $')

# Plot the AAPL closing price overlaid with the moving averages
bars[['close']].plot(ax=ax1, color='r', lw=2.)
signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

# Plot the "buy" trades against AAPL
ax1.plot(signals.ix[signals.positions == 1.0].index,
         signals.short_mavg[signals.positions == 1.0],
         '^', markersize=10, color='m')

# Plot the "sell" trades against AAPL
ax1.plot(signals.ix[signals.positions == -1.0].index,
         signals.short_mavg[signals.positions == -1.0],
         'v', markersize=10, color='k')

# Plot the equity curve in dollars
ax2 = fig.add_subplot(412, ylabel='Portfolio value in $')
pf['total'].plot(ax=ax2, lw=2.)

# Plot the "buy" and "sell" trades against the equity curve
ax2.plot(pf.ix[signals.positions == 1.0].index,
         pf.total[signals.positions == 1.0],
         '^', markersize=10, color='m')
ax2.plot(pf.ix[signals.positions == -1.0].index,
         pf.total[signals.positions == -1.0],
         'v', markersize=10, color='k')

# signal
ax3 = fig.add_subplot(413, ylabel='signal')
signals.signal.plot(ax=ax3)

# signal
ax4 = fig.add_subplot(414, ylabel='signal')
signals.positions.plot(ax=ax4)

# Plot the figure
fig.show()













