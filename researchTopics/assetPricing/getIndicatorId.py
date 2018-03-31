#-*-coding: utf-8 -*-
#author:tyhj
#getIndicatorId.py 2017/9/8 22:37


from params import myIndicatorPath,myIndicatorIdPath

import multiprocessing
import os
import pandas as pd

# from zht.util.sysu import multiProcess
from zht.util.mathu import getSortedPortId
from zht.util.listu import chunkify


def func(fns):
    for fn in fns:
        df = pd.read_csv(os.path.join(myIndicatorPath, fn), index_col=0)
        dfid = getSortedPortId(df, 10)
        dfid.to_csv(os.path.join(myIndicatorIdPath, fn))


if __name__=='__main__':
    fns=os.listdir(myIndicatorPath)
    multiNum=4
    arglist=chunkify(fns,multiNum)
    for i in range(multiNum):
        p=multiprocessing.Process(target=func,args=(arglist[i],))
        p.start()












