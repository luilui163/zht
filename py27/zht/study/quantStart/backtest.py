#-*-coding: utf-8 -*-
#@author:tyhj

from abc import ABCMeta,abstractmethod

class Strategy(object):
    '''strategy is an abstract base class providing an interface for all
    subsequent(inherited) trading strategies.

    The goal of a (derived) Strategy object is to output a list of signals,
    which has the form of a time series indexed pandas DataFrame.

    In this instance only a single symbol/instrument is supported.

    '''
    __metaclass__=ABCMeta

    @abstractmethod
    def generate_signals(selfself):
        '''
        An implementation is required to return the DataFrame of symbols
        containing the signals to go long,short or hold(1,-1,0).
        :return:
        '''
        raise NotImplementedError('should implement generate_signals')


class Portfolio(object):
    '''
    An abstract base class representing a portfolio of positions (including
    both instruments and cash),determined on the basis of a set of signals
    provided by a Strategy.
    '''
    __metaclass__=ABCMeta

    @abstractmethod
    def generate_positions(self):
        '''
        Provides the logic to determine how the portfolio positions are allocated
        on the basis of  forecasting signals and available cash.
        '''
        raise NotImplementedError('should impelement')

    @abstractmethod
    def backtest_portfolio(self):
        '''
        Provides the logic to generate the trading orders and subsequent equity
        curve(i.e. growth of total equity),as a sum of holdings and cash,and
        the bar-period returns associated with this curve based on the 'positions'
        DataFrame.

        Produces a portfolio object that can be examined by other classes/functions.
        :return:
        '''
        raise NotImplementedError('should implement backtest_portfolio()!')



