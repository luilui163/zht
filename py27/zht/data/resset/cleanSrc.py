#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
from zht.data.resset import renameColnames
from zht.util.dfFilter import filterDf
import os
from zht.util.stru import cleanStockId
from zht.data.util.toMysql import toMysql

def cleanTHRFACDAT_MONTHLY():
    df=pd.read_csv(r'D:\quantDb\sourceData\resset\data\THRFACDAT_MONTHLY.csv')
    df.columns=['Exchflg','Mktflg','Date','Rmrf_tmv','Smb_tmv','Hml_tmv','Rmrf_mc','Smb_mc','Hml_mc','nobs']
    df.to_csv(r'D:\quantDb\resset\THRFACDAT_MONTHLY.csv')
    # print df.head()


def cleanPMONRET_FF():
    path=r'D:\quantDb\sourceData\resset\data\PMONRET_FF.csv'
    df=pd.read_csv(path)
    df.columns=['Exchflg','Mktflg','Sizeflg','BMflg','Date','SampSize','Pmonret_tmv','Pmonret_mc','nobs']
    df.to_csv(r'D:\quantDb\resset\PMONRET_FF.csv')
    # print df.head()

# cleanTHRFACDAT_MONTHLY()
# cleanPMONRET_FF()

# for i in range(1,7):
#     path=r'D:\quantDb\sourceData\resset\data\FININD_%s.csv'%i
#     df=pd.read_csv(path,index_col=0)

def IS_ALL():
    dfs=[]
    for i in range(1,13):
        path=r'D:\quantDb\sourceData\resset\data\IS_ALL_%s.csv'%i
        df=pd.read_csv(path,error_bad_lines=False,encoding='gbk') #skip those bad lines
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns=renameColnames.rename(df.columns)
        dfs.append(df)
        print i

    com=pd.concat(dfs,axis=0)
    com.to_csv(r'D:\quantDb\resset\IS_ALL.csv',encoding='gbk')


def clean(tableName):
    directory=r'D:\quantDb\sourceData\resset\data'
    fns=os.listdir(directory)
    fns=[fn for fn in fns if fn.startswith(tableName)]
    dfs=[]
    for fn in fns:
        path=os.path.join(directory,fn)
        df=pd.read_csv(path,error_bad_lines=False)
        df=df.loc[:,~df.columns.str.contains('^Unnamed')]
        df.columns=renameColnames.rename(df.columns)
        dfs.append(df)
    com=pd.concat(dfs,axis=0)
    com.to_csv(r'D:\quantDb\resset\%s.csv'%tableName)


def renameFiles(dirpath):
    fns=[fn for fn in os.listdir(dirpath) if fn.endswith('.csv')]

    for fn in fns:
        items=fn.split('_')
        newItems=[items[0]]
        for item in items[1:]:
            if len(item)!=11:
                newItems.append(item)
        newname='_'.join(newItems)
        newname=newname.replace('(','')
        newname=newname.replace(')','')
        os.rename(os.path.join(dirpath,fn),os.path.join(dirpath,newname))
        print f

def cleanBS_ALL():
    df=pd.read_csv(r'D:\quantDb\researchTopics\fama\src\bs_all.csv',index_col=0)
    q1='A_StkCd is notnull'
    q2='AdjFlg == 0'
    q3='ReportType == Q4'
    q4='InfoSourceFlg == Q4'
    q5='ConFlg == 1'
    q6='LstFlg contains A'

    query=[q1,q2,q3,q4,q5,q6]
    # for q in query:
    #     print filterDf(df,q).shape

    df=filterDf(df,query)

    stockIds = open(r'D:\quantDb\mkt\dataset\stockIds\2017-07-22.txt').read().split()
    stockIds = [s[:-3] for s in stockIds]
    df['A_StkCd']=cleanStockId(df['A_StkCd']) # only care about A share
    df=df[df['A_StkCd'].isin(stockIds)]

    g=df.groupby(['A_StkCd','EndDt'])
    df=g.mean() #TODO: there is still some duplicates,take average of the duplicates

    df=df.reset_index()
    df.to_csv(r'e:\aa\bs_all_zht.csv')
    toMysql(df,'bs_all_zht','resset')

def cleanFININD():
    df = pd.read_csv(r'e:\aa\finind.csv', index_col=0)
    q1 = 'A_StkCd is notnull'
    q2 = 'AdjFlg == 0'
    q3 = 'ReportType == Q4'
    # q4 = 'InfoSourceFlg == Q4'
    q5 = 'ConFlg == 1'
    # q6 = 'LstFlg contains A'

    query = [q1, q2, q3,q5]

    stockIds = open(r'D:\quantDb\mkt\dataset\stockIds\2017-07-22.txt').read().split()
    stockIds = [s[:-3] for s in stockIds]
    df['A_Stkcd'] = cleanStockId(df['A_Stkcd'])  # only care about A share
    df = df[df['A_Stkcd'].isin(stockIds)]

    g = df.groupby(['A_Stkcd', 'EndDt'])
    df = g.mean()  # TODO: there is still some duplicates,take average of the duplicates

    df = df.reset_index()
    df.to_csv(r'e:\aa\finind_zht.csv')
    toMysql(df, 'finind_zht', 'resset')

