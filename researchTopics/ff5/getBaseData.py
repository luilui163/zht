#-*-coding: utf-8 -*-
#author:tyhj
#getBaseData.py 2017/7/23 9:20

import pandas as pd
from zht.util.stru import cleanStockId,extractDate
from zht.util.dfFilter import filterDf

def get_rf():
    df=pd.read_csv(r'D:\quantDb\researchTopics\ff5\src\bdmonrfret_rf.csv',index_col=0)
    df.index=[ind[:-3] for ind in df.index]
    df.columns=['rf']
    return df

def get_rm(type='Mretmc'):
    '''
    :param type:Mretmc,Mrettmv,Mretmc
    :return:
    '''
    df = pd.read_csv(r'D:\quantDb\researchTopics\ff5\src\monretm_rm.csv', index_col=0)
    df.index = [ind[:-3] for ind in df.index]
    rm=df[[type]]
    rm.columns=['rm']
    return rm

def get_btm():
    df=pd.read_csv(u'D:/quantDb/researchTopics/ff5/src/fi_t9_每股净资产.csv',index_col=0)
    df.index=cleanStockId(df.index)
    df=df[['Accper','F091001A']]
    df.columns=['date','btm']
    df['date']=extractDate(df['date'])
    q='date endswith 12-31'
    df=filterDf(df,q)
    return df







df=pd.read_csv(u'D:/quantDb/researchTopics/ff5/src/is_all_OP.csv',index_col=0)

df=df.reset_index()

g=df.groupby(['ComCd','EndDt'])
counts=g.size()
uniq=counts.unique()

df=df.set_index(['ComCd','EndDt'])
print df.head()






#TODO: given stockIds














