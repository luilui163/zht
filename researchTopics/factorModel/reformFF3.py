#-*-coding: utf-8 -*-
#author:tyhj
#reformFF3.py 2017/10/1 11:30

import multiprocessing
import itertools

from zht.util.listu import chunkify

from tools import *
from params import  *
from classicalModels import *
from constructPlayingField import getValidIndicators
import shutil

def getMyFactors():
    fns=os.listdir(id3p)

    for fn in fns:
        df=pd.read_csv(os.path.join(id3p,fn),index_col=0)
        portRet=calPortRet(df)
        factor=portRet.iloc[:,-1]-portRet.iloc[:,0]
        factor.to_csv(os.path.join(myfp,fn))
        print fn


def buildMyModels():
    '''
    add a new factor to ff3 to construct a 4 factor model
    :return:
    '''
    iv=get_ff3()
    fns=os.listdir(myfp)
    for fn in fns:
        factor=iv.copy(deep=True)
        factor[fn[:-4]]=pd.read_csv(os.path.join(myfp,fn),index_col=0)
        factor.to_csv(os.path.join(mymp,fn))
        print fn
    bms=os.listdir(bmp)
    for bm in bms:
        shutil.copyfile(os.path.join(bmp,bm),os.path.join(mymp,bm))


def regressOnMyFactors():
    ALPHA=pd.DataFrame()
    ALPHAT=pd.DataFrame()

    indicatorNames = [fn[:-4] for fn in os.listdir(idrp)]
    fns=os.listdir(mymp)
    for i,fn in enumerate(fns):
        iv=pd.read_csv(os.path.join(mymp,fn),index_col=0)
        for indicatorName in indicatorNames:
            tmpdf=pd.read_csv(os.path.join(idrp,indicatorName+'.csv'),index_col=0)
            df=pd.DataFrame()
            df['10-1']=tmpdf.iloc[:,-1]-tmpdf.iloc[:,0]
            df[iv.columns.tolist()]=iv
            df=df.dropna(axis=0,how='any')

            # TODO: get valid indicators
            if df.shape[0] > 100:
                coef, t, r2, resid = pandasu.reg(df)
                alpha = coef[0]
                alphat = t[0]
                ALPHA.loc['model__'+fn[:-4],indicatorName]=alpha
                ALPHAT.loc['model__'+fn[:-4],indicatorName]=alphat
        print i,fn

    ALPHA.to_csv(os.path.join(rff3p,'alpha.csv'))
    ALPHAT.to_csv(os.path.join(rff3p,'alphat.csv'))

    alphatSummary=ALPHAT.T.copy(deep=True)
    for i, col in enumerate(alphatSummary.columns):
        alphatSummary.loc['gt2', col] = alphatSummary[alphatSummary[col] > 2.0].shape[0]
        alphatSummary.loc['lt-2', col] = alphatSummary[alphatSummary[col] < -2.0].shape[0]
        alphatSummary.loc['sum', col] = alphatSummary.loc['gt2', col] + alphatSummary.loc['lt-2', col]
        print i

    sind = ['gt2', 'lt-2', 'sum']
    newIndex = sind + [ind for ind in alphatSummary.index if ind not in sind]

    alphatSummary = alphatSummary.reindex(index=newIndex)
    alphatSummary = alphatSummary.sort_values('gt2', axis=1)

    alphatSummary.T.to_csv(os.path.join(rff3p,'alphatSummary.csv'))


def get_alphatSummary1():
    '''
    add thresh 3 to compare the models
    :return:
    '''
    df=pd.read_csv(os.path.join(rff3p,'alphatSummary.csv'),index_col=0)
    df=df.T

    for i,col in enumerate(df.columns):
        df.loc['gt3',col]=df[df[col]>3.0].shape[0]
        df.loc['lt-3',col]=df[df[col]<-3.0].shape[0]
        df.loc['sum3',col]=df.loc['gt3',col]+df.loc['lt-3',col]
        print i

    sumInds=['gt2','lt-2','sum','gt3','lt-3','sum3']
    newInds=sumInds+[ind for ind in df.index if ind not in sumInds]
    df=df.reindex(index=newInds)
    df=df.T
    df.to_csv(os.path.join(rff3p,'alphatSummary1.csv'))







