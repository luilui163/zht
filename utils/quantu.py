# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-11  14:23
# NAME:assetPricing-quantu.py

import numpy as np


def annualisedSharpe(dailyEret,N=252):
    '''
    Calculate the annualised Sharpe ratio of a returns stream
    based on a number of trading periods,N.N defaults to 252,which
    then assumes a stream of daily returns.

    The function assumes that the returns are the excess of those
    compared to a benchmark
    Args:
        dailyEret:
        N:

    Returns:

    '''
    return np.sqrt(N)*dailyEret.mean()/dailyEret.std()


def informationRatio(pnl):
    '''
    information ratio
    Args:
        pnl:

    Returns:

    '''
    return pnl.mean()/pnl.std()


