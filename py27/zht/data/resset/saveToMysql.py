#-*-coding: utf-8 -*-
#@author:tyhj
import sqlalchemy
import os
import pandas as pd
from sqlalchemy.types import TEXT


def toMysql(df,tableName,dbname):
    engine=sqlalchemy.create_engine('mysql+mysqldb://root:root@localhost/%s'%dbname)
    df.to_sql(tableName,engine,if_exists='replace',dtype={col:TEXT for col in df.columns},chunksize=100)
    print 'saved %s successfully!'%tableName


def _getName(fn):
    return '_'.join(fn.split('_')[:-1])


def saveAll():
    dirpath=r'D:\quantDb\sourceData\resset\data'
    fns=os.listdir(dirpath)

    names=list(set([_getName(fn) for fn in fns]))
    for name in names[3:]:
        subdfs=[]
        for f in [fn for fn in fns if _getName(fn)==name]:
            sub=pd.read_csv(os.path.join(dirpath,f),error_bad_lines=False)
            # sub=pd.read_csv(os.path.join(dirpath,f))
            sub=sub.loc[:,~sub.columns.str.contains('^Unnamed')]
            subdfs.append(sub)
        df=pd.concat(subdfs,axis=0)
        toMysql(df,name.lower(),'resset') #using lower character as table name in mysql
        print name



def save(name):
    filepath=r'D:\quantDb\sourceData\resset\data\%s_1.csv'%name
    df=pd.read_csv(filepath)#do not use index_col=0
    df=df.loc[:,~df.columns.str.contains('^Unnamed')]
    toMysql(df,name.lower(),'resset')

name='BDMONRFRET'
save(name)


# name='tot_equity'
# filepath=r'D:\quantDb\researchTopics\fama\src\tot_equity.csv'
# df = pd.read_csv(filepath,index_col=0)  # do not use index_col=0
# df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
# toMysql(df.T, name.lower(), 'wind')






