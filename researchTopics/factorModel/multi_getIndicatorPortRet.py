#-*-coding: utf-8 -*-
#author:tyhj
#multi_getIndicatorPortRet.py 2017/9/21 0:08

import pandas as pd
import multiprocessing

from zht.util.listu import chunkify

from params import *
from tools import *


def func(fns):
    for fn in fns:
        id=pd.read_csv(os.path.join(id10p,fn),index_col=0)
        portRet=calPortRet(id)
        portRet.to_csv(os.path.join(idrp,fn))
        print fn



if __name__=='__main__':
    fns=os.listdir(id10p)
    n=2
    argList=chunkify(fns,n)

    for i in xrange(n):
        p=multiprocessing.Process(target=func,args=(argList[i],))
        p.start()














