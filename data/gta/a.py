# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-18  00:20
# NAME:zht-a.py
import os
import pandas as pd

dirpath=r'E:\a\gta20180412\unrars'
fn=r'STK_ListedCoInfoAnl.txt'

df=pd.read_csv(os.path.join(dirpath,fn),encoding='ISO-8859-1',skiprows=[1,2],error_bad_lines=False,warn_bad_lines=True) #TODO: compression

