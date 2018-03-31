# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-11  14:22
# NAME:assetPricing-plotu.py

import matplotlib.pyplot as plt

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


