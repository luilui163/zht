#-*-coding: utf-8 -*-
#author:tyhj
#getBaseData.py 2017/7/30 11:53
import pandas as pd
import os
import numpy as np
import re
from zht.util.dfFilter import filterDf

def save_df(df,name):
    df.to_csv(os.path.join(r'D:\quantDb\researchTopics\crossSection\resset',name+'.csv'))

def read_src(tbname):
    dirpath=r'D:\quantDb\sourceData\resset\data'

    p=re.compile(tbname+'_\d+.csv')

    fns=os.listdir(dirpath)
    fns=sorted([fn for fn in fns if re.match(p,fn)])
    df=pd.concat([pd.read_csv(os.path.join(dirpath,fn),error_bad_lines=False) for fn in fns],axis=0)
    return df

def get_indictor(name,tbname,fldname,timefld):
    df=read_src(tbname)
    cols=['Stkcd',timefld,fldname]

    df=df[cols]
    df[timefld]=[d[:-3] for d in df[timefld]]

    subdfs=[]
    for stockId,x in list(df.groupby('Stkcd')):
        tmpdf=x[[timefld,fldname]]
        tmpdf = tmpdf.set_index(timefld)
        tmpdf.columns = [stockId]
        subdfs.append(tmpdf)
        print stockId
    table=pd.concat(subdfs,axis=1)
    table=table.sort_index(ascending=True)

    save_df(table,name)

def get_size():
    name='size'
    tbname='MONMV'
    fldname='Montmv'
    timefld='Date'
    get_indictor(name,tbname,fldname,timefld)

def get_ret():
    name = 'ret'
    tbname = 'MONRET'
    fldname = 'Monret'
    timefld = 'Date'
    get_indictor(name, tbname, fldname, timefld)

def get_rf():
    name = 'rf'
    tbname = 'MONRET'
    fldname = 'MonRfRet'
    timefld = 'Date'

    df = read_src(tbname)
    cols = [timefld, fldname]

    df = df[cols]
    df[timefld] = [d[:-3] for d in df[timefld]]
    df=df.set_index(timefld)

    df=df.drop_duplicates()
    del df.index.name
    df.columns=[name]
    save_df(df,name)

def get_rm():
    name = 'rm'
    tbname = 'MONRET'
    fldname = 'Mrettmv'
    timefld = 'Date'

    df = read_src(tbname)
    cols = [timefld, fldname]

    df = df[cols]
    df[timefld] = [d[:-3] for d in df[timefld]]
    df = df.set_index(timefld)

    df = df.drop_duplicates()
    del df.index.name
    df.columns = [name]
    save_df(df, name)


# name='bv'
# dbname='gta'
# tbname='FS_Combas'
# fldname='A003000000'
# timefld='Accper'

def get_sample():
    name='bv'
    dbname='resset'
    tbname='BS_ALL'
    fldname='TotShareEquit'
    timefld='Accper'

    dfraw = read_src(tbname)
    q1='AccStd == 1'
    q2='ConFlg == 1'
    q3='AdjFlg == 1'
    q4='ReportType == Q4'
    q5='InfoSource == Q4'
    q6='BulType == 20'

    df=filterDf(dfraw,[q1,q2,q3,q4])

    # cols=['ComCd','EndDt','LstFlg','InfoPubDt',fldname]
    # df=df[cols]

    df=df.sort_values(['ComCd','EndDt'])

    header=['ComCd','EndDt',fldname]
    # cols=header+[col for col in df.columns if col not in header]
    df=df[header]

    print df.iloc[:50,:12]

    a=df.groupby(['ComCd','EndDt']).mean()
    a=a.reset_index()
    subdfs=[]
    for stockId,x in list(a.groupby('ComCd')):
        x=x[['EndDt','TotShareEquit']]
        x=x.set_index('EndDt')
        x.columns=[stockId]
        subdfs.append(x)
        print stockId

    table=pd.concat(subdfs,axis=1)
    save_df(table,'sample')

# cols = ['Stkcd', timefld, fldname]
#
# df = df[cols]
# df[timefld] = [d[:-3] for d in df[timefld]]
#
# subdfs = []
# for stockId, x in list(df.groupby('Stkcd')):
#     tmpdf = x[[timefld, fldname]]
#     tmpdf = tmpdf.set_index(timefld)
#     tmpdf.columns = [stockId]
#     subdfs.append(tmpdf)
#     print stockId
# table = pd.concat(subdfs, axis=1)
# table = table.sort_index(ascending=True)
#
# save_df(table, name)




