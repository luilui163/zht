#-*-coding: utf-8 -*-
#author:tyhj
#quantu.py 2017/9/9 10:23
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

def plotCumulativeRet(pnl):
    '''
    plot the cumulative return line plot
    Args:
        pnl: series

    Returns:

    '''

    ind=pnl.first_valid_index()
    pnl=pnl[ind:]
    pnl=pnl.fillna(0)
    cumsum=pnl.cumsum()

    #Turn interactive plotting off
    plt.ioff()
    fig=plt.figure()
    cumsum.plot()
    #plt.show()
    plt.close(fig)
    return fig











