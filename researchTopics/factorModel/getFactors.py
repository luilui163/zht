#-*-coding: utf-8 -*-
#author:tyhj
#getFactors.py 2017/8/17 10:55
import pandas as pd
import numpy as np
import os

from zht.data.resset import ressetApi
from zht.data.gta import gtaApi
from zht.util import pandasu
from zht.util.dfFilter import filterDf
from zht.util.mathu import *


from params import *
from main import get_portRet



#TODO:nfc stocks

def get_ff3Factors():
    size=pd.read_csv(os.path.join())







def get_ff3Factors():
    '''
    get smb and hml in ff3 model
    Returns:

    '''
    #TODO:think about weighted average rather than equal weighted
    def func1(x):#factor return
        return (x[13]+x[23])/2-(x[11]+x[21])/2
    def func2(x):#smb
        return (x[11]+x[12]+x[13])/3-(x[21]+x[22]+x[23])/3

    model='2x3'
    vars=['size','btm']
    portRet=get_portRet(vars,model)

    portRet.columns=[int(float(col)) for col in portRet.columns]
    hml=portRet.apply(func1,axis=1)#factor return

    smb=portRet.apply(func2,axis=1)

    hml.to_csv(os.path.join(ff3FactorP,'hml.csv'))
    smb.to_csv(os.path.join(ff3FactorP,'smb.csv'))



