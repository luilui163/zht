#-*-coding: utf-8 -*-
#author:tyhj
#csv2mysql.py 2017/7/27 11:16
import pandas as pd
import MySQLdb
import os

dirpath=r'D:\quantDb\sourceData\gta\data\csv'
fns=os.listdir(dirpath)
fns=sorted(fns,key=lambda x:os.path.getsize(os.path.join(dirpath,x)))
def _func(x):
    if isinstance(x,str):
        return '"%s"'%x.replace('"','').replace(',','').replace('/','').replace('\\','')
    elif pd.isnull(x):
        return 'NULL'
    else:
        return str(x)

tns=[fn[:-4] for fn in fns]
for c,tn in enumerate(tns[2032:]):
    df=pd.read_csv(os.path.join(r'D:\quantDb\sourceData\gta\data\csv',tn+'.csv'))
    info=pd.read_csv(os.path.join(r'D:\quantDb\sourceData\gta\data\tables',tn+'.csv'),index_col=0)
    sql1=''
    sql1+='CREATE TABLE %s(\n'%tn
    for i in range(len(info)):
        fldname=info['Fldname'][i]
        typename=info['Typename'][i]
        # if typename in ['Datetime','Ntext','Image','Nvarchar']: #the MySQL server version is different,
        #     datatype='TEXT'#TODO:
        # else:
        #     mergerdatatype = info['Mergerdatatype'][i]
        #     datatype=typename+mergerdatatype[1:]
        datatype = 'LONGTEXT'
        if i==len(info)-1:
            sql1+='`%s` %s\n'%(fldname,datatype) #use back tick character (`) to escape reserved words in mysql
        else:
            sql1+='`%s` %s,\n'%(fldname,datatype)
    sql1+=');'
    with open(r'D:\quantDb\sourceData\gta\data\sql\%s.sql'%tn,'w') as f:
        f.write(sql1)

    db=MySQLdb.connect(host='localhost',user='root',passwd='root',db='gta')
    cursor=db.cursor()
    cursor.execute('DROP TABLE IF EXISTS %s'%tn)
    cursor.execute(sql1)
    for i in range(df.shape[0]):
        print c, tn, i
        s=','.join([_func(x) for x in df.iloc[i,:]])
        sql2='''INSERT INTO %s VALUES (%s);'''%(tn,s)
        cursor.execute(sql2)
    db.commit()
    db.close()


# with open('sql2.sql','w') as f:
#     f.write(sql2)
