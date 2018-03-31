#-*-coding: utf-8 -*-
#@author:tyhj

import copy
from tools import technical
from data import datahandler_all,tool
import pandas as pd
import numpy as np

# df=datahandler.get_data('000009.SZ')
# dif,dea,bar=technical.macd(df['Close'])

class MacdStrategy:
    '''
    Requires:
    symbol - A stock symbol on which to form a strategy on.
    bars - A DataFrame of bars for the above symbol.
    '''
    def __init__(self,symbol):
        self.symbol=symbol
        self.bars=datahandler_all.get_data(symbol)
        self.macd=self.get_macd()
        self.signals=self.get_signals()

    def get_macd(self):
        dif, dea, bar = technical.macd(self.bars['Close'])
        self.bars['macd']=dif

    def get_signals(self):
        # signals=pd.DataFrame(index=self.bars.index)
        # signals['signal']=np.sign(self.bars['macd'])
        self.bars['signal']=np.sign(self.bars['macd'])

ms=MacdStrategy('000009.SZ')















