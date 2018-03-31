#-*-coding: utf-8 -*-
#@author:tyhj
import os
import pandas as pd
from zht.data import preprocessing

from scipy.stats import pearsonr
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler


def corrAvgTrend(factorName,factorPath,returnPath,offsetList=range(-10,10)):
    fns1=os.listdir(factorPath)
    fns2=os.listdir(returnPath)
    fns=[fn for fn in fns1 if fn in fns2]

    corrAvgDf=pd.DataFrame()
    for offset in offsetList:
        corrS=pd.Series()
        for i in range(abs(offset),len(fns)-abs(offset)):
            # TODO:maybe we do not need all the history data to cal the avg of the corrs
            returnDf=pd.read_csv(os.path.join(returnPath,fns[i]),index_col=0)
            factorDf=pd.read_csv(os.path.join(factorPath,fns[i-offset]),index_col=0)
            factorDf=preprocessing.winsorize(factorDf,factorDf.columns[0])
            comDf=returnDf.copy()
            comDf[factorName]=factorDf[factorName]
            comDf=comDf.dropna(axis=0)
            corr=comDf.corr().iat[0,1]
            date=fns[i][:-4]
            corrS[date]=corr
            print offset,date
        avg=corrS.mean()
        corrAvgDf.at[offset,'corr']=avg
    return corrAvgDf


def corrAvgTrend1(factorName,factorPath,returnPath,offsetList=range(-10,10)):
    fns1=os.listdir(factorPath)
    fns2=os.listdir(returnPath)
    fns=[fn for fn in fns1 if fn in fns2]

    corrAvgDf=pd.DataFrame()
    for offset in offsetList:
        corrS=pd.Series()
        for i in range(abs(offset),len(fns)-abs(offset)):
            # TODO:maybe we do not need all the history data to cal the avg of the corrs
            returnDf=pd.read_csv(os.path.join(returnPath,fns[i]),index_col=0)
            factorDf=pd.read_csv(os.path.join(factorPath,fns[i-offset]),index_col=0)
            factorDf=preprocessing.winsorize(factorDf,factorDf.columns[0])
            comDf=returnDf.copy()
            comDf[factorName]=factorDf[factorName]
            comDf=comDf.dropna(axis=0)
            x=comDf.iloc[:,0]
            y=comDf.iloc[:,1]
            x=MinMaxScaler().fit_transform(x)
            y = MinMaxScaler().fit_transform(y)
            corr,_= pearsonr(x, y)
            date=fns[i][:-4]
            corrS[date]=corr
            print offset,date
        avg=corrS.mean()
        corrAvgDf.at[offset,'corr']=avg
    return corrAvgDf



#TODO:use rolling method to speed up the process







