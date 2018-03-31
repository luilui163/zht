#-*-coding: utf-8 -*-
#author:tyhj
#downloadRAR.py 2017/7/25 15:30
import urllib
import requests
import os
import pandas as pd


def getFailedURL():
    path=r'D:\quantDb\sourceData\gta\data\menu.csv'
    df=pd.read_csv(path,index_col=0)
    urls=df['url'].tolist()
    names=[url.split('/')[-1] for url in urls]
    dirpath=r'D:\quantDb\sourceData\gta\data\zip'
    fns=os.listdir(dirpath)
    newnames=[name for name in names if name not in fns]
    with open(r'D:\quantDb\sourceData\gta\data\failedURL.txt','w') as f:
        for newname in newnames:
            f.write('http://119.147.213.33/ssishistory/CN/'+newname+'\n')

# url=r'http://119.147.213.33/ssishistory/CN/68_1725_IME_Intst2.rar'
# urllib.urlretrieve(url,'test.zip')















