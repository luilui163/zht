#-*-coding: utf-8 -*-
#author:tyhj
#multi_getIndicatorId.py 2017/9/8 22:37


from params import *

import multiprocessing
import os
import pandas as pd

# from zht.util.sysu import multiProcess
from zht.util.mathu import getSortedPortId
from zht.util.listu import chunkify


def func(fns):
    for fn in fns:
        df = pd.read_csv(os.path.join(fip, fn), index_col=0)
        dfid = getSortedPortId(df, 10)
        dfid.to_csv(os.path.join(fiip, fn))


if __name__=='__main__':
    fns1=os.listdir(fip)
    fns2=os.listdir(fiip)
    fns=[fn for fn in fns1 if fn not in fns2]

    # fns=os.listdir(fip)
    multiNum=3
    arglist=chunkify(fns,multiNum)
    for i in range(multiNum):
        p=multiprocessing.Process(target=func,args=(arglist[i],))
        p.start()












