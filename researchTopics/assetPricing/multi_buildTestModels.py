#-*-coding: utf-8 -*-
#author:tyhj
#multi_buildTestModels.py 2017/9/17 15:13

import multiprocessing
import os
import pandas as pd
import uuid
import itertools

from zht.util.mathu import getSortedPortId
from zht.util.listu import chunkify


from calPortRet import calPortRet
from params import *
from  constructModel import buildModel



def func(args):
    for arg in args:
        vars,model=arg[0],arg[1]
        iv=buildModel(vars,model)
        iv.to_csv(os.path.join(mdp, '%s_%s.csv' % (model, '-'.join(vars))))


if __name__=='__main__':
    multiNum=3

    fns=os.listdir(indid2p)
    indicators=[fn[:-4] for fn in fns]

    varslist = []

    #3 factor,with rp and size as the given factors,find a new factor
    model='2x2'
    for var in indicators:
        if var!='size':
            vars=['size',var]
            varslist.append((vars,model))

    #4 factor,with rp and size as the given factors,find 2 new factors
    model='2x2x2'
    tmpIndicators=[ind for ind in indicators if ind!='size']
    combs=itertools.combinations(tmpIndicators,2)
    for var in combs:
        varslist.append((['size']+list(var),model))

    arglist=chunkify(varslist,multiNum)
    for i in range(multiNum):
        p=multiprocessing.Process(target=func,args=(arglist[i],))
        p.start()












