# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-12  00:49
# NAME:zht-download_rar.py
from urllib.request import urlretrieve
from pyunpack import Archive

import os
import pandas as pd
import time

from utils.dateu import get_current_time

path_rar=r'e:\a\rars'
path_unrar=r'e:\a\unrars'

def download_all_rar():
    info=pd.read_csv(r'D:\zht\database\quantDb\sourceData\gta\20180410\crawler\info.csv',index_col=0,encoding='gbk')

    for i in range(1500,info.shape[0]):#TODO:
        url=info['DownSimplePath'][i]
        print('{} -> starting {}  {}'.format(get_current_time(),i,url,url))
        try:
            urlretrieve(url,os.path.join(path_rar,os.path.basename(url)))
        except:
            print('{} -> Failed {}  {}'.format(get_current_time(),i,url,url))
        time.sleep(1)

def get_undownload():
    info = pd.read_csv(r'D:\zht\database\quantDb\sourceData\gta\20180410\crawler\info.csv', index_col=0, encoding='gbk')
    downloaded=os.listdir(path_rar)
    undownloaded=[]
    for f in info['DownSimplePath']:
        if f.split('/')[-1] not in downloaded:
            undownloaded.append(f)
    return undownloaded

def unrar_all():
    directory=r'E:\a\rars'
    fns=os.listdir(directory)
    for i,fn in enumerate(fns):
        Archive(os.path.join(directory,fn)).extractall(path_unrar)
        time=get_current_time()
        print('{} -> {} {}'.format(time,i,fn))





