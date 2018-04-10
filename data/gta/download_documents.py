# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-10  09:52
# NAME:zht-download_documents.py

import urllib.request
import pandas as pd
import os
import json
import time
import pandas as pd

def download_documents1():
    directory=r'E:\a\pdf'

    info=pd.read_csv(r'D:\zht\database\quantDb\sourceData\gta\data\menuNew1.csv',encoding='gbk')
    info=info[['dbname','DBTitle','Dbid']]
    info['name']=info['dbname']+'-'+info['DBTitle']

    info=info.drop_duplicates(subset=['Dbid'])

    for ind in info.index:
        name=info.loc[ind,'name']
        dbid=info.loc[ind,'Dbid']
        url = r'http://www.gtarsc.com/SingleTable/DownLoadUseHelper?dbid={dbid}'.format(dbid=dbid)
        urllib.request.urlretrieve(url,os.path.join(directory,name+'.pdf'))
        time.sleep(0.1)
        print(ind)

def parse_json():
    directory=r'D:\zht\database\quantDb\sourceData\gta\20180410\crawler\json'
    fns=os.listdir(directory)

    items=[]
    for fn in fns:
        with open(os.path.join(directory,fn)) as f:
            js=json.load(f)

            #db information
            dbid=js['DBID']
            dbTitle=js['DBTitle']

            #node information
            nodeid=js['TableView']['NodeId']
            nodeTitle=js['TableView']['NodeTitle']

            #table information
            tbTitle=js['TableView']['TBTitle']
            tbName=js['TableView']['TBName']
            tbId=js['TableView']['TBId']

            startTime=js['TableView']['StartTime']
            endTime=js['TableView']['EndTime']

            downloadPath=js['DownSimplePath']
            items.append((dbid,dbTitle,nodeid,nodeTitle,tbTitle,tbName,tbId,startTime,endTime,downloadPath))

    df=pd.DataFrame(items,
                    columns=['DBID','DBTitle','nodeId','NodeTitle',
                             'TBTitle','TBName','TBId','StartTime','EndTime','DownSimplePath'],
                    index=[s[:-4] for s in fns])


