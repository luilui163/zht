#-*-coding: utf-8 -*-
#@author:tyhj
from zht.util.dfFilter import filterDf
import pandas as pd

def getFama3():
    query1='Exchflg == 0' #所有交易所
    query2='Mktflg == A'#只考虑A股

    df=pd.read_csv(r'D:\quantDb\resset\THRFACDAT_MONTHLY.csv',index_col=0)
    df=filterDf(df,[query1,query2])
    return df


def getPortRet():
    query1='Exchflg == 0' #所有交易所
    query2='Mktflg == A'#只考虑A股

    df=pd.read_csv(r'D:\quantDb\resset\PMONRET_FF.csv',index_col=0)
    df = filterDf(df, [query1, query2])
    return df


def getRm():
    query1='Exchflg == 0' #所有交易所
    query2='Mktflg == A'#只考虑A股

    df=pd.read_csv(r'D:\quantDb\resset\MONCRETM.csv')
    df = filterDf(df, [query1, query2])
    return df


def getIS_ALL():
    query1='LstFlg in ["A","AB"]' #all A shares
    query2='AccStd == 1' #new accounting standard
    query3='ConFlg == 2'#combined report
    query4='ReportType == Q4' #annual report

    query=[query1,query2,query3,query4]

    path=r'D:\quantDb\resset\IS_ALL.csv'
    df=pd.read_csv(path,index_col=0,encoding='gbk')
    df=filterDf(df,query)
    return df


def getFININD():
    query1='LstFlg in ["A","AB"]' #all A shares
    query2='AccStd == 1' #new accounting standard
    query3='ConFlg == 2'#combined report
    query4='ReportType == Q4' #annual report

    query = [query1, query2, query3, query4]

    path=r'D:\quantDb\resset\FININD.csv'
    df=pd.read_csv(path,index_col=0,encoding='gb2312',error_bad_lines=False)
    df=filterDf(df,query)
    return df

#momentum factor
def getMomentum():
    q1='ExchFlg == 0'
    q2='MktFlg == A'
    q=[q1,q2]

    path=r'D:\quantDb\sourceData\resset\data\MOMFAC_MONTHLY_30PER_1.csv'
    df=pd.read_csv(path)

    invalidcols=[]
    for col in df.columns:
        if 'Unnamed' in col:
            invalidcols.append(col)
    df=df.drop(invalidcols,axis=1)

    df=filterDf(df,q)

    df=df.set_index('Date')
    df=df.drop(['ExchFlg','MktFlg'],axis=1)

    del df.index.name
    df.index=[ind[:-3] for ind in df.index]

    return df









