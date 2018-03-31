#-*-coding: utf-8 -*-
#@author:tyhj

import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from pandas_datareader import DataReader

try:
    from sklearn.qda import QDA
except:
    import sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis as QDA

from backtest import Strategy,Portfolio
from forecast import create_lagged_series

'''

Note that this is not a particularly realistic trading strategy!
We are unlikely to ever achieve an opening or closing price
due to many factors such as excessive opening volatility,
order routing by the brokerage and potential liquidity issues
around the open/close. In addition we have not included
transaction costs. These would likely be a substantial
percentage of the returns as there is a round-trip trade
carried out every day. Thus our forecaster needs to be
relatively accurate at predicting daily returns,
otherwise transaction costs will eat all of our trading
returns.'''


class SNPDorecastingStrategy(Strategy):
    '''
    Requires:
    symbol - A stock symbol on which to form a strategy on.
    bars - A DataFrame of bars for the above symbol.
    '''

    def __init__(self,symbol,bars):
        self.symbol=symbol
        self.bars=bars
        self.create_periods()
        self.fit_model()

    def create_periods(self):
        '''create training/test periods'''
        self.start_train=datetime.datetime(2001,1,10)
        self.start_test=datetime.datetime(2005,1,1)
        self.end_period=datetime.datetime(2005,12,31)

    def fit_model(self):
        '''
        Fits a Quadratic Discriminant analyser to the US
        stock market index (^GPSC in Yahoo).
        '''
        #Create a lagged series of the S$P500 US stock market index
        snpret=create_lagged_series(self.symbol,self.start_train,
                                    self.end_period,lags=5)

        #Use the prior two days of returns as predictor values,
        #with direction as the response
        X=snpret[['Lag1','Lag2']]
        y=snpret['Direction']

        #Create training and test sets
        X_train=X[X.index<self.start_test]
        y_train=y[y.index<self.start_test]

        #Create the predicting factors for use
        #in direction forecasting
        self.predictors=X[X.index>=self.start_test]

        #Create the Quadratic Discriminant Analysisi model
        #and the forecasting strategy
        self.model=QDA()
        self.model.fit(X_train,y_train)

    def generate_signals(self):
        '''
        Returns the DataFrame of symbols containing the signals
        to go long,short or hold {1,-1 or 0}.
        '''
        signals=pd.DataFrame(index=self.bars.index)
        signals['signal']=0.0

        #predict the subsequent period with the QDA model
        signals['signal']=self.model.predict(self.predictors)

        #Remove the first five signal entries to eliminate
        #NaN issues with the signals DataFrame
        signals['signal'][0:5]=0.0
        # signals['positions']=signals['signal'].diff()

        return signals


class MarketIntrdayPortfolio(Portfolio):
    '''
    buys or sells 500 shares of an asset at the opening price of
    every bar,depending upon the direction of the forecast,closing
    out the trade at the close of the bar.

    Requires:
    symbol - A stock symbol with forms the basis of the portfolio.
    bars - A DataFrame of bars for a symbol set.
    signals - A pandas DataFrame of signals {1,0,-1} for each symbol.
    initial_capital - The amount in cash at the start of the portfolio.
    '''

    def __init__(self,symbol,bars,signals,initial_capital=100000.0):
        self.symbol=symbol
        self.bars=bars
        self.signals=signals
        self.initial_capital=float(initial_capital)
        self.positions=self.generate_positions()

    def generate_positions(self):
        '''
        Generate the positions DataFrame.bsed on the signals
        provided by the 'signals' DataFrame.
        '''
        positions=pd.DataFrame(index=self.signals.index).fillna(0.0)

        #Long or short 500 shares of SPY based on
        #directional signal every day
        positions[self.symbol]=500*self.signals['signal']
        return positions

    def backtest_portfolio(self):
        '''
        backtest the portfolio and return a DataFrame
        containing the equity curve and the percentage
        returns.
        '''
        #Set the portfolio object to have the same time period
        #as the positions DataFrame
        portfolio=pd.DataFrame(index=self.positions.index)
        pos_diff=self.positions.diff()

        #work out the intraday profit of the difference
        #in open and closing prices and then determine
        #the daily profit by longing if an up is predicted
        #and shorting if a down day is predicted
        portfolio['price_diff']=self.bars['Close']-self.bars['Open']
        portfolio['price_diff'][0:5]=0.0
        portfolio['profit']=self.positions[self.symbol]*portfolio['price_diff']

        #Generate the equity curve and percentage returns
        portfolio['total']=self.initial_capital+portfolio['profit'].cumsum()
        portfolio['returns']=portfolio['total'].pct_change()
        return portfolio

if __name__=='__main__':
    start_test=datetime.datetime(2005,1,1)
    end_period=datetime.datetime(2005,12,31)

    #Obtain the bars for SPY ETF which tracks the S$P500 index
    # bars=DataReader('SPY','yahoo',start_test,end_period)
    symbol = '000001'
    bars = pd.read_csv(r'000001.csv', index_col=0)
    bars = bars.iloc[-100:, :]

    ind = list([str(m) for m in bars.index])
    new_ind = ['-'.join(d.split(r'/')) for d in ind]
    bars.index = [pd.Timestamp(nd) for nd in new_ind]



    #Create the S$P500 forecasting strategy
    snpf=SNPDorecastingStrategy ('^GSPC',bars)
    signals=snpf.generate_signals()

    #Create the portfolio based on the forecaster
    portfolio=MarketIntrdayPortfolio('SPY',bars,signals,initial_capital=100000.0)
    returns=portfolio.backtest_portfolio()

    #Plot results
    fig=plt.figure()
    fig.patch.set_facecolor('white')

    #Plot the price  of the SPY ETF
    ax1=fig.add_subplot(211,ylabel='SPY ETF price in $')
    bars['Close'].plot(ax=ax1,color='r',lw=2.)

    #plot the equity curve
    ax2=fig.add_subplot(212,ylabel='Portfolio value in $')
    returns['total'].plot(ax=ax2,lw=2.)

    fig.show()



