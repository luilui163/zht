#-*-coding: utf-8 -*-
#author:tyhj
#dataApi.py 2017/8/17 12:17
import pandas as pd
import os

from zht.util.dfFilter import filterDf
from zht.util.pandasu import flatten2panel

def readFromSrc(tbname):
    df=pd.read_csv(os.path.join(r'D:\quantDb\sourceData\gta\data\csv',tbname+'.csv'))
    return df

def get_mktRetD():
    '''
    daily market return
    the market refer to all the A-share stocks and the stocks in Growth Enterprise Market

    Returns:

    '''
    tbname='TRD_Cndalym'
    indVar='Trddt'

    targetVar='Cdretwdos'
    newName='mktRetD'
    q1='Markettype == 21'#combine the A-share and Growth Enterprise Market


    df=readFromSrc(tbname)
    df=filterDf(df,q1)

    df=df.set_index(indVar)
    df=df.sort_index()
    df=df[[targetVar]]
    del df.index.name
    df.columns=[newName]
    return df

def get_stockRetD():
    '''
    stock daily return with dividend
    Returns:dataframe

    '''
    tbname='TRD_Dalyr'
    targetVar='Dretwd'

    df=readFromSrc(tbname)
    df=df[['Stkcd','Trddt','Dretwd']]

    m=flatten2panel(df,'Trddt','Stkcd',targetVar)
    return m

def get_stockVolD():
    '''
    stock daily trading volume,the unit is Chinese Yuan
    Returns:

    '''
    tbname='TRD_Dalyr'
    targetVar='Dnvaltrd'
    df=readFromSrc(tbname)
    df=flatten2panel(df,'Trddt','Stkcd',targetVar)
    return df














