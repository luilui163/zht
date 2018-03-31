#-*-coding: utf-8 -*-
#author:tyhj
#multi_buildTestModels.py 2017/9/27 14:40

import pandas as pd
import numpy as np
import os
import multiprocessing
import itertools

from zht.util.listu import chunkify

from tools import *
from params import  *
from constructPlayingField import getValidIndicators


def func(args):
    for arg in args:
        vars,model=arg[0],arg[1]
        iv=buildModel(vars,model)
        iv.to_csv(os.path.join(mdp,'%s_%s.csv'%(model,'-'.join(vars))))


#TODO: sort independently rather conditional


if __name__=='__main__':
    n=4

    indicators=getValidIndicators()

    varslist=[]

    #3 factor,with rp and size as the given factors,find a new factor
    model='2x3'
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

    #get unprocessed combinations
    fns=os.listdir(mdp)
    ran=[]
    ran=[(fn[:-4].split('_')[-1].split('-'),fn.split('_')[0]) for fn in fns]
    torun=[item for item in varslist if item not in ran]

    arglist=chunkify(torun,n)
    for i in range(n):
        p=multiprocessing.Process(target=func,args=(arglist[i],))
        p.start()


#TODO:use queue to store f











