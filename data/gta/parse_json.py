# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-11  19:57
# NAME:zht-parse_json.py

import os
import json
import pandas as pd


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
        print(fn)

    df=pd.DataFrame(items,
                    columns=['DBID','DBTitle','nodeId','NodeTitle',
                             'TBTitle','TBName','TBId','StartTime','EndTime','DownSimplePath'],
                    index=[s[:-4] for s in fns])
    df=df.sort_index()
    df.to_csv(r'D:\zht\database\quantDb\sourceData\gta\20180410\crawler\info.csv',encoding='gbk')

parse_json()


