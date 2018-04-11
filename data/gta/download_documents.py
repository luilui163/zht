# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-10  09:52
# NAME:zht-download_documents.py

import urllib.request
import pandas as pd
import os
import time

def download_documents():
    directory=r'D:\zht\database\quantDb\sourceData\gta\20180410\crawler\documents'

    info=pd.read_csv(r'D:\zht\database\quantDb\sourceData\gta\20180410\crawler\info.csv',index_col=0,encoding='gbk')
    info=info.drop_duplicates(subset=['DBID','DBTitle'])
    for i,ind in enumerate(info.index):
        dbid=info.loc[ind,'DBID']
        dbTitle=info.loc[ind,'DBTitle']
        url = r'http://www.gtarsc.com/SingleTable/DownLoadUseHelper?dbid={dbid}'.format(dbid=dbid)
        urllib.request.urlretrieve(url,os.path.join(directory,'{}_{}.pdf'.format(dbTitle,dbid)))
        time.sleep(0.1)
        print(time.strftime('%Y-%m-%d %H:%M:%S'),i,ind)


download_documents()
