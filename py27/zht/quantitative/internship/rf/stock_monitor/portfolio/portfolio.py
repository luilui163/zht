#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import numpy as np

class MarketOnClosePortfolio:
    '''
    Requires:
    symbol - A stock symbol which forms the basis of the portfolio.
    bars - A DataFrame of bars for a symbol set.
    signals - A pandas DataFrame of signals (1,0,-1) for each symbol.
    initial_capital - The amount in cash at the start of the portfolio.
    '''
    def __init__(self,symbol,bars,signals,initial_capital=100000.0):
        self.symbol=symbol
        self.bars=bars
        self.signals=signals
        self.initial_capital=float(initial_capital)
        self.positions=self.generate_positions()
        self.portfolio=self.backtest_portfolio()

    def generate_positions(self):
        positions=pd.DataFrame(index=self.signals.index).fillna(0.0)
        positions[self.symbol]=100*self.signals['signal']
        return positions

    def backtest_portfolio(self):
        portfolio=self.positions*self.bars['Close']
        pos_diff=self.positions.diff()
        portfolio['holdings']=(self.positions*self.bars['Close']).sum(axis=1)
        portfolio['cash']=self.initial_capital-(pos_diff*self.bars['Close']).sum(axis=1).cumsum()

        portfolio['total']=portfolio['cash']+portfolio['holdings']
        portfolio['returns']=portfolio['total'].pct_change()
        return portfolio



















