#-*-coding: utf-8 -*-
#author:tyhj
#constructModel.py 2017/9/17 15:14

import os
import pandas as pd
import uuid
import itertools

from zht.util.mathu import getSortedPortId
from zht.util.listu import chunkify
from zht.util import pandasu

from calPortRet import calPortRet
from params import *


def intersectionFactorRet(vars,model):
    '''

    Args:
        vars:list or tuple
        model: '2x2','2x3','3x2','3x3','2x2x2','2x3x3' and so on.

    Returns:

    '''
    if len(model.split('x'))==2:
        var1, var2 = vars[0], vars[1]
        n1,n2=tuple(model.split('x'))

        id1=pd.read_csv(os.path.join(indidp,n1,var1+'.csv'),index_col=0)
        id2=pd.read_csv(os.path.join(indidp,n2,var2+'.csv'),index_col=0)

        id1,id2=pandasu.get_inter_frame([id1,id2])

        portId=id1*10+id2
        portRet=calPortRet(portId)

        highCols1=[col for col in portRet.columns if str(col)[0]==n1]
        lowCols1=[col for col in portRet.columns if str(col)[0]=='1']
        factor1 = portRet[highCols1].mean(axis=1) - portRet[lowCols1].mean(axis=1)

        highCols2=[col for col in portRet.columns if str(col)[1]==n2]
        lowCols2=[col for col in portRet.columns if str(col)[1]=='1']
        factor2 = portRet[highCols2].mean(axis=1) - portRet[lowCols2].mean(axis=1)
        return factor1, factor2

    elif len(model.split('x'))==3:
        var1,var2,var3=vars[0],vars[1],vars[2]
        n1,n2,n3=tuple(model.split('x'))

        id1=pd.read_csv(os.path.join(indidp,n1,var1+'.csv'),index_col=0)
        id2=pd.read_csv(os.path.join(indidp,n2,var2+'.csv'),index_col=0)
        id3=pd.read_csv(os.path.join(indidp,n3,var3+'.csv'),index_col=0)

        id1,id2,id3=pandasu.get_inter_frame([id1,id2,id3])

        portId=id1*100+id2*10+id3
        portRet=calPortRet(portId)

        highCols1=[col for col in portRet.columns if str(col)[0]==n1]
        lowCols1=[col for col in portRet.columns if str(col)[0]=='1']
        factor1 = portRet[highCols1].mean(axis=1) - portRet[lowCols1].mean(axis=1)

        highCols2=[col for col in portRet.columns if str(col)[1]==n2]
        lowCols2=[col for col in portRet.columns if str(col)[1]=='1']
        factor2 = portRet[highCols2].mean(axis=1) - portRet[lowCols2].mean(axis=1)

        highCols3=[col for col in portRet.columns if str(col)[2]==n3]
        lowCols3=[col for col in portRet.columns if str(col)[2]=='1']
        factor3 = portRet[highCols3].mean(axis=1) - portRet[lowCols3].mean(axis=1)
        return factor1,factor2,factor3

def buildModel(vars,model):
    factors=intersectionFactorRet(vars,model)
    iv=pd.DataFrame()
    iv['rp'] = pd.read_csv(os.path.join(bdp, 'rp.csv'), index_col=0)['rp']
    for i,factor in enumerate(factors):
        iv[vars[i]]=factor

    return iv
















