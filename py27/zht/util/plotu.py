#-*-coding: utf-8 -*-
#author:tyhj
#plotu.py 2017/10/2 10:34
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













