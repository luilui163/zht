#-*-coding: utf-8 -*-
#@author:tyhj

import sqlalchemy
import os
import pandas as pd
from sqlalchemy.types import TEXT

import pandas as pd
import MySQLdb
import os

def _toMysql(df,tableName,dbname):
    engine=sqlalchemy.create_engine('mysql+mysqldb://root:root@localhost/%s'%dbname)
    df.to_sql(tableName,engine,if_exists='replace',chunksize=100)
    print 'saved %s successfully!'%tableName

def toMysql(df,tableName,dbname):
    engine=sqlalchemy.create_engine('mysql+mysqldb://root:root@localhost/%s'%dbname)
    df.to_sql(tableName,engine,dtype={col:TEXT for col in df.columns},if_exists='replace',chunksize=100)
    print 'saved %s successfully!'%tableName



def _func(x):
    if isinstance(x,str):
        return '"%s"'%x.replace('"','').replace(',','').replace('/','').replace('\\','')
    elif pd.isnull(x):
        return 'NULL'
    else:
        return str(x)

def df2mysql(df,tbname,dbname,datatype='LONGTEXT'):#TODO:
    '''
    default property:1,replace if exists,2,datatypa are all 'LONGTEXT'
    '''

    tbname=tbname.lower()
    db = MySQLdb.connect(host='localhost', user='root', passwd='root', db=dbname)
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS %s' % tbname) #drop if exists
    sql1 = 'CREATE TABLE %s(\n' % tbname
    for i in range(df.shape[1]):
        if i==df.shape[1]-1:
            sql1+='`%s` %s\n'%(df.columns.tolist()[i],datatype) #use back tick character (`) to escape reserved words in mysql
        else:
            sql1 += '`%s` %s,\n' % (df.columns.tolist()[i], datatype)
    sql1 += ');'

    cursor.execute(sql1)

    for i in range(df.shape[0]):
        s = ','.join([_func(x) for x in df.iloc[i, :]])
        sql2 = '''INSERT INTO %s VALUES (%s);''' % (tbname, s)
        cursor.execute(sql2)
    db.commit()
    db.close()







