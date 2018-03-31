#-*-coding: utf-8 -*-
#author:tyhj
#tablesNew2mysql.py 2017/7/28 9:22
import pandas as pd
import os
from sqlalchemy.types import TEXT
import sqlalchemy
from zht.data.util  import toMysql

def gettablesNew():
    dirpath=r'D:\quantDb\sourceData\gta\data\tablesNew'
    df=pd.read_csv(r'D:\quantDb\sourceData\gta\data\table.csv',index_col=0)
    g=df.groupby('TBName')

    wrongFiles=[]
    for t in g:
        print t[0]
        try:
            t[1].to_csv(os.path.join(dirpath,t[0]+'.csv'),encoding='gbk')
        except UnicodeEncodeError:
            t[1].to_csv(os.path.join(dirpath,t[0]+'.csv'))
            wrongFiles.append(t[0])



dirpath=r'D:\quantDb\sourceData\gta\data\tablesNew'
fns=os.listdir(dirpath)
for fn in fns:
    df=pd.read_csv(os.path.join(dirpath,fn),index_col=0)
    toMysql.df2mysql(df,fn[:-4].lower(),'gtamenu')
    print fn











