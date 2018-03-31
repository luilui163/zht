#-*-coding: utf-8 -*-
#@author:tyhj
import os
import pandas as pd
import numpy as np
from zht.data import data_handler
from zht import tool
from datetime import datetime

from WindPy import *
w.start()

def get_codes_from_wind():
    today=datetime.today().strftime('%Y-%m-%d')
    wdata=w.wset("sectorconstituent","date=%s;sectorid=a001010100000000"%today)
    codes=wdata.Data[1]
    with open(r'C:\data\wind\dataset\codes\%s.txt'%today,'w') as f:
        for code in codes:
            f.write(code+'\n')

def get_codes():
    path=r'C:\data\wind\dataset\codes\2017-04-16.txt'
    codes=open(path).read().split('\n')[:-1]
    return codes


#市值,后复权数据
def get_mkt_cap():
    codes=get_codes()
    today=datetime.today().strftime('%Y-%m-%d')
    wdata=w.wsd(','.join(codes), "mkt_cap_CSRC", "2000-01-01", today, "unit=1;Period=M;Days=Alldays;PriceAdj=B")
    dates=[t.strftime('%Y-%m-%d') for t in wdata.Times]

    df=pd.DataFrame(wdata.Data,index=codes,columns=dates)
    df=df.T
    df=df[:-1]
    df.to_csv(r'C:\data\wind\factor\mkt_cap.csv')

#PB,  PB的倒数就会book to market ratio
def get_pb():
    codes=get_codes()
    today=datetime.today().strftime('%Y-%m-%d')
    wdata=w.wsd(','.join(codes), "pb", "2000-01-01", today, "ruleType=3;Period=M;Days=Alldays;PriceAdj=B")
    dates=[t.strftime('%Y-%m-%d') for t in wdata.Times]

    df=pd.DataFrame(wdata.Data,index=codes,columns=dates)
    df=df.T
    df=df[:-1]
    df.to_csv(r'C:\data\wind\factor\pb.csv')



