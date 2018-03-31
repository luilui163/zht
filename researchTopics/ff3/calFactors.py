#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
from zht.util.dfFilter import filterDf
from zht.util.stru import cleanStockId
import numpy as np

#RMW
def getRMW():
    #The data are from wind
    df1=pd.read_csv(r'D:\quantDb\researchTopics\fama\src\oper_rev.csv',index_col=0)
    df2=pd.read_csv(r'D:\quantDb\researchTopics\fama\src\selling_dist_exp.csv',index_col=0)
    df3=pd.read_csv(r'D:\quantDb\researchTopics\fama\src\fin_exp_is.csv',index_col=0)
    df4=pd.read_csv(r'D:\quantDb\researchTopics\fama\src\gerl_admin_exp.csv',index_col=0)
    df5=pd.read_csv(r'D:\quantDb\researchTopics\fama\src\tot_equity.csv',index_col=0)

    stockIds=df1.columns.tolist()
    rmw=pd.DataFrame()
    for i,stockId in enumerate(stockIds):
        tmpdf=pd.DataFrame()
        tmpdf['a']=df1[stockId]
        tmpdf['b']=df2[stockId]
        tmpdf['c']=df3[stockId]
        tmpdf['d']=df4[stockId]
        tmpdf['e']=df5[stockId]

        tmpdf['b']=tmpdf['b'].fillna(0)
        tmpdf['c']=tmpdf['c'].fillna(0)
        tmpdf['d']=tmpdf['d'].fillna(0)

        rmw[stockId]=(tmpdf['a']-tmpdf['b']-tmpdf['c']-tmpdf['d'])/tmpdf['e']
        print i,stockId

    rmw.to_csv(R'D:\quantDb\researchTopics\fama\rmw.csv')




#TODO: ff5
#TODO:compare







