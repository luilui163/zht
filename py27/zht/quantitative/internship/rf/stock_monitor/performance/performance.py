#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import numpy as np

def create_drawdowns(pnl):
    '''
    Parameters:
    pnl - A pandas Series representing period percentage returns.

    Returns:
    drawdoun,duration - Highest peak-to-trough drawdown and duration.
    :param pnl:
    :return:
    '''
    #Calculate the cumulative returns curve
    #and set up the High Water Mark
    hwm=[0]

    #Create the drawdown and duration series
    idx=pnl.index
    drawdown=pd.Series(index=idx)
    duration=pd.Series(index=idx)

    #Loop over the index range
    for t in range(1,len(idx)):
        hwm.append(max(hwm[t-1],pnl.ix[t]))
        drawdown.ix[t]=(hwm[t]-pnl.ix[t])
        duration.ix[t]=(0 if drawdown.ix[t]==0 else duration.ix[t-1]+1)
    return drawdown,drawdown.max(),duration.max()












