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


def func(fps):
    for fp in fps:
        df=pd.read_csv(fp,index_col=0)
        df.index=[ind[:-3] for ind in df.index]
        newIndex=[ind for ind in df.index if ind.endswith('12')]
        df=df.reindex(index=newIndex)

        dfid2=getSortedPortId(df,2)
        dfid3=getSortedPortId(df,3)

        dfid2.to_csv(os.path.join(chunk2p, os.path.basename(fp)))
        dfid3.to_csv(os.path.join(chunk3p, os.path.basename(fp)))
        print fp

if __name__=='__main__':
    fns1=os.listdir(myIndicatorPath)
    fns2=os.listdir(fip)
    fps=[os.path.join(myIndicatorPath,fn) for fn in fns1]
    fps+=[os.path.join(fip,fn) for fn in fns2]

    multiNum=3
    arglist=chunkify(fps,multiNum)
    for i in range(multiNum):
        p=multiprocessing.Process(target=func,args=(arglist[i],))
        p.start()












