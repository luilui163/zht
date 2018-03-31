#-*-coding: utf-8 -*-
#author:tyhj
#multi_getPortRet.py 2017/9/9 9:22

import os
import pandas as pd
import numpy as np
import multiprocessing

from zht.util.listu import chunkify
from zht.util import pandasu
from params import *

def func(fns):
    for fn in fns:
        portId = pd.read_csv(os.path.join(fiip, fn), index_col=0)
        portId.index = [ind[:-3] for ind in portId.index]
        inds = [ind for ind in portId.index if ind[-2:] == '12']
        portId = portId.loc[inds]

        portId = portId.T
        ret = pd.read_csv(os.path.join(bdp, 'ret.csv'), index_col=0)
        weight = pd.read_csv(os.path.join(bdp, 'weight.csv'), index_col=0)
        ports = np.sort([p for p in portId.iloc[:, -1].unique() if not np.isnan(p)])
        portRet = pd.DataFrame()
        for month in portId.columns.tolist():
            year = month[:4]
            validmonths = [year + '-0' + str(i) for i in range(7, 10)]
            validmonths += [year + '-1' + str(i) for i in range(3)]
            validmonths += [str(int(year) + 1) + '-0' + str(i) for i in range(1, 7)]

            for port in ports:#TODO
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
            print fn,month

        portRet.to_csv(os.path.join(prp, fn))

if __name__=='__main__':
    fns = os.listdir(fiip)
    multiNum=3
    argList=chunkify(fns,multiNum)

    for i in xrange(multiNum):
        p=multiprocessing.Process(target=func,args=(argList[i],))
        p.start()