def cleanIS_ALL():
    df = pd.read_csv(r'e:\aa\is_all.csv', index_col=0)
    q1 = 'A_StkCd is notnull'
    q2 = 'AdjFlg == 0'
    q3 = 'ReportType == Q4'
    q4 = 'InfoSourceFlg == Q4'
    q5 = 'ConFlg == 1'

    query = [q1, q2, q3, q4, q5]
    # for q in query:
    #     print filterDf(df,q).shape

    df = filterDf(df, query)

    stockIds = open(r'D:\quantDb\mkt\dataset\stockIds\2017-07-22.txt').read().split()
    stockIds = [s[:-3] for s in stockIds]
    df['A_StkCd'] = cleanStockId(df['A_StkCd'])  # only care about A share
    df = df[df['A_StkCd'].isin(stockIds)]

    g = df.groupby(['A_StkCd', 'EndDt'])
    df = g.mean()  # TODO: there is still some duplicates,take average of the duplicates

    df = df.reset_index()
    df.to_csv(r'e:\aa\is_all_zht.csv')
    toMysql(df, 'is_all_zht', 'resset')

def cleanFINRATIO():
    df = pd.read_csv(r'e:\aa\finratio.csv', index_col=0)
    q1 = 'A_Stkcd is notnull'
    q3 = 'Reporttype == Q4'

    query = [q1,q3]
    # for q in query:
    #     print filterDf(df,q).shape

    df = filterDf(df, query)

    stockIds = open(r'D:\quantDb\mkt\dataset\stockIds\2017-07-22.txt').read().split()
    stockIds = [s[:-3] for s in stockIds]
    df['A_Stkcd'] = cleanStockId(df['A_Stkcd'])  # only care about A share
    df = df[df['A_Stkcd'].isin(stockIds)]

    g = df.groupby(['A_Stkcd', 'Enddt'])
    if len(g.size().unique())>1:# TODO: there is still some duplicates,take average of the duplicates
        df = g.mean()

    df = df.reset_index()
    df.to_csv(r'e:\aa\finratio_zht.csv')
    toMysql(df, 'finratio_zht', 'resset')







import pandas as pd
from zht.util.dfFilter import filterDf
from zht.util.stru import cleanStockId
import numpy as np

is_all=pd.read_csv(r'e:\aa\is_all_zht.csv',index_col=0)
is_all['A_StkCd']=cleanStockId(is_all['A_StkCd'])
stockIds=np.sort(is_all['A_StkCd'].unique())
dates=np.sort(is_all['EndDt'].unique().tolist())
is_all=is_all.set_index(['A_StkCd','EndDt'])
# is_all=is_all.sort_values(['EndDt','A_StkCd'],ascending=[True,True])

factors=['OpRev','OpExp','FinanExp','AdmExp']
dic={factor:pd.DataFrame() for factor in factors}

for factor in factors:
    for date in dates:
        for stockId in stockIds:
            try:
                dic[factor].loc[date,stockId]=is_all.loc[(stockId,date),factor]
            except KeyError:
                pass
        print factor,date
    dic[factor].to_csv(r'D:\quantDb\researchTopics\fama\src\%s.csv'%factor.lower())


#=========================================================
bs_all=pd.read_csv(r'e:\aa\bs_all_zht.csv',index_col=0)
bs_all['A_StkCd']=cleanStockId(bs_all['A_StkCd'])
stockIds=np.sort(bs_all['A_StkCd'].unique())
dates=np.sort(bs_all['EndDt'].unique().tolist())
bs_all=bs_all.set_index(['A_StkCd','EndDt'])


df=pd.DataFrame()
factor='TotShareEquit'
for date in dates:
    for stockId in stockIds:
        try:
            df.loc[date, stockId] = is_all.loc[(stockId, date), factor]
        except KeyError:
            pass
    print factor, date
df.to_csv(R'D:\quantDb\researchTopics\fama\src\%s.csv'%factor)

#=======================================================================

finratio=pd.read_csv(r'e:\aa\finratio_zht.csv',index_col=0)
finratio['A_Stkcd']=cleanStockId(finratio['A_Stkcd'])
stockIds=np.sort(finratio['A_Stkcd'].unique())
dates=np.sort(finratio['Enddt'].unique().tolist())
finratio=finratio.set_index(['A_Stkcd','Enddt'])


df=pd.DataFrame()
factor='Totassgrrt'
for date in dates:
    for stockId in stockIds:
        try:
            df.loc[date, stockId] = is_all.loc[(stockId, date), factor]
        except KeyError:
            pass
    print factor, date
df.to_csv(R'D:\quantDb\researchTopics\fama\src\%s.csv'%factor)
