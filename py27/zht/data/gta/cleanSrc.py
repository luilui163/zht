#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import os
import sys
from zht.util.dateu import normalize_date
from zht.util.stru import cleanStockId
from zht.data.util.toMysql import toMysql

#行情数据月
def mkt():
    directory=u'D:\quantDb\sourceData\gta\行情数据月'
    fns=os.listdir(directory)
    fns=[fn for fn in fns if fn.endswith('.xls')]
    fns=sorted(fns)

    subdfs=[]
    for fn in fns:
        subdf=pd.read_excel(os.path.join(directory,fn))
        subdf=subdf[2:]
        subdfs.append(subdf)
    df=pd.concat(subdfs)
    df=df.reset_index()
    del df['index']

    df.to_csv(r'D:\quantDb\mkt\monthly\mkt.csv',date_format='%Y-%m')

#每股指标
def indicatorOfPerShare():
    path=u'D:\quantDb\sourceData\gta\每股指标\FI_T9.csv'
    df=pd.read_csv(path)
    df['Stkcd']=cleanStockId(df['Stkcd'])
    df['Accper']=normalize_date(df['Accper'])

    df.to_csv(u'D:\quantDb\每股指标\gta\FI_T9.csv')

#三因子 月
def fama3():
    path=u'D:\quantDb\sourceData\gta\三因子月\STK_MKT_ThrfacMonth.xls'
    df=pd.read_excel(path)
    df=df[2:]

    df=df.reset_index()
    del df['index']
    df.to_csv(u'D:\quantDb\三因子月\STK_MKT_ThrfacMonth.csv')




















