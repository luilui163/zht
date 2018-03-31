#-*-coding: utf-8 -*-
#author:tyhj
#multi_estimateAlphaOnAllTestModels.py 2017/9/27 21:43
import pandas as pd
import multiprocessing

from zht.util.listu import chunkify

from params import *
from tools import *


indicatorNames=[fn[:-4] for fn in os.listdir(idrp)]

def estimateAlpha(indicatorName,model):
    if model in ['capm','ff3','carhart4','liq4','ff5','hxz4']:
        iv=pd.read_csv(os.path.join(bmp,model+'.csv'),index_col=0)
    else:#TODO:new model path is mdp.
        iv=pd.read_csv(os.path.join(mdp,model+'.csv'),index_col=0)

    tmpdf=pd.read_csv(os.path.join(idrp,indicatorName+'.csv'),index_col=0)

    df=pd.DataFrame()
    df['10-1']=tmpdf.iloc[:,-1]-tmpdf.iloc[:,0]
    df[iv.columns.tolist()]=iv

    df=df.dropna(axis=0,how='any')

    alpha=None
    alphat=None

    #TODO: get valid indicators
    if df.shape[0]>100:
        coef, t, r2, resid = pandasu.reg(df)
        alpha=coef[0]
        alphat=t[0]
    return alpha,alphat

def func(models):
    global indicatorNames
    for model in models:
        alphaDf=pd.DataFrame()
        alphatDf=pd.DataFrame()
        for indicatorName in indicatorNames:
            alpha,alphat=estimateAlpha(indicatorName,model)
            alphaDf.loc[indicatorName,model]=alpha
            alphatDf.loc[indicatorName,model]=alphat
        alphaDf.to_csv(os.path.join(alphap,model+'.csv'))
        alphatDf.to_csv(os.path.join(alphatp,model+'.csv'))
        print model




if __name__=='__main__':
    n=3
    models=getValidModels()
    argList=chunkify(models,n)

    for i in xrange(n):
        p=multiprocessing.Process(target=func,args=(argList[i],))
        p.start()




