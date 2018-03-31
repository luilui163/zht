#-*-coding: utf-8 -*-
#@author:tyhj

from copy import deepcopy
from qsforex.event.event import OrderEvent
from qsforex.portfolio.position import Position

class Portfolio(object):
    def __init__(self,ticker,events,base='GBP',leverage=20,equity=100000.0,risk_per_trade=0.02):
        self.ticker=ticker
        self.events=events
        self.base=base
        self.leverage=leverage
        self.equity=equity
        self.balance=deepcopy(self.equity)
        self.risk_per_trade=risk_per_trade
        self.trade_units=self.calc_risk_position_size()
        self.positions={}

    def calc_risk_position_size(self):
        return self.equity*self.risk_per_trade

    def add_new_position(self,side,market,units,exposure,add_price,
                         remove_price):
        ps=Position(side,market,units,exposure,add_price,remove_price)
        self.positions[market]=ps

    def add_position_units(self,market,units,exposure,add_price,remove_price):













