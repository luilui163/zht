#-*-coding: utf-8 -*-
#author:tyhj
#calPortRet.py 2017/9/16 16:27
import os

import pandas as pd
import numpy as np

from zht.util import pandasu

from params import *


def calPortRet(portId,delay=6):
    '''
    monthly,calculate weighted return and the weight is market value

    Args:
        portId: dataframe with index as timestamp like '2012-12'
        delay: since the date in portId is the date of report date,the data is not available the
                this date,so the delay is needed and default delay is 6 months.

    Returns:

    '''
    portId = portId.T
    ret = pd.read_csv(os.path.join(bdp, 'ret.csv'), index_col=0)
    weight = pd.read_csv(os.path.join(bdp, 'weight.csv'), index_col=0)
    ports = np.sort([p for p in np.unique(portId.fillna(0.0)) if p!=0.0])
    portRet = pd.DataFrame()

    for month in portId.columns.tolist():
        year=month[:4]
        validmonths=pd.date_range(str(int(year)+1)+'-07',str(int(year)+2)+'-07',freq='M')
        validmonths=[m.strftime('%Y-%m') for m in validmonths]

        for port in ports:  # TODO
            stocks = portId[portId[month] == port].index.tolist()
            for validmonth in validmonths:
                if validmonth in ret.index.tolist():
                    try:  # There might be  no intersection stocks between ret columns and stocks,especially at the start of the 1990s
                        tmp = pd.DataFrame()
                        tmp['ret'] = ret.loc[validmonth, stocks]
                        tmp['weight'] = weight.loc[validmonth, stocks]
                        tmp = tmp.dropna(axis=0, how='any')
                        pr = pandasu.mean_self(tmp, 'ret', 'weight')
                        portRet.loc[validmonth, port] = pr
                    except KeyError:
                        portRet.loc[validmonth, port] = np.NaN
        print month

    return portRet










