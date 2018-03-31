#-*-coding: utf-8 -*-
#author:tyhj
#df2mysql.py 2017/7/27 16:01
import sqlalchemy
import os
import pandas as pd
from sqlalchemy.types import TEXT


def toMysql(df,tableName,dbname):
    engine=sqlalchemy.create_engine('mysql+mysqldb://root:root@localhost/%s?charset=utf8'%dbname)
    df.to_sql(tableName,engine,if_exists='replace',dtype={col:TEXT for col in df.columns},chunksize=100)
    print 'saved %s successfully!'%tableName

def saveTables():
    dirpath=r'D:\quantDb\sourceData\gta\data\tables'
    fns=os.listdir(dirpath)
    for i,fn in enumerate(fns):
        df=pd.read_csv(os.path.join(dirpath,fn),index_col=0)
        toMysql(df,fn[:-4].lower(),'gtamenu')
        print i,fn







