#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import os
import time
from zht.util.dfFilter import filterDf
from zht.util import pandasu
from zht.util.mathu import getRankIdArr
from zht.util.stru import cleanStockId

query1='Markettype in [1,4,16]' #A股
query2='Typrep == A' #合并报表
mvType = 'Msmvosd'  # 月个股流通市值
retType = 'Mretwd'  # 考虑现金红利再投资的月个股回报率

sizeNum=2
btmNum=3

sizeQNum=5
btmQNum=5

def getMkt():
    global query1
    df=pd.read_csv(r'D:\quantDb\mkt\monthly\mkt.csv',index_col=0)
    df['Stkcd']=cleanStockId(df['Stkcd'])
    df=filterDf(df, query1)
    return df

def getIndicator():
    global query2
    df=pd.read_csv(u'D:\quantDb\每股指标\gta\FI_T9.csv',index_col=0,dtype={'Stkcd':str})
    df['Stkcd'] = cleanStockId(df['Stkcd'])
    df=filterDf(df, query2)
    return df

def fama3():
    path=u'D:\quantDb\三因子月\STK_MKT_ThrfacMonth.csv'
    df=pd.read_csv(path,index_col=0)
    query='MarkettypeID == P9709'  #A share and growth Enterprises Market
    df1=filterDf(df,query)
    return df1


#=================================================================================
#============================set condition========================================
mkt=getMkt()
indicator=getIndicator()

#================================================================================
#================================================================================

def _getRmrf(retType='Mretwd'):
    months=mkt['Trdmnt'].unique().tolist()
    months=sorted(months)[1:] #第一个月缺失数据
    rmrf=pd.DataFrame(columns=['rm'])
    for month in months:
        tmp=pd.DataFrame()
        tmp['mv']=mkt[mkt['Trdmnt']==month][mvType]
        tmp['ret']=mkt[mkt['Trdmnt']==month][retType]
        tmp=tmp.dropna(axis=0,how='any')
        r=pandasu.mean_self(tmp,'ret','mv')
        print month,r
        rmrf.loc[month,'rm']=r
    rmrf['rf']=pd.read_csv(r'D:\quantDb\mkt\dataset\rf.csv',index_col=0)['rf']
    if retType=='Mretnd':
        rmrf.to_csv(r'D:\quantDb\researchTops\fama\rmrf1.csv')
    else:
        rmrf.to_csv(r'D:\quantDb\researchTops\fama\rmrf.csv')

def getRmrf(retType='Mretwd'):
    #Mretwd:include the dividend earnings
    #Mretwd:do not include the dividend earnings
    if retType=='Mretwd':
        rmrf=pd.read_csv(r'D:\quantDb\researchTops\fama\rmrf.csv',index_col=0)
    elif retType=='Mretnd':
        rmrf = pd.read_csv(r'D:\quantDb\researchTops\fama\rmrf1.csv',index_col=0)
    return rmrf

def getRmrf1(retType='Mretnd'):
    months = mkt['Trdmnt'].unique().tolist()
    months = sorted(months)[1:]  # 第一个月缺失数据
    rmrf = pd.DataFrame(columns=['rm'])
    for month in months:
        tmp = pd.DataFrame()
        tmp['mv'] = mkt[mkt['Trdmnt'] == month][mvType]
        tmp['ret'] = mkt[mkt['Trdmnt'] == month][retType]
        tmp = tmp.dropna(axis=0, how='any')
        r = pandasu.mean_self(tmp, 'ret', 'mv')
        print month, r
        rmrf.loc[month, 'rm'] = r
    rmrf['rf'] = pd.read_csv(r'D:\quantDb\mkt\dataset\rf.csv', index_col=0)['rf']
    rmrf.to_csv(r'D:\quantDb\researchTops\fama\rmrf1.csv')

#sort size in the june of every year
def getSizeId(sizeNum):
    directory=r'D:\quantDb\researchTops\fama\sizeId%s'%sizeNum
    if not os.path.exists(directory):
        os.makedirs(directory)

    query='Trdmnt endswith 06'
    dfSize=filterDf(mkt,query)[['Stkcd','Trdmnt',mvType]]
    months=sorted(dfSize['Trdmnt'].unique().tolist())
    for month in months:
        subdf=dfSize[dfSize['Trdmnt']==month]
        # subdf.loc[:,'rank']=subdf[mvType].rank()
        subdf.loc[:,'sizeId']=getRankIdArr(subdf[mvType],sizeNum)
        subdf=subdf.set_index('Stkcd')
        del subdf.index.name
        subdf=subdf[['sizeId']]
        subdf.to_csv(os.path.join(directory,month+'.csv'))
        # subdf.to_csv(r'D:\quantDb\researchTops\fama\sizeId\%s.csv'%month)
        print month

#get book-to-market ratio
def getBtmId(btmNum):#TODO: not equal splitted 30% 70%?
    directory=r'D:\quantDb\researchTops\fama\btmId%s'%btmNum
    if not os.path.exists(directory):
        os.makedirs(directory)
    # bv=bvDf['F091001A']
    Accpers=sorted(indicator['Accper'].unique().tolist())
    yearends=[Accper for Accper in Accpers if Accper.split('-')[1]=='12']
    for yearend in yearends:
        december=yearend[:-3]
        tmpdf=pd.DataFrame()

        bvdf=indicator[indicator['Accper']==yearend]
        bvdf=bvdf.set_index('Stkcd')
        tmpdf['bv']=bvdf['F091001A']

        mvdf=mkt[mkt['Trdmnt']==december] #use the ME of year t-1
        mvdf=mvdf.set_index('Stkcd')

        tmpdf['mv']=mvdf['Mclsprc']
        tmpdf=tmpdf.dropna(axis=0,how='any')#TODO: if there is no mv drop this stock,how about using the data before this report?
        tmpdf['btm']=tmpdf['bv']/tmpdf['mv']  #TODO: delete the stocks with bv smaller than 0?
        #TODO:delete the stocks listed in latest 2 years?
        tmpdf['btmId']=getRankIdArr(tmpdf['btm'],btmNum)
        btmId=tmpdf[['btmId']]
        tmpdf.to_csv(os.path.join(directory, december + '.csv'))
        # btmId.to_csv(r'D:\quantDb\researchTops\fama\btmId\%s.csv'%december)

        print yearend,len(bvdf),len(mvdf),len(tmpdf)
    #TODO:do not use the book-to-market of 2016-12,since,there are some stocks that have not issue the report
#TODO:the sorting process should be put behind the process of calculateing rm and book-to-market?



#TODO:sort independently,how about dependently?





#sort book-to-market in the june of every year by using the data in the december of the last year

# if __name__=='__main__':
#     getSizeId(sizeNum)
#     getBtmId(btmNum)
#     getSizeId(sizeQNum)
#     getBtmId(btmQNum)
