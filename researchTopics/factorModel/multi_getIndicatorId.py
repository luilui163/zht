#-*-coding: utf-8 -*-
#author:tyhj
#multi_getIndicatorId.py 2017/9/19 12:26

import multiprocessing
import os
import pandas as pd

from zht.util.listu import chunkify
from zht.util import pandasu

from params import *
from tools import *


def func(fns):
    for fn in fns:
        indicator=fn[:-4]
        id2=getIndicatorId(indicator,2)
        id3=getIndicatorId(indicator,[0.3,0.7])#TODO: 3 or [0.3,0.7]
        id10=getIndicatorId(indicator,10)

        id2.to_csv(os.path.join(id2p,fn))
        id3.to_csv(os.path.join(id3p,fn))
        id10.to_csv(os.path.join(id10p,fn))
        print indicator


if __name__=='__main__':
    fns=os.listdir(idp)
    n=4
    arglist=chunkify(fns,n)

    for i in range(n):
        p=multiprocessing.Process(target=func,args=(arglist[i],))
        p.start()












